from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.timestamp_mixin import TimestampMixin


class Strategy(TimestampMixin, Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    description = Column(String(1024), nullable=True)

    strategy_type = Column(String(100), index=True, nullable=False)
    alpha_id = Column(Integer, ForeignKey("alphas.id"), index=True, nullable=False)

    rebalance_frequency = Column(Float, nullable=True)

    status = Column(String(50), index=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    alpha = relationship("Alpha", backref="strategies")


# Late import to avoid circular imports at module load time
from app.modules.alpha_engine.models import Alpha  # noqa: E402

