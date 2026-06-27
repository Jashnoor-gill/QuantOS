from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.core.database import Base
from app.core.timestamp_mixin import TimestampMixin


class VolatilityForecast(TimestampMixin, Base):
    __tablename__ = "volatility_forecasts"

    id = Column(Integer, primary_key=True, index=True)

    asset_symbol = Column(String(50), index=True, nullable=False)
    forecast_date = Column(DateTime, nullable=False, index=True)

    historical_volatility = Column(Float, nullable=True)
    predicted_volatility = Column(Float, nullable=True)

    model_name = Column(String(100), nullable=True)
    confidence_score = Column(Float, nullable=True)

    forecast_horizon = Column(String(50), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

