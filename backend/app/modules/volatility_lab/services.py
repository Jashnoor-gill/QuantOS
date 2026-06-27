from typing import Optional

from sqlalchemy.orm import Session

from app.modules.volatility_lab.models import VolatilityForecast
from app.modules.volatility_lab.schemas import (
    VolatilityForecastCreate,
    VolatilityForecastUpdate,
)


def get_volatility_forecast(db: Session, forecast_id: int) -> Optional[VolatilityForecast]:
    return db.query(VolatilityForecast).filter(VolatilityForecast.id == forecast_id).first()


def list_volatility_forecasts(
    db: Session,
    asset_symbol: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    q = db.query(VolatilityForecast)
    if asset_symbol:
        q = q.filter(VolatilityForecast.asset_symbol == asset_symbol)
    return q.offset(skip).limit(limit).all()


def create_volatility_forecast(db: Session, payload: VolatilityForecastCreate) -> VolatilityForecast:
    db_obj = VolatilityForecast(
        asset_symbol=payload.asset_symbol,
        forecast_date=payload.forecast_date,
        historical_volatility=payload.historical_volatility,
        predicted_volatility=payload.predicted_volatility,
        model_name=payload.model_name,
        confidence_score=payload.confidence_score,
        forecast_horizon=payload.forecast_horizon,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_volatility_forecast(
    db: Session,
    forecast_id: int,
    payload: VolatilityForecastUpdate,
) -> Optional[VolatilityForecast]:
    obj = get_volatility_forecast(db, forecast_id)
    if obj is None:
        return None

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def delete_volatility_forecast(db: Session, forecast_id: int) -> bool:
    obj = get_volatility_forecast(db, forecast_id)
    if obj is None:
        return False

    db.delete(obj)
    db.commit()
    return True

