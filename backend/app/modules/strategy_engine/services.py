from typing import Optional

from sqlalchemy.orm import Session

from app.modules.alpha_engine.models import Alpha
from app.modules.strategy_engine.models import Strategy
from app.modules.strategy_engine.schemas import StrategyCreate, StrategyUpdate


def get_strategy(db: Session, strategy_id: int) -> Optional[Strategy]:
    return db.query(Strategy).filter(Strategy.id == strategy_id).first()


def list_strategies(
    db: Session,
    status: Optional[str] = None,
    strategy_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    q = db.query(Strategy)
    if status:
        q = q.filter(Strategy.status == status)
    if strategy_type:
        q = q.filter(Strategy.strategy_type == strategy_type)
    return q.offset(skip).limit(limit).all()


def create_strategy(db: Session, payload: StrategyCreate) -> Strategy:
    # Ensure alpha exists
    alpha = db.query(Alpha).filter(Alpha.id == payload.alpha_id).first()
    if alpha is None:
        # Keep service layer consistent with Users/Factor Engine (routes raise HTTPException)
        raise ValueError("Alpha not found")

    db_obj = Strategy(
        name=payload.name,
        description=payload.description,
        strategy_type=payload.strategy_type,
        alpha_id=payload.alpha_id,
        rebalance_frequency=payload.rebalance_frequency,
        status=payload.status,
    )

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_strategy(
    db: Session,
    strategy_id: int,
    payload: StrategyUpdate,
) -> Optional[Strategy]:
    obj = get_strategy(db, strategy_id)
    if obj is None:
        return None

    data = payload.model_dump(exclude_unset=True)

    # If alpha_id is being updated, validate alpha exists
    if "alpha_id" in data and data["alpha_id"] is not None:
        alpha_id = data["alpha_id"]
        alpha = db.query(Alpha).filter(Alpha.id == alpha_id).first()
        if alpha is None:
            raise ValueError("Alpha not found")

    for k, v in data.items():
        setattr(obj, k, v)

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def delete_strategy(db: Session, strategy_id: int) -> bool:
    obj = get_strategy(db, strategy_id)
    if obj is None:
        return False

    db.delete(obj)
    db.commit()
    return True

