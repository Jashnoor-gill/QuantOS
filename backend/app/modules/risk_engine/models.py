from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.timestamp_mixin import TimestampMixin


class RiskMetric(TimestampMixin, Base):
    __tablename__ = "risk_metrics"

    id = Column(Integer, primary_key=True, index=True)

    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), index=True, nullable=False)

    var_95 = Column(Float, nullable=True)
    var_99 = Column(Float, nullable=True)
    expected_shortfall = Column(Float, nullable=True)
    beta = Column(Float, nullable=True)
    volatility = Column(Float, nullable=True)
    max_drawdown = Column(Float, nullable=True)

    risk_score = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    portfolio = relationship("Portfolio", backref="risk_metrics")


# Late import to avoid circular imports at module load time
from app.modules.portfolio_optimizer.models import Portfolio  # noqa: E402

