from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AlphaCreate(BaseModel):
    name: str
    description: Optional[str] = None
    expression: str
    status: str
    sharpe: Optional[float] = None
    turnover: Optional[float] = None
    fitness: Optional[float] = None


class AlphaUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    expression: Optional[str] = None
    status: Optional[str] = None
    sharpe: Optional[float] = None
    turnover: Optional[float] = None
    fitness: Optional[float] = None


class AlphaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    expression: str
    status: str

    sharpe: Optional[float]
    turnover: Optional[float]
    fitness: Optional[float]

    created_at: datetime


class AlphaListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[AlphaResponse]

