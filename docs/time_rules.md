# Time & Market Rules

This document defines all time-related and market-session rules.
These rules are mandatory and must be enforced consistently across the system.

---

## 1. Timezone Rules

- All system time must be handled in IST
- Timezone identifier: Asia/Kolkata
- No usage of system-local time without explicit conversion
- All logs, candles, and decisions must record time in IST

---

## 2. Market Session (NSE)

- Market open: 09:15 IST
- Market close: 15:30 IST
- Pre-market and post-market data must be ignored
- No new trades after 15:15 IST (configurable later)

---

## 3. Candle Definition (15-Minute)

- Candle intervals:
  - 09:15 – 09:30
  - 09:30 – 09:45
  - 09:45 – 10:00
  - …
- Candle timestamps represent the **close time**
- Only fully closed candles may be used for decisions

---

## 4. Candle Validation Rules

A candle is considered valid only if:
- Duration ≥ 12 minutes
- Volume ≥ configured minimum threshold
- OHLC values are present and non-null

If any validation fails:
- Candle must be rejected
- Strategy evaluation must not proceed

---

## 5. Live Price Handling

- Live LTP may be used only for:
  - Monitoring
  - Exit management
- Live LTP must NOT be used to generate new entries
- Entry decisions rely strictly on closed candles

---

## 6. Holidays & Non-Trading Days

- A static list of NSE holidays must be maintained
- On holidays:
  - System must not start market loops
  - No data polling or signal generation

Dynamic holiday APIs may be added in later phases.

---

## 7. Failure Handling (Time-Related)

- If system time drifts or becomes uncertain:
  - Halt signal generation
- If candle boundaries cannot be reliably determined:
  - Return NO TRADE

---

## 8. Change Policy

- Market hours may be parameterized
- Candle timeframe changes require Phase 0 reset
- Validation thresholds may be tuned with documentation
