"""Compare the separately written candidate engine to independent fixtures."""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.integrate import quad
from scipy.special import expit
from statsmodels.tools.numdiff import approx_fprime

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/diagnostics/glmm"
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / "analysis"))
from nested_logit import NestedBernoulli
CANDIDATE_SHA256 = hashlib.sha256((ROOT / "analysis/nested_logit.py").read_bytes()).hexdigest()


def make_frame(fixture, item="fixture"):
    rows = []
    for a, (n, s) in enumerate(fixture["actor_counts_n_s"]):
        for row in range(n):
            rows.append({"text_id": item, "akteur_id": str(a), "y": int(row < s),
                         "polsys": 1, "socdiv": 1, "mediatype": 1})
    return pd.DataFrame(rows)


def main():
    reference = json.loads((OUT / "reference_results.json").read_text(encoding="utf-8"))
    comparisons = []
    for fixture in reference["fixtures"]:
        frame = make_frame(fixture)
        theta = np.array([fixture["eta"], 0, 0, 0, 0, 0,
                          .5 * np.log(max(fixture["item_variance"], 1e-24)),
                          .5 * np.log(max(fixture["actor_variance"], 1e-24))])
        result = {"fixture": fixture["fixture"], "reference_log_likelihood": fixture["log_likelihood"],
                  "reference_absolute_error_estimate": fixture["absolute_error_estimate"], "approximations": []}
        for points in (7, 11, 21):
            candidate = NestedBernoulli(frame, "y", points=points)
            ll, score = candidate.evaluate(theta, score=True)
            # One mixed fixture checks the score/derivative distinction. Repeating
            # the full numerical Jacobian for every integration fixture adds no
            # independent coverage and becomes costly with damped adaptation.
            exact_derivative_of_approximation = (approx_fprime(theta, candidate.evaluate, epsilon=2e-5, centered=True)
                                                if fixture["fixture"] == "synthetic_mixed" else None)
            detail = {"points": points, "candidate_log_likelihood": ll, "difference_from_reference": ll - fixture["log_likelihood"],
                      "integrated_score": score.tolist(), "finite_difference_score": None if exact_derivative_of_approximation is None else exact_derivative_of_approximation.tolist(),
                      "max_integrated_vs_finite_difference_score": None if exact_derivative_of_approximation is None else float(np.max(np.abs(score - exact_derivative_of_approximation))),
                      "adaptation": candidate.last_diagnostic}
            result["approximations"].append(detail)
            if points == 21:
                assert abs(ll-fixture["log_likelihood"]) < 1e-8, fixture["fixture"]
        if "joint_mvagh_7" in fixture:
            result["joint_mvagh_7_log_likelihood"] = fixture["joint_mvagh_7"]["log_likelihood"]
            result["recursive_7_minus_full_joint_7"] = result["approximations"][0]["candidate_log_likelihood"] - fixture["joint_mvagh_7"]["log_likelihood"]
        comparisons.append(result)
        print("checked", fixture["fixture"], flush=True)
    # Frequency compression and ordering must preserve the exact evaluated target.
    selected = reference["fixtures"][0]
    repeated = pd.concat([make_frame(selected, item=f"copy_{i}") for i in range(4)], ignore_index=True)
    theta = np.r_[selected["eta"], np.zeros(5), .5*np.log(selected["item_variance"]), .5*np.log(selected["actor_variance"])]
    compressed = NestedBernoulli(repeated, "y", compress=True).evaluate(theta)
    uncompressed = NestedBernoulli(repeated, "y", compress=False).evaluate(theta)
    shuffled = NestedBernoulli(repeated.sample(frac=1, random_state=17), "y", compress=True).evaluate(theta)
    assert max(abs(compressed-uncompressed), abs(shuffled-compressed)) < 1e-12

    # The random-effect marginal convention is a prior logistic-normal mean.
    # Algebraic 1D reduction and tensor7 share an integral, but not identical nodes.
    z, w = np.polynomial.hermite_e.hermegauss(7)
    w = w / np.sqrt(2*np.pi)
    eta, vi, va = -1.4, .7, 1.3
    exact_margin, margin_error = quad(lambda q: float(expit(eta+np.sqrt(vi+va)*q)*np.exp(-q*q/2)/np.sqrt(2*np.pi)), -12, 12, epsabs=2e-13, epsrel=2e-11)
    one7 = float(w @ expit(eta + np.sqrt(vi+va)*z))
    tensor7 = float(np.sum(w[:, None] * w[None, :] * expit(eta + np.sqrt(vi)*z[:, None] + np.sqrt(va)*z[None, :])))
    report = {"status": "all_fixture_accuracy_and_invariance_assertions_passed", "candidate_path": "analysis/nested_logit.py", "candidate_sha256": CANDIDATE_SHA256,
              "reference_path": "outputs/diagnostics/glmm/reference_results.json",
              "comparisons": comparisons, "frequency_compression": {"compressed": compressed, "uncompressed": uncompressed, "shuffled": shuffled, "passed": True},
              "prediction_quadrature_caution": {"eta": eta, "item_variance": vi, "actor_variance": va, "quad_mean": exact_margin,
                  "quad_absolute_error_estimate": margin_error, "combined_variance_1d_gh7": one7, "separate_intercepts_tensor_gh7": tensor7,
                  "tensor7_minus_quad": tensor7-exact_margin, "combined1d7_minus_quad": one7-exact_margin,
                  "note": "The exact Gaussian-sum reduction is valid; neither finite GH7 grid is established as the original Stata internal marginal-prediction grid."}}
    (OUT / "candidate_comparison.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    pd.DataFrame([{ "fixture": r["fixture"], "points": a["points"], "log_likelihood": a["candidate_log_likelihood"],
                    "difference_from_quad": a["difference_from_reference"], "score_derivative_difference": a["max_integrated_vs_finite_difference_score"]}
                  for r in comparisons for a in r["approximations"]]).to_csv(OUT / "candidate_comparison.csv", index=False)
    print(json.dumps({"fixtures": len(comparisons), "max_absolute_log_likelihood_error_by_points":
        {p:max(abs(r["approximations"][i]["difference_from_reference"]) for r in comparisons) for i,p in enumerate((7,11,21))},
        "joint_versus_recursive_7": {r["fixture"]:r["recursive_7_minus_full_joint_7"] for r in comparisons if "recursive_7_minus_full_joint_7" in r},
        "prediction_quadrature": report["prediction_quadrature_caution"]}, indent=2))


if __name__ == "__main__":
    main()
