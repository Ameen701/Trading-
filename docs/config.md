# Configuration Management

This document defines how configuration and secrets are managed in the system.
Configuration controls behavior; code controls logic.

---

## 1. Configuration Principles

- Configuration must be external to code
- No hard-coded values in business logic
- Configuration changes must not require code changes
- Defaults must be safe and conservative

---

## 2. Configuration Types

### 2.1 Environment Variables (`.env`)

Used for:
- Broker API keys
- Telegram bot token
- Sensitive credentials
- Environment identifiers (DEV / PROD)

Rules:
- `.env` files must never be committed to Git
- Environment variables must be accessed via a single loader
- Missing secrets must halt startup safely

---

### 2.2 YAML Configuration Files (`/config`)

Used for:
- Strategy parameters
- Risk parameters
- Time and market thresholds
- Feature toggles

Files:
- `base.yaml` — shared defaults
- `dev.yaml` — development overrides
- `prod.yaml` — production overrides

Rules:
- YAML files may be committed
- No secrets allowed in YAML
- All parameters must have documented meaning

---

## 3. Loading Order

Configuration must be loaded in the following order:
1. Base configuration
2. Environment-specific overrides
3. Environment variables

Later sources override earlier ones.

---

## 4. Validation Rules

- All required configuration values must be validated at startup
- Invalid or missing configuration must:
  - Prevent system startup
  - Log clear error messages
- Runtime configuration mutation is not allowed in Phase 1

---

## 5. Change Management

- Parameter tuning is allowed with documentation
- Structural config changes require review
- Configuration changes must be traceable via Git history

---

## 6. Change Policy

- Adding new parameters is allowed
- Removing or renaming parameters requires review
- Secrets handling rules are non-negotiable
