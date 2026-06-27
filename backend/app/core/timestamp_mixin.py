from datetime import datetime

class TimestampMixin:
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()