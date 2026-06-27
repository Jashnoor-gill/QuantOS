from typing import Optional

from sqlalchemy.orm import Session

from app.modules.factor_engine.models import FactorExposure
from app.modules.factor_engine.schemas import FactorExposureCreate, FactorExposureUpdate


def get_factor_exposure(db: Session, exposure_id: int) -> Optional[FactorExposure]:
    return db.query(FactorExposure).filter(FactorExposure.id == exposure_id).first()


def list_factor_exposures(
    db: Session,
    factor_name: Optional[str] = None,
    symbol: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    q = db.query(FactorExposure)

    if factor_name:
        q = q.filter(FactorExposure.factor_name == factor_name)
    if symbol:
        q = q.filter(FactorExposure.symbol == symbol)

    return q.offset(skip).limit(limit).all()


def create_factor_exposure(db: Session, payload: FactorExposureCreate) -> FactorExposure:
    db_obj = FactorExposure(
        factor_name=payload.factor_name,
        symbol=payload.symbol,
        exposure=payload.exposure,
        weight=payload.weight,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_factor_exposure(
    db: Session,
    exposure_id: int,
    payload: FactorExposureUpdate,
) -> Optional[FactorExposure]:
    obj = get_factor_exposure(db, exposure_id)
    if obj is None:
        return None

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def delete_factor_exposure(db: Session, exposure_id: int) -> bool:
    obj = get_factor_exposure(db, exposure_id)
    if obj is None:
        return False

    db.delete(obj)
    db.commit()
    return True

