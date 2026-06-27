from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.backtesting_engine.schemas import (
    BacktestCreate,
    BacktestListResponse,
    BacktestResponse,
    BacktestUpdate,
)
from app.modules.backtesting_engine.services import (
    create_backtest,
    delete_backtest,
    get_backtest,
    list_backtests,
    update_backtest,
)

router = APIRouter()


@router.post(
    "/backtests",
    response_model=BacktestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(payload: BacktestCreate, db: Session = Depends(get_db)):
    try:
        return create_backtest(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/backtests",
    response_model=BacktestListResponse,
)
def list(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    items = list_backtests(db, status=status, skip=skip, limit=limit)
    return BacktestListResponse(items=items)


@router.get("/backtests/{backtest_id}", response_model=BacktestResponse)
def get(backtest_id: int, db: Session = Depends(get_db)):
    obj = get_backtest(db, backtest_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Backtest not found")
    return obj


@router.put("/backtests/{backtest_id}", response_model=BacktestResponse)
def update(
    backtest_id: int,
    payload: BacktestUpdate,
    db: Session = Depends(get_db),
):
    try:
        obj = update_backtest(db, backtest_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Backtest not found")
    return obj


@router.delete("/backtests/{backtest_id}")
def delete(backtest_id: int, db: Session = Depends(get_db)):
    ok = delete_backtest(db, backtest_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Backtest not found")
    return {"deleted": True}

