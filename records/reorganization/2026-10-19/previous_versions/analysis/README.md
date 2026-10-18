# Python analysis entry points

Read [the results index](../docs/replication_results.md) and [execution specification](../docs/execution_specification.md).

Run all stages from the repository root:

```powershell
rtk proxy .venv/Scripts/python.exe -X utf8 analysis/run_replication.py
```

The same stages are available in `01_replication.ipynb`: data, reliability, ordinal, binary, summaries and checks. Use `--stage NAME` for one stage. Binary fitting can take substantial time. The runner saves command logs and stops on failure; diagnostics must still be inspected.

- prepare_replication.py: hash/domain/nesting checks and original-code recodes.
- reliability_reproduction.py: original selected independent-rating matrices, agreement coefficients and conditional uncertainty.
- ordinal_reproduction.py: descriptive tables, cumulative models, original diagnostics and predictions.
- nested_logit.py / run_binary_models.py: frequentist three-level Bernoulli models and their nulls with seven-point recursive adaptive integration.
- binary_predictions.py: prior-marginal probabilities and discrete AMEs with full-covariance delta uncertainty.
- compare_replication.py: comparison to separately stored published targets and 12 hypothesis targets.

The finite historical integration grid/build is not completely recovered. These limitations are recorded beside results rather than hidden by changing the model. The notebook is a runnable interface; execution evidence resides in records/run_logs/skill2.
