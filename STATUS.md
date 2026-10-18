# Project status

Updated: 2026-10-19. Stage: user-authorized skill-2 Python reproduction. See docs/replication_results.md for actual calculated results, numerical limitations and current fit status. Student reading/diagram attestations and final submission approval remain pending. Use START_HERE.md for navigation.

## Completed

- The user selected the Option 3 content-analysis article.
- The assignment and selected paper were read; initial theory, measurement, model notes, and published comparison targets were drafted.
- The directory structure, three project skills, and required record templates were created.
- Local copies of the assignment and article were registered without altering their originals.
- The private repository was verified: https://github.com/jiayima961/COMD7290-Research-Replication-Ma-Jiayi
- Repository material checks and official static validation of all three skill files passed. These checks are not evidence of substantive skill invocation.
- Four relevant codebooks, the author Stata package, two independent-coder rating workbooks, and the reliability script were downloaded; originals and checksums are retained locally.
- The initial upload contained 48 files, verified against local Git blob checksums. The repository remained private.
- On the user's correction, all 35 repository-authored files containing Chinese and the separate local workflow guide were translated into English. The workflow filenames and links were updated; see records/language_audit.md.
- On the user's request, an isolated Python 3.12.14 environment, 15 direct analysis/notebook packages and their dependencies were installed from official PyPI. The local project kernel is registered; `pip check` passed and the launcher reported Notebook 7.6.3. Exact package versions are pinned.
- The synthetic environment notebook completed in a fresh project kernel: all package imports, Excel/Stata round trips, categorical-design calculations, known-answer nominal alpha, ordered-logit convergence/probabilities and plotting passed. See `records/run_logs/python_environment_check.json` and `python_environment_setup.md`. No original research data were used in these checks.
- The author code confirms Stata 16 compatibility mode. The Python coverage assessment documents unresolved equivalence for the three-level binary models, proportional-odds diagnostics, reliability outputs and marginal-effect conventions.
- The first skill now includes source-based theory reconstruction, all six hypotheses, measurement/model contracts, an original model-diagram specification and a deterministic validator. The test evidence and review corrections are indexed in `records/skill_tests/specify-empirical-study/TEST_REPORT.md`.
- Actual Codex app-server discovery found all three enabled repository skills from this repository's working directory. The outer `E:/Statistics with AI` directory did not discover them; use the repository root or an explicit full skill path. Discovery does not prove invocation of skills 2 or 3.
- An isolated fresh-context invocation of the first skill produced source-linked test artifacts from original inputs and a labelled synthetic explanation. It preserves pending student approval. Its initial coverage defect was found during source/output review and corrected; the initial receipts remain preserved. No research models or reliability estimates were run.
- The student then supplied a real initial written explanation. It is preserved in `records/student_inputs/2026-10-18_initial_theory_explanation_v1.txt`; actual first-skill personal feedback is in `docs/theory_feedback_v1.md`, with request, source checks and a handoff in `records/skill_invocations/2026-10-18_specify-empirical-study_theory-review/`. Ten quoted ORs were source-checked; raw versus adjusted recognition rankings and the source's own ambiguity are documented.
- Student v2 and second-round feedback are now saved. V2 visibly incorporates the major first-round changes; all 13 explicit OR= entries match the source tables. Current files and both review rounds are ordered in `START_HERE.md`, linked prominently from README. The initial student input, first feedback and completed review/test records remain at their registered paths.

## Current scope and remaining work

- D011 explicitly authorizes faithful Python-only data checks, reliability, descriptives, hypothesis fits and numerical verification. It supersedes earlier task-level no-fit/deferral limits. The source-bound specification is docs/execution_specification.md.
- Actual skill-2 results and limitations are indexed in docs/replication_results.md; completed numerical evidence must not be confused with earlier synthetic skill-1 fixtures.
- Historical finite-grid and reliability-build equivalence limits remain explicit. Do not claim a complete original-executable match merely because printed values agree.
- Complete skill 3, the separate justified substantive sensitivity analysis, student-owned reading/diagram records, final report and acceptance. Computational reproduction does not itself complete all course checkpoints.
- Keep the repository private and do not invite the instructor. The D012 repository cleanup and latest-result synchronization are being verified; see records/reorganization/2026-10-19. No final release or submission has been performed.
- All project-authored files remain English. Preserve original sources, earlier student submissions and completed historical evidence.

## Project identity

- Project/local folder: `COMD7290-Research Replication-Ma Jiayi`.
- GitHub repository: `COMD7290-Research-Replication-Ma-Jiayi`.
- Canonical URL: https://github.com/jiayima961/COMD7290-Research-Replication-Ma-Jiayi
- The administrative rename and reference updates are separate from the pending research tasks.
- The GitHub rename was verified against repository ID 1423254230; visibility remains private. The local folder and origin URL use the new names.

## Reader layout and reusable packages (D012)

- Use START_HERE.md and docs/skills/README.md to find both tested skill packages,
  their real invocations and test evidence. Skill 3 remains unfinished.
- Canonical scientific paths are stable. Auxiliary guides are in docs/guides;
  historical writers are in tools/maintenance. Previous versions and a move map
  are retained under records/reorganization/2026-10-19; no file was deleted.
- The runtime wrappers and notebook now support ordinary Python without RTK.
  tools/restore_inputs.py verifies/restores excluded exact-version inputs.
- This cleanup preserves the saved numerical work; it is not a new full refit.
