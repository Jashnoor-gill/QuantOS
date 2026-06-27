from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text

from app.core.database import Base
from app.core.timestamp_mixin import TimestampMixin


class AIConversation(TimestampMixin, Base):
    __tablename__ = "ai_conversations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False, index=True)

    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)

    model_name = Column(String(200), nullable=True)

    token_usage = Column(Integer, nullable=True)
    latency_ms = Column(Float, nullable=True)

    status = Column(String(50), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

