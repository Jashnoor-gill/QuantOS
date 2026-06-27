from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.factor_engine.schemas import (
    FactorExposureCreate,
    FactorExposureListResponse,
    FactorExposureResponse,
    FactorExposureUpdate,
)
from app.modules.factor_engine.services import (
    create_factor_exposure,
    delete_factor_exposure,
    get_factor_exposure,
    list_factor_exposures,
    update_factor_exposure,
)

router = APIRouter()


@router.post(
    "/exposures",
    response_model=FactorExposureResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(payload: FactorExposureCreate, db: Session = Depends(get_db)):
    return create_factor_exposure(db, payload)


@router.get(
    "/exposures",
    response_model=FactorExposureListResponse,
)
def list_exposures(
    factor_name: Optional[str] = None,
    symbol: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    items = list_factor_exposures(
        db,
        factor_name=factor_name,
        symbol=symbol,
        skip=skip,
        limit=limit,
    )
    return FactorExposureListResponse(items=items)


@router.get("/exposures/{exposure_id}", response_model=FactorExposureResponse)
def get(exposure_id: int, db: Session = Depends(get_db)):
    obj = get_factor_exposure(db, exposure_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factor exposure not found")
    return obj


@router.put("/exposures/{exposure_id}", response_model=FactorExposureResponse)
def update(
    exposure_id: int,
    payload: FactorExposureUpdate,
    db: Session = Depends(get_db),
):
    obj = update_factor_exposure(db, exposure_id, payload)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factor exposure not found")
    return obj


@router.delete("/exposures/{exposure_id}")
def delete(exposure_id: int, db: Session = Depends(get_db)):
    ok = delete_factor_exposure(db, exposure_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factor exposure not found")
    return {"deleted": True}

