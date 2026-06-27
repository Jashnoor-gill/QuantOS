from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PortfolioCreate(BaseModel):
    name: str
    description: Optional[str] = None
    strategy_id: int

    capital: float
    expected_return: Optional[float] = None
    volatility: Optional[float] = None
    sharpe_ratio: Optional[float] = None

    optimization_method: Optional[str] = None
    status: str


class PortfolioUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    strategy_id: Optional[int] = None

    capital: Optional[float] = None
    expected_return: Optional[float] = None
    volatility: Optional[float] = None
    sharpe_ratio: Optional[float] = None

    optimization_method: Optional[str] = None
    status: Optional[str] = None


class PortfolioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]

    strategy_id: int

    capital: float
    expected_return: Optional[float]
    volatility: Optional[float]
    sharpe_ratio: Optional[float]

    optimization_method: Optional[str]
    status: str

    created_at: datetime


class PortfolioListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[PortfolioResponse]

