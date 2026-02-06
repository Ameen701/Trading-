"""
historical.py

Phase-1 Historical Market Data Adapter (Angel SmartAPI)

Responsibilities:
- Fetch broker-provided historical candles (NO aggregation)
- Respect Angel API interval + max-days constraints
- Chunk requests safely
- Convert raw candles → internal Candle model
- Run Phase-1 validation
- Emit clean, time-ordered candles

NOT responsible for:
- Backtesting logic
- Indicator calculation
- Strategy execution
- Data storage (raw candles)
- Synthetic candle creation
"""

from datetime import datetime, timedelta
from typing import List
from zoneinfo import ZoneInfo

from SmartApi import SmartConnect

from app.data.models import Candle
from app.data.validation import validate_candle
from app.data.logger import log


IST = ZoneInfo("Asia/Kolkata")

# -----------------------------
# Angel interval → max days map
# -----------------------------
INTERVAL_MAX_DAYS = {
    "ONE_MINUTE": 30,
    "THREE_MINUTE": 60,
    "FIVE_MINUTE": 100,
    "TEN_MINUTE": 100,
    "FIFTEEN_MINUTE": 200,
    "THIRTY_MINUTE": 200,
    "ONE_HOUR": 400,
    "ONE_DAY": 2000,
}


class HistoricalDataFetcher:
    """
    Angel SmartAPI Historical Candle Adapter.

    Phase-1 guarantees:
    - Uses broker-provided candles only
    - No resampling or aggregation
    - No missing candle filling
    - Deterministic, auditable output
    """

    def __init__(self, smart_api: SmartConnect):
        self.smart_api = smart_api

    # =========================
    # Public API
    # =========================

    def fetch_candles(
        self,
        exchange: str,
        symbol: str,
        symbol_token: str,
        interval: str,
        from_date: datetime,
        to_date: datetime,
    ) -> List[Candle]:
        """
        Fetch historical candles for a symbol.

        Returns:
        - List[Candle] (validated, ordered)
        """

        if interval not in INTERVAL_MAX_DAYS:
            raise ValueError(f"Unsupported interval: {interval}")

        log(
            "HISTORICAL_FETCH_STARTED",
            layer="historical",
            symbol=symbol,
            interval=interval,
            from_date=from_date.isoformat(),
            to_date=to_date.isoformat(),
        )

        all_candles: List[Candle] = []

        for chunk_start, chunk_end in self._chunk_date_range(
            from_date, to_date, INTERVAL_MAX_DAYS[interval]
        ):
            raw_data = self._fetch_chunk(
                exchange=exchange,
                symbol_token=symbol_token,
                interval=interval,
                from_date=chunk_start,
                to_date=chunk_end,
            )

            candles = self._convert_and_validate(
                raw_data=raw_data,
                symbol=symbol,
                interval=interval,
            )

            all_candles.extend(candles)

        # Ensure strict time order
        all_candles.sort(key=lambda c: c.open_time)

        log(
            "HISTORICAL_FETCH_COMPLETED",
            layer="historical",
            symbol=symbol,
            interval=interval,
            candle_count=len(all_candles),
        )

        return all_candles

    # =========================
    # Internal helpers
    # =========================

    def _fetch_chunk(
        self,
        exchange: str,
        symbol_token: str,
        interval: str,
        from_date: datetime,
        to_date: datetime,
    ):
        """
        Fetch a single Angel API chunk.
        """

        params = {
            "exchange": exchange,
            "symboltoken": symbol_token,
            "interval": interval,
            "fromdate": from_date.strftime("%Y-%m-%d %H:%M"),
            "todate": to_date.strftime("%Y-%m-%d %H:%M"),
        }

        try:
            response = self.smart_api.getCandleData(params)
        except Exception as exc:
            log(
                "HISTORICAL_API_ERROR",
                layer="historical",
                symbol="SYSTEM",
                error=str(exc),
                params=params,
            )
            return []

        if not response or not response.get("status"):
            log(
                "HISTORICAL_API_FAILED",
                layer="historical",
                symbol="SYSTEM",
                response=response,
            )
            return []

        return response.get("data", [])

    def _convert_and_validate(
        self,
        raw_data: list,
        symbol: str,
        interval: str,
    ) -> List[Candle]:
        """
        Convert raw Angel candles → internal Candle model
        and apply Phase-1 validation.
        """

        candles: List[Candle] = []

        for row in raw_data:
            try:
                ts, open_p, high_p, low_p, close_p, volume = row

                open_time = datetime.fromisoformat(ts).astimezone(IST)

                # Infer end_time from interval (Angel candles are closed)
                end_time = self._infer_end_time(open_time, interval)

                candle = Candle(
                    symbol=symbol,
                    timeframe=interval,
                    open_price=open_p,
                    high_price=high_p,
                    low_price=low_p,
                    close_price=close_p,
                    volume=volume,
                    number_of_trades=0,  # Historical API does NOT provide tick count
                    open_time=open_time,
                    close_time=end_time,
                    is_closed=True,
                    mode="historical",
                )

                is_valid, reason = validate_candle(candle)

                if is_valid:
                    candles.append(candle)
                else:
                    log(
                        "HISTORICAL_CANDLE_REJECTED",
                        layer="historical",
                        symbol=symbol,
                        reason=reason,
                        timestamp=open_time.isoformat(),
                    )

            except Exception as exc:
                log(
                    "HISTORICAL_CANDLE_PARSE_ERROR",
                    layer="historical",
                    symbol=symbol,
                    error=str(exc),
                    raw_row=row,
                )

        return candles

    def _chunk_date_range(
        self,
        start: datetime,
        end: datetime,
        max_days: int,
    ):
        """
        Yield (chunk_start, chunk_end) pairs
        respecting Angel max-days constraint.
        """

        delta = timedelta(days=max_days)
        cursor = start

        while cursor < end:
            chunk_end = min(cursor + delta, end)
            yield cursor, chunk_end
            cursor = chunk_end

    def _infer_end_time(self, open_time: datetime, interval: str) -> datetime:
        """
        Infer candle end_time based on interval.

        Phase-1:
        - Deterministic mapping
        - No dynamic inference
        """

        minutes_map = {
            "ONE_MINUTE": 1,
            "THREE_MINUTE": 3,
            "FIVE_MINUTE": 5,
            "TEN_MINUTE": 10,
            "FIFTEEN_MINUTE": 15,
            "THIRTY_MINUTE": 30,
            "ONE_HOUR": 60,
            "ONE_DAY": 1440,
        }

        minutes = minutes_map[interval]
        return open_time + timedelta(minutes=minutes)

        # Phase-2:
        # - Exchange calendar aware end_time
        # - Holiday / early close handling
