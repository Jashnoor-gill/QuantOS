import yfinance as yf
import pandas as pd

def fetch_historical_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetches historical OHLCV data from Yahoo Finance.
    """
    ticker = yf.Ticker(symbol)
    history = ticker.history(start=start_date, end=end_date)
    return history

def search_symbols(query: str, limit: int = 10):
    """
    Searches for stock symbols using yfinance.
    Note: yfinance does not have a direct search function like some other APIs.
    This is a placeholder for a more advanced search provider.
    A common approach is to use a pre-compiled list of symbols or another service.
    For this project, we'll simulate a search.
    """
    # This is a very basic mock search.
    # In a real application, you'd use a more robust symbol provider.
    if query.lower() == "tech":
        return ["AAPL", "GOOG", "MSFT", "AMZN", "TSLA", "NVDA", "META", "ADBE", "INTC", "CSCO"][:limit]
    
    # Fallback to just returning the query as a symbol if it's a likely ticker
    if len(query) <= 5 and query.isalpha():
        return [query.upper()]
        
    return []

