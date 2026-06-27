from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RiskMetricCreate(BaseModel):
    portfolio_id: int

    var_95: Optional[float] = None
    var_99: Optional[float] = None
    expected_shortfall: Optional[float] = None
    beta: Optional[float] = None
    volatility: Optional[float] = None
    max_drawdown: Optional[float] = None

    risk_score: Optional[float] = None


class RiskMetricUpdate(BaseModel):
    portfolio_id: Optional[int] = None

    var_95: Optional[float] = None
    var_99: Optional[float] = None
    expected_shortfall: Optional[float] = None
    beta: Optional[float] = None
    volatility: Optional[float] = None
    max_drawdown: Optional[float] = None

    risk_score: Optional[float] = None


class RiskMetricResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    portfolio_id: int

    var_95: Optional[float]
    var_99: Optional[float]
    expected_shortfall: Optional[float]
    beta: Optional[float]
    volatility: Optional[float]
    max_drawdown: Optional[float]

    risk_score: Optional[float]

    created_at: datetime


class RiskMetricListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[RiskMetricResponse]

