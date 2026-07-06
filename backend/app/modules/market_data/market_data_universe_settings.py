from __future__ import annotations

# This module exists as a single place to keep the initial default universe.
# It is intentionally not coupled to FastAPI settings so it can be reused
# without importing environment configuration.

DEFAULT_UNIVERSE: list[str] = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "META",
    "NVDA",
    "TSLA",
    "NFLX",
    "AMD",
    "INTC",
    "JPM",
    "GS",
    "BAC",
    "V",
    "MA",
    "SPY",
    "QQQ",
    "IWM",
    "DIA",
    "TLT",
    "GLD",
    "SLV",
]


def resolve_universe(symbols: list[str] | None) -> list[str]:
    """Return requested universe if provided; otherwise return default universe."""
    if symbols and len(symbols) > 0:
        return symbols
    return list(DEFAULT_UNIVERSE)

