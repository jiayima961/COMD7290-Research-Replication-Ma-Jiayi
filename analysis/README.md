# Analysis entry points

Read [the execution specification](../docs/execution_specification.md), [results explanation](../docs/replication_results.md) and [setup/input instructions](../docs/guides/teacher_quickstart.md).

Run from the repository root with the project Python environment:

```powershell
python analysis/run_replication.py
python analysis/run_replication.py --stage data
```

RTK is optional. The same stages are available in [01_replication.ipynb](01_replication.ipynb). The runner logs commands and stops on failure. A full run replaces canonical numerical outputs; copy the existing result set before an independent rerun. Binary fitting can take substantial time.

| Stage | Programs | Saved outputs |
| --- | --- | --- |
| data | prepare_replication.py | Local data/prepared; outputs/diagnostics/data_audit.json |
| reliability | reliability_reproduction.py | outputs/reproduced/reliability; outputs/diagnostics/reliability |
| ordinal | ordinal_reproduction.py | Descriptives; models/ordinal; predictions/ordinal; diagnostics/ordinal |
| binary | run_binary_models.py, nested_logit.py | M2/M3 full/null fits, coefficients and covariance |
| summaries | binary_predictions.py, compare_replication.py | Binary margins/AMEs; comparison.csv; hypothesis_tests.csv |
| checks | tests/skill2 programs | Independent data/likelihood/curvature diagnostics |

[00_environment_check.ipynb](00_environment_check.ipynb) is a synthetic environment check. [01_replication.ipynb](01_replication.ipynb) is an unexecuted interface to the real saved modules; actual study execution evidence is in [records/run_logs/skill2](../records/run_logs/skill2/). These distinctions must survive reuse.

The statistical model modules and saved numerical results were preserved during the directory cleanup. Historical finite-grid and package-build identity remains limited; see the execution specification rather than interpreting code portability as exact original executable parity.

## Full verified reproduction

`python analysis/run_verified_replication.py` runs the unchanged research pipeline,
then the [complete reconciler](verify_and_package.py), the independent skill 3
checks and the [separate country sensitivity](skill3_sensitivity.py). Use a copy
to preserve existing outputs. Actual source/input-only clean runs are recorded in
[skill 3 logs](../records/run_logs/skill3/); the existing environment is reused.
For completed fits, the three verification stages can be run separately without
repeating the expensive binary fitting. The [report index](../report/verification/README.md)
explains agreements, discrepancies, unavailable targets and remaining limits.
