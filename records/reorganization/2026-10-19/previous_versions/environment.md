# Software and execution environment

## Scope

The user authorized a project-local Python/Jupyter installation on 2026-10-18 (D007). This provides a foundation for notebooks, data preparation and supported analyses. Equivalence to the complete original Stata workflow remains unverified. No original study models have been fitted.

## Python environment

- Windows, 64-bit CPython 3.12.14.
- Isolated environment: `.venv/` in the project root; excluded from Git.
- The available Codex bundled Python was used to create the environment. The `py` launcher reported no separately registered Python installation, and the `python` PATH entry was a Windows Store alias.
- The environment depends on its base Python installation. If that installation is removed or the project is moved, recreate `.venv` with an installed Python 3.12 interpreter and the dependency files; do not copy the environment directory.
- Source for installed packages: official PyPI, using binary wheels. Direct tested versions are in `requirements.txt`; the resolved Windows/Python 3.12 environment is in `requirements-lock.txt`.
- Text files use UTF-8; project CSV files use UTF-8 with a BOM for spreadsheet compatibility.

| Purpose | Direct packages |
| --- | --- |
| Tables and numerical calculations | `numpy`, `pandas`, `scipy` |
| Statistical models and categorical design matrices | `statsmodels`, `patsy` |
| Stata and Excel file access | `pyreadstat`, `openpyxl` |
| Charts | `matplotlib`, `seaborn` |
| Krippendorff alpha | `krippendorff` |
| Notebook interfaces and Python kernel | `notebook`, `jupyterlab`, `ipykernel` |
| Notebook validation and fresh-kernel execution | `nbformat`, `nbclient` |

Installing a package does not establish the correct model specification or statistical equivalence. In particular, this package set does not provide a verified direct replacement for the author's three-level `melogit` fits or complete `kappaetc` output. See [Python route assessment](docs/python_route_assessment.md).

## Open Jupyter Notebook

1. Double-click `Start_Jupyter_Notebook.cmd` in the project folder. RTK must be available on PATH; it was resolved locally as `E:\RTK\bin\rtk.exe`.
2. Leave its console window open while using Jupyter in the browser.
3. Open `analysis/00_environment_check.ipynb` and select **Python (COMD7290 - Ma Jiayi)**.
4. Use **Run > Run All Cells**. A `passed` status checks the foundation on synthetic data; it is not a reproduction result.
5. To stop the server, return to its console, press Ctrl+C and confirm shutdown if prompted.

The launcher binds to `127.0.0.1`, retains Jupyter's default authentication, and uses project-local temporary configuration, runtime and plotting directories. The registered kernel is local to `.venv`; it is discovered by Jupyter launched from this environment. A separately installed Jupyter application may need a separate kernel registration.

## Environment verification and records

The environment notebook completed successfully in a fresh project Python kernel on 2026-10-18. It checks imports of all 15 direct dependencies, synthetic Excel/Stata round trips and value-label metadata, a categorical design matrix, nominal Krippendorff alpha with a known answer, convergence and valid probabilities for a synthetic five-category ordered-logit model, and PNG rendering. It never reads original research data.

- Machine-readable result and installed versions: `records/run_logs/python_environment_check.json`.
- Setup commands, observed failures and verification status: `records/run_logs/python_environment_setup.md`.
- The executed environment notebook retains its synthetic check output.

The initial sandboxed notebook execution stalled and was stopped. The same notebook passed after permission-approved execution outside the sandbox, allowing communication with the local kernel. The package installation and checks did not require disabling Jupyter authentication or changing system Python packages.

To run the same foundation checks directly from the project root:

```powershell
rtk proxy .\.venv\Scripts\python.exe tools/check_python_environment.py
```

For repository structure, registered source hashes and placeholder integrity:

```powershell
rtk proxy .\.venv\Scripts\python.exe tools/check_repository.py
```

Neither command is the full research-analysis entry point, and neither demonstrates successful invocation of all three project skills.

## Recreate dependencies

On another Windows machine with Python 3.12 already installed, create `.venv` from that interpreter. For example, if it is registered with the Windows Python launcher:

```powershell
rtk proxy py -3.12 -m venv .venv
rtk proxy .\.venv\Scripts\python.exe -m pip install --index-url https://pypi.org/simple -r requirements-lock.txt
rtk proxy .\.venv\Scripts\python.exe -m ipykernel install --sys-prefix --name comd7290-python --display-name "Python (COMD7290 - Ma Jiayi)"
rtk proxy .\.venv\Scripts\python.exe -m pip check
```

The lock file includes Windows dependencies. A different operating system requires its own resolved environment and renewed checks.

## Original Stata requirements and unresolved settings

The inspected author script `MedCon_Civility_an.do`, dated 2021-04-24, specifies `version 16` and lists `blindschemes`, `gologit2`, `omodel`, and `grc1leg2`. Its multilevel models use `intpoints(7)`. The package readme is dated 2021-04-20. These are source-code requirements, not evidence of a local Stata installation or an executed original fit.

The reliability script, dated 2020-11-01, also specifies Stata 16 and requires `kappaetc`. Its imported filenames differ from the website download names. Preserve the originals and record path mappings in a project execution copy. Its identity weights and conditional standard errors need to be matched rather than silently replaced with other conventions. Neither original script has been run.

Before substantive fitting, record the approved specification, engine and package versions, commands, input versions, missing-data rules, estimator and integration settings, convergence criteria, confidence intervals, runtime and log locations. Check how probabilities and marginal effects handle random effects. The full statistical rerun command and software-equivalence demonstration are pending.
