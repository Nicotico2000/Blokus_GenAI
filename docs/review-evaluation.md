# Review Evaluation

Use this rubric to evaluate whether a review activity was effective.

| Dimension | Strong evidence | Weak evidence |
| --- | --- | --- |
| Requirements quality | Requirement IDs are present, correct, and mapped to acceptance criteria | Requirements are implied or missing |
| Code correctness | Reviewer cites concrete behavior paths and potential regressions | Reviewer only gives broad approval |
| Test sufficiency | Positive/negative tests and fixture coverage are verified | "Tests pass" without scope check |
| AI-output control | Validation and adoption decision logged in `docs/ai-usage.md` | AI content adopted without validation record |
| Traceability | Requirement, issue, file, test, and evidence links are explicit | Links are partial or absent |
| Human-review visibility | Non-author reviewer signs off and concerns are resolved | No visible independent review |

## Minimum acceptance for review records

- Artifact under review is identified.
- Review objective is stated.
- Validation method is explicit.
- Outcome is one of: accepted, revised, rejected, deferred.
- Follow-up action is recorded when revisions are required.
