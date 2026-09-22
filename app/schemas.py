from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


Status = Literal["Lead", "Prospect", "Customer", "Churned"]


class ClientBase(BaseModel):
    client_date: date
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=30)
    company: str | None = Field(default=None, max_length=150)
    budget: float = Field(default=0, ge=0)
    status: Status = "Lead"
    source: str | None = Field(default=None, max_length=80)
    notes: str | None = Field(default=None, max_length=2000)


class ClientCreate(ClientBase):
    pass


class ClientUpdate(ClientBase):
    pass


class ClientOut(ClientBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
