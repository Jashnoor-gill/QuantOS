from typing import Optional

from sqlalchemy.orm import Session

from app.modules.stat_arb_engine.models import StatArbPair
from app.modules.stat_arb_engine.schemas import StatArbPairCreate, StatArbPairUpdate


def get_stat_arb_pair(db: Session, pair_id: int) -> Optional[StatArbPair]:
    return db.query(StatArbPair).filter(StatArbPair.id == pair_id).first()


def list_stat_arb_pairs(
    db: Session,
    status: Optional[str] = None,
    asset_1: Optional[str] = None,
    asset_2: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    q = db.query(StatArbPair)

    if status:
        q = q.filter(StatArbPair.status == status)
    if asset_1:
        q = q.filter(StatArbPair.asset_1 == asset_1)
    if asset_2:
        q = q.filter(StatArbPair.asset_2 == asset_2)

    return q.offset(skip).limit(limit).all()


def create_stat_arb_pair(db: Session, payload: StatArbPairCreate) -> StatArbPair:
    db_obj = StatArbPair(
        asset_1=payload.asset_1,
        asset_2=payload.asset_2,
        spread_mean=payload.spread_mean,
        spread_std=payload.spread_std,
        z_score=payload.z_score,
        hedge_ratio=payload.hedge_ratio,
        signal=payload.signal,
        status=payload.status,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_stat_arb_pair(
    db: Session,
    pair_id: int,
    payload: StatArbPairUpdate,
) -> Optional[StatArbPair]:
    obj = get_stat_arb_pair(db, pair_id)
    if obj is None:
        return None

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def delete_stat_arb_pair(db: Session, pair_id: int) -> bool:
    obj = get_stat_arb_pair(db, pair_id)
    if obj is None:
        return False

    db.delete(obj)
    db.commit()
    return True

