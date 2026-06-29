from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, List, Optional, Sequence, Tuple

import math


def _safe_mean(xs: Sequence[float]) -> Optional[float]:
    if not xs:
        return None
    return sum(xs) / len(xs)


def _pct_returns(equity: Sequence[float]) -> List[float]:
    # equity[i] -> equity[i+1]
    rets: List[float] = []
    for i in range(1, len(equity)):
        prev = equity[i - 1]
        cur = equity[i]
        if prev is None or cur is None:
            continue
        if prev == 0:
            continue
        rets.append((cur - prev) / prev)
    return rets


def sharpe_ratio(returns: Sequence[float], risk_free_rate: float = 0.0, periods_per_year: int = 252) -> Optional[float]:
    """Sharpe = (mean(r - rf)) / std(r)."""
    if len(returns) < 2:
        return None

    excess = [r - (risk_free_rate / periods_per_year) for r in returns]
    mean_excess = _safe_mean(excess)
    if mean_excess is None:
        return None

    var = sum((x - mean_excess) ** 2 for x in excess) / (len(excess) - 1)
    std = math.sqrt(var)
    if std == 0:
        return None
    return mean_excess / std * math.sqrt(periods_per_year)


def sortino_ratio(returns: Sequence[float], risk_free_rate: float = 0.0, periods_per_year: int = 252) -> Optional[float]:
    """Sortino uses downside deviation (only negative excess returns)."""
    if len(returns) < 2:
        return None

    excess = [r - (risk_free_rate / periods_per_year) for r in returns]
    downside = [x for x in excess if x < 0]
    if not downside:
        # No downside risk => undefined / infinite; return None
        return None

    mean_excess = _safe_mean(excess)
    if mean_excess is None:
        return None

    downside_var = sum((x - 0) ** 2 for x in downside) / len(downside)
    downside_dev = math.sqrt(downside_var)
    if downside_dev == 0:
        return None

    return (mean_excess / downside_dev) * math.sqrt(periods_per_year)


def cagr(equity: Sequence[float], periods_per_year: int = 252) -> Optional[float]:
    if len(equity) < 2:
        return None
    start = equity[0]
    end = equity[-1]
    if start is None or end is None:
        return None
    if start <= 0 or end <= 0:
        return None

    n_periods = len(equity) - 1
    years = n_periods / periods_per_year
    if years <= 0:
        return None

    return (end / start) ** (1 / years) - 1


def annualized_volatility(returns: Sequence[float], periods_per_year: int = 252) -> Optional[float]:
    if len(returns) < 2:
        return None
    mean = _safe_mean(returns)
    if mean is None:
        return None
    var = sum((x - mean) ** 2 for x in returns) / (len(returns) - 1)
    return math.sqrt(var) * math.sqrt(periods_per_year)


def maximum_drawdown(equity: Sequence[float]) -> Optional[float]:
    if len(equity) < 2:
        return None
    peak = equity[0]
    max_dd = 0.0
    for x in equity:
        if x is None:
            continue
        peak = max(peak, x)
        if peak == 0:
            continue
        dd = (x - peak) / peak
        max_dd = min(max_dd, dd)
    return max_dd


def calmar_ratio(returns: Sequence[float], equity: Sequence[float], periods_per_year: int = 252) -> Optional[float]:
    cagr_val = cagr(equity, periods_per_year=periods_per_year)
    mdd = maximum_drawdown(equity)
    if cagr_val is None or mdd is None:
        return None
    if mdd == 0:
        return None
    return cagr_val / abs(mdd)


def win_rate(returns: Sequence[float]) -> Optional[float]:
    if not returns:
        return None
    wins = sum(1 for r in returns if r > 0)
    return wins / len(returns)


def profit_factor(returns: Sequence[float]) -> Optional[float]:
    """Profit factor = sum(gains)/abs(sum(losses))."""
    if not returns:
        return None
    gains = sum(r for r in returns if r > 0)
    losses = sum(r for r in returns if r < 0)
    if losses == 0:
        return None
    return gains / abs(losses)


def drawdown_series_from_equity(equity: Sequence[float]) -> List[float]:
    if not equity:
        return []
    peak = equity[0]
    out: List[float] = []
    for x in equity:
        if x is None:
            out.append(0.0)
            continue
        peak = max(peak, x)
        if peak == 0:
            out.append(0.0)
            continue
        out.append((x - peak) / peak)
    return out


@dataclass
class AnalyticsComputationInput:
    equity_series: Sequence[float]


def compute_from_equity(equity_series: Sequence[float]):
    returns = _pct_returns(equity_series)

    sharpe = sharpe_ratio(returns)
    sortino = sortino_ratio(returns)
    cagr_val = cagr(equity_series)
    vol = annualized_volatility(returns)
    mdd = maximum_drawdown(equity_series)
    calmar = calmar_ratio(returns, equity_series)
    wr = win_rate(returns)
    pf = profit_factor(returns)

    return {
        "sharpe_ratio": sharpe,
        "sortino_ratio": sortino,
        "cagr": cagr_val,
        "annualized_volatility": vol,
        "maximum_drawdown": mdd,
        "calmar_ratio": calmar,
        "win_rate": wr,
        "profit_factor": pf,
        "returns": returns,
        "drawdown_series": drawdown_series_from_equity(equity_series),
    }

