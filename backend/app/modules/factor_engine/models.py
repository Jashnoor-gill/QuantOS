from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.core.database import Base
from app.core.timestamp_mixin import TimestampMixin


class FactorExposure(TimestampMixin, Base):
    __tablename__ = "factor_exposures"

    id = Column(Integer, primary_key=True, index=True)
    factor_name = Column(String(100), index=True, nullable=False)
    symbol = Column(String(50), index=True, nullable=False)

    exposure = Column(Float, nullable=False)
    weight = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

