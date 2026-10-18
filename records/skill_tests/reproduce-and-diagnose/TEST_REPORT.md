# Skill 2 execution and test record

Date: 2026-10-18. Skill: `reproduce-and-diagnose`, version 1.1.0. Actual invocation: explicit loading of `.agents/skills/reproduce-and-diagnose/SKILL.md` in this project chat, followed by source inspection, executable Python implementation, real analyses and checks. This was not a mere skeleton or hypothetical demonstration.

The user's request authorized real Python-only reliability, descriptive and hypothesis-model reproduction and saving all results. It supersedes the earlier postponement of skill 2. No Stata execution occurred. Student reading attestations and final submission approval were not inferred.

## Behavioral evidence

- Ordinal branch: `analysis/ordinal_reproduction.py`; isolated forward-test artifacts retained in `tmp/skill2_forward/ordinal/`. Actual canonical results, source bindings, run receipt and output hashes are under `records/run_logs/skill2/ordinal/`. Thirteen meaningful checks include an historical Wolfe–Gould known answer, independent statsmodels fits for all three links, probability/gradient checks and unchanged originals. Failed generalized-model diagnostics remain failed rather than being adjusted to the printed p value.
- Reliability branch: independent rater input, author selections and separately implemented alpha checks; canonical results and diagnostics retained in the reliability directories. The official published comparison was inspected after the implementation/fits, not used as a fitting target.
- Advanced-model branch: independent QUADPACK and high-point fixed-quadrature references, structural fixtures and candidate-grid checks under `outputs/diagnostics/glmm/`; these establish likelihood checks, not an independent full-model refit or exact original executable equivalence.
- Data and negative test: `tests/skill2/data_checks.py` independently reads raw data using pyreadstat, confirms descriptive counts, rejects a synthetic invalid code, then recovers from an untouched valid copy. Evidence: `outputs/diagnostics/data_independent_checks.json`.

Independent branch agents used separate implementation/output paths. They had project context and sources; this was not a blinded external human audit. Scoped forward-test requests and subsequent corrections were supplied through the collaboration tool. Exact per-run underlying model identifiers were not exposed and are not invented.

## Runtime discovery and static validation

The existing app-server discovery probe initially failed twice before initialization with `Codex app-server closed before returning the discovery response`. The second command, stdout/stderr and exit status are recorded in `records/run_logs/skill2/discovery_attempt.*`. A subsequent `codex --version` check exposed denied runtime temporary-alias access under `E:/Codex/tmp`. With approved runtime filesystem access, the probe succeeded: Codex Desktop 0.160.1 discovered all three enabled repository skills, with no project errors. See `discovery.json` and `records/run_logs/skill2/discovery_with_runtime_access.*`. This read-only probe performed no inference and is distinct from the actual invocation.

The skill was explicitly read and applied. The skill-creator frontmatter validator returned `Skill is valid!` before the final minor instruction revision; rerun validation is recorded with final package checks. Static validation does not certify statistical correctness.

## Observed corrections and limitations

An earlier M2 candidate fit stopped on failure of posterior-moment adaptation during an optimizer trial. The failure log is retained. The implementation allows 400 iterations and applies half-step damping after 20 ordinary moment iterations while preserving the same fixed point; this is a Python numerical choice. Invalid warmup trial parameters are rejected and logged, while the final target must converge. An always-damped trial was unnecessarily slow and was stopped; it did not change the statistical model. An earlier M3 log marked running was interrupted by the session/usage interruption and is not accepted as a completed fit. New runs use separate log names. A notebook-generation inline command failed shell quoting before writing; the saved helper then generated and validated the notebook successfully.

The seven-point engine implements the original statistical likelihood and specified node count, but public documentation does not fully establish historical finite-grid identity. This limitation is material to the user's exact-parameter request and remains explicit in `docs/execution_specification.md` and the GLMM method note. No missing setting is silently invented. Completed estimates, validation status, unresolved numerical issues and final-fit integration checks are indexed from `docs/replication_results.md`.

## Final saved-result checks

All four binary full/null fits completed with successful final optimization. Independent scaled-gradient and three-step observed-curvature checks passed for each saved vector; independent high-order integration quantified seven-point approximation error separately. The result set contains 60 reliability coefficient rows, 45 published model-cell comparisons, 12 directional hypothesis targets, 40 ordinal margins/25 ordinal AMEs and 16 binary margins/10 binary AMEs. Forty-four model cells match printed rounding; the M2 mixed-system OR differs slightly and is retained.

The initial final repository check exposed missing legacy `status` and `tolerance` columns in the new comparison schema. The comparison generator was corrected to retain those columns, rerun, and the repository material check passed. Python syntax checks passed for all 14 analysis/verification modules, copied-input tests passed, and `git diff --check` passed. Final artifact hashes and 84 resolved navigation links are recorded in the invocation receipt. These checks do not convert invalid source diagnostics or unrecovered historical settings into verified claims.
