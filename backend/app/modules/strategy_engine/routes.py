from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.strategy_engine.schemas import (
    StrategyCreate,
    StrategyListResponse,
    StrategyResponse,
    StrategyUpdate,
)
from app.modules.strategy_engine.services import (
    create_strategy,
    delete_strategy,
    get_strategy,
    list_strategies,
    update_strategy,
)

router = APIRouter()


@router.post(
    "/strategies",
    response_model=StrategyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(payload: StrategyCreate, db: Session = Depends(get_db)):
    try:
        return create_strategy(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/strategies",
    response_model=StrategyListResponse,
)
def list(
    status: Optional[str] = None,
    strategy_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    items = list_strategies(
        db,
        status=status,
        strategy_type=strategy_type,
        skip=skip,
        limit=limit,
    )
    return StrategyListResponse(items=items)


@router.get("/strategies/{strategy_id}", response_model=StrategyResponse)
def get(strategy_id: int, db: Session = Depends(get_db)):
    obj = get_strategy(db, strategy_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Strategy not found")
    return obj


@router.put("/strategies/{strategy_id}", response_model=StrategyResponse)
def update(
    strategy_id: int,
    payload: StrategyUpdate,
    db: Session = Depends(get_db),
):
    try:
        obj = update_strategy(db, strategy_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Strategy not found")
    return obj


@router.delete("/strategies/{strategy_id}")
def delete(strategy_id: int, db: Session = Depends(get_db)):
    ok = delete_strategy(db, strategy_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Strategy not found")
    return {"deleted": True}

