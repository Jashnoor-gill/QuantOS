from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class FactorExposureCreate(BaseModel):
    factor_name: str
    symbol: str
    exposure: float
    weight: Optional[float] = None


class FactorExposureUpdate(BaseModel):
    factor_name: Optional[str] = None
    symbol: Optional[str] = None
    exposure: Optional[float] = None
    weight: Optional[float] = None


class FactorExposureResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    factor_name: str
    symbol: str
    exposure: float
    weight: Optional[float]
    created_at: datetime
    updated_at: datetime


class FactorExposureListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[FactorExposureResponse]

