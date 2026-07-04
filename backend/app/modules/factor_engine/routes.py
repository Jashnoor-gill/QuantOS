
from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.factor_engine import services
from app.modules.factor_engine.schemas import (
    GenerateFactorsRequest,
    GenerateFactorsResponse,
    FactorExposureListResponse
)
from ..market_data.services import get_assets_by_symbols

router = APIRouter()

@router.post(
    "/generate/momentum",
    response_model=GenerateFactorsResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate Momentum Factors",
)
def generate_momentum(
    payload: GenerateFactorsRequest,
    db: Session = Depends(get_db)
):
    """
    Generate momentum factors (Momentum20, Momentum60) for a given set of symbols and date range.
    """
    count = services.generate_momentum_factors(db, payload)
    return {"message": "Momentum factors generated successfully.", "factors_generated": count}


@router.post(
    "/generate/sma",
    response_model=GenerateFactorsResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate Simple Moving Average (SMA) Factors",
)
def generate_sma(
    payload: GenerateFactorsRequest,
    db: Session = Depends(get_db)
):
    """
    Generate SMA factors (SMA20, SMA50) for a given set of symbols and date range.
    """
    count = services.generate_sma_factors(db, payload)
    return {"message": "SMA factors generated successfully.", "factors_generated": count}


@router.post(
    "/generate/volatility",
    response_model=GenerateFactorsResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate Volatility Factors",
)
def generate_volatility(
    payload: GenerateFactorsRequest,
    db: Session = Depends(get_db)
):
    """
    Generate volatility factors (Volatility20) for a given set of symbols and date range.
    """
    count = services.generate_volatility_factors(db, payload)
    return {"message": "Volatility factors generated successfully.", "factors_generated": count}


@router.post(
    "/generate/all",
    response_model=GenerateFactorsResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate All Factors",
)
def generate_all(
    payload: GenerateFactorsRequest,
    db: Session = Depends(get_db)
):
    """
    Generate all available factors for a given set of symbols and date range.
    """
    count = services.generate_all_factors(db, payload)
    return {"message": "All factors generated successfully.", "factors_generated": count}


@router.get(
    "/exposures",
    response_model=FactorExposureListResponse,
    summary="Get Factor Exposures",
)
def get_exposures(
    symbols: Optional[List[str]] = Query(None, description="List of symbols to filter by."),
    factor_names: Optional[List[str]] = Query(None, description="List of factor names to filter by."),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    skip: int = 0,
    limit: int = 1000,
    db: Session = Depends(get_db),
):
    """
    Retrieve stored factor exposures with filtering options.
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

    items = services.list_factor_exposures(
        db,
        asset_ids=asset_ids,
        factor_names=factor_names,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit,
    )
    return FactorExposureListResponse(items=items)

