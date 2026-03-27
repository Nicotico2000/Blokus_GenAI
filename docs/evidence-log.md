# Evidence Log

Use this log for reproducible evidence of implementation and review outcomes.

## Logging policy

- Add one row per meaningful attempt or verification event.
- Link requirement IDs and issue IDs whenever possible.
- Record both what worked and what failed.
- Include direct evidence pointers (test output, fixture path, commit, PR, screenshot, or notes).

## Template

| Date (YYYY-MM-DD) | Area | Related issue | Related requirement | What was attempted | What worked | What failed | Evidence | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-03-27 | Repository setup | I-01, I-20 | R-NF-03, R-NF-05 | Added requirements baseline and traceability matrix | Required docs created and linked | Live GitHub sync pending environment access | `docs/requirements.md`, `docs/traceability-matrix.md` | Sync labels/issues when API access is available |

## Suggested area tags

- `engine-core`
- `cli`
- `serialization`
- `transforms`
- `fixtures`
- `evaluation-harness`
- `documentation`
- `review`
