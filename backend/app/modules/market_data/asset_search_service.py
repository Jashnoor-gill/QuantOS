from __future__ import annotations

from sqlalchemy.orm import Session

from app.modules.market_data.models import Asset
from app.modules.market_data.yahoo_provider import search_symbols
from app.modules.market_data.schemas import AssetListResponse


def search_assets_service(db: Session, query: str, limit: int = 10) -> AssetListResponse:
    # Resolve candidates via provider
    candidates = search_symbols(query, limit=limit)
    if not candidates:
        return AssetListResponse(items=[])

    assets = db.query(Asset).filter(Asset.symbol.in_(candidates)).limit(limit).all()
    return AssetListResponse(items=assets)

