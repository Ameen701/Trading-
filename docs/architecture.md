# System Architecture

This document defines the high-level architecture of the intraday trading system.
It specifies module responsibilities and interaction rules.

---

## 1. Architectural Principles

- Single responsibility per module
- Clear input/output contracts between modules
- No circular dependencies
- Business logic must not depend on external interfaces
- Risk control overrides all decision layers

---

## 2. Core Modules Overview

The system is composed of the following core modules:

1. Market Data Engine
2. Indicator Engine
3. Strategy Engine
4. Risk Engine
5. State Manager
6. Output / Interface Layer
7. Orchestration Services

---

## 3. Module Responsibilities

### 3.1 Market Data Engine (`app/data`)

Responsibilities:
- Broker API integration (WebSocket + REST fallback)
- Live LTP handling
- Historical candle fetching
- 15-minute candle construction
- Data validation and normalization

Rules:
- Only source of market data truth
- No strategy or risk logic allowed

---

### 3.2 Indicator Engine (`app/indicators`)

Responsibilities:
- Calculation of technical indicators (EMA, RSI, ATR, Volume SMA)
- Operates only on CLOSED candles

Rules:
- Pure functions only
- No access to account, positions, or risk data

---

### 3.3 Strategy Engine (`app/strategy`)

Responsibilities:
- Evaluate indicator outputs
- Apply entry rules
- Generate trade signals:
  - BUY / SELL / NO_TRADE
- Provide optional signal strength scoring

Rules:
- Must not calculate quantity
- Must not define stop-loss or targets
- Must not access broker or account state directly

---

### 3.4 Risk Engine (`app/risk`)

Responsibilities:
- Position sizing
- Stop-loss and target calculation
- Daily loss limits
- Trade frequency limits
- Volatility-based risk adjustment
- Trade veto logic

Rules:
- Has final authority to approve or reject trades
- No dependency on strategy internals

---

### 3.5 State Manager (`app/state`)

Responsibilities:
- Track open positions
- Track daily P&L
- Track trade counts and cooldowns
- Maintain session-level state

Rules:
- Single source of truth for current session state
- No market data fetching

---

### 3.6 Output / Interface Layer (`app/adapters`)

Responsibilities:
- Telegram notifications
- User interaction (ACK / feedback)
- Future broker order placement (optional)

Rules:
- No trading logic
- No decision-making authority

---

### 3.7 API Layer (`app/api`)

Responsibilities:
- FastAPI routes
- Health checks
- Status and monitoring endpoints

Rules:
- Translate requests to internal calls
- Must not contain business logic

---

### 3.8 Orchestration Services (`app/services`)

Responsibilities:
- Market-hour scheduling
- Execution flow coordination
- Triggering data → indicators → strategy → risk

Rules:
- Orchestration only
- No business decisions

---

## 4. Data Flow (High Level)

Market Data  
→ Indicators  
→ Strategy  
→ Risk  
→ State Update  
→ Output / Notification

At any point:
- If data is invalid → stop
- If risk rejects → stop

---

## 5. Forbidden Patterns

- Strategy calling broker APIs
- Indicators accessing state or risk
- API routes containing trading logic
- Risk rules being overridden by strategy or ML
- Circular imports between modules
