# Python/Jupyter environment setup

Date: 2026-10-18. Authorization: the user explicitly requested package installation; see D007. All steps concerned software preparation and synthetic checks. No original study model was fitted.

## Environment and installation scope

- Base: Codex bundled CPython 3.12.14, Windows 64-bit.
- Installation target: project `.venv/`, excluded from Git.
- Package index: <https://pypi.org/simple>, with binary wheels only.
- Fifteen direct dependencies were resolved with their transitive dependencies. Exact versions are in `requirements.txt` and `requirements-lock.txt`.
- The project kernel `comd7290-python`, displayed as `Python (COMD7290 - Ma Jiayi)`, is registered under `.venv/share/jupyter/kernels/`. It was not registered system-wide.
- Installation working files and the full pip download report/log are local-only under `tmp/python-install/`.

The actual setup was driven by temporary Python wrappers in the workspace's outer `tmp/` directory: `prepare_python_environment.py`, `install_python_packages.py`, and `finish_python_setup.py`. They set writable project-local temporary paths, invoke the interpreter directly, retain the pip report, and execute the notebook using `nbclient`. The final wrapper was invoked with the project `.venv` interpreter.

The principal installation operations, expressed as reproducible RTK commands from the project root, are:

```powershell
rtk proxy <base-Python-3.12-executable> -m venv .venv
rtk proxy .\.venv\Scripts\python.exe -m pip install --index-url https://pypi.org/simple --only-binary=:all: -r requirements.txt
rtk proxy .\.venv\Scripts\python.exe -m ipykernel install --sys-prefix --name comd7290-python --display-name "Python (COMD7290 - Ma Jiayi)"
rtk proxy .\.venv\Scripts\python.exe -m pip check
```

Use a real Python 3.12 interpreter in place of the angle-bracket placeholder. On this computer the base interpreter was `C:\Users\86150\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`. For rebuilding the resolved Windows environment, use `requirements-lock.txt` instead of the direct-only file.

## Observed failures and resolutions

1. The Windows `py -0p` probe reported no registered Python installation; the Python PATH entries were Windows Store aliases. Used the already available bundled Python rather than treating an alias as an installed interpreter.
2. The first `venv` bootstrap failed while `ensurepip` wrote to the sandbox's default temporary directory. Repeated the bootstrap with `TEMP` and `TMP` set to a writable directory inside project `tmp/`; it succeeded.
3. The sandboxed pip attempt could not connect to the configured proxy (`WinError 10013`). Repeated the same scoped PyPI installation with permission-approved execution outside the sandbox; it exited successfully. Package targets remained in `.venv`.
4. The first fresh-kernel notebook execution stalled inside the sandbox. Inspected and stopped only the exact setup helper and its own children. The same synthetic notebook then completed with permission-approved execution outside the sandbox. The successful run used a 30-second kernel-start timeout and a 120-second cell timeout. It emitted Windows event-loop fallback and local kernel-transport warnings; neither prevented execution.

No package-resolution conflict or analysis-test failure was observed. No Jupyter authentication settings were disabled to make the tests pass.

## Observed verification

- `pip check`: `No broken requirements found.`
- `rtk proxy cmd /d /c Start_Jupyter_Notebook.cmd --version`: exit 0; `7.6.3`.
- `analysis/00_environment_check.ipynb`: validated with `nbformat`, executed from a fresh `comd7290-python` kernel with `nbclient`, and saved with executed output. All code cells completed without error outputs.
- Fifteen direct package imports passed.
- Synthetic Excel/Stata data round trips and Stata value-label metadata passed.
- Synthetic categorical design matrix and numerical logistic function passed.
- A nominal Krippendorff alpha example with known perfect agreement returned the expected answer.
- A five-category ordered-logit model on 600 synthetic observations converged, with finite estimates and predicted category probabilities summing to one. Its fixed seed was 7290; these are not published or reproduced study estimates.
- Matplotlib/seaborn produced a valid PNG using synthetic values.
- `rtk proxy .\.venv\Scripts\python.exe tools/check_repository.py`: material checks passed, including registered original-source hashes and empty unreproduced-result placeholders.

Machine-readable evidence, including actual package versions and the successful check timestamp, is in `records/run_logs/python_environment_check.json`.

## Limits and next work

This is a working Python/Jupyter foundation, not evidence of complete Stata equivalence or successful invocation of the three project skills. Check the original three-level frequentist models, seven-point integration, proportional-odds tests, full reliability output, sample/coder matching, probability summaries and marginal effects before substantive estimation. The student still needs to review the detailed specification.
