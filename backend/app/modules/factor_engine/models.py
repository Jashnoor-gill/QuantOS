
from datetime import date
from sqlalchemy import Column, Date, DateTime, Float, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.timestamp_mixin import TimestampMixin

class FactorExposure(TimestampMixin, Base):
    __tablename__ = "factor_exposures"

    id = Column(Integer, primary_key=True, index=True)
    
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    factor_name = Column(String(100), index=True, nullable=False)

    exposure = Column(Float, nullable=False)
    weight = Column(Float, nullable=True) # Could be used for portfolio construction

    asset = relationship("Asset", back_populates="factor_exposures")
    
    __table_args__ = (
        UniqueConstraint('asset_id', 'date', 'factor_name', name='_asset_date_factor_uc'),
    )
