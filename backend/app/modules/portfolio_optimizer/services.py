from typing import Optional

from sqlalchemy.orm import Session

from app.modules.portfolio_optimizer.models import Portfolio
from app.modules.portfolio_optimizer.schemas import PortfolioCreate, PortfolioUpdate
from app.modules.strategy_engine.models import Strategy


def get_portfolio(db: Session, portfolio_id: int) -> Optional[Portfolio]:
    return db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()


def list_portfolios(
    db: Session,
    status: Optional[str] = None,
    optimization_method: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    q = db.query(Portfolio)
    if status:
        q = q.filter(Portfolio.status == status)
    if optimization_method:
        q = q.filter(Portfolio.optimization_method == optimization_method)
    return q.offset(skip).limit(limit).all()


def create_portfolio(db: Session, payload: PortfolioCreate) -> Portfolio:
    strategy = db.query(Strategy).filter(Strategy.id == payload.strategy_id).first()
    if strategy is None:
        raise ValueError("Strategy not found")

    db_obj = Portfolio(
        name=payload.name,
        description=payload.description,
        strategy_id=payload.strategy_id,
        capital=payload.capital,
        expected_return=payload.expected_return,
        volatility=payload.volatility,
        sharpe_ratio=payload.sharpe_ratio,
        optimization_method=payload.optimization_method,
        status=payload.status,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_portfolio(
    db: Session,
    portfolio_id: int,
    payload: PortfolioUpdate,
) -> Optional[Portfolio]:
    obj = get_portfolio(db, portfolio_id)
    if obj is None:
        return None

    data = payload.model_dump(exclude_unset=True)

    if "strategy_id" in data and data["strategy_id"] is not None:
        strategy = db.query(Strategy).filter(Strategy.id == data["strategy_id"]).first()
        if strategy is None:
            raise ValueError("Strategy not found")

    for k, v in data.items():
        setattr(obj, k, v)

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def delete_portfolio(db: Session, portfolio_id: int) -> bool:
    obj = get_portfolio(db, portfolio_id)
    if obj is None:
        return False

    db.delete(obj)
    db.commit()
    return True


import pandas as pd
from app.modules.portfolio_optimizer.optimizer import (
    mean_variance_optimization,
    minimum_variance_portfolio,
    risk_parity_portfolio,
    efficient_frontier,
)
from app.modules.portfolio_optimizer.schemas import (
    OptimizeRequest,
    EfficientFrontierResponse,
    EfficientFrontierPoint,
)


def _prepare_returns_df(payload: OptimizeRequest) -> pd.DataFrame:
    returns_dict = {item.asset_id: item.returns for item in payload.returns}
    return pd.DataFrame(returns_dict)


def run_mean_variance_optimization(payload: OptimizeRequest):
    returns_df = _prepare_returns_df(payload)
    result = mean_variance_optimization(
        returns_df,
        target_return=payload.target_return or 0.10,
        risk_aversion=payload.risk_aversion or 0.5,
    )
    return result


def run_minimum_variance_portfolio(payload: OptimizeRequest):
    returns_df = _prepare_returns_df(payload)
    result = minimum_variance_portfolio(returns_df)
    return result


def run_risk_parity_portfolio(payload: OptimizeRequest):
    returns_df = _prepare_returns_df(payload)
    result = risk_parity_portfolio(returns_df)
    return result


def run_efficient_frontier(payload: OptimizeRequest):
    returns_df = _prepare_returns_df(payload)
    frontier_df = efficient_frontier(returns_df)
    points = [
        EfficientFrontierPoint(
            return_val=row["return"],
            volatility=row["volatility"],
            sharpe_ratio=row["sharpe_ratio"],
        )
        for _, row in frontier_df.iterrows()
    ]
    return EfficientFrontierResponse(points=points)

