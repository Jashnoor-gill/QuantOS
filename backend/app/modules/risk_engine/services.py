from typing import Optional

from sqlalchemy.orm import Session

from app.modules.portfolio_optimizer.models import Portfolio
from app.modules.risk_engine.models import RiskMetric
from app.modules.risk_engine.schemas import RiskMetricCreate, RiskMetricUpdate


def get_risk_metric(db: Session, risk_metric_id: int) -> Optional[RiskMetric]:
    return db.query(RiskMetric).filter(RiskMetric.id == risk_metric_id).first()


def list_risk_metrics(
    db: Session,
    portfolio_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
):
    q = db.query(RiskMetric)
    if portfolio_id is not None:
        q = q.filter(RiskMetric.portfolio_id == portfolio_id)
    return q.offset(skip).limit(limit).all()


def create_risk_metric(db: Session, payload: RiskMetricCreate) -> RiskMetric:
    portfolio = db.query(Portfolio).filter(Portfolio.id == payload.portfolio_id).first()
    if portfolio is None:
        raise ValueError("Portfolio not found")

    db_obj = RiskMetric(
        portfolio_id=payload.portfolio_id,
        var_95=payload.var_95,
        var_99=payload.var_99,
        expected_shortfall=payload.expected_shortfall,
        beta=payload.beta,
        volatility=payload.volatility,
        max_drawdown=payload.max_drawdown,
        risk_score=payload.risk_score,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_risk_metric(
    db: Session,
    risk_metric_id: int,
    payload: RiskMetricUpdate,
) -> Optional[RiskMetric]:
    obj = get_risk_metric(db, risk_metric_id)
    if obj is None:
        return None

    data = payload.model_dump(exclude_unset=True)

    if "portfolio_id" in data and data["portfolio_id"] is not None:
        portfolio = db.query(Portfolio).filter(Portfolio.id == data["portfolio_id"]).first()
        if portfolio is None:
            raise ValueError("Portfolio not found")

    for k, v in data.items():
        setattr(obj, k, v)

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def delete_risk_metric(db: Session, risk_metric_id: int) -> bool:
    obj = get_risk_metric(db, risk_metric_id)
    if obj is None:
        return False

    db.delete(obj)
    db.commit()
    return True

