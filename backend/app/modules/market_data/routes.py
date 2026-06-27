from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.market_data.schemas import (
    AssetCreate,
    AssetListResponse,
    AssetResponse,
    AssetUpdate,
    PriceBarCreate,
    PriceBarListResponse,
    PriceBarResponse,
    PriceBarUpdate,
)
from app.modules.market_data.services import (
    create_asset,
    create_price_bar,
    delete_asset,
    delete_price_bar,
    get_asset,
    get_price_bar,
    list_assets,
    list_price_bars,
    update_asset,
    update_price_bar,
)

router = APIRouter()


# Asset CRUD
@router.post("/assets", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
def create_asset_route(payload: AssetCreate, db: Session = Depends(get_db)):
    return create_asset(db, payload)


@router.get("/assets", response_model=AssetListResponse)
def list_assets_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = list_assets(db, skip=skip, limit=limit)
    return AssetListResponse(items=items)


@router.get("/assets/{asset_id}", response_model=AssetResponse)
def get_asset_route(asset_id: int, db: Session = Depends(get_db)):
    obj = get_asset(db, asset_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    return obj


@router.put("/assets/{asset_id}", response_model=AssetResponse)
def update_asset_route(asset_id: int, payload: AssetUpdate, db: Session = Depends(get_db)):
    obj = update_asset(db, asset_id, payload)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    return obj


@router.delete("/assets/{asset_id}")
def delete_asset_route(asset_id: int, db: Session = Depends(get_db)):
    ok = delete_asset(db, asset_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    return {"deleted": True}


# PriceBar CRUD
@router.post("/price-bars", response_model=PriceBarResponse, status_code=status.HTTP_201_CREATED)
def create_price_bar_route(payload: PriceBarCreate, db: Session = Depends(get_db)):
    try:
        return create_price_bar(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/price-bars", response_model=PriceBarListResponse)
def list_price_bars_route(
    asset_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    items = list_price_bars(db, asset_id=asset_id, skip=skip, limit=limit)
    return PriceBarListResponse(items=items)


@router.get("/price-bars/{price_bar_id}", response_model=PriceBarResponse)
def get_price_bar_route(price_bar_id: int, db: Session = Depends(get_db)):
    obj = get_price_bar(db, price_bar_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price bar not found")
    return obj


@router.put("/price-bars/{price_bar_id}", response_model=PriceBarResponse)
def update_price_bar_route(
    price_bar_id: int,
    payload: PriceBarUpdate,
    db: Session = Depends(get_db),
):
    try:
        obj = update_price_bar(db, price_bar_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price bar not found")
    return obj


@router.delete("/price-bars/{price_bar_id}")
def delete_price_bar_route(price_bar_id: int, db: Session = Depends(get_db)):
    ok = delete_price_bar(db, price_bar_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price bar not found")
    return {"deleted": True}

