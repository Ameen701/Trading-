This document is authoritative for file placement.
If a conflict exists between code and documentation, this document wins.

## Repository Structure Diagram

```text
intraday-trading-engine/
├── README.md
├── LICENSE
├── .gitignore
│
├── app/
│   ├── README.md
│   ├── main.py
│   ├── core/
│   ├── data/
│   ├── indicators/
│   ├── strategy/
│   ├── risk/
│   ├── state/
│   ├── api/
│   ├── services/
│   └── adapters/
│
├── config/
│   ├── base.yaml
│   ├── dev.yaml
│   └── prod.yaml
│
├── docs/
│   ├── README.md
│   ├── product_constraints.md
│   ├── architecture.md
│   ├── tech_stack.md
│   ├── time_rules.md
│   ├── error_policy.md
│   ├── logging.md
│   ├── config.md
│   ├── workflow.md
│   ├── file_structure.md
│   ├── project_overview.md
│   ├── roadmap.md
│   └── current_status.md
│
└── tests/
    ├── README.md
    ├── unit/
    └── integration/



# File Structure

This document explains the repository layout and the responsibility of each
directory. It acts as a placement guide for humans and AI-assisted coding.

---

## Root Level

- README.md  
  High-level project description and purpose.

- LICENSE  
  Project license information.

- .gitignore  
  Files and folders excluded from version control.

---

## /app

Contains all backend application code.  
No experiments, scripts, or documentation should be placed here.

### /app/main.py
Application entry point.
Initializes the FastAPI app and system startup logic.

---

### /app/core
Shared foundations used across the system.

Contains:
- Common data models (e.g., Candle, Signal, TradePlan)
- Enums and constants
- Shared utilities

Must NOT:
- Contain strategy, risk, or API-specific logic

---

### /app/data
Market data ingestion and candle construction.

Contains:
- Broker API integration
- WebSocket handling
- REST fallbacks
- Candle building and validation

Must NOT:
- Contain strategy or risk logic

---

### /app/indicators
Pure technical indicator calculations.

Contains:
- EMA, RSI, ATR, Volume-based indicators
- Stateless, deterministic functions

Must NOT:
- Access account, risk, or position data
- Make trading decisions

---

### /app/strategy
Trade entry logic.

Contains:
- Strategy rules
- Signal generation (BUY / SELL / NO_TRADE)
- Optional strength or quality scoring

Must NOT:
- Calculate position size
- Define stop-loss or targets
- Access broker APIs

---

### /app/risk
Capital protection and risk control.

Contains:
- Position sizing logic
- Stop-loss and target calculation
- Daily loss limits
- Trade veto rules

Has final authority to approve or reject trades.

---

### /app/state
Session and runtime state.

Contains:
- Open positions
- Daily P&L
- Trade counts and cooldowns
- Session-level memory

Must NOT:
- Fetch market data
- Contain trading logic

---

### /app/api
External API layer.

Contains:
- FastAPI routes
- Health and status endpoints

Must NOT:
- Contain business or trading logic

---

### /app/services
System orchestration and control flow.

Contains:
- Schedulers
- Market-hour loops
- Execution pipelines

Must NOT:
- Make trading decisions

---

### /app/adapters
External integrations.

Contains:
- Telegram notifications
- User interaction handlers
- Future broker order adapters

Must NOT:
- Contain strategy or risk logic

---

## /config

Configuration files controlling system behavior.

Contains:
- base.yaml (default configuration)
- dev.yaml (development overrides)
- prod.yaml (production overrides)

Must NOT:
- Store secrets or API keys

---

## /docs

All project documentation.

Contains:
- System contracts (constraints, architecture, rules)
- Project meta docs (roadmap, status, decisions)
- File structure reference (this document)

---

## /tests

Automated tests.

### /tests/unit
Unit tests for individual modules.

### /tests/integration
Integration tests across multiple components.

Tests must not rely on live market data.

### Transitional note (current repository)
The repository currently includes temporary validation scripts under `/test/`:
- `test_login.py`
- `test_live.py`
- `test_historical.py`

These are broker-connected validation scripts and should be migrated into the
`/tests` structure as deterministic tests over time.

---

## Placement Rule (Important)

If unsure where code belongs:
1. Check this document
2. Check `architecture.md`
3. Choose the **lowest-level responsible module**

When in doubt, do not place the code.
