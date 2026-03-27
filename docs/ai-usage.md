# AI Usage Log

This log documents AI assistance used during engineering. Runtime behavior of the delivered solution must remain independent of LLM services (`R-C-01`).

## Logging policy

- Capture AI usage before or at merge time.
- Each entry must include validation and adoption decision.
- Do not mark output as adopted without human review or executable validation.

## Template

| Date (YYYY-MM-DD) | Tool / model | Task supported | Prompt or prompt category | Output summary | Validation performed | Adoption decision | Related files / issues |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-03-27 | GPT-based coding assistant | Repository governance setup | Requirements/doc-structure drafting | Drafted requirements, review, traceability, and issue-seed artifacts | Human inspection and repository consistency checks | Adopted with edits | `docs/requirements.md`, `docs/traceability-matrix.md`, `docs/issue-seed.md`, I-01, I-20 |

## Minimum validation checklist for AI-assisted outputs

- Requirement IDs and wording checked against baseline scope.
- File references verified to exist in repository.
- Commands/scripts validated for reproducibility expectations.
- Tests run for code changes, if code paths were modified.
