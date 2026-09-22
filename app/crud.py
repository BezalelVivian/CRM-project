from datetime import date, datetime

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from .models import Client
from .schemas import ClientCreate, ClientUpdate


def list_clients(
    db: Session,
    search: str | None = None,
    status: str | None = None,
):
    query = db.query(Client)

    if search:
        term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Client.name.ilike(term),
                Client.email.ilike(term),
                Client.company.ilike(term),
                Client.phone.ilike(term),
            )
        )

    if status and status != "All":
        query = query.filter(Client.status == status)

    return query.order_by(Client.client_date.desc(), Client.id.desc()).all()


def get_client(db: Session, client_id: int):
    return db.query(Client).filter(Client.id == client_id).first()


def create_client(db: Session, data: ClientCreate):
    client = Client(**data.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def update_client(db: Session, client_id: int, data: ClientUpdate):
    client = get_client(db, client_id)
    if not client:
        return None

    for key, value in data.model_dump().items():
        setattr(client, key, value)

    client.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(client)
    return client


def delete_client(db: Session, client_id: int):
    client = get_client(db, client_id)
    if not client:
        return False

    db.delete(client)
    db.commit()
    return True


def analytics(db: Session):
    total = db.query(func.count(Client.id)).scalar() or 0
    total_budget = db.query(func.coalesce(func.sum(Client.budget), 0)).scalar() or 0
    average_budget = db.query(func.coalesce(func.avg(Client.budget), 0)).scalar() or 0

    status_rows = (
        db.query(Client.status, func.count(Client.id))
        .group_by(Client.status)
        .all()
    )

    budget_rows = (
        db.query(Client.status, func.coalesce(func.sum(Client.budget), 0))
        .group_by(Client.status)
        .all()
    )

    monthly_rows = (
        db.query(
            func.year(Client.client_date),
            func.month(Client.client_date),
            func.count(Client.id),
            func.coalesce(func.sum(Client.budget), 0),
        )
        .group_by(func.year(Client.client_date), func.month(Client.client_date))
        .order_by(func.year(Client.client_date), func.month(Client.client_date))
        .all()
    )

    source_rows = (
        db.query(Client.source, func.count(Client.id))
        .filter(Client.source.isnot(None), Client.source != "")
        .group_by(Client.source)
        .order_by(func.count(Client.id).desc())
        .all()
    )

    recent = (
        db.query(Client)
        .order_by(Client.created_at.desc())
        .limit(5)
        .all()
    )

    status_counts = {status: count for status, count in status_rows}
    status_budgets = {status: float(total) for status, total in budget_rows}

    months = []
    for year, month, count, budget in monthly_rows:
        months.append(
            {
                "label": date(year, month, 1).strftime("%b %Y"),
                "count": count,
                "budget": float(budget),
            }
        )

    return {
        "total_clients": total,
        "total_budget": float(total_budget),
        "average_budget": float(average_budget),
        "status_counts": status_counts,
        "status_budgets": status_budgets,
        "monthly": months,
        "sources": [
            {"source": source, "count": count}
            for source, count in source_rows
        ],
        "recent": recent,
    }
