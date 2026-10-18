# Setup and rerun on another computer

1. Clone the private repository with an authorized GitHub account and open its root folder in the agent. Start with [the skill guide](../skills/README.md). Do not open only the parent folder or copy only the skill entry files.
2. Install Python 3.12 and create an environment. These Windows commands assume the Python launcher is installed:

```powershell
py -3.12 -m venv .venv
.venv/Scripts/python.exe -m pip install --index-url https://pypi.org/simple -r requirements-lock.txt
.venv/Scripts/python.exe -m pip check
.venv/Scripts/Activate.ps1
```

If activation is unavailable, replace `python` below with `.venv/Scripts/python.exe`. The lock records the tested Windows environment. Other operating systems need a separately resolved environment and renewed checks. [environment.md](../../environment.md) describes the original machine. RTK is optional.

3. Obtain lawful copies of the assignment and article; place them at `sources/local/COMD7290_assignment.pdf` and `sources/local/Lob_et_al_2024.pdf`. File names alone do not establish the expected version. The manifests give exact hashes. If your copy differs, record and investigate that difference rather than disabling hash checks.
4. Restore registered author datasets, independent ratings, codebooks and archived method sources:

```powershell
python tools/restore_inputs.py --download --report records/run_logs/input_restoration.json
python tools/restore_inputs.py
python tools/check_repository.py
```

The first command requests network downloads only from the manifest's direct URLs and extracts named ZIP members. Existing files are never overwritten. Downloads must match saved SHA-256 values before being written. A changed/unavailable upstream version causes a recorded failure; obtain the registered version lawfully and keep the mismatch visible. The page snapshot may change over time and may need to be supplied from a lawful archived copy. The original student's computer already has these sources. Repository code and aggregate results can be inspected without them; source-dependent validation and refitting require them.

5. Run selected stages or all stages from the repository root:

```powershell
python analysis/run_replication.py --stage data
python analysis/run_replication.py --stage reliability
python analysis/run_replication.py --stage ordinal
python analysis/run_replication.py --stage binary
python analysis/run_replication.py --stage summaries
python analysis/run_replication.py --stage checks
```

`python analysis/run_replication.py` runs all stages in that order. Full nested-model fits can take substantial time. Preserve a copy of the repository/results before a new independent run because canonical output names are reused; dated wrapper logs are created for each run. No Stata executable is used. Do not accept a failed convergence/identification diagnostic as a successful fit.

6. For notebooks, install/register the project kernel and launch from this environment:

```powershell
python -m ipykernel install --sys-prefix --name comd7290-python --display-name "Python (COMD7290 - Ma Jiayi)"
python -m notebook
```

On Windows the root `Start_Jupyter_Notebook.cmd` is an alternative. Open [01_replication.ipynb](../../analysis/01_replication.ipynb); it calls the same modules. The environment notebook uses synthetic data. Neither notebook's mere presence is evidence of a completed research run.

7. Read [replication results](../replication_results.md), [comparison.csv](../../outputs/comparison.csv), [hypothesis_tests.csv](../../outputs/reproduced/hypothesis_tests.csv), and [diagnostics](../../outputs/diagnostics/README.md). Historical finite-grid/build identity remains unresolved even where printed values agree.

To reconstruct the archived skill-1 test inputs after restoring canonical sources, use `python tools/prepare_specification_test.py --case-root records/skill_tests/specify-empirical-study/forward_case`. Then use the regression command in [tests/README.md](../../tests/README.md). New test results belong in new dated paths, not over the historical receipts.
