# Logging & Observability

This document defines logging standards for the intraday trading system.
Logs are treated as a first-class system output.

---

## 1. Logging Principles

- All logs must be structured
- Logs must be human-readable and machine-parsable
- Every trading decision must be explainable from logs
- Silent failures are strictly forbidden

---

## 2. Log Format

- Format: JSON
- Encoding: UTF-8

Required fields for all logs:
- timestamp (IST, ISO 8601)
- level (INFO / WARNING / ERROR / CRITICAL)
- module (e.g., data, strategy, risk)
- message (short human-readable summary)

Optional but recommended fields:
- symbol
- candle_time
- strategy_id
- trade_id
- reason
- metadata (key-value map)

---

## 3. Decision Logging (Mandatory)

Every signal evaluation must log:
- Input candle timestamp
- Strategy result (BUY / SELL / NO_TRADE)
- Reason for decision
- If rejected:
  - Explicit rejection reason
  - Rejecting module (strategy / risk / state)

There must be no trade without a corresponding log entry.

---

## 4. Risk & Safety Logging

The following must always be logged:
- Risk rejections
- Daily loss limit hits
- Trade frequency blocks
- Volatility-based scaling decisions

Risk-related logs should include:
- Capital at risk
- Calculated position size
- Risk percentage used

---

## 5. Error & Exception Logging

- All exceptions must be caught and logged
- Stack traces logged only at ERROR or CRITICAL level
- No exception should terminate the system silently

CRITICAL logs must indicate:
- Trading halted
- Manual intervention required

---

## 6. External Interaction Logging

Log events for:
- Telegram messages sent
- User acknowledgements or feedback
- External API failures (broker, messaging)

External failures must be logged without leaking secrets.

---

## 7. Log Storage & Retention

- Phase 0 / Phase 1:
  - Console logs only
- Phase 2 onward:
  - File-based logs
  - Rotation and retention policies may be added

Logs must never block system execution.

---

## 8. Change Policy

- Log field additions are allowed
- Removal of required fields requires review
- Logging must not be weakened to improve performance
