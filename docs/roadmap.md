

This document defines the phased evolution of the trading decision system.
The roadmap prioritizes correct sequencing, capital safety, and long-term
expandability over rapid feature addition.

Only one phase may be active at a time.

---

## 🟢 LEVEL 0 — Foundations (Before MVP)

**Goal**
Ensure the system is built on stable, explicit, and enforceable assumptions.

**Locked Constraints**

* Initial focus on intraday trading
* 15-minute candle timeframe
* Manual execution
* NSE as the initial market
* Single broker data source
* Risk-first, discipline-over-frequency philosophy

**Technical Decisions**

* Python as the core language
* FastAPI for decision and control APIs
* Telegram as the human interaction layer
* In-memory state only (no persistence)

**Rules**

* No trading logic
* No indicators
* No strategy code

**Deliverables**

* Repository structure
* Documentation contracts
* Architecture and safety rules

**Exit Criteria**

* All Phase 0 documentation committed
* File structure finalized
* No ambiguity in scope or rules

---

## 🟢 LEVEL 1 — Core MVP (Intraday Decision Engine)

**Goal**
Build a system that can reliably decide **when not to trade**.

### Core Components

**Market Data Engine**

* Broker API integration (Angel, Shoonya, or Fyers)
* Historical candle preload at startup
* Live LTP monitoring
* Accurate 15-minute candle construction
* Single source of candle truth

**Indicator Engine**

* EMA (fast and slow)
* RSI
* ATR
* Volume average
* Calculations only on closed candles
* No repainting and no ML involvement

**Strategy Engine**

* Single, rule-based strategy
* Outputs limited to:

  * BUY, SELL, or NO_TRADE
  * Entry price
  * Strategy identifier
* No quantity, stop-loss, or target logic
* No risk overrides

**Risk Engine**

* Capital input handling
* Risk per trade calculation
* Daily loss limit (kill switch)
* Position sizing
* Stop-loss and target calculation
* Final trade veto authority

**State Manager**

* Daily P&L tracking
* Open position tracking
* Trade count limits
* Cooldown enforcement

**Output Layer**

* Telegram-based trade plans
* Risk summaries
* Manual execution only
* No automated order placement

**Result of Level 1**

* Logic-level TradingView replacement
* Disciplined trading decision assistant
* Capital-protecting system

**Exit Criteria**

* Stable intraday behavior
* Risk rules always enforced
* System comfortable producing full no-trade days

---

## 🟡 LEVEL 2 — Stability and Control (MVP+)

**Goal**
Reduce drawdowns and improve robustness, not intelligence.

**Market Stability Controls**

* ATR spike detection
* Volume anomaly detection
* Index-level volatility awareness
* Scheduled event avoidance (RBI, Budget)

**Exit Improvements**

* Structure-based early exits
* Time-based exits
* Rule-based trailing stop-loss

**Persistence Layer**

* SQLite as initial storage
* Optional MySQL later
* Storage of trades, P&L, decisions, and rejections

**Purpose**
Enable audits, diagnostics, and learning.

**Result of Level 2**

* Fewer poor-quality trades
* Better drawdown control
* Calmer system behavior

**Exit Criteria**

* Reliable historical records
* Observable improvement in stability

---

## 🟠 LEVEL 3 — ML Filtering (Non-Predictive)

**Goal**
Use machine learning to filter trade quality, not to predict price.

**Allowed Usage**

* Trade quality scoring
* Volatility regime classification
* Time-of-day performance analysis
* Strategy suitability checks

**Inputs**

* Indicator values
* Time features
* Volatility metrics
* Volume data
* Past trade outcomes

**Outputs**

* Confidence or quality scores
* Risk adjustment suggestions

**Strict Rules**

* ML must not generate entries
* ML must not define stop-loss or targets
* ML must not override the risk engine

**Exit Criteria**

* Measurable improvement in trade quality
* ML influence fully explainable

---

## 🔵 LEVEL 4 — News and Context Awareness

**Goal**
Avoid trading during chaotic or uncertain market conditions.

**Context Sources**

* Economic calendars (RBI, CPI)
* Earnings schedules
* Free RSS-based market feeds

**Usage**

* Event density detection
* Uncertainty spike identification
* No directional prediction from news

**Exit Criteria**

* Reduced exposure during event-driven volatility
* Clear contextual explanations for trade suppression

---

## 🟣 LEVEL 5 — Reasoning and Explainability (LLM Layer)

**Goal**
Make system behavior transparent and understandable.

**LLM Responsibilities**

* Explain trade rejections
* Summarize daily and weekly behavior
* Generate structured trade journals
* Answer questions such as:

  * Why were there no trades today?
  * Why was this exit early?

**Hard Restrictions**

* No price prediction
* No trade decision authority
* No modification of risk rules

LLMs consume structured system output only.

**Exit Criteria**

* Clear human-readable explanations
* Improved review and learning process

---

## 🟤 LEVEL 6 — Optional Automation

**Goal**
Introduce automation only after sustained stability and confidence.

**Scope**

* Semi-automated order placement
* Broker-side stop-loss and target handling
* Manual confirmation workflows

**Conditions**

* Sustained profitability
* Controlled drawdowns
* High confidence in system behavior

Automation remains optional and reversible.

---

## 🔒 Phase Discipline Rules

* Phases must be completed sequentially
* Features from future phases must not be introduced early
* Any deviation must update this document
* Safety and discipline override speed

---

## Final Principle

Perfection is not feature count.
Perfection is correct sequencing.

---