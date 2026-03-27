# Requirements Baseline

This document is the stable requirements source of truth for this repository. Actionable implementation work should be tracked in GitHub Issues, but requirements must remain stable here with explicit IDs.

## Project scope

- Build a configurable Blokus engine in plain Python.
- Deliver a Phase 1 Classic baseline and prepare for a Phase 2 Duo extension through configuration.
- Keep strong traceability between requirements, code, tests, documentation, and evidence.

## Phase 1 scope

- Classic mode baseline with four-player gameplay.
- Minimal CLI and JSON state contracts.
- Move validation, move application, legal move listing, and state serialization.
- Automated tests, reproducible scripts, and fixtures.

## Phase 2 scope

- Add Duo support by extending the same engine configuration layer.
- Add Duo-specific contracts, fixtures, tests, and evaluation evidence.
- Treat Classic to Duo as a requirements-evolution case study.

## Constraints

- Plain Python implementation.
- No heavy GUI dependency for baseline acceptance.
- No LLM runtime dependency in the delivered runtime solution.
- No online multiplayer requirement for baseline delivery.

## Functional requirements

- `R-F-01`: The system shall provide a configurable Blokus engine that supports Classic and Duo modes.
- `R-F-02`: The system shall provide a minimal CLI.
- `R-F-03`: The system shall load a game state from JSON.
- `R-F-04`: The system shall validate proposed move legality.
- `R-F-05`: The system shall apply a valid move.
- `R-F-06`: The system shall list legal moves.
- `R-F-07`: The system shall print or serialize resulting game state.
- `R-F-08`: The system shall support human players.
- `R-F-09`: The system shall support at least one simple computer player.
- `R-F-10`: The system shall enforce rulebook conditions necessary to start, continue, and terminate a Classic game session.
- `R-F-11`: Classic mode shall support four-player gameplay baseline.
- `R-F-12`: Duo mode shall support two-player gameplay with Duo-specific board and starting positions.
- `R-F-13`: The system shall support piece transformations required for legal placements.
- `R-F-14`: The same engine implementation shall be extended by configuration to support Duo.

## Non-functional requirements

- `R-NF-01`: The repository shall be testable.
- `R-NF-02`: The repository shall provide reproducible install, test, and run workflows.
- `R-NF-03`: The repository shall maintain clear ownership, traceable contributions, and issue-based tracking.
- `R-NF-04`: The implementation shall prioritize correctness over sophisticated UI or strong AI play strength.
- `R-NF-05`: Project documents shall include direct evidence links for major claims.

## Constraint and exclusion requirements

- `R-C-01`: The delivered runtime solution shall have no LLM runtime dependency.
- `R-C-02`: Heavy GUI is out of scope for baseline acceptance.
- `R-C-03`: A strong AI player is optional only.
- `R-C-04`: Online multiplayer is out of scope.

## Documentation requirements

- `R-D-01`: `TEAM_SUMMARY.md` exists.
- `R-D-02`: `OWNERSHIP.md` exists.
- `R-D-03`: Individual portfolio deliverables are required later.
- `R-D-04`: Project shall document owned-package contributions with evidence.
- `R-D-05`: Project shall document guideline applications.
- `R-D-06`: Project shall document reproducible counterexamples.
- `R-D-07`: Reviewing guideline package is required.
- `R-D-08`: Reviewing guideline package shall address reviewing tasks in this project.
- `R-D-09`: Project report shall analyze guideline usage, failures, and refinements.
- `R-D-10`: AI usage shall be documented.

## Evaluation requirements

- `R-E-01`: Project shall provide an evaluation harness.
- `R-E-02`: Project shall evaluate implementation quality and correctness for Classic and Duo.
- `R-E-03`: Project shall treat Classic to Duo as a requirements-evolution case study.
- `R-E-04`: Report shall explain what broke, what the LLM suggested, and what actually worked.
- `R-E-05`: AI-assisted engineering claims shall be evidence-based.

## Reproducibility requirements

- `R-R-01`: Repository shall include reproducible install, test, and run scripts.
- `R-R-02`: Project shall maintain an evidence log of what worked and failed.
- `R-R-03`: Counterexamples shall be documented with enough detail to reproduce failure and refinement.
- `R-R-04`: AI usage documentation shall identify tool/model, task, prompt or prompt category, validation method, and adoption decision.

## Testing and validation requirements

- `R-T-01`: Automated test suite exists.
- `R-T-02`: Tests cover key rules and transforms.
- `R-T-03`: Tests and evaluation harness shall later cover both Classic and Duo.
- `R-T-04`: Project shall include validation evidence for legality checking, move application, and serialization.
- `R-T-05`: AI-assisted outputs shall be validated before adoption.
- `R-T-06`: Project shall use fixtures or equivalent repeatable test inputs where appropriate.

## Out-of-scope baseline

- Strong AI gameplay quality beyond a simple baseline strategy.
- Production-grade online services, matchmaking, or multiplayer infrastructure.
- Rich GUI as a gating requirement for core correctness acceptance.

## Open risks and open issues

- Duo mode is not fully implemented yet in runtime config and tests.
- Requirements may drift if issue descriptions diverge from this baseline.
- Human-review evidence can become inconsistent without PR checklist discipline.
- Counterexample capture is currently process-driven and needs ongoing enforcement.

## Traceability notes

- Requirement-to-implementation/test mapping lives in `docs/traceability-matrix.md`.
- Work items should reference requirement IDs in issue bodies and PRs.
- Evidence for requirement claims should be logged in `docs/evidence-log.md`.
- AI-assisted changes should be logged in `docs/ai-usage.md` before adoption.
