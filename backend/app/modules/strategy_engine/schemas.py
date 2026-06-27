from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class StrategyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    strategy_type: str
    alpha_id: int
    rebalance_frequency: Optional[float] = None
    status: str


class StrategyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    strategy_type: Optional[str] = None
    alpha_id: Optional[int] = None
    rebalance_frequency: Optional[float] = None
    status: Optional[str] = None


class StrategyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]

    strategy_type: str
    alpha_id: int
    rebalance_frequency: Optional[float]

    status: str

    created_at: datetime


class StrategyListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[StrategyResponse]

