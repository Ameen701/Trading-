# Documentation Overview

This directory contains all official documentation for the trading decision
system. These documents define system constraints, architecture, workflow,
and current project state.

Documentation in this folder is considered **authoritative**.
If there is a conflict between code and documentation, the documentation wins.

---

## Purpose of This Folder

The `docs/` directory exists to:

- Lock system assumptions and constraints
- Prevent scope creep and unsafe changes
- Guide AI-assisted development
- Provide clarity for future contributors
- Preserve decision history and project context

---

## How to Use These Documents

- Read **Phase 0 documents** before writing any new logic
- Update `current_status.md` whenever the project phase changes
- Do not modify core documents casually
- Treat documentation changes as production changes

---

## Document Index

### Core System Contracts
These documents define non-negotiable system rules.

- `product_constraints.md`  
  Defines what the system is allowed and not allowed to do.

- `architecture.md`  
  High-level system design and interaction between components.

- `tech_stack.md`  
  Approved technologies and tools.

- `time_rules.md`  
  Market hours, candle rules, and time handling.

- `error_policy.md`  
  How the system behaves under failure conditions.

- `logging.md`  
  Logging and observability rules.

- `config.md`  
  Configuration and secrets management rules.

- `workflow.md`  
  Development and AI-assisted coding workflow.

- `file_structure.md`  
  Repository layout and file placement rules.

---

### Project Management Documents
These documents track intent, direction, and reality.

- `project_overview.md`  
  High-level purpose and philosophy of the project.

- `roadmap.md`  
  Phased development plan and sequencing.

- `current_status.md`  
  Current phase, progress, and next steps.

---

## Update Rules

- `roadmap.md` changes rarely and deliberately
- `current_status.md` changes frequently and honestly
- Core contract documents change only with strong justification

All documentation changes must be committed to version control.

---

## Guiding Principle

Documentation is not optional.
It is part of the system.
