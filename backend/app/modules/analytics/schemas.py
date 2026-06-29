from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class AnalyticsSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sharpe_ratio: Optional[float] = None
    sortino_ratio: Optional[float] = None
    cagr: Optional[float] = None
    annualized_volatility: Optional[float] = None
    maximum_drawdown: Optional[float] = None
    calmar_ratio: Optional[float] = None
    win_rate: Optional[float] = None
    profit_factor: Optional[float] = None


class PerformancePoint(BaseModel):
    name: str
    value: float


class AnalyticsPerformanceResponse(BaseModel):
    # For now this is a generic series; backend may choose monthly/daily bins.
    equity_series: List[PerformancePoint] = []
    drawdown_series: List[PerformancePoint] = []


class AnalyticsRiskResponse(BaseModel):
    # Generic distribution of returns (optional)
    monthly_returns: List[PerformancePoint] = []


# Query params
class AnalyticsQuery(BaseModel):
    # Choose which backtest or portfolio to use. For now these are optional.
    backtest_id: Optional[int] = None
    portfolio_id: Optional[int] = None
    # For future: provide returns series directly.

