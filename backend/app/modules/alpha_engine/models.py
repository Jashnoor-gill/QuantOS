from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.core.database import Base
from app.core.timestamp_mixin import TimestampMixin


class Alpha(TimestampMixin, Base):
    __tablename__ = "alphas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    description = Column(String(1024), nullable=True)
    expression = Column(String(2048), nullable=False)

    status = Column(String(50), index=True, nullable=False)

    sharpe = Column(Float, nullable=True)
    turnover = Column(Float, nullable=True)
    fitness = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

