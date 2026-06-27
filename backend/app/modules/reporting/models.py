from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.core.database import Base
from app.core.timestamp_mixin import TimestampMixin


class ResearchReport(TimestampMixin, Base):
    __tablename__ = "research_reports"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)
    report_type = Column(String(100), nullable=True)
    content = Column(Text, nullable=False)

    generated_by = Column(String(255), nullable=True)
    status = Column(String(50), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

