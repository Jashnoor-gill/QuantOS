from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.alpha_engine import services
from app.modules.alpha_engine.schemas import (
    GenerateAlphaSignalRequest,
    GenerateAlphaSignalResponse,
    AlphaSignalListResponse
)
from ..market_data.services import get_assets_by_symbols

router = APIRouter()

@router.post(
    "/generate",
    response_model=GenerateAlphaSignalResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate Alpha Signals",
)
def generate_signals(
    payload: GenerateAlphaSignalRequest,
    db: Session = Depends(get_db)
):
    """
    Generate alpha signals (Momentum, Trend, Risk-Adjusted, Composite) for a given set of symbols and date range.
    This requires factor exposures to be pre-calculated.
    """
    count = services.generate_alpha_signals(db, payload)
    return {"message": "Alpha signals generated successfully.", "signals_generated": count}


@router.get(
    "/signals",
    response_model=AlphaSignalListResponse,
    summary="Get Alpha Signals",
)
def get_signals(
    symbols: Optional[List[str]] = Query(None, description="List of symbols to filter by."),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    skip: int = 0,
    limit: int = 1000,
    db: Session = Depends(get_db),
):
    """
    Retrieve stored alpha signals with filtering options.
    """
    asset_ids = None
    if symbols:
        assets = get_assets_by_symbols(db, symbols)
        if len(assets) != len(symbols):
            found_symbols = {asset.symbol for asset in assets}
            missing_symbols = set(symbols) - found_symbols
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Assets not found for symbols: {', '.join(missing_symbols)}",
            )
        asset_ids = [asset.id for asset in assets]

    items = services.list_alpha_signals(
        db,
        asset_ids=asset_ids,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit,
    )
    return AlphaSignalListResponse(items=items)
