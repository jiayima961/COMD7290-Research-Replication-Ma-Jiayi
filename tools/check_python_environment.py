"""Check the Python foundation on synthetic data only; never fit study models."""
from datetime import datetime, timezone
from importlib import import_module, metadata
from io import BytesIO
from pathlib import Path
import json
import os
import platform
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = {
    "numpy": "numpy", "pandas": "pandas", "scipy": "scipy",
    "statsmodels": "statsmodels", "patsy": "patsy", "pyreadstat": "pyreadstat",
    "openpyxl": "openpyxl", "matplotlib": "matplotlib", "seaborn": "seaborn",
    "krippendorff": "krippendorff", "jupyterlab": "jupyterlab", "notebook": "notebook",
    "ipykernel": "ipykernel", "nbformat": "nbformat", "nbclient": "nbclient",
}


def run_checks():
    scratch = ROOT / "tmp" / "python-check"
    scratch.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(scratch / "matplotlib"))
    import matplotlib
    matplotlib.use("Agg")
    for module in PACKAGES.values():
        import_module(module)

    import numpy as np
    import pandas as pd
    import pyreadstat
    import krippendorff
    import matplotlib.pyplot as plt
    import seaborn as sns
    from patsy import dmatrix
    from scipy.special import expit
    from statsmodels.miscmodels.ordinal_model import OrderedModel

    checks = []
    if Path(sys.prefix).resolve() != (ROOT / ".venv").resolve():
        raise RuntimeError("Select the project .venv kernel before running this check.")
    checks.append("Project virtual environment and all direct imports")

    synthetic = pd.DataFrame({"id": [1, 2, 3], "group": [0, 1, 0], "score": [1.5, 2.5, 3.5]})
    with tempfile.TemporaryDirectory(dir=scratch) as folder:
        folder = Path(folder)
        xlsx = folder / "synthetic.xlsx"
        synthetic.to_excel(xlsx, index=False, engine="openpyxl")
        pd.testing.assert_frame_equal(synthetic, pd.read_excel(xlsx, engine="openpyxl"))
        dta = folder / "synthetic.dta"
        pyreadstat.write_dta(synthetic, str(dta), variable_value_labels={"group": {0: "A", 1: "B"}})
        restored, labels = pyreadstat.read_dta(str(dta), apply_value_formats=False, user_missing=True)
        np.testing.assert_allclose(restored.to_numpy(), synthetic.to_numpy())
        if labels.variable_value_labels["group"] != {0: "A", 1: "B"}:
            raise AssertionError("Stata value-label metadata was not preserved.")
    checks.append("Synthetic Excel and Stata round trips, including Stata value labels")

    design = dmatrix("1 + C(group)", synthetic, return_type="dataframe")
    if design.shape != (3, 2) or not np.allclose(expit([0]), [0.5]):
        raise AssertionError("Formula or numerical foundation failed.")
    checks.append("Categorical design matrix and logistic numerical function")

    # Known perfect agreement with variation between units; not an author estimate.
    ratings = np.array([[0, 1, 0, 1], [0, 1, 0, 1]], dtype=float)
    if not np.isclose(krippendorff.alpha(ratings, level_of_measurement="nominal"), 1.0):
        raise AssertionError("Known-answer nominal reliability check failed.")
    checks.append("Known-answer nominal Krippendorff alpha on synthetic ratings")

    rng = np.random.default_rng(7290)
    x = rng.normal(size=600)
    latent = 0.7 * x + rng.logistic(size=x.size)
    outcome = np.digitize(latent, [-1.2, -0.3, 0.6, 1.5])
    model = OrderedModel(outcome, pd.DataFrame({"x": x}), distr="logit")
    fitted = model.fit(method="bfgs", maxiter=200, disp=False)
    prediction = np.asarray(fitted.model.predict(fitted.params))
    if not fitted.mle_retvals["converged"] or not np.isfinite(fitted.params).all():
        raise AssertionError("Synthetic ordered-logit model did not converge.")
    if prediction.shape != (600, 5) or not np.allclose(prediction.sum(axis=1), 1):
        raise AssertionError("Synthetic ordinal probabilities failed.")
    checks.append("Synthetic five-category ordered logit: convergence and valid probabilities")

    figure, axis = plt.subplots()
    sns.barplot(data=synthetic, x="group", y="score", errorbar=None, ax=axis)
    buffer = BytesIO()
    figure.savefig(buffer, format="png")
    plt.close(figure)
    if not buffer.getvalue().startswith(b"\x89PNG\r\n\x1a\n"):
        raise AssertionError("PNG generation failed.")
    checks.append("Matplotlib and seaborn render a synthetic plot")

    result = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(), "platform": platform.system(),
        "in_project_venv": True,
        "packages": {name: metadata.version(name) for name in PACKAGES},
        "checks_passed": checks, "status": "passed",
        "study_models_fitted": False,
        "stata_equivalence_verified": False,
        "remaining": ["Three-level frequentist binary GLMM and integration/prediction settings",
                      "Proportional-odds diagnostics and complete kappaetc-equivalent reliability output"],
    }
    report = ROOT / "records" / "run_logs" / "python_environment_check.json"
    report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(run_checks(), indent=2))
