from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.core.database import Base
from app.core.timestamp_mixin import TimestampMixin


class StatArbPair(TimestampMixin, Base):
    __tablename__ = "stat_arb_pairs"

    id = Column(Integer, primary_key=True, index=True)

    asset_1 = Column(String(50), index=True, nullable=False)
    asset_2 = Column(String(50), index=True, nullable=False)

    spread_mean = Column(Float, nullable=True)
    spread_std = Column(Float, nullable=True)

    z_score = Column(Float, nullable=True)
    hedge_ratio = Column(Float, nullable=True)
    signal = Column(Float, nullable=True)

    status = Column(String(50), index=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

