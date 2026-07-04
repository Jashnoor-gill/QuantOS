import pandas as pd
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date
from scipy.stats import zscore
from sqlalchemy import delete, and_

from .models import AlphaSignal
from .schemas import AlphaSignalCreate, GenerateAlphaSignalRequest
from ..market_data.models import Asset
from ..factor_engine.models import FactorExposure

def get_factor_exposures_for_assets(db: Session, asset_ids: List[int], start_date: date, end_date: date) -> pd.DataFrame:
    """
    Fetches factor exposures for a list of assets and returns it as a pandas DataFrame.
    """
    if not asset_ids:
        return pd.DataFrame()

    required_factors = ['Momentum20', 'Momentum60', 'SMA20', 'SMA50', 'Volatility20']

    exposures_query = (
        db.query(FactorExposure.date, FactorExposure.asset_id, FactorExposure.factor_name, FactorExposure.exposure)
        .filter(
            FactorExposure.asset_id.in_(asset_ids),
            FactorExposure.date >= start_date,
            FactorExposure.date <= end_date,
            FactorExposure.factor_name.in_(required_factors)
        )
        .order_by(FactorExposure.asset_id, FactorExposure.date)
    )

    exposures_df = pd.read_sql(exposures_query.statement, db.get_bind())

    if exposures_df.empty:
        return pd.DataFrame()

    # Pivot the table to have factors as columns
    pivoted_df = exposures_df.pivot_table(index=['date', 'asset_id'], columns='factor_name', values='exposure').reset_index()
    pivoted_df['date'] = pd.to_datetime(pivoted_df['date'])
    pivoted_df = pivoted_df.set_index(['date', 'asset_id']).sort_index()
    
    # Forward fill any missing values within each asset group
    pivoted_df = pivoted_df.groupby(level='asset_id').ffill()

    return pivoted_df

def calculate_alpha_signals(factors_df: pd.DataFrame) -> pd.DataFrame:
    """Calculates all alpha signals from a DataFrame of factor exposures."""
    signals = pd.DataFrame(index=factors_df.index)

    # 1. AlphaMomentum = Momentum20
    if 'Momentum20' in factors_df.columns:
        signals['alpha_momentum'] = factors_df['Momentum20']

    # 2. AlphaTrend = SMA20/SMA50 - 1
    if 'SMA20' in factors_df.columns and 'SMA50' in factors_df.columns:
        # To avoid division by zero, replace 0s in SMA50 with a small number or NaN
        sma50 = factors_df['SMA50'].replace(0, pd.NA)
        signals['alpha_trend'] = factors_df['SMA20'] / sma50 - 1

    # 3. AlphaRiskAdjusted = Momentum60/Volatility20
    if 'Momentum60' in factors_df.columns and 'Volatility20' in factors_df.columns:
        vol20 = factors_df['Volatility20'].replace(0, pd.NA)
        signals['alpha_risk_adjusted'] = factors_df['Momentum60'] / vol20
        
    # 4. AlphaComposite = zscore(Momentum20)+zscore(Momentum60)-zscore(Volatility20)
    if all(f in factors_df.columns for f in ['Momentum20', 'Momentum60', 'Volatility20']):
        # Calculate z-scores cross-sectionally for each day
        z_mom20 = factors_df.groupby(level='date')['Momentum20'].transform(lambda x: zscore(x, nan_policy='omit'))
        z_mom60 = factors_df.groupby(level='date')['Momentum60'].transform(lambda x: zscore(x, nan_policy='omit'))
        z_vol20 = factors_df.groupby(level='date')['Volatility20'].transform(lambda x: zscore(x, nan_policy='omit'))
        signals['alpha_composite'] = z_mom20 + z_mom60 - z_vol20

    return signals.dropna(how='all')


def generate_alpha_signals(db: Session, payload: GenerateAlphaSignalRequest) -> int:
    """
    Generate and store alpha signals based on factor exposures.
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

    # Fetch factor exposures
    factors_df = get_factor_exposures_for_assets(db, asset_ids, payload.start_date, payload.end_date)
    
    if factors_df.empty or not all(f in factors_df.columns for f in ['Momentum20', 'Momentum60', 'SMA20', 'SMA50', 'Volatility20']):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not retrieve all required factor exposures (Momentum20, Momentum60, SMA20, SMA50, Volatility20) for the given assets and date range. Please generate factors first."
        )

    # Calculate alpha signals
    alpha_signals_df = calculate_alpha_signals(factors_df)

    if alpha_signals_df.empty:
        return 0
        
    alpha_signals_df = alpha_signals_df.reset_index()

    # Filter for the requested date range again to be safe
    alpha_signals_df = alpha_signals_df[alpha_signals_df['date'].dt.date >= payload.start_date]

    if alpha_signals_df.empty:
        return 0

    new_signals = [
        AlphaSignalCreate(
            asset_id=row['asset_id'],
            date=row['date'].date(),
            alpha_momentum=row.get('alpha_momentum'),
            alpha_trend=row.get('alpha_trend'),
            alpha_risk_adjusted=row.get('alpha_risk_adjusted'),
            alpha_composite=row.get('alpha_composite'),
        )
        for row in alpha_signals_df.to_dict('records')
    ]

    with db.begin_nested():
        # Delete existing signals for the same assets and date range
        stmt = delete(AlphaSignal).where(
            and_(
                AlphaSignal.asset_id.in_(asset_ids),
                AlphaSignal.date >= payload.start_date,
                AlphaSignal.date <= payload.end_date,
            )
        )
        db.execute(stmt)

        # Bulk insert new signals
        db.bulk_insert_mappings(AlphaSignal, [sig.model_dump(exclude_none=True) for sig in new_signals])
    
    db.commit()

    return len(new_signals)


def list_alpha_signals(
    db: Session,
    asset_ids: Optional[List[int]] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 1000,
) -> List[AlphaSignal]:
    q = db.query(AlphaSignal).join(Asset)

    if asset_ids:
        q = q.filter(AlphaSignal.asset_id.in_(asset_ids))
    if start_date:
        q = q.filter(AlphaSignal.date >= start_date)
    if end_date:
        q = q.filter(AlphaSignal.date <= end_date)

    return q.order_by(AlphaSignal.date.desc(), AlphaSignal.asset_id).offset(skip).limit(limit).all()
