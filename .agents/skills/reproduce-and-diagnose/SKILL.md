---
name: reproduce-and-diagnose
description: Execute approved MedCon independent-coder reliability, ordinal tone and three-level actor-reference logistic models while preserving units, coding and diagnostics.
metadata:
  version: "1.1.0"
---

# reproduce-and-diagnose

## Inputs

Source-bound execution specification and current user authorization, unchanged author data, original independent ratings, measurement dictionary, execution environment, and inspected author code. Read [the execution contract](references/execution_contract.md). Preserve the distinction between authorization to run the faithful source specification and unfinished student reading/diagram attestations. The user's explicit request to implement and run the original analyses authorizes that work; do not ask for the same authorization again.

## Procedure

1. Bind sources and settings to an execution-specification version. Inspect actual recodes, reference groups, independent-rating selection, estimator, likelihood, quadrature, covariance and prediction conventions. Retrieve primary command documentation/source for undocumented defaults; distinguish recovered defaults from unpinned original builds. Log discrepancies instead of changing the paper's hypothesis to match results.
2. Verify hashes, value domains, missing codes, independent-rating columns, identifier collisions and nesting. Preserve original files. Construct prepared analysis files programmatically and save every exclusion/count. Context predictors are fixed categories, not a country-media-item random hierarchy. A matched-rater workbook can contain units absent from the final analysis; do not replace it with consensus data.
3. Estimate the original reliability suite from independent ratings. Match identity weights, missing-rater handling, two-rater versus all-rater selections, conditional standard errors, 95% intervals and benchmarking where established. Do not infer an unverified import placeholder mapping from column order alone.
4. Refit item proportional-odds ordered logit and original alternative links. Reconstruct both original proportional-odds diagnostics, retaining the numeric RHS used by omodel separately from the factor RHS used by gologit2. Check sparse outcome support, identifiability, convergence and covariance before accepting diagnostic statistics.
5. Fit both separate frequentist Bernoulli/logit models with Gaussian actor/statement random intercepts nested in item random intercepts. Match the original seven integration points, fixed effects, sample and maximum-likelihood target. Validate a Python implementation with known-answer/independently integrated likelihood checks before accepting substantive fits. Mean/variance adaptive quadrature is not a unique finite grid: disclose unrecovered posterior orthogonalization and prediction-grid details. Do not call exact executable equivalence established merely because seven points or rounded coefficients match. Bayesian binomial mixed models, linear mixed models, ordinary logistic regression and unverified Laplace approximations do not replace this main estimator.
6. Save full and null model coefficients, covariance, intercept variances, likelihood/fit, convergence and integration checks. Compute probabilities and discrete category AMEs with the verified original random-effect convention and delta-method uncertainty. Numerical convergence is separate from agreement with a printed result.
7. Inspect outputs against source targets and retain all computed values, including discrepancies and failed diagnostics. Run a harmless negative test only on synthetic/copied inputs; demonstrate detection and recovery. Save executable code, actual outputs, logs, model artifacts and a concise findings/index page. Keep published values, new estimates, numerical integration checks and any deliberately different sensitivity fit separate.

## Outputs

Executable analysis/ code, data/prepared/ inputs, outputs/reproduced/ results, outputs/diagnostics/, and records/run_logs/. Record data/specification versions, commands, runtime, unresolved entries, and actual skill invocation. Write project-authored explanations and labels in English while preserving exact source identifiers.

## Validation

Sample construction must be traceable. Distinguish coefficients, odds ratios, probabilities, and percentage-point changes. Align model settings with primary evidence. Refit models rather than copying saved estimates. Statistical significance is not a software-test criterion.

For this project, use `analysis/prepare_replication.py`, `analysis/reliability_reproduction.py`, `analysis/ordinal_reproduction.py`, `analysis/nested_logit.py` and `analysis/binary_predictions.py`. Consult `docs/execution_specification.md` and the result index for exact commands. Check independent raw counts and copied-input rejection with `tests/skill2/data_checks.py`; check the nested likelihood with `tests/skill2/glmm_reference.py` and `tests/skill2/check_nested_logit.py`. Preserve invalid generalized ordinal probabilities, singular information and repeated coder identities as substantive findings, rather than silently adjusting data or degrees of freedom.

## Stopping rules

Stop the affected fit without applicable user authorization, required inputs, valid matching/nesting, an established estimator, or convergence. Record the issue and continue independent authorized analyses. Source-code ambiguity stops only the dependent claim. Do not silently recode, change estimators, simplify the model, tune to published values or label a partial result as fully equivalent. User-authorized integration diagnostics may vary quadrature points separately; retain the original seven-point result as the faithful configuration. No Stata execution is permitted for the current Python-only task. Scientific approval, completed foundational reading and independent verification must not be fabricated.
