# Software and execution environment

The user authorized a project-local Python/Jupyter environment and faithful
Python reproduction. Real analyses were completed on 2026-10-18. See
[replication results](docs/replication_results.md), [execution specification](docs/execution_specification.md)
and [teacher setup](docs/guides/teacher_quickstart.md).

- Tested system: Windows, 64-bit CPython 3.12.14.
- Project environment: `.venv/`, excluded from Git; recreate it on another machine.
- Direct packages: [requirements.txt](requirements.txt); full tested Windows lock:
  [requirements-lock.txt](requirements-lock.txt). Original installation used official PyPI.
- Text: UTF-8; existing CSVs may use a UTF-8 BOM for spreadsheet compatibility.
- RTK is optional. Standard Python runs the wrappers and notebooks. When found
  on PATH, the command logger uses RTK and records that actual command.

The direct package set provides NumPy/Pandas/SciPy, statsmodels/patsy,
pyreadstat/openpyxl, matplotlib/seaborn, krippendorff and Jupyter tools.
The three-level frequentist binary estimator is implemented in
[analysis/nested_logit.py](analysis/nested_logit.py); package installation alone
does not provide or validate that estimator.

For another Windows computer, follow the complete environment/input instructions
in [teacher_quickstart.md](docs/guides/teacher_quickstart.md). Run with the new
environment's Python. Do not copy this machine's `.venv`; it depends on the base
interpreter. The lock file includes Windows dependencies. Other systems require
their own environment resolution and renewed checks.

Open Jupyter with `Start_Jupyter_Notebook.cmd`, or `python -m notebook` from
the activated environment. The launcher binds to 127.0.0.1 and retains default
authentication. It keeps runtime/configuration caches in the project's `tmp/`.
The synthetic [environment notebook](analysis/00_environment_check.ipynb)
completed in a fresh kernel; the [replication notebook](analysis/01_replication.ipynb)
is an unexecuted interface to the saved statistical modules. Real research
execution evidence is in [records/run_logs/skill2](records/run_logs/skill2/).

The author analysis script specifies Stata 16 compatibility mode and seven
integration points. No Stata program was executed. Python implements the original
statistical likelihood and specified settings with independently checked numerical
calculations. Historical finite adaptive-grid details, original package builds,
and invalid generalized-ordinal diagnostics remain explicitly limited. Read the
execution specification before making an exact software-equivalence claim.

The [early Python route assessment](docs/guides/python_route_assessment.md) and
[original setup record](records/run_logs/python_environment_setup.md) are retained
as dated historical context. The [2026-10-19 checks](records/reorganization/2026-10-19/README.md)
cover relocation and portable execution, not another full research-model refit.
