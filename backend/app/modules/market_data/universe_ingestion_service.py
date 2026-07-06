from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Sequence

from sqlalchemy.orm import Session

from app.modules.market_data.ingestion_service import ingest_historical_data
from app.modules.market_data.market_data_universe_settings import resolve_universe
from app.modules.market_data.models import Asset, PriceBar
from app.modules.market_data.schemas import (
    IngestUniverseRequest,
    IngestUniverseResponse,
    IngestUniverseSymbolResult,
)


def _utc_today_bounds(now_utc: datetime) -> tuple[datetime, datetime]:
    start = datetime(
        year=now_utc.year,
        month=now_utc.month,
        day=now_utc.day,
        tzinfo=timezone.utc,
    )
    end = start.replace(day=start.day)  # same day
    return start, end


def get_latest_pricebar_timestamp_for_symbol(db: Session, symbol: str) -> Optional[datetime]:
    asset = db.query(Asset).filter(Asset.symbol == symbol).first()
    if not asset:
        return None

    # latest timestamp among stored price bars
    latest = (
        db.query(PriceBar.timestamp)
        .filter(PriceBar.asset_id == asset.id)
        .order_by(PriceBar.timestamp.desc())
        .first()
    )

    if not latest:
        return None

    return latest[0]


def is_updated_today(latest_ts: Optional[datetime], now_utc: datetime) -> bool:
    if latest_ts is None:
        return False

    # Treat timestamps as UTC if they are naive.
    if latest_ts.tzinfo is None:
        latest_ts = latest_ts.replace(tzinfo=timezone.utc)

    now_day = now_utc.date()
    return latest_ts.date() == now_day


def ingest_universe_service(
    db: Session,
    request: Optional[IngestUniverseRequest] = None,
    batch_size: int = 10,
) -> IngestUniverseResponse:
    now_utc = datetime.now(timezone.utc)

    requested_symbols = None
    if request is not None:
        requested_symbols = request.symbols

    symbols = resolve_universe(requested_symbols)

    success_count = 0
    skipped_count = 0
    failure_count = 0
    results: list[IngestUniverseSymbolResult] = []

    # Process in server-side batches.
    for i in range(0, len(symbols), batch_size):
        batch = symbols[i : i + batch_size]
        for symbol in batch:
            try:
                latest_ts = get_latest_pricebar_timestamp_for_symbol(db, symbol)
                if is_updated_today(latest_ts, now_utc):
                    skipped_count += 1
                    results.append(
                        IngestUniverseSymbolResult(
                            symbol=symbol,
                            status="skipped",
                            message="Already updated today",
                        )
                    )
                    continue

                ingest_result = ingest_historical_data(db, symbol)
                success_count += 1
                results.append(
                    IngestUniverseSymbolResult(
                        symbol=symbol,
                        status="ingested",
                        message=str(ingest_result.get("message", "Ingested"))
                        if isinstance(ingest_result, dict)
                        else "Ingested",
                    )
                )
            except Exception as e:
                failure_count += 1
                results.append(
                    IngestUniverseSymbolResult(
                        symbol=symbol,
                        status="failed",
                        message=str(e),
                    )
                )

    return IngestUniverseResponse(
        success_count=success_count,
        failure_count=failure_count,
        skipped_count=skipped_count,
        results=results,
    )

