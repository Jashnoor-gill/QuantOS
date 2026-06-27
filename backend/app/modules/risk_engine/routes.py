from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.risk_engine.schemas import (
    RiskMetricCreate,
    RiskMetricListResponse,
    RiskMetricResponse,
    RiskMetricUpdate,
)
from app.modules.risk_engine.services import (
    create_risk_metric,
    delete_risk_metric,
    get_risk_metric,
    list_risk_metrics,
    update_risk_metric,
)

router = APIRouter()


@router.post(
    "/risk-metrics",
    response_model=RiskMetricResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(payload: RiskMetricCreate, db: Session = Depends(get_db)):
    try:
        return create_risk_metric(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/risk-metrics",
    response_model=RiskMetricListResponse,
)
def list(
    portfolio_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    items = list_risk_metrics(db, portfolio_id=portfolio_id, skip=skip, limit=limit)
    return RiskMetricListResponse(items=items)


@router.get("/risk-metrics/{risk_metric_id}", response_model=RiskMetricResponse)
def get(risk_metric_id: int, db: Session = Depends(get_db)):
    obj = get_risk_metric(db, risk_metric_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Risk metric not found")
    return obj


@router.put("/risk-metrics/{risk_metric_id}", response_model=RiskMetricResponse)
def update(
    risk_metric_id: int,
    payload: RiskMetricUpdate,
    db: Session = Depends(get_db),
):
    try:
        obj = update_risk_metric(db, risk_metric_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Risk metric not found")
    return obj


@router.delete("/risk-metrics/{risk_metric_id}")
def delete(risk_metric_id: int, db: Session = Depends(get_db)):
    ok = delete_risk_metric(db, risk_metric_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Risk metric not found")
    return {"deleted": True}

