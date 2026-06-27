from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.timestamp_mixin import TimestampMixin


class Backtest(TimestampMixin, Base):
    __tablename__ = "backtests"

    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), index=True, nullable=False)

    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    initial_capital = Column(Float, nullable=False)
    final_capital = Column(Float, nullable=False)

    total_return = Column(Float, nullable=True)
    sharpe_ratio = Column(Float, nullable=True)
    max_drawdown = Column(Float, nullable=True)

    status = Column(String(50), index=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    strategy = relationship("Strategy", backref="backtests")


# Late import to avoid circular imports at module load time
from app.modules.strategy_engine.models import Strategy  # noqa: E402

