from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import crud
from .database import Base, engine, get_db
from .schemas import ClientCreate, ClientOut, ClientUpdate

BASE_DIR = Path(__file__).resolve().parent

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PulseCRM",
    description="Industry-style CRM built with FastAPI and MySQL.",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(directory=BASE_DIR / "templates")


# =========================
# DASHBOARD
# =========================

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    data = crud.analytics(db)

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "data": data,
        },
    )


# =========================
# CLIENTS PAGE
# =========================

@app.get("/clients", response_class=HTMLResponse)
def clients_page(
    request: Request,
    search: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
):
    clients = crud.list_clients(db, search, status)

    return templates.TemplateResponse(
        request=request,
        name="clients.html",
        context={
            "request": request,
            "clients": clients,
            "search": search or "",
            "status": status or "All",
        },
    )


# =========================
# NEW CLIENT PAGE
# =========================

@app.get("/clients/new", response_class=HTMLResponse)
def new_client_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="client_form.html",
        context={
            "request": request,
            "client": None,
            "mode": "Create",
        },
    )


# =========================
# EDIT CLIENT PAGE
# =========================

@app.get("/clients/{client_id}/edit", response_class=HTMLResponse)
def edit_client_page(
    request: Request,
    client_id: int,
    db: Session = Depends(get_db),
):
    client = crud.get_client(db, client_id)

    if not client:
        raise HTTPException(
            status_code=404,
            detail="Client not found.",
        )

    return templates.TemplateResponse(
        request=request,
        name="client_form.html",
        context={
            "request": request,
            "client": client,
            "mode": "Edit",
        },
    )


# =========================
# ANALYSIS PAGE
# =========================

@app.get("/analysis", response_class=HTMLResponse)
def analysis_page(
    request: Request,
    db: Session = Depends(get_db),
):
    data = crud.analytics(db)

    return templates.TemplateResponse(
        request=request,
        name="analysis.html",
        context={
            "request": request,
            "data": data,
        },
    )


# =========================
# API - LIST CLIENTS
# =========================

@app.get("/api/clients", response_model=list[ClientOut])
def api_list_clients(
    search: str | None = Query(default=None),
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return crud.list_clients(db, search, status)


# =========================
# API - CREATE CLIENT
# =========================

@app.post("/api/clients", response_model=ClientOut, status_code=201)
def api_create_client(
    data: ClientCreate,
    db: Session = Depends(get_db),
):
    return crud.create_client(db, data)


# =========================
# API - UPDATE CLIENT
# =========================

@app.put("/api/clients/{client_id}", response_model=ClientOut)
def api_update_client(
    client_id: int,
    data: ClientUpdate,
    db: Session = Depends(get_db),
):
    client = crud.update_client(db, client_id, data)

    if not client:
        raise HTTPException(
            status_code=404,
            detail="Client not found.",
        )

    return client


# =========================
# API - DELETE CLIENT
# =========================

@app.delete("/api/clients/{client_id}")
def api_delete_client(
    client_id: int,
    db: Session = Depends(get_db),
):
    deleted = crud.delete_client(db, client_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Client not found.",
        )

    return {
        "message": "Client deleted successfully."
    }


# =========================
# API - ANALYTICS
# =========================

@app.get("/api/analytics")
def api_analytics(
    db: Session = Depends(get_db),
):
    data = crud.analytics(db)

    data.pop("recent", None)

    return data