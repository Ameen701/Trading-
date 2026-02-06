"""
symbols.py

Static symbol ↔ token mapping for Angel SmartAPI (NSE).

Purpose:
- Single source of truth for tradable instruments
- Explicit whitelist (safety > convenience)
- Human-readable symbols for the rest of the system

Phase-1:
- Manually maintained
- No API calls
- No dynamic updates

Phase-2 (future):
- Auto-generate from Angel instrument dump
- Daily token freshness validation
- Manual override for critical symbols
"""

# ============================
# NSE SYMBOL → ANGEL TOKEN MAP
# ============================

SYMBOL_TOKEN_MAP: dict[str, str] = {
    "RELIANCE": "2885",
    "TCS": "11536",
    "HDFCBANK": "1333",
    "INFY": "1594",
    "ICICIBANK": "4963",
    "HINDUNILVR": "1394",
    "ITC": "1660",
    "SBIN": "3045",
    "BHARTIARTL": "10604",
    "KOTAKBANK": "1922",
    "LT": "11483",
    "AXISBANK": "5900",
    "BAJFINANCE": "317",
    "ASIANPAINT": "236",
    "MARUTI": "10999",
    "TITAN": "3506",
    "SUNPHARMA": "3351",
    "NESTLEIND": "17963",
    "ULTRACEMCO": "11532",
    "HCLTECH": "7229",
    "WIPRO": "3787",
    "NTPC": "11630",
    "POWERGRID": "14977",
    "ONGC": "2475",
    "ADANIPORTS": "15083",
    "TATASTEEL": "3499",
    "INDUSINDBK": "5258",
    "TECHM": "13538",
    "BAJAJFINSV": "16675",
    "HDFCLIFE": "467",
    "COALINDIA": "20374",
    "M&M": "2031",
    "DRREDDY": "881",
    "GRASIM": "1232",
    "CIPLA": "694",
    "SBILIFE": "21808",
    "JSWSTEEL": "11723",
    "DIVISLAB": "10940",
    "BRITANNIA": "547",
    "EICHERMOT": "910",
    "APOLLOHOSP": "157",
    "TATACONSUM": "3432",
    "UPL": "11287",
    "HINDALCO": "1363",
    "BAJAJ-AUTO": "16669",
    "ADANIENT": "25",
    "HEROMOTOCO": "1348",
    "LTIM": "17818",
    "PIDILITIND": "2664",
    "VEDL": "3063",
    "BPCL": "526",
    "IOC": "1624",
    "GODREJCP": "10099",
    "DABUR": "772",
    "HAVELLS": "9819",
    "MARICO": "4067",
    "SIEMENS": "3150",
    "AMBUJACEM": "1270",
    "DLF": "14732",
    "GAIL": "4717",
    "BERGEPAINT": "404",
    "COLPAL": "15141",
    "BANDHANBNK": "2263",
    "INDIGO": "11195",
    "BOSCHLTD": "2181",
    "PNB": "10666",
    "SAIL": "2963",
    "NMDC": "15332",
    "DMART": "19913",
    "ACC": "22",
    "BANKBARODA": "4668",
    "CANBK": "10794",
    "RECLTD": "15355",
    "PFC": "14299",
    "IRCTC": "13611",
    "MUTHOOTFIN": "23650",
    "CHOLAFIN": "685",
    "LICHSGFIN": "1997",
    "SBICARD": "17971",
    "MFSL": "2142",
    "ABCAPITAL": "21614",
    "ICICIGI": "21770",
    "ADANIPOWER": "17388",
    "TATAPOWER": "3426",
    "TORNTPOWER": "13786",
    "JINDALSTEL": "6733",
    "TATACOMM": "3721",
    "LUPIN": "10440",
    "BIOCON": "11373",
    "MOTHERSON": "4204",
    "SHREECEM": "3103",
    "TRENT": "1964",
    "PAGEIND": "14413",
    "ABB": "13",
    "BEL": "383",
    "OFSS": "10738",
    "BALKRISIND": "335",
    "BATAINDIA": "371",
    "YESBANK": "11915",
    "IDEA": "14366"
}
# ============================
# OPTIONAL SAFE HELPERS
# ============================

def get_token(symbol: str) -> str | None:
    """
    Return Angel token for a symbol.
    Safe lookup. No exceptions.
    """
    return SYMBOL_TOKEN_MAP.get(symbol)


def get_all_symbols() -> list[str]:
    """
    Return list of all configured symbols.
    """
    return list(SYMBOL_TOKEN_MAP.keys())


def get_all_tokens() -> list[str]:
    """
    Return list of all Angel tokens.
    """
    return list(SYMBOL_TOKEN_MAP.values())
