from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.volatility_lab.schemas import (
    VolatilityForecastCreate,
    VolatilityForecastListResponse,
    VolatilityForecastResponse,
    VolatilityForecastUpdate,
)
from app.modules.volatility_lab.services import (
    create_volatility_forecast,
    delete_volatility_forecast,
    get_volatility_forecast,
    list_volatility_forecasts,
    update_volatility_forecast,
)

router = APIRouter()


@router.post(
    "/volatility-forecasts",
    response_model=VolatilityForecastResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(payload: VolatilityForecastCreate, db: Session = Depends(get_db)):
    return create_volatility_forecast(db, payload)


@router.get(
    "/volatility-forecasts",
    response_model=VolatilityForecastListResponse,
)
def list(
    asset_symbol: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    items = list_volatility_forecasts(db, asset_symbol=asset_symbol, skip=skip, limit=limit)
    return VolatilityForecastListResponse(items=items)


@router.get("/volatility-forecasts/{forecast_id}", response_model=VolatilityForecastResponse)
def get(forecast_id: int, db: Session = Depends(get_db)):
    obj = get_volatility_forecast(db, forecast_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Volatility forecast not found")
    return obj


@router.put("/volatility-forecasts/{forecast_id}", response_model=VolatilityForecastResponse)
def update(
    forecast_id: int,
    payload: VolatilityForecastUpdate,
    db: Session = Depends(get_db),
):
    obj = update_volatility_forecast(db, forecast_id, payload)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Volatility forecast not found")
    return obj


@router.delete("/volatility-forecasts/{forecast_id}")
def delete(forecast_id: int, db: Session = Depends(get_db)):
    ok = delete_volatility_forecast(db, forecast_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Volatility forecast not found")
    return {"deleted": True}

