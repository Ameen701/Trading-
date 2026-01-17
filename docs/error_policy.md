# Error Handling Policy

This document defines how the system must behave when errors, missing data,
or unexpected conditions occur. The priority is capital protection.

---

## 1. Core Principle

- The system must **fail safe**, not fail fast
- When in doubt, the system must return **NO TRADE**
- Silent failures are not allowed

---

## 2. Market Data Errors

If any of the following occur:
- Broker API timeout or disconnect
- Missing historical candles
- Invalid or malformed OHLC data
- WebSocket feed interruption without fallback

Then:
- Signal generation must be halted
- Strategy evaluation must not proceed
- System must return NO TRADE
- Error must be logged with context

---

## 3. Candle & Indicator Errors

If:
- Candle validation fails
- Indicator calculation fails
- Required indicator values are missing

Then:
- That candle must be skipped
- No partial or fallback calculations
- Strategy must not be evaluated on incomplete data

---

## 4. Strategy Evaluation Errors

If:
- Strategy logic throws an exception
- Required inputs are unavailable
- Internal consistency checks fail

Then:
- Treat as NO TRADE
- Do not retry within the same candle
- Log the failure with strategy identifier

---

## 5. Risk Engine Errors

If:
- Position sizing fails
- Stop-loss or target cannot be computed
- Daily loss state is unavailable

Then:
- Trade must be rejected
- No fallback risk assumptions allowed
- System must not place or suggest a trade

Risk engine failure always blocks execution.

---

## 6. State Management Errors

If:
- Open positions cannot be reliably determined
- P&L state is inconsistent
- Trade count or cooldown state is missing

Then:
- Halt new trade approvals
- Allow exits only (if applicable)
- Log state inconsistency as CRITICAL

---

## 7. External Interface Errors

If:
- Telegram notification fails
- User feedback cannot be recorded

Then:
- Trading logic may continue
- Failure must be logged
- Notifications may be retried safely

External interface failures must not affect decisions.

---

## 8. Retry Policy

- Data fetch retries may be attempted with backoff
- Strategy and risk evaluation must not be retried blindly
- Retries must not violate candle boundaries

---

## 9. Severity Levels

- INFO: Normal operational messages
- WARNING: Recoverable issues, no impact on decisions
- ERROR: Decision blocked, NO TRADE enforced
- CRITICAL: System safety risk, trading halted

---

## 10. Change Policy

- Error handling behavior is part of system safety
- Changes require explicit review
- Relaxing safety rules is not allowed without justification
