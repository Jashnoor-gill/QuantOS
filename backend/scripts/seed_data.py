import math
import random
from datetime import datetime, timedelta
from typing import Iterable, List, Sequence, Tuple

from sqlalchemy.orm import Session


# Ensure project root is on sys.path so `import app...` works when running:
#   python scripts/seed_data.py
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.core.database import Base, SessionLocal, engine

from app.modules.alpha_engine.models import Alpha
from app.modules.backtesting_engine.models import Backtest
from app.modules.factor_engine.models import FactorExposure
from app.modules.market_data.models import Asset, PriceBar
from app.modules.portfolio_optimizer.models import Portfolio
from app.modules.strategy_engine.models import Strategy


# ---- Quant-style demo helpers ----

FACTOR_DEFINITIONS: Sequence[Tuple[str, str]] = [
    ("Momentum", "MOM"),
    ("Value", "VAL"),
    ("Size", "SMB"),
    ("Volatility", "VOL"),
    ("Quality", "QUAL"),
    ("MeanReversion", "MR"),
]

STRATEGY_TYPES: Sequence[str] = [
    "Momentum",
    "Value",
    "Quality",
    "Volatility",
    "MeanReversion",
    "Multi-Factor",
]

STATUSES: Sequence[str] = ["draft", "active", "paused", "archived"]


def _rng(seed: int) -> random.Random:
    return random.Random(seed)


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _make_expression(strategy_type: str, alpha_index: int) -> str:
    # Simple, readable pseudo-formula strings (fits the schema: expression field is a string).
    # Keep them deterministic-ish.
    base = alpha_index % 7
    if strategy_type == "Momentum":
        return f"rank(log(close)) - rank(log(sma(close, {10 + base})))"
    if strategy_type == "Value":
        return f"-rank(log(price_to_book)) + rank(sma(growth, {20 + base}))"
    if strategy_type == "Size":
        return f"rank(-log(market_cap)) + 0.5*rank(sma(earnings_yield, {15 + base}))"
    if strategy_type == "Volatility":
        return f"-rank(rolling_std(close, {14 + base})) + rank(sma(close, {9 + base}))"
    if strategy_type == "Quality":
        return f"rank(roe) + 0.7*rank(gross_margin) - 0.3*rank(debt_to_equity)"
    if strategy_type == "MeanReversion":
        return f"-zscore(close, {21 + base})"

    # Multi-Factor
    return (
        f"0.3*rank(log(close) - log(sma(close,{12 + base}))) + "
        f"0.25*rank(roe) - 0.2*rank(rolling_std(close,{18 + base})) + "
        f"0.25*(-zscore(close,{20 + base}))"
    )


def _generate_assets(rng: random.Random, n: int) -> List[Asset]:
    sectors = ["Tech", "Healthcare", "Finance", "Energy", "Industrials", "Consumer"]
    exchanges = ["NYSE", "NASDAQ", "AMEX"]

    assets: List[Asset] = []
    for i in range(1, n + 1):
        symbol = f"AS{i:03d}"
        name = f"Asset {i:03d}"
        asset_type = rng.choice(["Equity", "ETF"])
        exchange = rng.choice(exchanges)
        asset = Asset(
            symbol=symbol,
            name=name,
            asset_type=asset_type,
            exchange=exchange,
        )
        assets.append(asset)

    return assets


def _generate_price_bars(rng: random.Random, asset: Asset, days: int = 90) -> List[PriceBar]:
    # Generate a small history to make the data feel real; dashboard uses factor exposures only,
    # but idempotent seeding should keep things coherent.
    end = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    start = end - timedelta(days=days)

    # Start close around 20-200, random walk with volatility regime.
    price = rng.uniform(30, 200)
    vol = rng.uniform(0.01, 0.04)

    bars: List[PriceBar] = []
    current = start
    while current <= end:
        drift = rng.uniform(-0.0003, 0.0006)
        shock = rng.gauss(0, vol)
        ret = drift + shock
        open_ = price
        close = max(0.5, price * (1 + ret))
        high = max(open_, close) * (1 + abs(rng.gauss(0, vol / 2)))
        low = min(open_, close) * (1 - abs(rng.gauss(0, vol / 2)))
        volume = rng.uniform(5e5, 5e6)

        bars.append(
            PriceBar(
                asset=asset,
                timestamp=current,
                open=float(open_),
                high=float(high),
                low=float(low),
                close=float(close),
                volume=float(volume),
            )
        )

        price = close
        current += timedelta(days=1)

    return bars


def _factor_exposure_rows(
    rng: random.Random,
    assets: Sequence[Asset],
    factor_names: Sequence[str],
    per_factor_assets: int,
) -> Iterable[Tuple[str, str, float, float]]:
    # Return (factor_name, symbol, exposure, weight)
    # Ensure exactly ~50 rows total with decent concentration.
    for factor_name in factor_names:
        # Choose assets; deterministic choice via rng.
        chosen = rng.sample(list(assets), k=per_factor_assets)
        for a in chosen:
            # Exposure: typical z-score range
            exposure = rng.gauss(0, 1.2)
            # Weight: small tilts
            weight = _clamp(exposure / 5.0 + rng.gauss(0, 0.05), -0.5, 0.5)
            yield (factor_name, a.symbol, float(exposure), float(weight))


def _quality_metric(rng: random.Random) -> float:
    # A pseudo quality metric between 0..1
    return _clamp(0.2 + 0.7 * rng.random() + rng.gauss(0, 0.05), 0.0, 1.0)


def _generate_alphas(rng: random.Random, n: int) -> List[Alpha]:
    alphas: List[Alpha] = []
    for i in range(1, n + 1):
        # Pick a strategy type and map to a factor/alpha style.
        st = rng.choice(list(STRATEGY_TYPES))
        # Status: slightly more active than draft
        status = rng.choices(
            population=["active", "draft", "paused"],
            weights=[0.55, 0.35, 0.1],
            k=1,
        )[0]

        # Realistic-ish risk/perf numbers
        sharpe = _clamp(rng.gauss(1.1, 0.6), -0.5, 3.5)
        turnover = _clamp(abs(rng.gauss(0.35, 0.2)), 0.01, 2.5)
        fitness = _clamp(rng.gauss(0.65, 0.25), -0.5, 1.5)

        expr = _make_expression(st, i)

        alphas.append(
            Alpha(
                name=f"Alpha {i:03d} ({st})",
                description=f"Demo alpha based on {st} signals; idempotent generated seed data.",
                expression=expr,
                status=status,
                sharpe=float(sharpe),
                turnover=float(turnover),
                fitness=float(fitness),
            )
        )

    return alphas


def _generate_strategies(rng: random.Random, alphas: Sequence[Alpha], n: int) -> List[Strategy]:
    strategies: List[Strategy] = []

    for i in range(1, n + 1):
        alpha = rng.choice(list(alphas))
        stype = rng.choice(list(STRATEGY_TYPES))
        rebalance = _clamp(rng.choice([5, 7, 10, 14, 21]) / 21.0 + rng.gauss(0, 0.05), 0.05, 1.0)
        status = rng.choices(
            population=["active", "draft", "paused"],
            weights=[0.6, 0.25, 0.15],
            k=1,
        )[0]

        strategies.append(
            Strategy(
                name=f"Strategy {i:02d}",
                description=f"Execution model for {stype} signals. Links to Alpha {alpha.id}.",
                strategy_type=stype,
                alpha_id=alpha.id,
                rebalance_frequency=float(rebalance),
                status=status,
            )
        )

    return strategies


def _generate_backtests(
    rng: random.Random,
    strategies: Sequence[Strategy],
    n: int,
) -> List[Backtest]:
    backtests: List[Backtest] = []
    end = datetime.utcnow().date()

    for i in range(1, n + 1):
        s = rng.choice(list(strategies))

        years = rng.choice([1, 2, 3, 4])
        start_date = datetime(end.year - years, rng.choice([1, 4, 7, 10]), 1)
        end_date = datetime(end.year, rng.choice([3, 6, 9, 12]), rng.choice([15, 20, 25]))

        initial = rng.uniform(50_000, 250_000)
        # total_return in proportion
        total_return = _clamp(rng.gauss(0.12, 0.18), -0.4, 1.0)
        final = float(initial * (1 + total_return))

        sharpe = _clamp(rng.gauss(1.0, 0.6), -0.6, 3.0)
        max_dd = _clamp(abs(rng.gauss(0.18, 0.12)), 0.02, 0.65)

        status = rng.choices(
            population=["completed", "running", "failed"],
            weights=[0.7, 0.2, 0.1],
            k=1,
        )[0]

        backtests.append(
            Backtest(
                strategy_id=s.id,
                start_date=start_date,
                end_date=end_date,
                initial_capital=float(initial),
                final_capital=final,
                total_return=float(total_return),
                sharpe_ratio=float(sharpe),
                max_drawdown=float(max_dd),
                status=status,
            )
        )

    return backtests


def _generate_portfolios(
    rng: random.Random,
    strategies: Sequence[Strategy],
    n: int,
) -> List[Portfolio]:
    methods = ["mean_variance", "risk_parity", "equal_weight", "max_sharpe"]

    portfolios: List[Portfolio] = []
    for i in range(1, n + 1):
        s = rng.choice(list(strategies))
        status = rng.choices(
            population=["active", "draft", "inactive"],
            weights=[0.65, 0.2, 0.15],
            k=1,
        )[0]

        capital = rng.uniform(250_000, 2_000_000)
        expected_return = _clamp(rng.gauss(0.09, 0.06), -0.2, 0.35)
        vol = _clamp(abs(rng.gauss(0.14, 0.07)), 0.02, 0.5)
        sharpe = _clamp(expected_return / max(vol, 1e-6), -2.0, 3.0)

        portfolios.append(
            Portfolio(
                name=f"Portfolio {i:02d}",
                description=f"Seed portfolio linked to Strategy {s.id}.",
                strategy_id=s.id,
                capital=float(capital),
                expected_return=float(expected_return),
                volatility=float(vol),
                sharpe_ratio=float(sharpe),
                optimization_method=rng.choice(methods),
                status=status,
            )
        )

    return portfolios


def _seed_exists(db: Session) -> bool:
    # Idempotency gate: if we already have factor exposures, assume dashboard-seeding done.
    return db.query(FactorExposure).limit(1).first() is not None


def seed(db: Session, seed_value: int = 1337) -> None:
    # Make sure schema is present.
    Base.metadata.create_all(bind=engine)

    if _seed_exists(db):
        print("Seed already exists; skipping (idempotent).")
        return

    rng = _rng(seed_value)

    # 1) Assets (20)
    assets = _generate_assets(rng, 20)
    db.add_all(assets)
    db.commit()
    # refresh to get IDs for relationships in price bars
    for a in assets:
        db.refresh(a)

    # Optional: price bars so the dataset is more realistic (not required by dashboard cards).
    # Keep it light but deterministic.
    for a in assets:
        bars = _generate_price_bars(rng, a, days=60)
        db.add_all(bars)
    db.commit()

    # 2) Factor exposures (50)
    # We'll allocate per-factor assets: 50 / 6 ~= 8, but need exactly 50.
    # Use allocation: 9+9+9+8+8+7=50 across factors.
    alloc = {
        "Momentum": 9,
        "Value": 9,
        "Size": 9,
        "Volatility": 8,
        "Quality": 8,
        "MeanReversion": 7,
    }

    factor_rows: List[FactorExposure] = []
    for factor_name, _symbol in FACTOR_DEFINITIONS:
        per = alloc[factor_name]
        for fn, sym, exposure, weight in _factor_exposure_rows(
            rng=rng,
            assets=assets,
            factor_names=[factor_name],
            per_factor_assets=per,
        ):
            factor_rows.append(
                FactorExposure(
                    factor_name=fn,
                    symbol=sym,
                    exposure=exposure,
                    weight=weight,
                )
            )

    # Sanity check
    if len(factor_rows) != 50:
        raise RuntimeError(f"Internal error: expected 50 factor exposures, got {len(factor_rows)}")

    db.add_all(factor_rows)
    db.commit()

    # 3) Alphas (25)
    # Create alphas first because strategies require alpha_id.
    alphas = _generate_alphas(rng, 25)
    db.add_all(alphas)
    db.commit()
    for a in alphas:
        db.refresh(a)

    # 4) Strategies (10)
    strategies = _generate_strategies(rng, alphas, 10)
    db.add_all(strategies)
    db.commit()
    for s in strategies:
        db.refresh(s)

    # 5) Backtests (15)
    backtests = _generate_backtests(rng, strategies, 15)
    db.add_all(backtests)
    db.commit()

    # 6) Portfolios (5)
    portfolios = _generate_portfolios(rng, strategies, 5)
    db.add_all(portfolios)
    db.commit()


def main():
    # CLI entrypoint: python scripts/seed_data.py (from project root)
    # But users may run from backend/; make it resilient.
    db: Session = SessionLocal()
    try:
        # Ensure DB is initialized.
        Base.metadata.create_all(bind=engine)
        seed(db)
        # Quick verification logs
        print("Verification:")
        print("assets:", db.query(Asset).count())
        print("factor_exposures:", db.query(FactorExposure).count())
        print("alphas:", db.query(Alpha).count())
        print("strategies:", db.query(Strategy).count())
        print("backtests:", db.query(Backtest).count())
        print("portfolios:", db.query(Portfolio).count())
    finally:
        db.close()


if __name__ == "__main__":
    main()

