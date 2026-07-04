from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

# --- Request Schemas ---

class GenerateAlphaSignalRequest(BaseModel):
    symbols: Optional[List[str]] = Field(None, description="List of asset symbols to generate signals for. If empty, runs for all assets.")
    start_date: date = Field(..., description="Start date for signal calculation.")
    end_date: date = Field(..., description="End date for signal calculation.")

# --- Response Schemas ---

class GenerateAlphaSignalResponse(BaseModel):
    message: str
    signals_generated: int

class AlphaSignalBase(BaseModel):
    asset_id: int
    date: date
    alpha_momentum: Optional[float] = None
    alpha_trend: Optional[float] = None
    alpha_risk_adjusted: Optional[float] = None
    alpha_composite: Optional[float] = None

class AlphaSignalCreate(AlphaSignalBase):
    pass

class AssetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    symbol: str
    name: Optional[str] = None

class AlphaSignalResponse(AlphaSignalBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    asset: AssetResponse
    created_at: datetime
    updated_at: datetime

AlphaSignalResponse.model_rebuild()

class AlphaSignalListResponse(BaseModel):
    items: List[AlphaSignalResponse]
