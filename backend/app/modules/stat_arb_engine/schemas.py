from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class StatArbPairCreate(BaseModel):
    asset_1: str
    asset_2: str

    spread_mean: Optional[float] = None
    spread_std: Optional[float] = None

    z_score: Optional[float] = None
    hedge_ratio: Optional[float] = None
    signal: Optional[float] = None

    status: str


class StatArbPairUpdate(BaseModel):
    asset_1: Optional[str] = None
    asset_2: Optional[str] = None

    spread_mean: Optional[float] = None
    spread_std: Optional[float] = None

    z_score: Optional[float] = None
    hedge_ratio: Optional[float] = None
    signal: Optional[float] = None

    status: Optional[str] = None


class StatArbPairResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    asset_1: str
    asset_2: str

    spread_mean: Optional[float]
    spread_std: Optional[float]

    z_score: Optional[float]
    hedge_ratio: Optional[float]
    signal: Optional[float]

    status: str

    created_at: datetime


class StatArbPairListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[StatArbPairResponse]

