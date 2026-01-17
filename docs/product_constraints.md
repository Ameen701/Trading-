# Product Constraints

This document defines the non-negotiable constraints for the intraday trading system.
These constraints act as a contract and must not change casually.

---

## 1. Trading Scope

- Market: NSE (India)
- Trading Type: Intraday only
- Timeframe: 15-minute candles
- Execution: Manual (no auto-trading in early phases)
- Instruments: To be finalized (Index / Cash / F&O)
- System is allowed to produce NO TRADE for an entire session

---

## 2. Strategy Constraints

- Only ONE strategy is allowed in Phase 1
- Strategy logic may only:
  - Generate BUY / SELL / NO_TRADE signals
  - Provide entry price suggestions
- Strategy must NOT:
  - Decide quantity
  - Decide stop-loss or targets
  - Override risk rules

---

## 3. Risk & Capital Protection (Non-Negotiable)

- Risk engine has veto power over all strategies
- Position sizing is always derived, never fixed
- Daily loss limit must exist
- Trade frequency limits may be enforced
- Capital protection has priority over profit

---

## 4. Data Integrity Rules

- Only CLOSED candles may be used for decisions
- Partial candles must be ignored
- If market data is missing or invalid → NO TRADE
- Candle validation rules apply (time & volume based)

---

## 5. System Behavior

- Deterministic behavior is preferred over prediction
- ML models (when added) may only FILTER trades, not decide them
- LLMs (when added) may only EXPLAIN decisions, not make them

---

## 6. Change Policy

- Parameter tuning is allowed with documentation
- Structural changes require explicit review
- Changes to the following require a Phase 0 reset:
  - Timeframe
  - Intraday-only constraint
  - Risk engine veto power
  - Manual execution assumption
