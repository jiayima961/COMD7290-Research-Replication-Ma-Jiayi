# Numerical and data diagnostics

- [data_audit.json](data_audit.json): source/sample construction; [data_independent_checks.json](data_independent_checks.json): independent counts plus invalid-code rejection/recovery.
- [reliability](reliability/): known-answer and independent checks, selections, missingness and source-method provenance. Subject-level matching/influence artifacts remain local and can be rebuilt.
- [ordinal](ordinal/): original-link fits, gradients/probabilities and the retained invalid/unidentified generalized-model diagnostics.
- [glmm](glmm/): independent likelihood fixtures, finite-grid comparisons, final-vector gradients and observed-curvature checks for M2/M3 and null models.
- [binary_likelihood_comparisons.csv](binary_likelihood_comparisons.csv): full/null comparison quantities.
- [binary_prediction_integration.csv](binary_prediction_integration.csv): prior-marginal prediction integration checks.

Read [replication_results.md](../../docs/replication_results.md) for what passed, what failed, and which historical settings remain unrecovered. Passing numerical checks does not establish exact Stata-build equivalence or causal identification.
