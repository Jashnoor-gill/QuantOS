
import pandas as pd
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date

from .models import FactorExposure
from .schemas import FactorExposureCreate, GenerateFactorsRequest
from ..market_data.models import Asset, PriceBar
from sqlalchemy import delete, and_

def get_prices_for_assets(db: Session, asset_ids: List[int], start_date: date, end_date: date) -> pd.DataFrame:
    """
    Fetches historical price data for a list of assets and returns it as a pandas DataFrame.
    """
    if not asset_ids:
        return pd.DataFrame()

    prices_query = (
        db.query(PriceBar.timestamp, PriceBar.asset_id, PriceBar.close)
        .filter(
            PriceBar.asset_id.in_(asset_ids),
            PriceBar.timestamp >= start_date,
            PriceBar.timestamp <= end_date,
        )
        .order_by(PriceBar.asset_id, PriceBar.timestamp)
    )

    prices_df = pd.read_sql(prices_query.statement, db.get_bind())

    if prices_df.empty:
        return pd.DataFrame()

    prices_df['timestamp'] = pd.to_datetime(prices_df['timestamp'])
    prices_df = prices_df.rename(columns={'timestamp': 'date'})
    prices_df = prices_df.set_index(['date', 'asset_id'])

    # Unstack, resample to daily, forward-fill gaps, then restack
    unstacked = prices_df['close'].unstack()
    daily_unstacked = unstacked.resample('D').last().ffill()
    daily_prices = daily_unstacked.stack(dropna=False).reset_index()
    daily_prices.columns = ['date', 'asset_id', 'close']
    daily_prices = daily_prices.set_index(['date', 'asset_id']).sort_index()

    return daily_prices

def calculate_momentum(prices: pd.DataFrame, window: int) -> pd.DataFrame:
    """Calculates momentum factor."""
    return prices.groupby(level='asset_id')['close'].transform(
        lambda x: x / x.shift(window) - 1
    ).to_frame(name=f'Momentum{window}')

def calculate_sma(prices: pd.DataFrame, window: int) -> pd.DataFrame:
    """Calculates simple moving average factor."""
    return prices.groupby(level='asset_id')['close'].transform(
        lambda x: x.rolling(window=window).mean()
    ).to_frame(name=f'SMA{window}')

def calculate_volatility(prices: pd.DataFrame, window: int) -> pd.DataFrame:
    """Calculates volatility factor."""
    daily_returns = prices.groupby(level='asset_id')['close'].transform(lambda x: x.pct_change())
    return daily_returns.groupby(level='asset_id').transform(
        lambda x: x.rolling(window=window).std()
    ).to_frame(name=f'Volatility{window}')

def _generate_factors(db: Session, payload: GenerateFactorsRequest, factor_calculators: list) -> int:
    """
    Generic function to generate and store factors based on a list of calculator functions.
    """
    if payload.symbols:
        assets = db.query(Asset).filter(Asset.symbol.in_(payload.symbols)).all()
        if len(assets) != len(payload.symbols):
            found_symbols = {asset.symbol for asset in assets}
            missing_symbols = set(payload.symbols) - found_symbols
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Assets not found for symbols: {', '.join(missing_symbols)}",
            )
        asset_ids = [asset.id for asset in assets]
    else:
        assets = db.query(Asset).all()
        asset_ids = [asset.id for asset in assets]

    if not asset_ids:
        return 0

    # We need to fetch enough data to warm up the longest calculation window
    max_window = 100 # A safe upper bound for lookback period
    import datetime
    effective_start_date = payload.start_date - datetime.timedelta(days=max_window * 2)

    prices_df = get_prices_for_assets(db, asset_ids, effective_start_date, payload.end_date)
    if prices_df.empty:
        return 0

    all_factors_df = pd.DataFrame(index=prices_df.index)
    factor_names = []

    for calculator in factor_calculators:
        factor_df = calculator(prices_df)
        all_factors_df = all_factors_df.join(factor_df)
        factor_names.extend(factor_df.columns)

    all_factors_df = all_factors_df.dropna().reset_index()
    
    # Filter for the requested date range
    all_factors_df = all_factors_df[all_factors_df['date'].dt.date >= payload.start_date]

    melted_factors = all_factors_df.melt(
        id_vars=['date', 'asset_id'],
        value_vars=factor_names,
        var_name='factor_name',
        value_name='exposure'
    )

    if melted_factors.empty:
        return 0

    new_exposures = [
        FactorExposureCreate(
            asset_id=row['asset_id'],
            date=row['date'].date(),
            factor_name=row['factor_name'],
            exposure=row['exposure']
        )
        for row in melted_factors.to_dict('records')
    ]

    with db.begin_nested():
        # Delete existing exposures for the same assets, factors, and date range
        stmt = delete(FactorExposure).where(
            and_(
                FactorExposure.asset_id.in_(asset_ids),
                FactorExposure.factor_name.in_(factor_names),
                FactorExposure.date >= payload.start_date,
                FactorExposure.date <= payload.end_date,
            )
        )
        db.execute(stmt)

        # Bulk insert new exposures
        db.bulk_insert_mappings(FactorExposure, [exp.model_dump() for exp in new_exposures])
    
    db.commit()

    return len(new_exposures)

def generate_momentum_factors(db: Session, payload: GenerateFactorsRequest) -> int:
    calculators = [
        lambda p: calculate_momentum(p, 20),
        lambda p: calculate_momentum(p, 60),
    ]
    return _generate_factors(db, payload, calculators)

def generate_sma_factors(db: Session, payload: GenerateFactorsRequest) -> int:
    calculators = [
        lambda p: calculate_sma(p, 20),
        lambda p: calculate_sma(p, 50),
    ]
    return _generate_factors(db, payload, calculators)

def generate_volatility_factors(db: Session, payload: GenerateFactorsRequest) -> int:
    calculators = [
        lambda p: calculate_volatility(p, 20),
    ]
    return _generate_factors(db, payload, calculators)

def generate_all_factors(db: Session, payload: GenerateFactorsRequest) -> int:
    calculators = [
        lambda p: calculate_momentum(p, 20),
        lambda p: calculate_momentum(p, 60),
        lambda p: calculate_sma(p, 20),
        lambda p: calculate_sma(p, 50),
        lambda p: calculate_volatility(p, 20),
    ]
    return _generate_factors(db, payload, calculators)

def list_factor_exposures(
    db: Session,
    asset_ids: Optional[List[int]] = None,
    factor_names: Optional[List[str]] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 1000,
) -> List[FactorExposure]:
    q = db.query(FactorExposure).join(Asset)

    if asset_ids:
        q = q.filter(FactorExposure.asset_id.in_(asset_ids))
    if factor_names:
        q = q.filter(FactorExposure.factor_name.in_(factor_names))
    if start_date:
        q = q.filter(FactorExposure.date >= start_date)
    if end_date:
        q = q.filter(FactorExposure.date <= end_date)

    return q.order_by(FactorExposure.date.desc(), FactorExposure.asset_id, FactorExposure.factor_name).offset(skip).limit(limit).all()
