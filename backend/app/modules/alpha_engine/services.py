from typing import Optional

from sqlalchemy.orm import Session

from app.modules.alpha_engine.models import Alpha
from app.modules.alpha_engine.schemas import AlphaCreate, AlphaUpdate


def get_alpha(db: Session, alpha_id: int) -> Optional[Alpha]:
    return db.query(Alpha).filter(Alpha.id == alpha_id).first()


def list_alphas(
    db: Session,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    q = db.query(Alpha)
    if status:
        q = q.filter(Alpha.status == status)
    return q.offset(skip).limit(limit).all()


def create_alpha(db: Session, payload: AlphaCreate) -> Alpha:
    db_obj = Alpha(
        name=payload.name,
        description=payload.description,
        expression=payload.expression,
        status=payload.status,
        sharpe=payload.sharpe,
        turnover=payload.turnover,
        fitness=payload.fitness,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_alpha(
    db: Session,
    alpha_id: int,
    payload: AlphaUpdate,
) -> Optional[Alpha]:
    obj = get_alpha(db, alpha_id)
    if obj is None:
        return None

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def delete_alpha(db: Session, alpha_id: int) -> bool:
    obj = get_alpha(db, alpha_id)
    if obj is None:
        return False

    db.delete(obj)
    db.commit()
    return True

