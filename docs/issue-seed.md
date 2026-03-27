# Issue Seed Backlog

Use this file as a ready-to-copy fallback when live GitHub issue creation is unavailable.

## Label set (target normalization)

Phase labels:

- `phase-1`
- `phase-2`
- `cross-phase`

Scope labels:

- `classic`
- `duo`
- `shared-engine`

Type labels:

- `requirement`
- `implementation`
- `testing`
- `documentation`
- `bug`
- `counterexample`
- `review`
- `decision`

Priority labels:

- `prio-high`
- `prio-medium`
- `prio-low`

Workflow labels:

- `blocked`
- `needs-human-review`
- `ready`
- `in-progress`

---

## I-01 [DOCUMENTATION] Draft requirements baseline in docs/requirements.md

- Summary: Create and maintain a stable requirements baseline with explicit IDs and phase boundaries.
- Motivation: Requirements must not live only in issues; stable source is needed for traceability.
- Related requirement IDs: `R-F-01` to `R-F-14`, `R-NF-03`, `R-D-05`.
- Acceptance criteria:
  - [ ] `docs/requirements.md` exists with required sections and IDs.
  - [ ] Phase 1 and Phase 2 scopes are explicit.
  - [ ] Constraints and out-of-scope are explicit.
- Deliverables: `docs/requirements.md`
- Suggested evidence: PR diff + review note verifying required IDs are present.
- Suggested labels: `phase-1`, `shared-engine`, `documentation`, `requirement`, `prio-high`, `ready`

## I-02 [DOCUMENTATION] Create OWNERSHIP.md

- Summary: Define ownership and reviewer coverage for core repository areas.
- Motivation: Clear ownership and review accountability are required for the course process.
- Related requirement IDs: `R-NF-03`, `R-D-02`, `R-D-04`.
- Acceptance criteria:
  - [ ] `OWNERSHIP.md` table includes required columns.
  - [ ] All key areas have owner/reviewer placeholders.
  - [ ] Acceptance basis and evidence columns reference concrete artifacts.
- Deliverables: `OWNERSHIP.md`
- Suggested evidence: PR diff + review confirmation.
- Suggested labels: `phase-1`, `shared-engine`, `documentation`, `decision`, `prio-high`, `ready`

## I-03 [DOCUMENTATION] Create TEAM_SUMMARY.md skeleton

- Summary: Provide a concise team summary template aligned with course reporting needs.
- Motivation: Team summary acts as a stable high-level checkpoint artifact.
- Related requirement IDs: `R-D-01`, `R-D-03`.
- Acceptance criteria:
  - [ ] Includes project scope, architecture summary, and key deliverables.
  - [ ] Includes placeholders for AI summary, key results, counterexamples, and Classic to Duo impact.
- Deliverables: `TEAM_SUMMARY.md`
- Suggested evidence: PR diff.
- Suggested labels: `phase-1`, `cross-phase`, `documentation`, `prio-medium`, `ready`

## I-04 [IMPLEMENTATION] Define core domain model for board, piece, move, player, and game state

- Summary: Ensure core domain model types and boundaries are explicit and stable.
- Motivation: Shared engine requires stable model contracts before Duo extension.
- Related requirement IDs: `R-F-01`, `R-F-14`.
- Acceptance criteria:
  - [ ] Core model artifacts are documented and implemented.
  - [ ] Game state remains serializable and mode-aware.
  - [ ] Traceability links updated.
- Deliverables: `src/blokus/models.py`, `docs/architecture.md`
- Suggested evidence: tests passing + traceability update.
- Suggested labels: `phase-1`, `shared-engine`, `implementation`, `prio-high`, `ready`

## I-05 [IMPLEMENTATION] Add Classic mode configuration

- Summary: Maintain Classic mode configuration as baseline in shared config.
- Motivation: Classic 4-player baseline is Phase 1 acceptance target.
- Related requirement IDs: `R-F-11`, `R-F-10`.
- Acceptance criteria:
  - [ ] Classic board size, players, and start corners are explicit.
  - [ ] Engine uses configuration at runtime.
- Deliverables: `src/blokus/config.py`, related tests
- Suggested evidence: `tests/test_engine.py` output.
- Suggested labels: `phase-1`, `classic`, `implementation`, `prio-high`, `ready`

## I-06 [IMPLEMENTATION] Add Duo mode configuration contract

- Summary: Define Duo mode data/config contract in preparation for Phase 2 implementation.
- Motivation: Duo support must be introduced by shared configuration, not duplicated engine logic.
- Related requirement IDs: `R-F-12`, `R-F-14`, `R-T-03`.
- Acceptance criteria:
  - [ ] Duo mode is represented in schema/contract artifacts.
  - [ ] Config constraints for board and players are explicit.
  - [ ] No duplicate engine path introduced.
- Deliverables: `schemas/mode_config.schema.json`, `docs/json-contracts.md`, `docs/architecture.md`
- Suggested evidence: schema review + traceability update.
- Suggested labels: `phase-2`, `duo`, `shared-engine`, `implementation`, `prio-medium`, `ready`

## I-07 [IMPLEMENTATION] Implement piece transformations

- Summary: Maintain and verify piece transformations required for legality.
- Motivation: Transform correctness is foundational to placement correctness.
- Related requirement IDs: `R-F-13`.
- Acceptance criteria:
  - [ ] Transform generation handles rotation + reflection with de-duplication.
  - [ ] Representation is test-backed.
- Deliverables: `src/blokus/pieces.py`
- Suggested evidence: `tests/test_pieces.py` output.
- Suggested labels: `phase-1`, `classic`, `implementation`, `prio-high`, `ready`

## I-08 [IMPLEMENTATION] Implement move legality checking

- Summary: Enforce legality checks for opening, continuation, and invalid placements.
- Motivation: Correct legality checking is the core correctness gate.
- Related requirement IDs: `R-F-04`, `R-F-10`.
- Acceptance criteria:
  - [ ] Turn order, in-bounds, overlap, opening-corner, and touch rules are enforced.
  - [ ] Illegal moves return actionable failure reasons.
- Deliverables: `src/blokus/engine.py`
- Suggested evidence: `tests/test_engine.py`, review notes.
- Suggested labels: `phase-1`, `classic`, `implementation`, `prio-high`, `ready`

## I-09 [IMPLEMENTATION] Implement move application

- Summary: Apply legal move and update game state consistently.
- Motivation: Transition correctness is required for CLI and harness reliability.
- Related requirement IDs: `R-F-05`, `R-T-04`.
- Acceptance criteria:
  - [ ] State transition updates board, history, turn, and remaining pieces.
  - [ ] Illegal applications are rejected.
- Deliverables: `src/blokus/engine.py`
- Suggested evidence: `tests/test_engine.py`, `tests/test_evaluate.py`.
- Suggested labels: `phase-1`, `classic`, `implementation`, `prio-high`, `ready`

## I-10 [IMPLEMENTATION] Implement legal move generation

- Summary: Enumerate legal moves for active player in deterministic order.
- Motivation: Needed for CLI legal listing and simple computer player.
- Related requirement IDs: `R-F-06`, `R-F-09`.
- Acceptance criteria:
  - [ ] Legal moves generated without duplicates.
  - [ ] Optional limit parameter supported.
- Deliverables: `src/blokus/engine.py`, `src/blokus/players.py`
- Suggested evidence: `tests/test_ai.py`, manual CLI output sample.
- Suggested labels: `phase-1`, `classic`, `implementation`, `prio-medium`, `ready`

## I-11 [IMPLEMENTATION] Implement JSON state load and serialization

- Summary: Ensure state can be loaded from and serialized to JSON reproducibly.
- Motivation: JSON contracts are required for CLI, fixtures, and reproducibility.
- Related requirement IDs: `R-F-03`, `R-F-07`, `R-T-04`.
- Acceptance criteria:
  - [ ] State load validates mode-compatible shape.
  - [ ] State round-trip is stable.
  - [ ] Contract docs/schemas reflect implementation.
- Deliverables: `src/blokus/models.py`, `schemas/game_state.schema.json`, `docs/json-contracts.md`
- Suggested evidence: `tests/test_serialization.py`.
- Suggested labels: `phase-1`, `shared-engine`, `implementation`, `prio-high`, `ready`

## I-12 [IMPLEMENTATION] Implement minimal CLI

- Summary: Provide minimal command surface for new/show/validate/apply/legal-moves/suggest/play.
- Motivation: CLI is required for reproducible interaction and grading.
- Related requirement IDs: `R-F-02`, `R-F-08`, `R-F-09`.
- Acceptance criteria:
  - [ ] Required commands exist and behave predictably.
  - [ ] Error handling is readable and script-friendly.
- Deliverables: `src/blokus/cli.py`, README command examples
- Suggested evidence: `tests/test_cli.py`, command transcripts.
- Suggested labels: `phase-1`, `shared-engine`, `implementation`, `prio-high`, `ready`

## I-13 [TESTING] Add fixtures for Classic placement legality

- Summary: Add repeatable fixtures for legality paths in Classic.
- Motivation: Fixtures support reproducible rule validation and regression checks.
- Related requirement IDs: `R-T-06`, `R-T-04`.
- Acceptance criteria:
  - [ ] Fixture files are valid and loadable.
  - [ ] At least one fixture exercises legal and illegal placement contexts.
- Deliverables: `fixtures/states/`, `fixtures/scenarios/`
- Suggested evidence: harness replay + review notes.
- Suggested labels: `phase-1`, `classic`, `testing`, `prio-medium`, `ready`

## I-14 [TESTING] Add transformation tests

- Summary: Expand tests for rotation/reflection behavior and symmetry de-duplication.
- Motivation: Transform bugs can silently corrupt legality and move generation.
- Related requirement IDs: `R-T-02`, `R-F-13`.
- Acceptance criteria:
  - [ ] Tests cover representative symmetry and asymmetry cases.
  - [ ] Duplicate transform regressions are detectable.
- Deliverables: `tests/test_pieces.py`
- Suggested evidence: test output.
- Suggested labels: `phase-1`, `classic`, `testing`, `prio-high`, `ready`

## I-15 [TESTING] Add serialization round-trip tests

- Summary: Verify JSON state remains stable after gameplay changes.
- Motivation: Serialization stability is required for fixtures and reproducibility.
- Related requirement IDs: `R-T-04`, `R-F-03`, `R-F-07`.
- Acceptance criteria:
  - [ ] Round-trip tests cover initial and in-progress states.
  - [ ] Controller metadata survives serialization.
- Deliverables: `tests/test_serialization.py`
- Suggested evidence: test output.
- Suggested labels: `phase-1`, `shared-engine`, `testing`, `prio-medium`, `ready`

## I-16 [TESTING] Add end-to-end Classic baseline test

- Summary: Keep an end-to-end Classic baseline test path as release gate.
- Motivation: Integrated correctness needs one high-signal acceptance check.
- Related requirement IDs: `R-T-01`, `R-NF-01`, `R-NF-02`, `R-E-01`.
- Acceptance criteria:
  - [ ] End-to-end scenario runs via harness and CI.
  - [ ] Failures are actionable and reproducible.
- Deliverables: `src/blokus/evaluate.py`, `tests/test_evaluate.py`, `.github/workflows/ci.yml`
- Suggested evidence: CI run + local script output.
- Suggested labels: `phase-1`, `classic`, `testing`, `prio-high`, `ready`

## I-17 [DOCUMENTATION] Create AI usage log

- Summary: Maintain structured disclosure of AI assistance and validation.
- Motivation: AI-assisted claims must be evidence-based and reviewable.
- Related requirement IDs: `R-D-10`, `R-R-04`, `R-E-05`, `R-T-05`.
- Acceptance criteria:
  - [ ] Required log fields are present.
  - [ ] Entries include validation and adoption decisions.
- Deliverables: `docs/ai-usage.md`
- Suggested evidence: completed log entry in PR.
- Suggested labels: `cross-phase`, `documentation`, `review`, `prio-high`, `ready`

## I-18 [DOCUMENTATION] Create evidence log

- Summary: Keep reproducible evidence for successful and failed attempts.
- Motivation: Course evaluation requires evidence of process, not only final state.
- Related requirement IDs: `R-R-02`, `R-R-03`, `R-NF-05`, `R-D-06`.
- Acceptance criteria:
  - [ ] Log template includes required fields.
  - [ ] At least one entry captures worked/failed outcomes and next action.
- Deliverables: `docs/evidence-log.md`
- Suggested evidence: updated log rows.
- Suggested labels: `cross-phase`, `documentation`, `counterexample`, `prio-high`, `ready`

## I-19 [DOCUMENTATION] Create JSON contract documentation

- Summary: Document schema purpose and usage with valid/invalid examples.
- Motivation: Contracts must be understandable by reviewers and implementers.
- Related requirement IDs: `R-F-03`, `R-F-07`, `R-D-05`.
- Acceptance criteria:
  - [ ] Purpose of each schema documented.
  - [ ] Valid and invalid object examples provided.
  - [ ] Relation to CLI/tests/fixtures documented.
- Deliverables: `docs/json-contracts.md`
- Suggested evidence: reviewer sign-off.
- Suggested labels: `phase-1`, `shared-engine`, `documentation`, `prio-medium`, `ready`

## I-20 [DOCUMENTATION] Create traceability matrix

- Summary: Map requirements to issues, files, tests, and evidence.
- Motivation: Traceability reduces review ambiguity and supports grading.
- Related requirement IDs: `R-NF-03`, `R-NF-05`.
- Acceptance criteria:
  - [ ] Matrix includes all baseline requirement IDs.
  - [ ] Each row links to concrete repository artifacts.
- Deliverables: `docs/traceability-matrix.md`
- Suggested evidence: matrix review checklist.
- Suggested labels: `cross-phase`, `documentation`, `requirement`, `prio-high`, `ready`

## I-21 [REVIEW] Human review of Phase 1 requirements

- Summary: Perform explicit human review of Phase 1 requirements baseline.
- Motivation: Requirements quality must be validated before major implementation work.
- Related requirement IDs: `R-D-07`, `R-D-08`, `R-D-09`.
- Acceptance criteria:
  - [ ] Reviewer confirms required IDs and scope boundaries.
  - [ ] Review outcome logged (accepted/revised/deferred).
- Deliverables: review notes linked from PR/evidence log
- Suggested evidence: `docs/evidence-log.md` entry + PR comment.
- Suggested labels: `phase-1`, `review`, `needs-human-review`, `prio-high`, `ready`

## I-22 [REVIEW] Human review of legality rules and acceptance tests

- Summary: Review legality implementation and acceptance tests with non-author reviewer.
- Motivation: Core rules are high risk and require explicit human validation.
- Related requirement IDs: `R-F-04`, `R-F-10`, `R-T-04`, `R-T-05`.
- Acceptance criteria:
  - [ ] Reviewer inspects legality paths and related tests.
  - [ ] At least one counterexample is checked or documented as not found.
  - [ ] Review result and follow-up actions are recorded.
- Deliverables: review notes + updated evidence log
- Suggested evidence: PR discussion + `docs/evidence-log.md` row.
- Suggested labels: `phase-1`, `classic`, `review`, `needs-human-review`, `prio-high`, `ready`
