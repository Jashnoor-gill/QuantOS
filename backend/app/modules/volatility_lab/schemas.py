from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class VolatilityForecastCreate(BaseModel):
    asset_symbol: str
    forecast_date: datetime

    historical_volatility: Optional[float] = None
    predicted_volatility: Optional[float] = None

    model_name: Optional[str] = None
    confidence_score: Optional[float] = None

    forecast_horizon: Optional[str] = None


class VolatilityForecastUpdate(BaseModel):
    asset_symbol: Optional[str] = None
    forecast_date: Optional[datetime] = None

    historical_volatility: Optional[float] = None
    predicted_volatility: Optional[float] = None

    model_name: Optional[str] = None
    confidence_score: Optional[float] = None

    forecast_horizon: Optional[str] = None


class VolatilityForecastResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    asset_symbol: str
    forecast_date: datetime

    historical_volatility: Optional[float]
    predicted_volatility: Optional[float]

    model_name: Optional[str]
    confidence_score: Optional[float]

    forecast_horizon: Optional[str]

    created_at: datetime


class VolatilityForecastListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[VolatilityForecastResponse]

