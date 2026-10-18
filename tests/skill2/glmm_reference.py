"""Independent nested Bernoulli likelihood fixtures; no study model is fitted.

Run from the repository root with the project Python. This deliberately uses
SciPy QUADPACK rather than the production engine or its fitted parameters.
"""
from __future__ import annotations

import hashlib
import json
import platform
import time
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from numpy.polynomial.hermite import hermgauss
from scipy.integrate import quad
from scipy.special import logsumexp, ndtr

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/diagnostics/glmm"
OUT.mkdir(parents=True, exist_ok=True)
SQRT2PI = np.sqrt(2.0 * np.pi)
QUAD_BOUND = 12.0
EPSABS = 2e-13
EPSREL = 2e-11


def phi(z):
    return np.exp(-0.5 * z * z) / SQRT2PI


def conditional_log_likelihood(eta, counts):
    """Counts are (n,s) for Bernoulli rows sharing an actor and eta.

    No binomial combinatorial coefficient: this is the original row likelihood.
    """
    counts = np.asarray(counts, dtype=float)
    n, s = counts[..., 0], counts[..., 1]
    return s * eta - n * np.logaddexp(0.0, eta)


def nested_quad(eta, item_variance, actor_variance, counts):
    counts = np.asarray(counts, dtype=int)
    sd_item, sd_actor = np.sqrt(item_variance), np.sqrt(actor_variance)
    maxima = np.zeros(len(counts))
    calls = 0

    def actor_value(z_item, index):
        nonlocal calls
        local_eta = eta + sd_item * z_item
        if actor_variance == 0:
            return float(np.exp(conditional_log_likelihood(local_eta, counts[index])))
        value, err = quad(
            lambda z_actor: float(phi(z_actor) * np.exp(conditional_log_likelihood(local_eta + sd_actor * z_actor, counts[index]))),
            -QUAD_BOUND, QUAD_BOUND, epsabs=EPSABS, epsrel=EPSREL, limit=250,
        )
        maxima[index] = max(maxima[index], err)
        calls += 1
        return value

    def integrand(z_item):
        return float(phi(z_item) * np.prod([actor_value(z_item, index) for index in range(len(counts))]))

    if item_variance == 0:
        value = float(np.prod([actor_value(0.0, index) for index in range(len(counts))]))
        outer_error = 0.0
    else:
        value, outer_error = quad(integrand, -QUAD_BOUND, QUAD_BOUND, epsabs=EPSABS, epsrel=EPSREL, limit=250)
    tail_bound = (len(counts) * (actor_variance > 0) + (item_variance > 0)) * 2 * ndtr(-QUAD_BOUND)
    # For factors in [0,1], the product's change is <= sum of factor changes.
    # QUADPACK's own errors are estimates; maximum is across sampled outer nodes.
    error_estimate = float(outer_error + maxima.sum() + tail_bound)
    return {
        "likelihood": value,
        "log_likelihood": float(np.log(value)),
        "quadpack_outer_absolute_error": float(outer_error),
        "max_sampled_actor_error_sum": float(maxima.sum()),
        "omitted_normal_tail_upper_bound": float(tail_bound),
        "absolute_error_estimate": error_estimate,
        "log_likelihood_error_estimate": error_estimate / value,
        "actor_integral_calls": calls,
    }


def one_dimension_quad(eta, variance, n, s):
    if variance == 0:
        return float(np.exp(conditional_log_likelihood(eta, (n, s))))
    return quad(lambda z: float(phi(z) * np.exp(conditional_log_likelihood(eta + np.sqrt(variance) * z, (n, s)))),
                -QUAD_BOUND, QUAD_BOUND, epsabs=EPSABS, epsrel=EPSREL, limit=250)[0]


def fixed_gh(eta, item_variance, actor_variance, counts, points):
    a, w = hermgauss(points)
    z, w = np.sqrt(2) * a, w / np.sqrt(np.pi)
    outer = []
    for zi in z:
        inner = [np.dot(w, np.exp(conditional_log_likelihood(eta + np.sqrt(item_variance) * zi + np.sqrt(actor_variance) * z, c))) for c in counts]
        outer.append(np.prod(inner))
    return float(np.dot(w, outer))


def joint_mvagh(eta, item_variance, actor_variance, counts, points=7, tolerance=1e-11, max_iterations=200):
    """Literal full-joint posterior-moment transformation for small synthetic q.

    This follows the public Stata16 formula, but its tolerance/iteration details
    are our explicit choices and are not asserted to be Stata internal defaults.
    """
    counts = np.asarray(counts, float)
    q = len(counts) + 1
    a, w = hermgauss(points)
    z, w = np.sqrt(2) * a, w / np.sqrt(np.pi)
    axes = np.meshgrid(*([np.arange(points)] * q), indexing="ij")
    idx = np.stack([x.ravel() for x in axes], axis=1)
    normal_nodes, log_w = z[idx], np.log(w[idx]).sum(axis=1)
    mu, covariance = np.zeros(q), np.eye(q)
    for iteration in range(max_iterations):
        chol = np.linalg.cholesky(covariance)
        v = mu + normal_nodes @ chol.T
        predictors = eta + np.sqrt(item_variance) * v[:, :1] + np.sqrt(actor_variance) * v[:, 1:]
        log_lik = conditional_log_likelihood(predictors, counts).sum(axis=1)
        # Prior / normal proposal ratio, with normalized standard-normal nodes.
        log_weighted = log_w + log_lik - 0.5 * (v * v).sum(axis=1) + 0.5 * (normal_nodes * normal_nodes).sum(axis=1) + np.log(np.diag(chol)).sum()
        log_value = logsumexp(log_weighted)
        posterior_weights = np.exp(log_weighted - log_value)
        new_mu = posterior_weights @ v
        centered = v - new_mu
        new_cov = (centered.T * posterior_weights) @ centered
        change = max(np.max(np.abs(new_mu - mu)), np.max(np.abs(new_cov - covariance)))
        if change < tolerance:
            return {"likelihood": float(np.exp(log_value)), "log_likelihood": float(log_value), "iterations": iteration + 1,
                    "posterior_mean": new_mu.tolist(), "posterior_covariance": new_cov.tolist(), "moment_change": float(change)}
        mu, covariance = new_mu, new_cov
    raise RuntimeError("Joint MVAGH moment iteration did not converge")


def main():
    started = time.perf_counter()
    fixtures = []
    synthetic = [
        ("synthetic_mixed", -0.7, 0.7, 1.3, [(3, 1), (2, 2)]),
        ("synthetic_rare", -2.0, 1.1, 0.6, [(4, 0), (3, 1)]),
        ("synthetic_large_variance", 0.8, 2.4, 3.1, [(2, 1), (3, 2)]),
        ("zero_both", -0.7, 0.0, 0.0, [(3, 1), (2, 2)]),
        ("zero_item", -0.7, 0.0, 1.3, [(3, 1), (2, 2)]),
        ("zero_actor", -0.7, 0.7, 0.0, [(3, 1), (2, 2)]),
        ("one_actor_variance_sum", 0.3, 0.7, 1.3, [(5, 2)]),
        ("one_row_symmetry", 0.0, 2.4, 3.1, [(1, 1)]),
    ]
    for name, eta, vi, va, counts in synthetic:
        result = {"fixture": name, "source": "synthetic", "eta": eta, "item_variance": vi, "actor_variance": va, "actor_counts_n_s": counts}
        result.update(nested_quad(eta, vi, va, counts))
        result["gh_81_likelihood"] = fixed_gh(eta, vi, va, counts, 81)
        result["gh_161_likelihood"] = fixed_gh(eta, vi, va, counts, 161)
        if name == "zero_both":
            result["analytic_likelihood"] = float(np.exp(3 * eta - 5 * np.logaddexp(0, eta)))
        elif name == "zero_item":
            result["reduced_likelihood"] = float(np.prod([one_dimension_quad(eta, va, n, s) for n, s in counts]))
        elif name in {"zero_actor", "one_actor_variance_sum"}:
            result["reduced_likelihood"] = one_dimension_quad(eta, vi + va, sum(c[0] for c in counts), sum(c[1] for c in counts))
        elif name == "one_row_symmetry":
            result["analytic_likelihood"] = 0.5
        if name in {"synthetic_mixed", "synthetic_rare", "synthetic_large_variance"}:
            result["joint_mvagh_7"] = joint_mvagh(eta, vi, va, counts)
        fixtures.append(result)

    raw_path = ROOT / "data/original/MedCon_Civility_actref.dta"
    data = pd.read_stata(raw_path, convert_categoricals=False)
    required = ["text_id", "akteur_id", "actrefoutbin", "actrefrecbin", "polsys", "socdiv", "mediatype"]
    data = data[required].dropna()
    sizes = data.groupby("text_id").agg(n_rows=("text_id", "size"), n_actors=("akteur_id", "nunique"))
    # Selection uses structure only, never estimated/published target values.
    ids = []
    for filt in [sizes.n_actors.eq(1) & sizes.n_rows.eq(1), sizes.n_actors.eq(2), sizes.n_rows.eq(sizes.n_rows.max()), sizes.n_actors.eq(sizes.n_actors.max())]:
        ids.append(sizes[filt].sort_index().index[0])
    ids = list(dict.fromkeys(ids))
    beta = np.array([-1.4, 0.2, -0.35, 0.45, -0.1, 0.3])
    for item in ids:
        rows = data[data.text_id.eq(item)]
        context = rows[["polsys", "socdiv", "mediatype"]].drop_duplicates()
        assert len(context) == 1, "Context predictors vary within selected item"
        raw_p, raw_s, raw_m = context.iloc[0]
        p, s, m = {1: 1, 2: 3, 3: 2}[raw_p], {1: 2, 2: 1}[raw_s], {1: 1, 2: 3, 3: 2}[raw_m]
        x = np.array([1, p == 2, p == 3, s == 2, m == 2, m == 3], float)
        eta = float(x @ beta)
        for outcome in ["actrefoutbin", "actrefrecbin"]:
            counts = [(len(gr), int(gr[outcome].sum())) for _, gr in rows.groupby("akteur_id", sort=True)]
            result = {"fixture": f"real_item_{item}_{outcome}", "source": "real_author_data_fixed_arbitrary_parameters",
                      "text_id": str(item), "outcome": outcome, "n_rows": len(rows), "n_actors": len(counts),
                      "context_raw": {"polsys": int(raw_p), "socdiv": int(raw_s), "mediatype": int(raw_m)},
                      "x": x.tolist(), "eta": eta, "item_variance": 0.7, "actor_variance": 1.3, "actor_counts_n_s": counts}
            result.update(nested_quad(eta, 0.7, 1.3, counts))
            result["gh_81_likelihood"] = fixed_gh(eta, 0.7, 1.3, counts, 81)
            result["gh_161_likelihood"] = fixed_gh(eta, 0.7, 1.3, counts, 161)
            fixtures.append(result)

    report = {"purpose": "Independent fixed-parameter integration checks; no model fitting and no published-value tuning",
              "source_file": str(raw_path.relative_to(ROOT)), "source_sha256": hashlib.sha256(raw_path.read_bytes()).hexdigest(),
              "software": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__, "pandas": pd.__version__},
              "parameters": {"beta": beta.tolist(), "beta_order": ["intercept", "polsys2", "polsys3", "socdiv2", "mediatype2", "mediatype3"],
                             "quad_bound_standard_deviations": QUAD_BOUND, "epsabs": EPSABS, "epsrel": EPSREL},
              "error_note": "QUADPACK errors are numerical estimates, not certified bounds. Inner error estimate is sum of maxima at sampled outer nodes. Normal truncation tail bound is rigorous because integrands are in [0,1]. GH81/GH161 supply an independent node-count check.",
              "fixtures": fixtures, "runtime_seconds": time.perf_counter() - started}
    (OUT / "reference_results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    table = []
    for f in fixtures:
        truth = f.get("analytic_likelihood", f.get("reduced_likelihood"))
        gh_difference = abs(f["gh_161_likelihood"] - f["likelihood"])
        assert gh_difference <= max(2e-12, f["likelihood"] * 2e-9), f["fixture"]
        if truth is not None:
            assert abs(f["likelihood"] - truth) < 2e-12, f["fixture"]
        table.append({"fixture": f["fixture"], "likelihood": f["likelihood"], "log_likelihood": f["log_likelihood"],
                      "estimated_absolute_error": f["absolute_error_estimate"], "gh161_minus_quad": f["gh_161_likelihood"] - f["likelihood"],
                      "known_answer_minus_quad": None if truth is None else truth - f["likelihood"]})
    pd.DataFrame(table).to_csv(OUT / "reference_results.csv", index=False)
    print(json.dumps({"fixtures": len(fixtures), "runtime_seconds": report["runtime_seconds"], "max_gh161_difference": max(abs(t["gh161_minus_quad"]) for t in table), "status": "all checks passed"}, indent=2))


if __name__ == "__main__":
    main()
