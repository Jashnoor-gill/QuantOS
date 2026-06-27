from typing import Optional

from sqlalchemy.orm import Session

from app.modules.backtesting_engine.models import Backtest
from app.modules.backtesting_engine.schemas import BacktestCreate, BacktestUpdate
from app.modules.strategy_engine.models import Strategy


def get_backtest(db: Session, backtest_id: int) -> Optional[Backtest]:
    return db.query(Backtest).filter(Backtest.id == backtest_id).first()


def list_backtests(
    db: Session,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    q = db.query(Backtest)
    if status:
        q = q.filter(Backtest.status == status)
    return q.offset(skip).limit(limit).all()


def create_backtest(db: Session, payload: BacktestCreate) -> Backtest:
    strategy = db.query(Strategy).filter(Strategy.id == payload.strategy_id).first()
    if strategy is None:
        raise ValueError("Strategy not found")

    db_obj = Backtest(
        strategy_id=payload.strategy_id,
        start_date=payload.start_date,
        end_date=payload.end_date,
        initial_capital=payload.initial_capital,
        final_capital=payload.final_capital,
        total_return=payload.total_return,
        sharpe_ratio=payload.sharpe_ratio,
        max_drawdown=payload.max_drawdown,
        status=payload.status,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_backtest(db: Session, backtest_id: int, payload: BacktestUpdate) -> Optional[Backtest]:
    obj = get_backtest(db, backtest_id)
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


def delete_backtest(db: Session, backtest_id: int) -> bool:
    obj = get_backtest(db, backtest_id)
    if obj is None:
        return False

    db.delete(obj)
    db.commit()
    return True

