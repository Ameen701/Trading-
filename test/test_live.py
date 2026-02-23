"""
TEST RUNNER USING INGESTION LAYER + PERSISTENCE

Purpose:
- Verify live candle correctness
- Persist closed candles to PostgreSQL
- Clean production-style wiring
"""

from typing import Dict
from zoneinfo import ZoneInfo
import os
import pyotp
from dotenv import load_dotenv
from SmartApi import SmartConnect

from app.data.builder import CandleBuilder
from app.data.ingestion import AngelWebSocketIngestion
from app.data.persistence import PostgresCandleRepository


# ======================================================
# ENV + LOGIN
# ======================================================

load_dotenv()

API_KEY = os.getenv("ANGEL_API_KEY")
CLIENT_CODE = os.getenv("ANGEL_CLIENT_CODE")
PIN = os.getenv("ANGEL_PIN")
TOTP_SECRET = os.getenv("ANGEL_TOTP_SECRET")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

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

TIMEFRAME_NAME = "ONE_MINUTE"
TIMEFRAME_SECONDS = 60

builders: Dict[str, CandleBuilder] = {
    symbol: CandleBuilder(
        symbol=symbol,
        timeframe=TIMEFRAME_NAME,
        timeframe_seconds=TIMEFRAME_SECONDS,
    )
    for symbol in SYMBOL_TOKEN_MAP
}

print("🛠 Builders created")


# ======================================================
# PERSISTENCE LAYER
# ======================================================

repository = PostgresCandleRepository(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
)

print("💾 Persistence layer connected")


# ======================================================
# CALLBACK: HANDLE CLOSED CANDLE
# ======================================================

def handle_closed_candle(candle):
    """
    This runs every time a candle closes.
    """
    repository.insert_candle(candle)


# ======================================================
# CREATE INGESTION
# ======================================================

ingestion = AngelWebSocketIngestion(
    auth_token=AUTH_TOKEN,
    api_key=API_KEY,
    client_code=CLIENT_CODE,
    feed_token=FEED_TOKEN,
    symbol_token_map=SYMBOL_TOKEN_MAP,
    builders=builders,
    on_candle_closed=handle_closed_candle,  # 🔥 clean wiring
)

print("🔄 Starting ingestion...\n")

try:
    ingestion.start()
except KeyboardInterrupt:
    print("\n🛑 Stopping system...")
    repository.close()
    print("✅ Clean shutdown complete")