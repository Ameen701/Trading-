from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from enum import Enum
from typing import Optional

from app.data.models import Candle
from app.data.validation import validate_candle


IST = ZoneInfo("Asia/Kolkata")
TIMEFRAME_SECONDS = 15 * 60  # Phase-1: 15m only


class CandleState(Enum):
    """
    Minimal candle lifecycle states.

    Phase-1:
    BUILDING -> CLOSED -> EMITTED / DROPPED

    Phase-2+:
    - Can add BUFFERED / INVALID / PARTIAL if needed
    """
    BUILDING = "building"
    CLOSED = "closed"
    EMITTED = "emitted"
    DROPPED = "dropped"


def get_candle_boundary(tick_time: datetime) -> datetime:
    """
    Align tick timestamp to NSE 15-minute boundary.

    Examples:
    09:17:42 -> 09:15:00
    09:42:05 -> 09:30:00

    Phase-2:
    - Extend to support multiple timeframes
    """
    minute = tick_time.minute
    aligned_minute = (minute // 15) * 15
    return tick_time.replace(
        minute=aligned_minute,
        second=0,
        microsecond=0
    )


class CandleBuilder:
    """
    Converts live ticks into closed, immutable 15m candles.

    Phase-1 guarantees:
    - Tick-driven closure ONLY
    - No synthetic candles
    - No timer-based logic
    - No data fixing
    - NO DATA -> NO TRADE

    IMPORTANT:
    ❌ Do NOT add timeout-based force close here
    ❌ Do NOT mutate closed candles
    """

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.current_candle: Optional[Candle] = None
        self.state: Optional[CandleState] = None
        self.last_tick_time: Optional[datetime] = None
        self.tz = IST

    def add_tick(
        self,
        price: float,
        quantity: int,
        tick_time: datetime,
    ) -> Optional[Candle]:
        """
        Process a single tick.

        Returns:
        - Closed Candle if one finishes
        - None otherwise
        """

        # ---------- TIMEZONE ENFORCEMENT (Phase-1 REQUIRED) ----------
        if tick_time.tzinfo is None:
            # Reject ambiguous timestamps — never guess
            # log("TICK_REJECTED_NAIVE_TIMEZONE")
            return None
        elif tick_time.tzinfo != self.tz:
            tick_time = tick_time.astimezone(self.tz)

        # ---------- ORDERING DEFENSE ----------
        if self.last_tick_time and tick_time < self.last_tick_time:
            # log("OUT_OF_ORDER_TICK_REJECTED")
            return None

        self.last_tick_time = tick_time

        # ---------- MARKET HOURS GATE (tick-level only) ----------
        if not self._is_market_time(tick_time):
            return None

        boundary = get_candle_boundary(tick_time)
        candle_end = boundary + timedelta(seconds=TIMEFRAME_SECONDS)

        # ---------- START FIRST CANDLE ----------
        if self.current_candle is None:
            self._start_new_candle(
                price=price,
                quantity=quantity,
                start_time=boundary,
                end_time=candle_end,
            )
            return None

        # ---------- UPDATE CURRENT CANDLE ----------
        if tick_time < self.current_candle.close_time:
            self._update_candle(price, quantity)
            return None

        # ---------- CLOSE CURRENT CANDLE ----------
        closed_candle = self._close_current_candle()

        # ---------- START NEXT CANDLE ----------
        new_boundary = get_candle_boundary(tick_time)
        self._start_new_candle(
            price=price,
            quantity=quantity,
            start_time=new_boundary,
            end_time=new_boundary + timedelta(seconds=TIMEFRAME_SECONDS),
        )

        return closed_candle

    # ==========================================================
    # Internal helpers
    # ==========================================================

    def _start_new_candle(
        self,
        price: float,
        quantity: int,
        start_time: datetime,
        end_time: datetime,
    ):
        self.current_candle = Candle(
            symbol=self.symbol,
            timeframe="15m",
            open_price=price,
            high_price=price,
            low_price=price,
            close_price=price,
            volume=quantity,
            tick_count=1,
            start_time=start_time,
            end_time=end_time,
            is_closed=False,
        )
        self.state = CandleState.BUILDING

    def _update_candle(self, price: float, quantity: int):
        if self.current_candle is None or self.state != CandleState.BUILDING:
            return

        candle = self.current_candle
        candle.high_price = max(candle.high_price, price)
        candle.low_price = min(candle.low_price, price)
        candle.close_price = price
        candle.volume += quantity
        candle.number_of_trades += 1

    def _close_current_candle(self) -> Optional[Candle]:
        if self.current_candle is None:
            return None

        candle = self.current_candle
        candle.is_closed = True
        self.state = CandleState.CLOSED

        is_valid, reason = validate_candle(candle)

        if is_valid:
            self.state = CandleState.EMITTED
            emitted = candle
        else:
            # log_rejection(candle, reason)
            self.state = CandleState.DROPPED
            emitted = None

        self.current_candle = None
        return emitted

    @staticmethod
    def _is_market_time(ts: datetime) -> bool:
        """
        Phase-1 tick-level market hours guard.
        Candle-level validation is handled elsewhere.
        """
        market_start = ts.replace(hour=9, minute=15, second=0, microsecond=0)
        market_end = ts.replace(hour=15, minute=30, second=0, microsecond=0)
        return market_start <= ts <= market_end
