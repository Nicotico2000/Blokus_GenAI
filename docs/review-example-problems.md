# Review Example Problems

Use these examples to calibrate review quality for this repository.

## Requirements review problems

- Requirement drift: issue says one behavior, `docs/requirements.md` says another.
- Phase boundary leak: Duo assumptions accidentally introduced into Phase 1 acceptance criteria.

## Code review problems

- Same-color edge contact is accidentally allowed in legality checks.
- Move generation emits duplicate placements due to symmetric transforms.
- Duo support introduced by branching engine logic instead of configuration.

## Test review problems

- Added rule path has only a positive test and no negative test.
- Fixture still parses but no longer reflects active mode contract.
- Serialization tests miss controller metadata fields and regress silently.

## AI-output review problems

- AI-produced code merged without execution or reviewer validation.
- AI-produced requirement text copied with IDs that conflict with baseline IDs.
- AI summary claims coverage for tests that do not exist.

## PR/evidence review problems

- PR links no requirement IDs and no issue.
- Evidence section says "tested locally" with no reproducible pointer.
- Counterexample discovered but not added to evidence or review docs.
