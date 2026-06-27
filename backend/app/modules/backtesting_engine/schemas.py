from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BacktestCreate(BaseModel):
    strategy_id: int
    start_date: datetime
    end_date: datetime
    initial_capital: float
    final_capital: float

    total_return: Optional[float] = None
    sharpe_ratio: Optional[float] = None
    max_drawdown: Optional[float] = None

    status: str


class BacktestUpdate(BaseModel):
    strategy_id: Optional[int] = None

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    initial_capital: Optional[float] = None
    final_capital: Optional[float] = None

    total_return: Optional[float] = None
    sharpe_ratio: Optional[float] = None
    max_drawdown: Optional[float] = None

    status: Optional[str] = None


class BacktestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    strategy_id: int

    start_date: datetime
    end_date: datetime

    initial_capital: float
    final_capital: float

    total_return: Optional[float]
    sharpe_ratio: Optional[float]
    max_drawdown: Optional[float]

    status: str

    created_at: datetime


class BacktestListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[BacktestResponse]

