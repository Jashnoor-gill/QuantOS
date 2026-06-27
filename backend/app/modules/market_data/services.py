from typing import Optional

from sqlalchemy.orm import Session

from app.modules.market_data.models import Asset, PriceBar
from app.modules.market_data.schemas import AssetCreate, AssetUpdate, PriceBarCreate, PriceBarUpdate


def get_asset(db: Session, asset_id: int) -> Optional[Asset]:
    return db.query(Asset).filter(Asset.id == asset_id).first()


def list_assets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Asset).offset(skip).limit(limit).all()


def create_asset(db: Session, payload: AssetCreate) -> Asset:
    db_obj = Asset(
        symbol=payload.symbol,
        name=payload.name,
        asset_type=payload.asset_type,
        exchange=payload.exchange,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_asset(db: Session, asset_id: int, payload: AssetUpdate) -> Optional[Asset]:
    obj = get_asset(db, asset_id)
    if obj is None:
        return None

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def delete_asset(db: Session, asset_id: int) -> bool:
    obj = get_asset(db, asset_id)
    if obj is None:
        return False

    db.delete(obj)
    db.commit()
    return True


def get_price_bar(db: Session, price_bar_id: int) -> Optional[PriceBar]:
    return db.query(PriceBar).filter(PriceBar.id == price_bar_id).first()


def list_price_bars(
    db: Session,
    asset_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
):
    q = db.query(PriceBar)
    if asset_id is not None:
        q = q.filter(PriceBar.asset_id == asset_id)
    return q.offset(skip).limit(limit).all()


def create_price_bar(db: Session, payload: PriceBarCreate) -> PriceBar:
    asset = get_asset(db, payload.asset_id)
    if asset is None:
        raise ValueError("Asset not found")

    db_obj = PriceBar(
        asset_id=payload.asset_id,
        timestamp=payload.timestamp,
        open=payload.open,
        high=payload.high,
        low=payload.low,
        close=payload.close,
        volume=payload.volume,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_price_bar(
    db: Session,
    price_bar_id: int,
    payload: PriceBarUpdate,
) -> Optional[PriceBar]:
    obj = get_price_bar(db, price_bar_id)
    if obj is None:
        return None

    data = payload.model_dump(exclude_unset=True)
    if "asset_id" in data and data["asset_id"] is not None:
        asset = get_asset(db, data["asset_id"])
        if asset is None:
            raise ValueError("Asset not found")

    for k, v in data.items():
        setattr(obj, k, v)

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def delete_price_bar(db: Session, price_bar_id: int) -> bool:
    obj = get_price_bar(db, price_bar_id)
    if obj is None:
        return False

    db.delete(obj)
    db.commit()
    return True

