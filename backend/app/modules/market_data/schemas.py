from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AssetCreate(BaseModel):
    symbol: str
    name: Optional[str] = None
    asset_type: Optional[str] = None
    exchange: Optional[str] = None


class AssetUpdate(BaseModel):
    symbol: Optional[str] = None
    name: Optional[str] = None
    asset_type: Optional[str] = None
    exchange: Optional[str] = None


class AssetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    symbol: str
    name: Optional[str]
    asset_type: Optional[str]
    exchange: Optional[str]
    created_at: datetime


class AssetListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[AssetResponse]


class PriceBarCreate(BaseModel):
    asset_id: int
    timestamp: datetime

    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[float] = None


class PriceBarUpdate(BaseModel):
    asset_id: Optional[int] = None
    timestamp: Optional[datetime] = None

    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[float] = None


class PriceBarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    asset_id: int
    timestamp: datetime

    open: Optional[float]
    high: Optional[float]
    low: Optional[float]
    close: Optional[float]
    volume: Optional[float]

    created_at: datetime


class PriceBarListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[PriceBarResponse]


class IngestUniverseRequest(BaseModel):
    symbols: Optional[list[str]] = None


class IngestUniverseSymbolResult(BaseModel):
    symbol: str
    status: str  # "ingested" | "skipped" | "failed"
    message: Optional[str] = None


class IngestUniverseResponse(BaseModel):
    success_count: int
    failure_count: int
    skipped_count: int
    results: list[IngestUniverseSymbolResult]


