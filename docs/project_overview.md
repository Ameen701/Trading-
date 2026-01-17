# Project Overview

This project is a disciplined, risk-first trading decision system designed to
support systematic trading across multiple time horizons.

While the long-term goal is to support intraday, swing, and positional trading,
the system currently focuses on intraday trading as its first controlled use case.

The system assists a human trader by producing structured, explainable, and
risk-managed trade plans — not by executing trades automatically.

---

## What This Project Is

- A backend-only trading decision engine
- Designed to support multiple trading horizons:
  - Intraday (current focus)
  - Swing (future)
  - Positional (future)
- Currently operates on intraday data using closed 15-minute candles
- Produces structured trade outcomes:
  - BUY / SELL / NO_TRADE
  - Entry price
  - Risk-managed trade plan
- Designed for manual execution by a human trader
- Built incrementally using a strict phase-based roadmap

---

## What This Project Is NOT

- Not a price prediction system
- Not a high-frequency trading system
- Not a fully autonomous trading bot (in early and mid phases)
- Not tied to a single timeframe or strategy forever
- Not dependent on TradingView or external charting tools

---

## Core Philosophy

- **Risk comes before opportunity**
- **No trade is a valid and often optimal outcome**
- **Correct sequencing beats feature richness**
- **Deterministic logic is preferred over black-box prediction**
- **Failures must be safe, explainable, and auditable**

---

## Current Focus (Phase Context)

At present, the system focuses exclusively on:

- Intraday trading
- Indian markets (NSE)
- Closed 15-minute candles
- Manual execution
- Single-strategy discipline

This focus is intentional and exists to establish correctness, safety, and
operational discipline before expanding scope.

---

## System Approach (High Level)

At a high level, the system works as follows:

1. Market data is ingested and validated
2. Indicators are computed on closed candles
3. Strategy logic evaluates potential trade setups
4. Risk rules approve, adjust, or reject trades
5. Session state is updated
6. Decisions and reasoning are communicated to the user

At any point, if conditions are unsafe or unclear, the system produces
**NO TRADE**.

---

## Intended Users

- Disciplined discretionary or semi-systematic traders
- Small teams building trading infrastructure
- Developers experimenting with systematic trading under strong risk constraints

This system is not intended for unsupervised retail auto-trading.

---

## Evolution Model

The system evolves through clearly defined phases:

- Early phases prioritize discipline, correctness, and safety
- Later phases introduce ML-based filtering and contextual awareness
- Support for additional timeframes and trading styles is added only after
  intraday behavior is stable and well understood
- Automation is optional and considered only after sustained profitability
  and drawdown control

The roadmap explicitly defines what belongs in each phase.

---

## Source of Truth

System behavior and constraints are governed by:

- `product_constraints.md`
- `architecture.md`
- `file_structure.md`
- `roadmap.md`

If ambiguity exists, these documents take precedence over code.

---

## Project Status

The current phase, progress, and next steps are tracked in:

- `current_status.md`
