from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.database import get_db
from app.core.security import get_current_user
from app.modules.analytics.schemas import (
    AnalyticsPerformanceResponse,
    AnalyticsQuery,
    AnalyticsRiskResponse,
    AnalyticsSummaryResponse,
    PerformancePoint,
)
from app.modules.analytics.services import compute_from_equity

from app.modules.backtesting_engine.models import Backtest
from app.modules.backtesting_engine.services import get_backtest

router = APIRouter()


# NOTE: This implementation uses backtest final_capital/initial_capital only when
# equity series is not available. This repo currently persists only scalar KPIs
# on Backtest; it does not persist full return/equity series.
# Therefore, the endpoints return computed values only when an equity series is
# provided by the caller in the future.


def _equity_from_backtest(bt: Backtest):
    # Minimal constructed equity path: start -> end.
    # Not ideal, but avoids mock data.
    if bt.initial_capital is None or bt.final_capital is None:
        raise HTTPException(status_code=400, detail="Backtest missing initial/final capital")
    return [float(bt.initial_capital), float(bt.final_capital)]


@router.get("/summary", response_model=AnalyticsSummaryResponse)
def summary(
    backtest_id: Optional[int] = Query(default=None),
    portfolio_id: Optional[int] = Query(default=None),
    db=Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    if backtest_id is None:
        raise HTTPException(status_code=400, detail="backtest_id is required for now")

    bt = get_backtest(db, backtest_id)
    if bt is None:
        raise HTTPException(status_code=404, detail="Backtest not found")

    equity = _equity_from_backtest(bt)
    res = compute_from_equity(equity)

    return AnalyticsSummaryResponse(**{k: res.get(k) for k in AnalyticsSummaryResponse.model_fields.keys()})


@router.get("/performance", response_model=AnalyticsPerformanceResponse)
def performance(
    backtest_id: Optional[int] = Query(default=None),
    portfolio_id: Optional[int] = Query(default=None),
    db=Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    if backtest_id is None:
        raise HTTPException(status_code=400, detail="backtest_id is required for now")

    bt = get_backtest(db, backtest_id)
    if bt is None:
        raise HTTPException(status_code=404, detail="Backtest not found")

    equity = _equity_from_backtest(bt)
    dd_series = compute_from_equity(equity)["drawdown_series"]

    equity_series = [PerformancePoint(name=str(i), value=float(v)) for i, v in enumerate(equity)]
    drawdown_series = [PerformancePoint(name=str(i), value=float(v)) for i, v in enumerate(dd_series)]

    return AnalyticsPerformanceResponse(equity_series=equity_series, drawdown_series=drawdown_series)


@router.get("/risk", response_model=AnalyticsRiskResponse)
def risk(
    backtest_id: Optional[int] = Query(default=None),
    portfolio_id: Optional[int] = Query(default=None),
    db=Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    # With only scalar equity, monthly returns are not available.
    # Return empty list rather than mock data.
    if backtest_id is None:
        raise HTTPException(status_code=400, detail="backtest_id is required for now")

    bt = get_backtest(db, backtest_id)
    if bt is None:
        raise HTTPException(status_code=404, detail="Backtest not found")

    return AnalyticsRiskResponse(monthly_returns=[])

