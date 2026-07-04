from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    Integer,
    String,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.timestamp_mixin import TimestampMixin


# OLD MODEL (required by Strategy Engine)
class Alpha(TimestampMixin, Base):
    __tablename__ = "alphas"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)

    expression = Column(String(5000), nullable=True)

    sharpe = Column(Float, nullable=True)
    turnover = Column(Float, nullable=True)
    fitness = Column(Float, nullable=True)

    status = Column(String(50), default="draft")


# NEW MODEL (Alpha Signals)
class AlphaSignal(TimestampMixin, Base):
    __tablename__ = "alpha_signals"

    id = Column(Integer, primary_key=True, index=True)

    asset_id = Column(
        Integer,
        ForeignKey("assets.id"),
        nullable=False,
        index=True,
    )

    date = Column(Date, nullable=False, index=True)

    alpha_momentum = Column(Float)
    alpha_trend = Column(Float)
    alpha_risk_adjusted = Column(Float)
    alpha_composite = Column(Float)

    asset = relationship(
        "Asset",
        back_populates="alpha_signals",
    )

    __table_args__ = (
        UniqueConstraint(
            "asset_id",
            "date",
            name="_asset_date_alpha_signal_uc",
        ),
    )