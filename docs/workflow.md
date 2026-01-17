# Development Workflow

This document defines how work is done in this repository.
The goal is clarity, safety, and steady progress without unnecessary process.

---

## 1. Core Workflow Principles

- This is a small, focused project
- All contributors follow the same workflow
- Code quality and correctness matter more than speed
- Documentation and code evolve together

---

## 2. Branching & Commits

- Default branch: main
- All changes are made on feature branches
- Direct commits to main are avoided
- Each branch should represent one logical change

Commit messages should be clear and descriptive.

---

## 3. Pull Requests & Reviews

- Every non-trivial change should go through a pull request
- Pull requests must:
  - Explain what changed
  - Explain why it changed
  - Mention any affected documentation

Even in a small team, review is used as a safety checkpoint.

---

## 4. Documentation Discipline

- Documentation is part of the system
- Any change that affects:
  - behavior
  - risk
  - timing
  - strategy logic
  must be reflected in documentation

Outdated documentation is treated as a defect.

---

## 5. AI-Assisted Development Rules

- AI is used as a coding assistant, not a decision-maker
- All AI-generated code must follow:
  - `product_constraints.md`
  - `architecture.md`
  - `file_structure.md`
- AI suggestions must be reviewed and understood before merging

AI must not:
- Introduce new frameworks
- Bypass risk rules
- Violate phase boundaries

---

## 6. Phase Discipline

- Only one phase is active at a time
- Features from future phases must not be added early
- Phase transitions happen only after:
  - stable behavior
  - updated documentation

Skipping or mixing phases is not allowed.

---

## 7. Testing Expectations

- Critical logic should be testable
- Market data, risk, and state logic have priority
- Tests must not rely on live market conditions

---

## 8. Change Policy

- Prefer small, incremental changes
- Large refactors require explicit discussion
- Emergency fixes must still follow safety rules
