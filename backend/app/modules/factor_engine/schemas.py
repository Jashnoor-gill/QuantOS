
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

# --- Request Schemas ---

class GenerateFactorsRequest(BaseModel):
    symbols: Optional[List[str]] = Field(None, description="List of asset symbols to generate factors for. If empty, runs for all assets.")
    start_date: date = Field(..., description="Start date for factor calculation.")
    end_date: date = Field(..., description="End date for factor calculation.")

# --- Response Schemas ---

class GenerateFactorsResponse(BaseModel):
    message: str
    factors_generated: int

class FactorExposureBase(BaseModel):
    asset_id: int
    date: date
    factor_name: str
    exposure: float
    weight: Optional[float] = None

class FactorExposureCreate(FactorExposureBase):
    pass

class FactorExposureUpdate(BaseModel):
    exposure: Optional[float] = None
    weight: Optional[float] = None

class FactorExposureResponse(FactorExposureBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    asset: 'AssetResponse' # To show symbol and other asset info
    created_at: datetime
    updated_at: datetime

class AssetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    symbol: str
    name: Optional[str] = None

# This is needed to resolve the forward reference
FactorExposureResponse.model_rebuild()

class FactorExposureListResponse(BaseModel):
    items: List[FactorExposureResponse]
