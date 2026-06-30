from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.modules.market_data.models import Asset, PriceBar
from app.modules.market_data.yahoo_provider import fetch_historical_data
from app.modules.market_data.services import get_asset, create_asset

def ingest_historical_data(db: Session, symbol: str):
    """
    Ingests historical data for a given symbol.
    """
    asset = db.query(Asset).filter(Asset.symbol == symbol).first()
    if not asset:
        # Asset auto-creation
        asset = create_asset(db, {"symbol": symbol, "name": symbol, "asset_type": "stock", "exchange": "NASDAQ"})

    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=5 * 365) # 5 years of data

    history = fetch_historical_data(symbol, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

    if history.empty:
        return {"message": f"No data found for symbol {symbol}"}

    for index, row in history.iterrows():
        # Duplicate-bar prevention
        existing_bar = db.query(PriceBar).filter(
            PriceBar.asset_id == asset.id,
            PriceBar.timestamp == index.to_pydatetime()
        ).first()

        if not existing_bar:
            price_bar = PriceBar(
                asset_id=asset.id,
                timestamp=index.to_pydatetime(),
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                volume=row['Volume']
            )
            db.add(price_bar)
    
    db.commit()
    return {"message": f"Successfully ingested {len(history)} bars for {symbol}"}

def get_symbol_history(db: Session, symbol: str):
    """
    Gets historical data for a given symbol from the database.
    """
    asset = db.query(Asset).filter(Asset.symbol == symbol).first()
    if not asset:
        return None
    
    return db.query(PriceBar).filter(PriceBar.asset_id == asset.id).all()
