# Verification programs

These programs test different claims; a structural check alone is not evidence of a successful statistical reproduction. Saved original test evidence is under [records/skill_tests](../records/skill_tests/) and [outputs/diagnostics](../outputs/diagnostics/).

| Programs | Purpose |
| --- | --- |
| skill1_specification/test_validator_cases.py | 12 meaningful specification cases, including wrong hypothesis direction, hierarchy and reliability inputs |
| skill2/data_checks.py | Independent raw counts and copied invalid-code rejection/recovery |
| skill2/glmm_reference.py, check_nested_logit.py | Independently integrated likelihoods and structural fixtures |
| skill2/check_glmm_full_likelihood.py | Independent saved-vector likelihood and gradient checks |
| skill2/check_glmm_fit_curvature.py | Observed-Hessian steps and covariance/score checks |
| repository/test_portable_execution.py | Runner transport, source restoration, notebook entry points and relocation checks |

After restoring archived case inputs, run skill-1 regression without replacing earlier evidence:

```powershell
python tests/skill1_specification/test_validator_cases.py --case-root records/skill_tests/specify-empirical-study/forward_case --output records/run_logs/skill1_new_regression.json
python tests/repository/test_portable_execution.py
```

`python analysis/run_replication.py --stage checks` reruns the numerical/data checks against restored inputs and saved fits and writes canonical diagnostic files. Use a separate project copy for an independent rerun if you need to retain the present artifacts byte-for-byte. The reorganization record distinguishes post-cleanup smoke tests from the original substantive verification.

## Skill 3 independent verification

`python tests/skill3/check_verification.py` independently reads raw inputs, fits
M1 with statsmodels, recalculates all 25 ordinal AMEs and 50 interval endpoints,
and exercises invalid-code, rounding and unavailable-target controls. It
supplements the saved skill 2 binary likelihood/curvature checks; M2/M3 were not
independently optimized in another engine. See the [test report](../records/skill_tests/verify-and-package/TEST_REPORT.md).
`python tools/verification_package_audit.py` checks preservation and the saved
clean-run, comparison, sensitivity, discovery, source and Word-review evidence.
It expects this completed local evidence package, not only a fresh code checkout.
