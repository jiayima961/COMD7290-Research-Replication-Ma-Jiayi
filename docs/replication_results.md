# Python replication: results and evidence

Updated 2026-10-18. This is the central results index for skill 2. All project-authored artifacts are English. Original input files remain unchanged. No Stata was executed. Results are local; this run has not uploaded them to GitHub.

## Read in this order

1. [Execution specification](execution_specification.md): original statistical models, recodes, settings and unrecovered historical details.
2. [Reliability report](../outputs/reproduced/reliability/REPORT.md): actual coefficients and uncertainty from independent-rating workbooks.
3. [Ordinal/descriptive findings](../outputs/diagnostics/ordinal/findings.md): M1, original alternative links, probabilities and assumption checks.
4. [Advanced-model method verification](../outputs/diagnostics/glmm/method_verification.md): independent likelihood checks and the precise cross-software equivalence boundary.
5. [Published-versus-reproduced comparisons](../outputs/comparison.csv): numerical differences; printed values are never relabelled as calculated estimates.
6. [Skill test and invocation record](../records/skill_tests/reproduce-and-diagnose/TEST_REPORT.md): what was actually executed, checks and failures.

## Results currently established

- Analytical data contain 1,700 items and 3,770 directed references, with 2,453 within-item actor groups in 1,183 items. No main-model required-field exclusions were needed. Raw tone counts are 1,491/159/28/17/5 for analysis values 0–4. References contain 192 outrage and 196 recognition events.
- Reliability: 10 author-selected analyses × six coefficients, conditional SEs and 95% intervals, plus both separately labelled benchmark conventions. All 30 published two-slot coefficients and five published sample counts match displayed precision. Independent alpha calculations agree to better than 1e-12. This does not prove that positional slots represent independent people: 182 matched actor rows repeat a named coder.
- M1: all five slopes, SEs and ORs match Table 3 at reported rounding. Log likelihood is -724.0003868022. Original probit and correctly oriented complementary log-log models were also fitted.
- All source descriptive groupings, five-category frequencies, 40 ordinal predictive margins and 25 ordinal discrete AMEs are saved with the original analysis units preserved.
- Independent raw-data checks and synthetic invalid-input detection/recovery passed. Full nested-model likelihood fixtures agree with independent high-accuracy integration as node count increases; finite-seven-node and historical implementation equivalence are separate issues.

Both binary full models and both nested null models have completed, with successful final optimization. All four have saved coefficients, covariance, random-intercept variances, ICCs, likelihood, AIC and convergence diagnostics. Independent final-vector integration and curvature checks are saved for every model. Binary predictions add 16 margins and 10 discrete AMEs, including full-covariance delta uncertainty and separate integration checks.

The [12 directional hypothesis tests](../outputs/reproduced/hypothesis_tests.csv) reproduce the original main pattern: H1a is contradicted at item level and unsupported at reference level; H1b is unsupported; H2a is supported at item level only; H2b has a significant association opposite to its prediction; H3a and H3b are supported in their specified comparisons. These are associations, not causal mechanisms.

Across 45 Table 3/4 coefficient, SE and OR cells, 44 fall within the printed two-decimal rounding interval. The exception is the M2 mixed-system OR: Python 2.246459 versus printed 2.24. M2 minus-two-log-likelihood is 1326.556979 versus published 1326.48; M3 is 1421.271116 versus 1421.27. The M2 discrepancy is retained. Agreement of the main hypothesis pattern is not a claim of exact historical finite-grid equivalence.

## Issues found, retained for the teacher

1. The article's text labels approximately .09 as Nagelkerke R-squared, while Table 3 labels it McFadden. Recalculation gives McFadden .08901439 and Nagelkerke .13147351.
2. The generalized ordered-logit diagnostic reaches the published rounded likelihood-ratio difference, but has unidentified/diverging parameters and seven negative unobserved-category probabilities. Its ordinary chi-square inference is not accepted. The separate Wolfe–Gould numeric-predictor check yields chi-square 7.43106347, df 9, p .59233333.
3. Under the original alternative probit link, the mixed-versus-consensus contrast has p .1493 although its sign is unchanged. Similar substantive patterns do not mean identical significance for every contrast.
4. Original reliability software build is unpinned. The historical benchmark method is reconstructed; the current source-verified method changes eight of 60 benchmark labels. Point coefficients and uncertainty verification are separate from these labels. Numeric -99 and the author's original column selections are preserved and audited.
5. The binary statistical model, hierarchy and seven-point setting are preserved, but public source material does not fully recover historical adaptive-grid and prediction-grid internals. Exact finite-arithmetic Stata equivalence cannot be promised. Higher-point comparisons quantify numerical error without replacing the configured seven-point result.

## Where each deliverable lives

| Material | Location |
|---|---|
| Reusable code | [analysis](../analysis/) |
| Jupyter entry point | [01_replication.ipynb](../analysis/01_replication.ipynb) |
| Prepared analysis and rating data | [data/prepared](../data/prepared/) |
| Reliability estimates and benchmarks | [outputs/reproduced/reliability](../outputs/reproduced/reliability/) |
| Descriptive tables | [outputs/reproduced/descriptives/ordinal](../outputs/reproduced/descriptives/ordinal/) |
| Model estimates, covariance and fit | [outputs/reproduced/models](../outputs/reproduced/models/) |
| Probabilities and AMEs | [outputs/reproduced/predictions](../outputs/reproduced/predictions/) |
| Failures, data checks, assumptions and integration | [outputs/diagnostics](../outputs/diagnostics/) |
| Original published targets | [outputs/published](../outputs/published/) |
| Commands, versions, runtimes and hashes | [records/run_logs/skill2](../records/run_logs/skill2/) |

## Rerun

From the project folder, use the existing project environment:

```powershell
rtk proxy .venv/Scripts/python.exe -X utf8 analysis/run_replication.py
```

To run one stage, add `--stage data`, `reliability`, `ordinal`, `binary`, `summaries` or `checks`. The notebook calls these same modules; it does not duplicate the formulas. Each stage retains command logs and stops on command failure. Read statistical diagnostics even when a command succeeds. A runnable notebook interface is not itself a second independent clean-room rerun.

Cross-software reproducibility tests computation under a stated model. It does not establish causality or robustness to every plausible specification. Student reading notes, theory-diagram authorship, final interpretation and submission approval remain student-owned tasks.
