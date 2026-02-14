

"""
TEMPORARY TEST RUNNER
Purpose: Verify live 1-minute candle correctness

⚠️ This file intentionally combines:
- Login
- Ingestion
- Candle printing

This is for testing only.
"""

from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Dict

import os
import pyotp
from dotenv import load_dotenv
from SmartApi import SmartConnect
from SmartApi.smartWebSocketV2 import SmartWebSocketV2

from app.data.builder import CandleBuilder


# ======================================================
# ENV + LOGIN
# ======================================================

load_dotenv()

API_KEY = os.getenv("ANGEL_API_KEY")
CLIENT_CODE = os.getenv("ANGEL_CLIENT_CODE")
PIN = os.getenv("ANGEL_PIN")
TOTP_SECRET = os.getenv("ANGEL_TOTP_SECRET")

IST = ZoneInfo("Asia/Kolkata")

print("🔐 Logging in to Angel...")

smartApi = SmartConnect(api_key=API_KEY)
totp = pyotp.TOTP(TOTP_SECRET).now()

session = smartApi.generateSession(CLIENT_CODE, PIN, totp)
if not session.get("status"):
    raise RuntimeError(f"Login failed: {session}")

AUTH_TOKEN = session["data"]["jwtToken"]
FEED_TOKEN = smartApi.getfeedToken()

print("✅ Login successful")


# ======================================================
# SYMBOLS + BUILDERS
# ======================================================

SYMBOL_TOKEN_MAP: Dict[str, str] = {
    "RELIANCE": "2885",
    "TCS": "11536",
    "HDFCBANK": "1333",
}

# One builder per symbol (1-minute candles for testing)
builders: Dict[str, CandleBuilder] = {
    symbol: CandleBuilder(
        symbol=symbol,
        timeframe="ONE_MINUTE",
        timeframe_seconds=1 * 60
    )
    for symbol in SYMBOL_TOKEN_MAP
}

# Reverse lookup (O(1))
TOKEN_SYMBOL_MAP = {v: k for k, v in SYMBOL_TOKEN_MAP.items()}


# ======================================================
# WEBSOCKET HANDLERS
# ======================================================

def on_open(wsapp):
    print("✅ WebSocket connected")

    token_list = [
        {
            "exchangeType": 1,  # NSE
            "tokens": list(SYMBOL_TOKEN_MAP.values()),
        }
    ]

    ws.subscribe(
        correlation_id="live_test",
        mode=2,  # QUOTE mode
        token_list=token_list,
    )

    print("📡 Subscribed to:", list(SYMBOL_TOKEN_MAP.keys()))
    print("⏳ Waiting for candles to close...\n")


def on_data(wsapp, message: dict):
    try:
        token = message.get("token")
        price = message.get("last_traded_price")
        quantity = message.get("last_traded_quantity")
        exchange_ts = message.get("exchange_timestamp")

        # Mandatory fields only
        if token is None or price is None or exchange_ts is None:
            return

        symbol = TOKEN_SYMBOL_MAP.get(token)
        if symbol is None:
            return

        price = price / 100  # paise → rupees
        tick_time = datetime.fromtimestamp(exchange_ts / 1000, tz=IST)

        builder = builders.get(symbol)
        if builder is None:
            return

        closed_candle = builder.add_tick(
            price=price,
            quantity=quantity or 1,
            tick_time=tick_time,
        )

        if closed_candle:
            # Display closed candle
            print(
                f"🕯️ {symbol:10s} | {closed_candle.timeframe:12s} | "
                f"{closed_candle.open_time.strftime('%H:%M')} → {closed_candle.close_time.strftime('%H:%M')} | "
                f"O:{closed_candle.open_price:>8.2f} "
                f"H:{closed_candle.high_price:>8.2f} "
                f"L:{closed_candle.low_price:>8.2f} "
                f"C:{closed_candle.close_price:>8.2f} | "
                f"Vol:{closed_candle.volume:>6} "
                f"Ticks:{closed_candle.number_of_trades:>4}"
            )

    except Exception as e:
        print(f"❌ Tick processing error: {e}")
        import traceback
        traceback.print_exc()


def on_error(wsapp, error):
    print("❌ WebSocket error:", error)


def on_close(wsapp):
    print("🔌 WebSocket closed")


# ======================================================
# START WEBSOCKET
# ======================================================

ws = SmartWebSocketV2(
    AUTH_TOKEN,
    API_KEY,
    CLIENT_CODE,
    FEED_TOKEN,
)

ws.on_open = on_open
ws.on_data = on_data
ws.on_error = on_error
ws.on_close = on_close

print("🔄 Connecting to WebSocket...\n")
ws.connect()