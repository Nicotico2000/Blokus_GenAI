# Team Summary

## Project scope

- Phase 1 baseline: Blokus Classic in plain Python with a minimal CLI, JSON state I/O, rule validation, move application, and legal-move listing.
- Phase 2 direction: add Blokus Duo by extending the same configurable engine, not by creating a second engine.
- Course process goals: requirements traceability, issue-driven execution tracking, reproducible evidence, and visible human review.

## Architecture summary

- Shared engine core: `src/blokus/engine.py`, `src/blokus/models.py`, `src/blokus/pieces.py`.
- Mode configuration boundary: `src/blokus/config.py` (Classic today, Duo planned).
- Interfaces: CLI in `src/blokus/cli.py`, optional GUI in `src/blokus/gui.py`.
- Verification surface: tests in `tests/`, fixtures in `fixtures/`, evaluation harness in `src/blokus/evaluate.py`.

## Key deliverables

- Stable requirements baseline: `docs/requirements.md`.
- Architecture and contracts: `docs/architecture.md`, `schemas/`, `docs/json-contracts.md`.
- Traceability and evidence: `docs/traceability-matrix.md`, `docs/evidence-log.md`, `docs/ai-usage.md`.
- Ownership and review discipline: `OWNERSHIP.md`, `.github/pull_request_template.md`, `docs/review-*.md`.

## AI tool usage summary (placeholder)

- Primary tools/models: `TBD`.
- Typical tasks supported: `TBD`.
- Validation and adoption policy summary: `TBD`.

## Key results (placeholder)

- Phase 1 status snapshot: `TBD`.
- Classic baseline pass/fail summary: `TBD`.
- Reproducibility check summary: `TBD`.

## Top counterexamples (placeholder)

- Counterexample A: `TBD`.
- Counterexample B: `TBD`.
- Counterexample C: `TBD`.

## Classic to Duo design impact (placeholder)

- What is expected to remain stable: `TBD`.
- What is expected to require refactoring: `TBD`.
- Risks to track during requirements evolution: `TBD`.
