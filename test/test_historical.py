


from datetime import datetime
import pyotp

from SmartApi import SmartConnect

from app.data.historical import HistoricalDataFetcher

import os
from dotenv import load_dotenv


load_dotenv()
# =========================
# 1. CREDENTIALS
# =========================

API_KEY = os.getenv("ANGEL_API_KEY")
CLIENT_CODE = os.getenv("ANGEL_CLIENT_CODE")
PIN = os.getenv("ANGEL_PIN")
TOTP_SECRET = os.getenv("ANGEL_TOTP_SECRET")



EXCHANGE = "NSE"
SYMBOL = "SBIN"
SYMBOL_TOKEN = "3045"
INTERVAL = "ONE_MINUTE"

FROM_DATE = datetime(2021, 2, 8, 9, 0)
TO_DATE   = datetime(2021, 3, 8, 9, 45)


# =========================
# 2. LOGIN
# =========================

smart = SmartConnect(API_KEY)

totp = pyotp.TOTP(TOTP_SECRET).now()
session = smart.generateSession(CLIENT_CODE, PIN, totp)

if not session["status"]:
    raise RuntimeError("Login failed")

print("✅ Login successful")


# =========================
# 3. FETCH HISTORICAL DATA
# =========================

fetcher = HistoricalDataFetcher(smart)

candles = fetcher.fetch_candles(
    exchange=EXCHANGE,
    symbol=SYMBOL,
    symbol_token=SYMBOL_TOKEN,
    interval=INTERVAL,
    from_date=FROM_DATE,
    to_date=TO_DATE,
)

print(f"\n📊 Fetched {len(candles)} candles:\n")

for candle in candles:
    print(
        candle.open_time,
        candle.open_price,
        candle.high_price,
        candle.low_price,
        candle.close_price,
        candle.volume,
    )


# =========================
# 4. LOGOUT
# =========================

smart.terminateSession(CLIENT_CODE)
print("\n🔒 Session terminated")

print(f"\n📊 Fetched {len(candles)} candles:\n")
