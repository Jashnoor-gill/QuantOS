from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.stat_arb_engine.schemas import (
    StatArbPairCreate,
    StatArbPairListResponse,
    StatArbPairResponse,
    StatArbPairUpdate,
)
from app.modules.stat_arb_engine.services import (
    create_stat_arb_pair,
    delete_stat_arb_pair,
    get_stat_arb_pair,
    list_stat_arb_pairs,
    update_stat_arb_pair,
)

router = APIRouter()


@router.post(
    "/stat-arb-pairs",
    response_model=StatArbPairResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(payload: StatArbPairCreate, db: Session = Depends(get_db)):
    return create_stat_arb_pair(db, payload)


@router.get(
    "/stat-arb-pairs",
    response_model=StatArbPairListResponse,
)
def list(
    status: Optional[str] = None,
    asset_1: Optional[str] = None,
    asset_2: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    items = list_stat_arb_pairs(
        db,
        status=status,
        asset_1=asset_1,
        asset_2=asset_2,
        skip=skip,
        limit=limit,
    )
    return StatArbPairListResponse(items=items)


@router.get("/stat-arb-pairs/{pair_id}", response_model=StatArbPairResponse)
def get(pair_id: int, db: Session = Depends(get_db)):
    obj = get_stat_arb_pair(db, pair_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stat arb pair not found")
    return obj


@router.put("/stat-arb-pairs/{pair_id}", response_model=StatArbPairResponse)
def update(
    pair_id: int,
    payload: StatArbPairUpdate,
    db: Session = Depends(get_db),
):
    obj = update_stat_arb_pair(db, pair_id, payload)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stat arb pair not found")
    return obj


@router.delete("/stat-arb-pairs/{pair_id}")
def delete(pair_id: int, db: Session = Depends(get_db)):
    ok = delete_stat_arb_pair(db, pair_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stat arb pair not found")
    return {"deleted": True}

