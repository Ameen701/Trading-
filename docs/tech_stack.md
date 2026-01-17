# Tech Stack

This document defines the approved technology stack for the intraday trading system.
The goal is stability, simplicity, and production readiness.

---

## 1. Programming Language

- Language: Python
- Minimum version: Python 3.10+
- Reason:
  - Strong ecosystem for data, ML, and APIs
  - Rapid development with readability
  - Widely supported in production

---

## 2. Backend Framework

- Framework: FastAPI
- ASGI Server: Uvicorn

Usage:
- REST APIs
- Health checks
- Internal control endpoints

Rules:
- FastAPI is used only as an interface layer
- Business logic must remain framework-agnostic

---

## 3. Market Data & Broker Integration

- Broker API: Angel One (SmartAPI)
- Data access:
  - WebSocket for live market data
  - REST API as fallback
- Candle timeframe: 15-minute (derived internally)

Rules:
- No dependency on TradingView
- Market data must pass validation before use

---

## 4. Scheduling & Execution

- Scheduling:
  - Internal Python scheduler (loop or APScheduler)
- Market-hour awareness enforced in code
- No external workflow orchestration tools

---

## 5. Storage

- Phase 0 / Phase 1:
  - In-memory storage only
- Phase 2 onward:
  - SQLite (local persistence)
  - MySQL (optional upgrade)

Rules:
- Storage layer must be replaceable
- No hard dependency on a specific database

---

## 6. Messaging & Notifications

- Primary channel: Telegram Bot API
- Usage:
  - Trade alerts
  - Risk summaries
  - System notifications
  - User feedback (ACK / SNOOZE)

Rules:
- Messaging is an output channel only
- No decision logic in notification handlers

---

## 7. Configuration & Secrets

- `.env` files:
  - API keys
  - Secrets
- YAML files:
  - Strategy parameters
  - Risk parameters
  - Environment configs

Rules:
- No secrets committed to Git
- No hard-coded values in code

---

## 8. Logging & Monitoring

- Logging:
  - Python `logging` module
  - JSON-formatted logs
- Log levels:
  - INFO, WARNING, ERROR, CRITICAL

Rules:
- All trade decisions must be logged
- Silent failures are not allowed

---

## 9. Explicitly Not Used

The following are intentionally excluded in early phases:
- TradingView (charts or alerts)
- n8n or similar workflow tools
- Auto-trading or unattended execution
- Paid market data services
- Heavy microservice architecture

---

## 10. Change Policy

- Minor library upgrades are allowed
- Core framework changes require review
- Language or framework changes require Phase 0 reset
