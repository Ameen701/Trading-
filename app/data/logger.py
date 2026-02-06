from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Any, Dict
import json
import sys
import uuid

IST = ZoneInfo("Asia/Kolkata")


def log(
    event: str,
    layer: str,
    symbol: str,
    timeframe: str | None = None,
    correlation_id: str | None = None,
    sequence_number: int | None = None,
    **payload: Any,
) -> None:
    """
    Phase-1 structured event logger.

    Guarantees:
    - Never raises exceptions
    - Emits structured JSON to stdout
    - ISO-8601 IST timestamps
    - No interpretation, no mutation

    This logger is intentionally DUMB.
    It records facts and gets out of the way.

    Phase-2+:
    - Add SQLite / file sinks
    - Add rotation
    - Add async buffering
    """

    try:
        event_record: Dict[str, Any] = {
            "timestamp": datetime.now(IST).isoformat(),
            "event": event,
            "layer": layer,
            "symbol": symbol,
        }

        if timeframe is not None:
            event_record["timeframe"] = timeframe

        if correlation_id is not None:
            event_record["correlation_id"] = correlation_id

        if sequence_number is not None:
            event_record["sequence_number"] = sequence_number

        if payload:
            event_record["payload"] = payload

        # Emit as JSON line (machine + human readable)
        sys.stdout.write(json.dumps(event_record, ensure_ascii=False) + "\n")
        sys.stdout.flush()

    except Exception:
        # Logger must NEVER break the system
        # Absolute last-resort fallback
        sys.stdout.write(
            json.dumps({
                "timestamp": datetime.now(IST).isoformat(),
                "event": "LOGGER_FAILURE",
                "layer": "logger",
                "symbol": symbol,
            }) + "\n"
        )
        sys.stdout.flush()
"""
PHASE-2 LOGGER EXTENSIONS (FUTURE — DO NOT IMPLEMENT NOW)

The following are INTENTIONAL future extensions.
They are documented here to prevent architectural drift.

-------------------------------------------------
1. PERSISTENCE LAYER (Phase-2)
-------------------------------------------------
- Add SQLite persistence for all events.
- Schema: event_logs table (append-only).
- One row per event.
- No updates. No deletes.

Fields:
- timestamp (ISO-8601 IST)
- event
- layer
- symbol
- timeframe (nullable)
- correlation_id (nullable)
- sequence_number (nullable)
- payload (JSON)

Rules:
- Logger must remain non-blocking.
- DB write failures must NEVER affect execution.
- Console output remains primary truth.

-------------------------------------------------
2. EVENT CORRELATION & SESSION TRACKING
-------------------------------------------------
- Introduce session_id per trading day.
- Correlate:
  Tick → Candle → Indicator → Strategy → Risk → Exit
- Enable full decision replay for audits.

Example:
session_id = "2026-01-21_REL_TRADING_SESSION"

-------------------------------------------------
3. FEED HEALTH & LATENCY METRICS
-------------------------------------------------
Log derived (not inferred) metrics only:
- websocket_message_latency_ms
- tick_interarrival_ms
- sequence_gap_detected

NO ACTIONS based on these metrics at logger level.
Actions belong to orchestration layer.

-------------------------------------------------
4. LOG ROTATION & RETENTION
-------------------------------------------------
- File-based JSONL logs:
  /logs/market_layer/YYYY-MM-DD.jsonl

- Rotation:
  - Daily OR 100MB (whichever first)
  - Old logs archived, never modified

- Retention policy:
  - Phase-2: 30 trading days
  - Phase-3+: configurable

-------------------------------------------------
5. OBSERVABILITY (READ-ONLY)
-------------------------------------------------
Expose read-only metrics:
- candles_emitted / rejected
- rejection_reason_counts
- feed_disconnect_count

Logger NEVER:
- Aggregates internally
- Emits alerts
- Makes decisions

-------------------------------------------------
6. STRICT NON-GOALS (FOREVER)
-------------------------------------------------
The logger must NEVER:
- Contain trading logic
- Trigger alerts directly
- Infer meaning from data
- Apply severity levels (INFO/WARN/ERROR)
- Mutate or fix data
- Block execution

Logger is a FACT RECORDER, not an ANALYST.

-------------------------------------------------
FINAL INVARIANT
-------------------------------------------------
"If the logger fails, trading continues.
If trading fails, the logger must explain why."

Any Phase-2 change that violates this invariant
must be rejected.
"""
