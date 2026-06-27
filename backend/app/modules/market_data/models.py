from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.timestamp_mixin import TimestampMixin


class Asset(TimestampMixin, Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)

    symbol = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=True)
    asset_type = Column(String(50), nullable=True)
    exchange = Column(String(100), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    price_bars = relationship(
        "PriceBar",
        back_populates="asset",
        cascade="all, delete-orphan",
    )


class PriceBar(TimestampMixin, Base):
    __tablename__ = "price_bars"

    id = Column(Integer, primary_key=True, index=True)

    asset_id = Column(Integer, ForeignKey("assets.id"), index=True, nullable=False)

    timestamp = Column(DateTime, index=True, nullable=False)

    open = Column(Float, nullable=True)
    high = Column(Float, nullable=True)
    low = Column(Float, nullable=True)
    close = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    asset = relationship("Asset", back_populates="price_bars")

