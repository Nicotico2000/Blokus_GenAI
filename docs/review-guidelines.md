# Review Guidelines

This guideline package is tailored to this Blokus repository and focuses on requirements, code, tests, AI-assisted output quality, and evidence discipline.

## 1. Requirements review

- Confirm the change references requirement IDs from `docs/requirements.md`.
- Confirm no issue or PR changes requirement meaning without updating `docs/requirements.md`.
- Confirm Phase 1 versus Phase 2 boundaries are explicit.

## 2. Code review

- Verify rule changes against expected gameplay constraints and current mode configuration.
- Confirm shared-engine decisions do not create separate Classic-only and Duo-only logic forks.
- Check for serialization stability and backward compatibility of fixture formats.

## 3. Test review

- Require at least one positive and one negative test for changed rule logic.
- Confirm transforms and legality paths are covered in automated tests.
- Confirm fixture-based tests remain deterministic and loadable.

## 4. AI-output review

- Require explicit validation before adoption (human inspection, tests, or fixture replay).
- Verify AI-produced claims are traceable to repository artifacts.
- Record adoption/rejection in `docs/ai-usage.md`.

## 5. Pull request review

- Use `.github/pull_request_template.md` as a merge gate.
- Require linked issue(s), requirement ID(s), validation evidence, and review scope.
- If `needs-human-review` label is present, do not merge without named human reviewer.

## 6. Evidence review

- Verify claims in docs map to concrete evidence links.
- Ensure failures and counterexamples are logged, not hidden.
- Ensure `docs/evidence-log.md` captures next action, not just result.

## Reviewer checklist

- Requirement IDs present and correct.
- Acceptance criteria can be verified.
- Tests/fixtures changed appropriately.
- Evidence links included.
- AI usage documented when relevant.
