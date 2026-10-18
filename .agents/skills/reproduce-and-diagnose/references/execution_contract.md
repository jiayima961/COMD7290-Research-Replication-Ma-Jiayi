# Skill 2 execution contract

Use the repository as cwd. Current task: Python-only faithful reproduction of the selected study. Existing published targets are comparisons, never fitted starting answers. Preserve original inputs and historical theory/skill tests. Keep authored files English and link current results prominently from START_HERE.md.

## Required model mapping

- Item tone archive1-5 becomes analysis0-4. Political system raw1/2/3 becomes1/3/2 (Consensus/Mixed/Majoritarian); socio-cultural raw1/2 becomes2/1 (Contested/Stable); media raw1/2/3 becomes1/3/2 (Blog/Website/Newspaper). Use actual author numeric recodes and categorical dummies.
- M1: common-slope ordered logistic likelihood, five outcome categories/four cutpoints, five dummy slopes, no separate free intercept. Original main design: i.polsys i.socdiv i.mediatype. Keep log-odds signs aligned across threshold conventions. Estimate observed-information covariance and95% intervals.
- M2/M3: separate reference outrage/recognition Bernoulli logits; intercept plus same five dummy slopes; Gaussian item and nested actor random intercepts; act_id built from text_id and akteur_id. Fixed predictors are constant within items. No cross-outcome covariance. Frequentist marginal maximum likelihood with7 quadrature points per random-effect dimension and verified original adaptation. Validate implementation; do not substitute a Bayesian estimator.
- Original syntax retains bare numeric polsys/socdiv/mediatype for Wolfe-Gould omodel; this is a different predictor design from the main categorical model. Preserve and explain this distinction. Alternative links must match the original gologit2 cumulative direction, not a similarly named reversed link.
- Independent ratings: author reliability syntax selects Ton_1-Ton_4; reference VALENZ/ANERKENNUNG/HETZE_NUM rater families, plus original long-name responsiveness fields mapped to Q/AG/AW/BM/CC by Stata's Excel importer. Establish mapping from original workbook/header positions, preserve all missing ratings and record selections. Identity weights, se(conditional),95%,benchmark(probabilistic) are source requirements. Retain all reported agreement coefficients where original method is established.

## Saved artifacts

- `analysis/`: readable modules and one rerun entry point; project-environment Jupyter notebook may call these modules rather than duplicate formulas.
- `data/prepared/`: derived files only, ignored from Git until redistribution reviewed. Preserve raw/prepared hashes and data/sample audit.
- `outputs/reproduced/reliability/`, `descriptives/`, `models/`, `predictions/`: new results, machine-readable tables and fitted model artifacts. Include coefficients, SEs, ORs, intervals, likelihood and actual sample counts.
- `outputs/diagnostics/`: convergence/Hessian/integration diagnostics, assumptions, design warnings, negative-test detection/recovery, and method checks. Failed or nonidentified diagnostics remain visible.
- `records/run_logs/skill2/`: source/spec versions, command/stdout/stderr/runtime records and manifest binding scripts/inputs/outputs. Do not invent exact model/build identifiers.
- `docs/replication_results.md`: current results map, completed targets, discrepancies, limits, next checks; START_HERE links it first for results.
- `records/skill_tests/reproduce-and-diagnose/`: actual discovery/invocation, static checks, isolated behavioral test evidence and observations. Distinguish implementer checks from independent statistical verification.

One result row should identify analysis_id, outcome, term/contrast, estimate, uncertainty/scale, source_data_version, specification_version and status. JSON model artifacts may carry covariance and settings without repeating every field in every CSV. Source conflicts, unrecovered defaults and unavailable appendix targets must be explicit in the coverage record. Do not turn an unavailable exact setting into an invented matching claim.
