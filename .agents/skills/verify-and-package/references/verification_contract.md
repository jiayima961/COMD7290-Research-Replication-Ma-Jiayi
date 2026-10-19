# Source and execution contract

Version 1.0.0, 2026-10-19. The project's root is the working directory. Use ordinary
Python from the activated project environment; RTK is optional on another computer.

| Evidence | Source | Comparison scope |
|---|---|---|
| Item distributions | Article Table 2 p.282 | All country/media and pooled percentage cells |
| Ordinal estimates | Table 3, Results pp.281–283 | Five slopes, SEs, ORs, stars, OR intervals, N, LL, R2 labels |
| Binary estimates | Table 4 p.286 | Both models, all five contrasts, sample/hierarchy counts, likelihood |
| Reference descriptives | Results pp.284–285 and Figure 2 | Printed percentages; graph-only cell vectors distinguished |
| Reliability | Official final inter-coder reliability page and author script | Five outcomes, six coefficients, two positional slots; all-slot and uncertainty targets unavailable |
| Ordinal AMEs | Official Additional Analyses for Löb et al. (2024) | All 25 AMEs and 50 interval endpoints; record cached/live access state |
| Binary AMEs | Results pp.286–287 | Ten AMEs and twenty interval endpoints |
| Assumption/robustness checks | Notes 1–3 pp.290–291 and author syntax | WG, generalized ordinal LR validity, alternative links, empty-model LR and boundary caveat |

The reconciler emits one row per uniquely identified quantity: analysis_id,
quantity, original/reproduced values, difference, tolerance, status, source locator,
evidence path, explanation, proposed cause and confidence, validation status.
For decimal displays tolerance is half of the final displayed unit, fixed before
comparison. Counts and significance tiers use exact integer agreement. No numeric
target means not_verifiable, even if the new calculation is sound. Equality to a
displayed number is not equality to an unavailable unrounded estimate.

Commands after restoring the exact registered inputs:

```text
python analysis/run_verified_replication.py
python tools/verification_package_audit.py
```

The first command refits the unchanged scientific pipeline, reconciles all
results, runs the independent checks and executes the separate sensitivity. It
may take twenty minutes or longer. To verify existing completed fits without
refitting, run analysis/verify_and_package.py, tests/skill3/check_verification.py
and analysis/skill3_sensitivity.py separately. Clean restart is
separately logged by tools/verification_clean_restart.py; its default destination
must not already exist. Preserve prior clean runs instead of deleting them.

Reports: report/verification/01_results_comparison.md and its DOCX; 02_python_stata_equivalence.md
and its DOCX. Technical synthesis is outputs/review_report.md. Coverage lives in
docs/analysis_inventory.csv and outputs/verification/comparison_coverage.csv.
Personal acceptance is recorded only from actual student input, separately from
AI technical checks. The third skill does not make a final release itself.
