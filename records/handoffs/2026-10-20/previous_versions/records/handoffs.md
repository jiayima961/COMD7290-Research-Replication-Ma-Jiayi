# Task functions and fresh-session handoffs

Separate four functions: theory/specification review, data/measurement analysis, model implementation, and replication verification. They can be performed at different times. An isolated fresh-context test has been demonstrated; the formal handoff of an approved real-study specification remains pending.

Each task must identify its task/model ID, approved scope, primary-source locators, input paths and checksums, specification version, dependencies, permitted tools and write locations, expected outputs, checks, and stopping conditions. At completion, list changed files, actual commands, results, limitations, and unresolved decisions.

A fresh session should recover context from README.md, STATUS.md, AGENTS.md, and records/decisions.md, then inspect original evidence. Do not rely solely on an implementer's summary. Record the date and actual receiving-session actions when a handoff succeeds; do not prefill success.

## 2026-10-18: isolated first-skill recovery test

Native agent `/root/skill1_forward_test` started with fork_turns=none, an explicit task, an isolated case, original inputs and the first skill's path. It recovered the case README, AGENTS, STATUS, decisions and input manifest before reconstructing the source-linked specification. It did not read the canonical earlier AI research drafts. Its receipt is `skill_tests/specify-empirical-study/forward_case/records/specification_handoff.md`; the exact dispatch prompt and runtime record are in that test's parent directory.

The initial blind invocation was followed by evaluator review and a documented coverage correction; initial snapshots and the ID crosswalk are retained. The receiving task's completed work is a synthetic workflow demonstration. It provides neither approved student input nor independently reproduced statistical quantities. The next real handoff requires the student's preliminary explanation/readings, their review of revisions and an approved specification. Skill 2's implementation/equivalence work remains deferred by the user.

## 2026-10-18: real student explanation reviewed

The student's written v1 is now preserved and the first skill has produced personal feedback. See `skill_invocations/2026-10-18_specify-empirical-study_theory-review/README.md` for the actual request, source/version bindings, commands and checks. This review took place in the current shared-context chat; it is not independent numerical verification or an approved-study fresh-session handoff. The next receiving task should recover the unchanged student v1, feedback F01-F09, pending reading/diagram records and the student's eventual decisions before making a revision. Do not treat the AI examples as accepted student text or the prior synthetic case as the student's specification.

## 2026-10-18: student v2 reviewed and current-version navigation

Start with the root START_HERE.md, then the preserved student v2, feedback round 2 and docs/student_review.md. The index retains the full v1-to-v2 review sequence and links the detailed receipts. The round-2 receipt is skill_invocations/2026-10-18_specify-empirical-study_theory-review_v2/README.md. V2 addresses the main first-round issues; remaining advice is focused refinement. A receiving task must distinguish visible textual changes from explicit approval, and must not re-request v1 or call the received v2 "pending." Actual foundational reading scopes, a student-created diagram, full-specification approval and the deferred skill-2 implementation validation remain pending.


## Current handoff: completed skill-2 computations

Start from START_HERE.md and docs/replication_results.md, then the execution specification, comparison.csv, hypothesis_tests.csv and branch diagnostics. Three primary models and two nulls have actual outputs; do not rerun expensive fits merely to recover context. All four binary fits have independent final-vector integration and curvature evidence. Keep M2's printed-value discrepancy, generalized ordinal diagnostic failure, reliability repeated-coder/build issues and exact finite-grid caveats visible. Earlier theory submissions and feedback remain unchanged. Remaining coursework includes skill 3, separately justified substantive sensitivity, student reading/diagram records and final report/acceptance. No latest outputs were pushed to GitHub.
