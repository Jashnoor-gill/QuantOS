from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.timestamp_mixin import TimestampMixin


class Portfolio(TimestampMixin, Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), index=True, nullable=False)
    description = Column(String(1024), nullable=True)

    strategy_id = Column(Integer, ForeignKey("strategies.id"), index=True, nullable=False)

    capital = Column(Float, nullable=False)
    expected_return = Column(Float, nullable=True)
    volatility = Column(Float, nullable=True)
    sharpe_ratio = Column(Float, nullable=True)

    optimization_method = Column(String(100), nullable=True)
    status = Column(String(50), index=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    strategy = relationship("Strategy", backref="portfolios")


# Late import to avoid circular imports at module load time
from app.modules.strategy_engine.models import Strategy  # noqa: E402

