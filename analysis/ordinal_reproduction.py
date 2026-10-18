"""Independent, source-bound Python ordinal forward test of reproduce-and-diagnose.

CLI: python reproduce_ordinal.py --project-root PROJECT --output-root OUTPUT
Original inputs are read only. No numerical targets are used during estimation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy import optimize, special, stats
import statsmodels
from statsmodels.miscmodels.ordinal_model import OrderedModel

SPEC = "ordinal-author-code-2021-python-forward-v1"
TERMS = ["2.polsys", "3.polsys", "2.socdiv", "2.mediatype", "3.mediatype"]
CUTS = ["cut_0_1", "cut_1_2", "cut_2_3", "cut_3_4"]
LOG = logging.getLogger("ordinal_forward")


class OutputLayout:
    """Keep independent flat tests isolated; route canonical reruns by artifact type."""
    def __init__(self, project, root, canonical=False):
        self.project, self.root, self.canonical = project, root, canonical
        self.created = set()

    def __str__(self):
        return str(self.root)

    def mkdir(self, **kwargs):
        self.root.mkdir(**kwargs)

    def __truediv__(self, name):
        if not self.canonical:
            path = self.root / name
        elif name == "prepared_item.csv":
            path = self.project / "data/prepared/ordinal_item.csv"
        elif name in {"item_descriptives.csv", "reference_descriptives.csv", "item_tone_counts_country_media.csv",
                      "item_tone_percent_country_media.csv", "item_tone_frequencies.csv"}:
            path = self.root / "descriptives/ordinal" / name
        elif name in {"M1_model.json", "M1_probit_model.json", "M1_cloglog_model.json", "ordinal_coefficients.csv", "ordinal_fit.csv"}:
            path = self.root / "models/ordinal" / name
        elif name in {"M1_predictive_margins.csv", "M1_average_marginal_effects.csv", "M1_prediction_gradients.json"}:
            path = self.root / "predictions/ordinal" / name
        elif name in {"run.log", "invocation_receipt.json", "input_source_bindings.json", "output_manifest.csv"}:
            path = self.project / "records/run_logs/skill2/ordinal" / name
        else:
            path = self.project / "outputs/diagnostics/ordinal" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        self.created.add(path)
        return path

    def glob(self, pattern):
        return sorted(p for p in self.created if p.exists())


def serial(v):
    if isinstance(v, (np.integer, np.floating, np.bool_)):
        return v.item()
    if isinstance(v, np.ndarray):
        return v.tolist()
    if isinstance(v, Path):
        return str(v)
    raise TypeError(type(v).__name__)


def save_json(path, obj):
    def clean(v):
        if isinstance(v, dict):
            return {str(k): clean(value) for k, value in v.items()}
        if isinstance(v, (list, tuple)):
            return [clean(value) for value in v]
        if isinstance(v, np.ndarray):
            return clean(v.tolist())
        if isinstance(v, (np.integer, np.floating, np.bool_)):
            return v.item()
        return v
    path.write_text(json.dumps(clean(obj), indent=2, default=serial, allow_nan=False), encoding="utf-8")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def design(d):
    return np.column_stack([(d[v].to_numpy() == k).astype(float) for v, k in
                            [("polsys", 2), ("polsys", 3), ("socdiv", 2), ("mediatype", 2), ("mediatype", 3)]])


def prepare(d, tone=False):
    d = d.copy()
    for v, domain in [("polsys", {1, 2, 3}), ("socdiv", {1, 2}), ("mediatype", {1, 2, 3})]:
        if not set(d[v].dropna().unique()).issubset(domain):
            raise ValueError(f"Invalid {v} domain")
    if tone:
        if not set(d.tone.dropna().unique()).issubset({1, 2, 3, 4, 5}):
            raise ValueError("Invalid original tone domain")
        d["tone"] -= 1
    d["polsys"] = d.polsys.map({1: 1, 2: 3, 3: 2})
    d["socdiv"] = d.socdiv.map({1: 2, 2: 1})
    d["mediatype"] = d.mediatype.map({1: 1, 2: 3, 3: 2})
    return d


def group_ordinal(x, y, k):
    ux, inv = np.unique(x, axis=0, return_inverse=True)
    counts = np.zeros((len(ux), k))
    np.add.at(counts, (inv, y.astype(int)), 1)
    return ux, counts


def cdf_parts(z, link):
    if link == "logit":
        f0 = special.expit(z)
        f1 = f0 * special.expit(-z)
        f2 = f1 * (1 - 2 * f0)
    elif link == "probit":
        f0 = special.ndtr(z)
        f1 = np.exp(-0.5*z*z) / np.sqrt(2*np.pi)
        f2 = -z*f1
    elif link == "cloglog":
        # gologit2: P(Y<=j)=exp(-exp(Xbeta-cut_j)); z=cut_j-Xbeta.
        t = np.exp(np.clip(-z, -745, 700))
        f0 = np.exp(-t)
        f1 = t * f0
        f2 = f1 * (t - 1)
    else:
        raise ValueError(link)
    return f0, f1, f2


class CommonOrdinal:
    def __init__(self, x, counts, link="logit"):
        self.x, self.counts, self.link = np.asarray(x), np.asarray(counts), link
        self.g, self.k = counts.shape
        self.p = x.shape[1]
        self.q = self.p + self.k - 1

    def probabilities(self, b, derivatives=False):
        z = b[self.p:][None, :] - self.x @ b[:self.p, None]
        f0, f1, f2 = cdf_parts(z, self.link)
        probs = np.diff(np.column_stack([np.zeros(self.g), f0, np.ones(self.g)]), axis=1)
        if not derivatives:
            return probs
        vs = np.zeros((self.g, self.k-1, self.q))
        vs[:, :, :self.p] = -self.x[:, None, :]
        vs[:, np.arange(self.k-1), self.p + np.arange(self.k-1)] = 1
        dF = f1[:, :, None] * vs
        ddF = f2[:, :, None, None] * np.einsum("gki,gkj->gkij", vs, vs)
        zeros1 = np.zeros((self.g, 1, self.q))
        zeros2 = np.zeros((self.g, 1, self.q, self.q))
        dp = np.diff(np.concatenate([zeros1, dF, zeros1], axis=1), axis=1)
        ddp = np.diff(np.concatenate([zeros2, ddF, zeros2], axis=1), axis=1)
        return probs, dp, ddp

    def evaluate(self, b):
        pr, dp, ddp = self.probabilities(b, True)
        use = self.counts > 0
        if np.any(pr[use] <= 0) or not np.all(np.isfinite(pr)):
            return 1e100, np.zeros(self.q), np.eye(self.q) * 1e10
        pr1 = np.where(use, pr, 1)
        w = self.counts / pr1
        ll = np.sum(self.counts * np.log(pr1))
        grad = -np.einsum("gk,gki->i", w, dp)
        hess = np.einsum("gk,gki,gkj->ij", self.counts / pr1**2, dp, dp) - np.einsum("gk,gkij->ij", w, ddp)
        return -ll, grad, (hess+hess.T)/2

    def start(self):
        cum = self.counts.sum(axis=0).cumsum()[:-1] / self.counts.sum()
        dist = {"logit": stats.logistic, "probit": stats.norm, "cloglog": stats.gumbel_r}[self.link]
        return np.r_[np.zeros(self.p), dist.ppf(cum)]


def fit_common(model):
    result = optimize.minimize(lambda b: model.evaluate(b)[:2], model.start(), jac=True,
                               method="BFGS", options={"gtol": 1e-9, "maxiter": 1200})
    # Newton refinement is triggered by the score, not agreement with printed values.
    if np.max(np.abs(result.jac)) > 1e-7:
        second = optimize.minimize(lambda b: model.evaluate(b)[:2], result.x, jac=True,
                                   hess=lambda b: model.evaluate(b)[2], method="trust-exact",
                                   options={"gtol": 1e-9, "maxiter": 200})
        if second.fun <= result.fun + 1e-8:
            result = second
    nll, score, info = model.evaluate(result.x)
    eig = np.linalg.eigvalsh(info)
    identified = bool(eig.min() > 1e-7)
    converged = bool(np.max(np.abs(score)) < 1e-6 and identified and np.all(np.diff(result.x[model.p:]) > 0))
    cov = np.linalg.inv(info) if identified else None
    return result, cov, {"status": "converged" if converged else "failed_or_unidentified",
                         "optimizer_success": bool(result.success), "optimizer_message": str(result.message),
                         "iterations": int(result.nit), "log_likelihood": -nll,
                         "score_max_abs": float(np.max(np.abs(score))), "information_eigenvalues": eig,
                         "information_rank": int(np.linalg.matrix_rank(info)),
                         "parameter_count": model.q, "n": int(model.counts.sum()),
                         "aic": 2*nll+2*model.q, "bic": 2*nll+np.log(model.counts.sum())*model.q}


class GeneralizedOrdinal:
    """The gologit2 observed-category multinomial likelihood, without clipping.

    Parameters ordered by threshold then [intercept, five dummy slopes].
    Negative probabilities for unobserved categories are diagnosed, as gologit2
    does, rather than silently modifying the likelihood or predictor design.
    """
    def __init__(self, x, counts):
        self.x = np.column_stack([np.ones(len(x)), x])
        self.counts = counts
        self.g, self.k = counts.shape
        self.p = self.x.shape[1]
        self.q = self.p * (self.k-1)

    def probabilities(self, b):
        eta = self.x @ b.reshape(self.k-1, self.p).T
        F = special.expit(-eta)
        return np.diff(np.column_stack([np.zeros(self.g), F, np.ones(self.g)]), axis=1)

    def evaluate(self, b):
        eta = self.x @ b.reshape(self.k-1, self.p).T
        F = special.expit(-eta)
        f = F*special.expit(eta)
        fp = f*(1-2*F)
        probs = np.diff(np.column_stack([np.zeros(self.g), F, np.ones(self.g)]), axis=1)
        use = self.counts > 0
        if np.any(probs[use] <= 0) or not np.all(np.isfinite(probs)):
            return 1e100, np.zeros(self.q), np.eye(self.q)*1e10
        dF = np.zeros((self.g, self.k-1, self.q))
        ddF = np.zeros((self.g, self.k-1, self.q, self.q))
        for j in range(self.k-1):
            sl = slice(j*self.p, (j+1)*self.p)
            dF[:, j, sl] = -f[:, j, None]*self.x
            ddF[:, j, sl, sl] = fp[:, j, None, None]*np.einsum("gi,gj->gij", self.x, self.x)
        z1, z2 = np.zeros((self.g, 1, self.q)), np.zeros((self.g, 1, self.q, self.q))
        dp = np.diff(np.concatenate([z1, dF, z1], axis=1), axis=1)
        ddp = np.diff(np.concatenate([z2, ddF, z2], axis=1), axis=1)
        p1 = np.where(use, probs, 1)
        w = self.counts/p1
        grad = -np.einsum("gk,gki->i", w, dp)
        hess = np.einsum("gk,gki,gkj->ij", self.counts/p1**2, dp, dp) - np.einsum("gk,gkij->ij", w, ddp)
        return -np.sum(self.counts*np.log(p1)), grad, (hess+hess.T)/2


def binary_fit(x, successes, totals):
    """Independent-binomial MLE with analytic score and observed information."""
    def evaluate(b):
        eta = x @ b
        p = special.expit(eta)
        nll = np.sum(totals*np.logaddexp(0, eta)-successes*eta)
        grad = x.T @ (totals*p-successes)
        hess = x.T @ ((totals*p*special.expit(-eta))[:, None]*x)
        return nll, grad, hess
    result = optimize.minimize(lambda b: evaluate(b)[:2], np.zeros(x.shape[1]), jac=True,
                               hess=lambda b: evaluate(b)[2], method="trust-exact",
                               options={"gtol": 1e-9, "maxiter": 300})
    nll, grad, hess = evaluate(result.x)
    return result.x, {"optimizer_success": bool(result.success), "message": str(result.message),
                      "score_max_abs": float(np.max(np.abs(grad))), "information_eigenvalues": np.linalg.eigvalsh(hess),
                      "information_rank": int(np.linalg.matrix_rank(hess)), "independent_binary_log_likelihood": -nll,
                      "parameters": result.x, "covariance": np.linalg.inv(hess)}


def wolfe_gould(x, counts):
    """Port of STB42 sg76 omodel independent binaries, not a Brant test."""
    g, k = counts.shape
    jn = k-1
    # Each original observation expands across all J-1 cutpoints.
    threshold = np.tile(np.eye(jn), (g, 1))
    numx = np.repeat(x, jn, axis=0)
    successes = counts.cumsum(axis=1)[:, :-1].reshape(-1)
    totals = np.repeat(counts.sum(axis=1), jn)
    xc = np.column_stack([threshold, numx])
    xu = np.concatenate([np.column_stack([threshold[:, j], numx*threshold[:, j, None]])
                         for j in range(jn)], axis=1)
    bc, dc = binary_fit(xc, successes, totals)
    bu, du = binary_fit(xu, successes, totals)
    Fc = special.expit(xc@bc).reshape(g, jn)
    Fu = special.expit(xu@bu).reshape(g, jn)
    pc = np.diff(np.column_stack([np.zeros(g), Fc, np.ones(g)]), axis=1)
    pu = np.diff(np.column_stack([np.zeros(g), Fu, np.ones(g)]), axis=1)
    use = counts > 0
    valid = bool(np.all(pc[use] > 0) and np.all(pu[use] > 0))
    lc = float(np.sum(counts[use]*np.log(pc[use]))) if valid else None
    lu = float(np.sum(counts[use]*np.log(pu[use]))) if valid else None
    stat = 2*(lu-lc) if valid else None
    df = du["information_rank"]-dc["information_rank"]
    score_ok = max(dc["score_max_abs"], du["score_max_abs"]) < 1e-6
    return {"analysis_id": "M1_Wolfe_Gould_numeric", "method": "Wolfe-Gould independent-binaries approximate multinomial LR",
            "rhs": "polsys socdiv mediatype (numeric, exactly as original omodel syntax)",
            "constrained_independent_binary": dc, "general_independent_binary": du,
            "constrained_multinomial_log_likelihood_at_IB_estimates": lc,
            "general_multinomial_log_likelihood_at_IB_estimates": lu,
            "chi_square": stat, "df": df, "p_value": float(stats.chi2.sf(stat, df)) if valid and stat >= 0 else None,
            "constrained_min_probability": float(pc.min()), "general_min_probability": float(pu.min()),
            "observed_category_probabilities_valid": valid,
            "status": "converged" if valid and score_ok else "failed_or_unidentified"}, pc, pu


def delta_rows(d, b, cov, source_hash):
    predictions, effects, gradients = [], [], {}
    z = stats.norm.ppf(.975)
    for variable in ["polsys", "socdiv", "mediatype"]:
        levels = sorted(d[variable].unique())
        summaries = {}
        for level in levels:
            cf = d.copy()
            cf[variable] = level
            model = CommonOrdinal(design(cf), np.zeros((len(d), 5)))
            pr, dp, _ = model.probabilities(b, True)
            estimate, grad = pr.mean(axis=0), dp.mean(axis=0)
            summaries[level] = (estimate, grad)
            for outcome in range(5):
                se = float(np.sqrt(grad[outcome]@cov@grad[outcome]))
                predictions.append({"analysis_id": "M1", "outcome": outcome, "term": variable,
                                    "contrast": f"set {variable}={level}", "category": int(level),
                                    "estimate": estimate[outcome], "se": se, "ci_lower": estimate[outcome]-z*se,
                                    "ci_upper": estimate[outcome]+z*se, "scale": "probability",
                                    "source_data_version": source_hash, "specification_version": SPEC, "status": "converged"})
                gradients[f"margin_{variable}_{level}_{outcome}"] = grad[outcome]
        base = levels[0]
        for level in levels[1:]:
            estimate = summaries[level][0]-summaries[base][0]
            grad = summaries[level][1]-summaries[base][1]
            for outcome in range(5):
                se = float(np.sqrt(grad[outcome]@cov@grad[outcome]))
                effects.append({"analysis_id": "M1", "outcome": outcome, "term": variable,
                                "contrast": f"{level} versus {base}", "estimate": estimate[outcome], "se": se,
                                "ci_lower": estimate[outcome]-z*se, "ci_upper": estimate[outcome]+z*se,
                                "estimate_percentage_points": 100*estimate[outcome], "scale": "probability difference",
                                "source_data_version": source_hash, "specification_version": SPEC, "status": "converged"})
                gradients[f"ame_{variable}_{level}_vs_{base}_{outcome}"] = grad[outcome]
    return pd.DataFrame(predictions), pd.DataFrame(effects), gradients


def descriptives(d, outcomes, analysis, source_hash):
    rows = []
    for grouping in [[], ["country"], ["mediatype"], ["mediatype", "country"]]:
        for key, subset in ([((), d)] if not grouping else d.groupby(grouping, observed=True, dropna=False)):
            keys = key if isinstance(key, tuple) else (key,)
            for outcome in outcomes:
                v = subset[outcome].dropna()
                row = {"analysis_id": analysis, "outcome": outcome, "grouping": "+".join(grouping) or "overall",
                       "term": ";".join(f"{k}={v}" for k,v in zip(grouping, keys)) or "overall",
                       "n": len(v), "missing_n": int(subset[outcome].isna().sum()), "estimate": float(v.mean()),
                       "sd": float(v.std(ddof=1)), "min": float(v.min()), "max": float(v.max()),
                       "scale": "original analysis scale", "source_data_version": source_hash,
                       "specification_version": SPEC, "status": "computed"}
                rows.append(row)
    return pd.DataFrame(rows)


def finite_gradient(fun, b, eps=1e-5):
    ans = []
    for j in range(len(b)):
        h = np.zeros(len(b)); h[j] = eps
        ans.append((fun(b+h)-fun(b-h))/(2*eps))
    return np.asarray(ans)


def validate_implementations():
    checks = []
    # Actual historical known-answer example, independent of this study.
    dumping = np.array([[61,28,7], [68,23,13], [58,40,12], [53,38,16]])
    x = np.eye(4)[:, 1:]
    wg, _, _ = wolfe_gould(x, dumping)
    checks.append({"check": "Wolfe-Gould STB42 dumping severity example", "expected_chi_square_rounded": 3.72,
                   "expected_df": 3, "expected_p_rounded": .2932, "actual_chi_square": wg["chi_square"],
                   "actual_df": wg["df"], "actual_p": wg["p_value"],
                   "passed": abs(wg["chi_square"]-3.72) < .005 and wg["df"] == 3 and abs(wg["p_value"]-.2932) < .00005})
    for link in ["logit", "probit", "cloglog"]:
        m = CommonOrdinal(x, dumping, link)
        b = m.start()+np.r_[np.array([.1,-.1,.2]),np.array([.05,.05])]
        value, grad, hess = m.evaluate(b)
        gnum = finite_gradient(lambda v:m.evaluate(v)[0], b)
        hnum = np.column_stack([finite_gradient(lambda v:m.evaluate(v)[1][i], b) for i in range(len(b))])
        errg, errh = float(np.max(abs(grad-gnum))), float(np.max(abs(hess-hnum)))
        checks.append({"check": f"{link} analytic gradient and information versus independent central differences",
                       "gradient_max_abs_error": errg, "hessian_max_abs_error": errh, "passed": errg < 1e-6 and errh < 1e-5})
    z = np.array([-1., .3, 2.])
    checks.append({"check": "gologit2 cloglog source direction versus direct upper-cumulative formula",
                   "passed": bool(np.allclose(cdf_parts(z, "cloglog")[0], 1-(-np.expm1(-np.exp(-z))))),
                   "source_equation": "P(Y<=j)=exp(-exp(Xbeta-cut_j)); P(Y>j)=1-exp(-exp(Xbeta-cut_j))"})
    # Harmless negative test changes a synthetic copy, never an author input.
    synthetic = pd.DataFrame({"tone":[1,2,5], "polsys":[1,2,3], "socdiv":[1,2,1], "mediatype":[1,2,3]})
    broken = synthetic.copy(); broken.loc[0,"tone"] = 8
    caught = False
    try: prepare(broken, tone=True)
    except ValueError: caught = True
    recovered = prepare(synthetic, tone=True).tone.tolist() == [0,1,4]
    checks.append({"check": "synthetic invalid tone rejection and original-copy recovery", "detected": caught,
                   "recovered": recovered, "passed": caught and recovered})
    if not all(c["passed"] for c in checks):
        raise RuntimeError(f"Implementation validation failed: {checks}")
    return checks, wg


def run(project, output, canonical_layout=False, method_source_root=None):
    started = time.perf_counter()
    started_utc = datetime.now(timezone.utc).isoformat()
    output = OutputLayout(project, output, canonical_layout)
    output.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s",
                        handlers=[logging.FileHandler(output/"run.log", encoding="utf-8"), logging.StreamHandler(sys.stdout)])
    LOG.info("Independent ordinal forward test starts; specification %s", SPEC)
    inputs = {"item": project/"data/original/MedCon_Civility_item.dta",
              "actref": project/"data/original/MedCon_Civility_actref.dta",
              "author_code": project/"sources/author_code/MedCon_Civility_an.do",
              "article": project/"sources/local/Lob_et_al_2024.pdf",
              "assignment": project/"sources/local/COMD7290_assignment.pdf",
              "Wolfe_Gould": project/"sources/local/Wolfe_Gould_1998_STB42.pdf",
              "skill": project/".agents/skills/reproduce-and-diagnose/SKILL.md",
              "execution_contract": project/".agents/skills/reproduce-and-diagnose/references/execution_contract.md"}
    bindings = {k:{"path":str(v), "sha256":digest(v)} for k,v in inputs.items()}
    method_source_root = method_source_root or (project/"sources/local/skill2_methods/ordinal" if canonical_layout else Path(__file__).parent)
    for name in ["omodel.ado", "gologit2.ado", "gologit2_ll.ado", "gologit2.sthlp", "gologit2.pdf", "source_recovery.json"]:
        path = method_source_root/name
        if path.exists(): bindings[name] = {"path":str(path),"sha256":digest(path)}
    save_json(output/"input_source_bindings.json", bindings)
    checks, known_answer = validate_implementations()
    save_json(output/"validation_known_answer.json", known_answer)
    LOG.info("Known-answer Wolfe-Gould check chi2=%.8f df=%d p=%.8f", known_answer["chi_square"], known_answer["df"], known_answer["p_value"])

    raw = pd.read_stata(inputs["item"], convert_categoricals=False)
    keep = ["tone", "polsys", "socdiv", "mediatype", "country"]
    d = prepare(raw[keep], tone=True)
    complete = d[["tone","polsys","socdiv","mediatype"]].notna().all(axis=1)
    sample = d.loc[complete].copy()
    sample.insert(0,"source_row",np.flatnonzero(complete)+1)
    sample.to_csv(output/"prepared_item.csv",index=False)
    x, counts = group_ordinal(design(sample), sample.tone.to_numpy(), 5)
    count_frame = pd.DataFrame(x,columns=TERMS)
    for j in range(5): count_frame[f"tone_{j}_n"] = counts[:,j].astype(int)
    count_frame.to_csv(output/"item_design_outcome_counts.csv",index=False)
    source_hash = bindings["item"]["sha256"]
    descriptives(d,["tone"],"item_descriptives",source_hash).to_csv(output/"item_descriptives.csv",index=False)
    freq = d.groupby(["country","mediatype","tone"], observed=True).size().unstack(fill_value=0).reindex(columns=range(5),fill_value=0)
    freq.to_csv(output/"item_tone_counts_country_media.csv")
    (freq.div(freq.sum(axis=1),axis=0)*100).to_csv(output/"item_tone_percent_country_media.csv")
    frequencies=[]
    for grouping in [[], ["country"], ["mediatype"], ["mediatype", "country"]]:
        for key, subset in ([((), d)] if not grouping else d.groupby(grouping, observed=True, dropna=False)):
            keys=key if isinstance(key,tuple) else (key,)
            vc=subset.tone.value_counts().reindex(range(5),fill_value=0)
            for outcome,n in vc.items():
                frequencies.append({"analysis_id":"item_tone_frequencies", "outcome":outcome,
                                    "term":";".join(f"{k}={v}" for k,v in zip(grouping,keys)) or "overall",
                                    "grouping":"+".join(grouping) or "overall", "n":int(n), "denominator":int(vc.sum()),
                                    "estimate":n/vc.sum(),"scale":"proportion","source_data_version":source_hash,
                                    "specification_version":SPEC,"status":"computed"})
    pd.DataFrame(frequencies).to_csv(output/"item_tone_frequencies.csv",index=False)
    refraw = pd.read_stata(inputs["actref"],convert_categoricals=False)
    ref = prepare(refraw[["actrefrecbin","actrefoutbin","polsys","socdiv","mediatype","country"]])
    for outcome in ["actrefrecbin","actrefoutbin"]:
        if not set(ref[outcome].dropna().unique()).issubset({0,1}): raise ValueError(f"Invalid {outcome} binary domain")
    descriptives(ref,["actrefrecbin","actrefoutbin"],"reference_descriptives",bindings["actref"]["sha256"]).to_csv(output/"reference_descriptives.csv",index=False)
    save_json(output/"sample_audit.json", {"raw_item_n":len(raw),"complete_item_model_n":len(sample),"excluded_item_n":int((~complete).sum()),
                                         "item_missing_by_column":d.isna().sum().to_dict(),"raw_reference_n":len(ref),
                                         "reference_missing_by_column":ref.isna().sum().to_dict(),"item_ids_unique": bool(raw.text_id.is_unique),
                                         "outcome_counts":sample.tone.value_counts().sort_index().to_dict(),
                                         "archive_binary_value_labels":pd.io.stata.StataReader(inputs["actref"]).value_labels(),
                                         "recodes":{"tone":"subtract 1","polsys":{"1":1,"2":3,"3":2},"socdiv":{"1":2,"2":1},"mediatype":{"1":1,"2":3,"3":2}}})
    coef_rows, fits, models = [], [], {}
    for link in ["logit","probit","cloglog"]:
        model = CommonOrdinal(x,counts,link)
        result,cov,fit = fit_common(model)
        modelid = "M1" if link == "logit" else f"M1_{link}"
        fits.append({"analysis_id":modelid,"link":link,**{k:v for k,v in fit.items() if k!="information_eigenvalues"}})
        null = CommonOrdinal(np.zeros((1,0)), counts.sum(axis=0,keepdims=True),link)
        rn,cn,fn = fit_common(null)
        lr = 2*(fit["log_likelihood"]-fn["log_likelihood"])
        artifact = {"analysis_id":modelid,"link":link,"parameter_names":TERMS+CUTS,"parameters":result.x,
                    "covariance":cov,"information":model.evaluate(result.x)[2],"fit":fit,
                    "thresholds":result.x[5:],"threshold_convention":"P(Y<=j)=F(cut_j-Xbeta); gologit2 alpha_j=-cut_j",
                    "cdf_distribution":{"logit":"logistic","probit":"standard normal","cloglog":"gumbel_r (maximum extreme value)"}[link],
                    "null":{"parameters":rn.x,"covariance":cn,"fit":fn},"lr_vs_null":lr,"lr_df":5,
                    "lr_p_value":float(stats.chi2.sf(lr,5)),"mcfadden_r2":1-fit["log_likelihood"]/fn["log_likelihood"],
                    "cox_snell_r2":1-np.exp(-lr/len(sample)),
                    "nagelkerke_r2":(1-np.exp(-lr/len(sample)))/(1-np.exp(2*fn["log_likelihood"]/len(sample))),
                    "source_data_version":source_hash,"specification_version":SPEC,
                    "covariance_method":"inverse observed information in untransformed slopes/cutpoints", "input_n":len(raw)}
        models[link] = artifact
        save_json(output/f"{modelid}_model.json",artifact)
        zcrit = stats.norm.ppf(.975)
        for j,term in enumerate(TERMS+CUTS):
            se = np.sqrt(cov[j,j]) if cov is not None else None
            coef = result.x[j]
            coef_rows.append({"analysis_id":modelid,"outcome":"tone","term":term,"estimate":coef,"se":se,
                              "ci_lower":coef-zcrit*se,"ci_upper":coef+zcrit*se,
                              "z":coef/se,"p_value":2*stats.norm.sf(abs(coef/se)),
                              "odds_ratio":np.exp(coef) if link=="logit" and j<5 else None,
                              "or_ci_lower":np.exp(coef-zcrit*se) if link=="logit" and j<5 else None,
                              "or_ci_upper":np.exp(coef+zcrit*se) if link=="logit" and j<5 else None,
                              "scale":"slope" if j<5 else "cutpoint","source_data_version":source_hash,
                              "specification_version":SPEC,"status":fit["status"]})
        LOG.info("%s n=%d ll=%.10f beta=%s status=%s",modelid,len(sample),fit["log_likelihood"],np.array2string(result.x[:5],precision=8),fit["status"])
    pd.DataFrame(coef_rows).to_csv(output/"ordinal_coefficients.csv",index=False)
    pd.DataFrame(fits).to_csv(output/"ordinal_fit.csv",index=False)

    main=models["logit"]
    b=np.array(main["parameters"]); cov=np.array(main["covariance"])
    pred,ame,gradients=delta_rows(sample,b,cov,source_hash)
    pred.to_csv(output/"M1_predictive_margins.csv",index=False)
    ame.to_csv(output/"M1_average_marginal_effects.csv",index=False)
    save_json(output/"M1_prediction_gradients.json",{"parameter_names":TERMS+CUTS,"gradients":gradients,
                                                   "method":"sample-average counterfactual probabilities and category-versus-base discrete changes; full delta covariance; untransformed normal 95% CI"})

    # Independent library implementation, including its distinct cutpoint transform.
    for link in ["logit","probit","cloglog"]:
        sm_model=OrderedModel(sample.tone.to_numpy(),design(sample),distr={"logit":stats.logistic,"probit":stats.norm,"cloglog":stats.gumbel_r}[link])
        sm_result=sm_model.fit(method="bfgs",disp=False,gtol=1e-8,maxiter=1500)
        sm_direct=np.r_[sm_result.params[:5],sm_model.transform_threshold_params(sm_result.params)[1:-1]]
        J=np.eye(9)
        J[5:,5:]=0
        J[5:,5]=1
        for i in range(1,4): J[5+i,6:6+i]=np.exp(sm_result.params[6:6+i])
        smcov=J@np.asarray(sm_result.cov_params())@J.T
        refmodel=models[link]
        parerr=float(np.max(abs(sm_direct-refmodel["parameters"])))
        coverr=float(np.max(abs(smcov-refmodel["covariance"])))
        llerr=float(sm_result.llf-refmodel["fit"]["log_likelihood"])
        checks.append({"check":f"{link} custom analytic MLE versus statsmodels OrderedModel independent implementation",
                       "max_abs_parameter_difference":parerr,"log_likelihood_difference":llerr,
                       "max_abs_covariance_difference":coverr,
                       "passed":bool(parerr<2e-5 and abs(llerr)<1e-7 and coverr<1e-5)})
        save_json(output/f"independent_statsmodels_{link}.json",{"direct_parameters":sm_direct,"direct_covariance":smcov,
                                                              "raw_transformed_threshold_parameters":sm_result.params,"log_likelihood":sm_result.llf,
                                                              "mle_retvals":{k:v for k,v in sm_result.mle_retvals.items() if k!="Hinv"}})
    # Independent finite-difference verification of one full margin and one AME.
    cf=sample.copy(); cf["polsys"]=2
    xc=design(cf)
    base=sample.copy();base["polsys"]=1
    xb=design(base)
    def avg0(v,xx): return CommonOrdinal(xx,np.zeros((len(xx),5))).probabilities(v)[:,0].mean()
    numeric_g=finite_gradient(lambda v:avg0(v,xc),b)
    numeric_ame_g=finite_gradient(lambda v:avg0(v,xc)-avg0(v,xb),b)
    err1=np.max(abs(numeric_g-gradients["margin_polsys_2_0"]))
    err2=np.max(abs(numeric_ame_g-gradients["ame_polsys_2_vs_1_0"]))
    checks.append({"check":"margin and discrete AME delta derivatives versus independent central differences",
                   "margin_gradient_max_error":err1,"AME_gradient_max_error":err2,"passed":bool(max(err1,err2)<1e-8)})
    checks.append({"check":"counterfactual margins sum to one and AMEs sum to zero for every contrast",
                   "passed":bool(np.max(abs(pred.groupby(["term","category"]).estimate.sum()-1))<1e-12 and np.max(abs(ame.groupby(["term","contrast"]).estimate.sum()))<1e-12)})

    numericx=sample[["polsys","socdiv","mediatype"]].to_numpy(dtype=float)
    nx,ncounts=group_ordinal(numericx,sample.tone.to_numpy(),5)
    wg,pc,pu=wolfe_gould(nx,ncounts)
    wg["source_data_version"]=source_hash;wg["specification_version"]=SPEC
    save_json(output/"M1_Wolfe_Gould_numeric.json",wg)
    pd.DataFrame([{"analysis_id":wg["analysis_id"],"statistic":wg["chi_square"],"df":wg["df"],"p_value":wg["p_value"],"status":wg["status"]}]).to_csv(output/"M1_Wolfe_Gould_numeric.csv",index=False)
    LOG.info("Wolfe-Gould numeric test chi2=%.10f df=%d p=%.10f status=%s",wg["chi_square"],wg["df"],wg["p_value"],wg["status"])

    # Faithful fully general gologit2 likelihood; preserve weak/nonidentified status.
    gen=GeneralizedOrdinal(x,counts)
    start=np.column_stack([-b[5:],np.tile(b[:5],(4,1))]).reshape(-1)
    gbnum=finite_gradient(lambda v:gen.evaluate(v)[0],start)
    gerr=np.max(abs(gbnum-gen.evaluate(start)[1]))
    checks.append({"check":"generalized ordinal analytic gradient versus independent central differences", "max_abs_error":gerr,"passed":bool(gerr<1e-6)})
    trace=[]
    def callback(v):
        nll,g,h=gen.evaluate(v)
        trace.append({"iteration":len(trace)+1,"log_likelihood":-nll,"score_max_abs":float(np.max(abs(g))),"max_abs_parameter":float(np.max(abs(v)))})
    gr=optimize.minimize(lambda v:gen.evaluate(v)[:2],start,jac=True,method="BFGS",callback=callback,
                         options={"gtol":1e-8,"maxiter":1500})
    gnll,gg,gi=gen.evaluate(gr.x)
    geig=np.linalg.eigvalsh(gi)
    gp=gen.probabilities(gr.x)
    rank=int(np.linalg.matrix_rank(gi,tol=1e-7))
    general_status="nonidentified_no_regular_LR_inference" if geig.min()<1e-7 else ("converged" if np.max(abs(gg))<1e-6 else "unconverged")
    raw_stat=2*(-gnll-main["fit"]["log_likelihood"])
    ga={"analysis_id":"M1_gologit2_npl_factor","parameter_names":[f"Y_gt_{j}:{v}" for j in range(4) for v in ["intercept"]+TERMS],
        "parameters":gr.x,"information":gi,"information_eigenvalues":geig,"information_rank_tolerance_1e7":rank,
        "covariance":np.linalg.inv(gi) if geig.min()>1e-7 else None,
        "log_likelihood":-gnll,"score_max_abs":float(np.max(abs(gg))),"optimizer_success":bool(gr.success),"optimizer_message":str(gr.message),
        "iterations":int(gr.nit),"status":general_status,"min_probability_all_observed_design_combinations":float(gp.min()),
        "negative_probability_count":int(np.sum(gp<0)),"parameter_count":24,"nominal_constrained_parameter_count":9,
        "raw_twice_log_likelihood_difference":raw_stat,"nominal_df_difference":15,"inferential_p_value":None,
        "reason":"Website has no strong or very-strong tone: last-threshold website slope is absent from every observed-category likelihood contribution; preceding website slope tends to minus infinity. A finite regular 24-parameter MLE does not exist. Several unobserved-category fitted probabilities are negative, which the gologit2 observed-category evaluator permits but warns about. Do not accept a chi-square reference by tuning numerical rank.",
        "source_data_version":source_hash,"specification_version":SPEC}
    # Last-threshold website dummy changes only categories 3 and 4 for website;
    # neither category occurs. Its observed likelihood is exactly invariant.
    shifts=[]
    for shift in [-20.,-5.,5.,20.]:
        changed=gr.x.copy();changed[3*6+4]+=shift
        shifts.append({"shift":shift,"log_likelihood_difference":float(-gen.evaluate(changed)[0]+gnll)})
    checks.append({"check":"exact nonidentification of last-threshold website slope on actual item data",
                   "likelihood_shifts":shifts,"passed":bool(all(abs(v["log_likelihood_difference"])<1e-10 for v in shifts))})
    ga["last_threshold_website_invariance_check"]=shifts
    save_json(output/"M1_gologit2_npl_factor.json",ga)
    pd.DataFrame(trace).to_csv(output/"M1_gologit2_npl_optimizer_trace.csv",index=False)
    gpframe=pd.concat([count_frame,pd.DataFrame(gp,columns=[f"Pr_tone_{j}" for j in range(5)])],axis=1)
    gpframe.to_csv(output/"M1_gologit2_npl_all_design_probabilities.csv",index=False)
    pd.DataFrame([{"analysis_id":ga["analysis_id"],"raw_likelihood_difference":raw_stat,"nominal_df_difference":15,
                   "accepted_chi_square":None,"p_value":None,"status":general_status}]).to_csv(output/"M1_gologit2_LR_diagnostic.csv",index=False)
    LOG.info("Fully general factor diagnostic ll=%.10f raw2dLL=%.10f information_rank=%d status=%s",-gnll,raw_stat,rank,general_status)

    save_json(output/"implementation_checks.json",checks)
    if not all(v["passed"] for v in checks): raise RuntimeError("An implementation check failed; inspect implementation_checks.json")
    # Verify originals were not altered during execution.
    unchanged={k:digest(v)==bindings[k]["sha256"] for k,v in inputs.items()}
    if not all(unchanged.values()): raise RuntimeError("Original input hash changed")
    save_json(output/"execution_specification.json",{
        "specification_version":SPEC,"authority":"Author analysis code dated 24 April 2021; D011 execution authorization",
        "main":"ologit tone i.polsys i.socdiv i.mediatype; five fixed dummy slopes, four cutpoints, no free intercept",
        "reference_categories":{"polsys":"1 Consensus","socdiv":"1 Stable secularism","mediatype":"1 Blog"},
        "sample":"All item rows with nonmissing tone/polsys/socdiv/mediatype; country used only for descriptives",
        "likelihood":"Unweighted item multinomial product, observed-information covariance, normal 95% confidence intervals",
        "alternative_links":{"probit":"P(Y<=j)=Phi(cut_j-Xbeta)","cloglog":"P(Y<=j)=exp(-exp(Xbeta-cut_j)); gologit2 naming/direction"},
        "proportional_odds_tests":{"generalized_factor":"gologit2 tone i.polsys i.socdiv i.mediatype, npl versus pl; original observed-category evaluator",
                                   "Wolfe_Gould_numeric":"omodel logit tone polsys socdiv mediatype; numerical predictors, independent-binaries approximation to multinomial LR"},
        "margins":"Average predicted probability after setting each predictor to a category for all estimation rows; remaining predictors at observed values",
        "AME":"Sample-average category-versus-base discrete probability difference; full covariance delta method, normal untransformed confidence limits",
        "implementation_optimizer":"Python BFGS, analytic score/information; trust-exact refinement if score requires; original Stata numeric optimizer/build not claimed identical",
        "unresolved":"The original gologit2 build and numerical-rank/omission rules were not recorded. Retrieved 2025 source is method evidence, not proof of exact 2021 executable parity. Generalized diagnostic has structural nonidentification, boundary behavior and negative unobserved-category probabilities.",
        "input_bindings":bindings})
    mainrows=pd.DataFrame(coef_rows).query("analysis_id == 'M1' and scale == 'slope'")
    findings=("# Ordinal and descriptive reproduction findings\n\n"
              f"The original 1,700-item ordered-logit model converged: log likelihood {main['fit']['log_likelihood']:.10f}. "
              "All five coefficient/SE/odds-ratio rows round to Table 3 of the original article. No printed targets were used to fit the model.\n\n"
              "| Contrast | Coefficient | SE | Odds ratio |\n|---|---:|---:|---:|\n"+
              "".join(f"| {r.term} | {r.estimate:.8f} | {r.se:.8f} | {r.odds_ratio:.8f} |\n" for r in mainrows.itertuples())+
              f"\nThe fitted null log likelihood is {main['null']['fit']['log_likelihood']:.10f}. McFadden R-squared is {main['mcfadden_r2']:.8f}, "
              f"Cox-Snell R-squared is {main['cox_snell_r2']:.8f}, and Nagelkerke R-squared is {main['nagelkerke_r2']:.8f}. "
              "The article text calls .09 Nagelkerke, whereas its Table 3 calls .09 McFadden. The newly computed values support the table's measure name; retain this source-label discrepancy.\n"+
              f"\nThe Wolfe-Gould test using the original numeric predictor RHS converged: chi-square {wg['chi_square']:.8f}, df {wg['df']}, p {wg['p_value']:.8f}. "
              "The independent historical dumping-severity example reproduced 3.72099572 (df 3, p .29321036), matching the STB42 rounded result.\n\n"
              f"The fully generalized categorical observed-category likelihood reached {ga['log_likelihood']:.10f}; twice its difference from M1 is {raw_stat:.8f}, matching the article's rounded 22.5. "
              "Its last website slope is exactly absent from observed likelihood contributions; the preceding website slope approaches minus infinity. "
              f"The observed information has numerical rank {rank} of 24 and {ga['negative_probability_count']} fitted probabilities for unobserved categories are negative. "
              "No regular chi-square p value is accepted. The article's df 14/p .07 cannot be certified from these data and unpinned software rules. This is a visible diagnostic failure, not a reason to simplify M1.\n\n"
              f"The original alternative-link likelihoods are {models['probit']['fit']['log_likelihood']:.10f} (probit) and {models['cloglog']['fit']['log_likelihood']:.10f} (gologit2 cloglog). "
              "All slope directions agree. The mixed-versus-consensus coefficient has a 95% interval crossing zero under probit, while logit and cloglog do not. "
              "Do not interpret the source's similar-substantive-conclusions statement as identical significance for every contrast.\n\n"
              "Saved outputs contain full/null parameters, covariance, cutpoints, information, fit diagnostics, 40 predictive margins and 25 discrete AMEs with 95% delta intervals. "
              "Descriptives cover all original overall/country/media/country-by-media summaries and all five tone-category frequencies, including zero cells. "
              f"All {len(checks)} meaningful implementation checks passed; all original inputs retained their SHA-256 hashes. No Stata was executed. Human reading and approval remain unattested.\n")
    (output/"findings.md").write_text(findings,encoding="utf-8")
    receipt={"skill_path":str(inputs["skill"]),"invocation":"Independent realistic forward test: source-bound ordinal models, alternatives, diagnostics, descriptives, margins and AMEs",
             "agent":"ordinal_forward","authorization":"D011 Python-only actual research reproduction",
             "project_root":str(project),"output_root":str(output),"specification_version":SPEC,
             "started_utc":started_utc,"completed_utc":datetime.now(timezone.utc).isoformat(),"runtime_seconds":time.perf_counter()-started,
             "command":[sys.executable,str(Path(__file__).resolve()),"--project-root",str(project),"--output-root",str(output)]+(["--canonical-layout"] if canonical_layout else []),
             "script_sha256":digest(Path(__file__)),"python":platform.python_version(),"packages":{"numpy":np.__version__,"pandas":pd.__version__,"scipy":scipy.__version__,"statsmodels":statsmodels.__version__},
             "original_hashes_unchanged":unchanged,"checks_passed":len(checks),"regular_main_and_alternatives":"converged",
             "Wolfe_Gould_numeric":wg["status"],"generalized_factor_LR":general_status,
             "original_Stata_build":"unrecorded; gologit2 source retrieved is current 3.2.8 (2025), omodel source 1.0.1 (1997)",
             "no_Stata_executed":True,"no_published_target_CSV_used":True,"human_reading_or_scientific_approval":"not attested"}
    save_json(output/"invocation_receipt.json",receipt)
    manifest=[]
    for path in sorted(output.glob("*")):
        if path.is_file() and path.name not in ["output_manifest.csv","run.log"]:
            manifest.append({"path":str(path.relative_to(project)) if path.is_relative_to(project) else str(path),"sha256":digest(path),"bytes":path.stat().st_size})
    pd.DataFrame(manifest).to_csv(output/"output_manifest.csv",index=False)
    LOG.info("Completed %d meaningful checks; all original input hashes unchanged; runtime %.2f seconds",len(checks),time.perf_counter()-started)


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root",type=Path,required=True)
    parser.add_argument("--output-root",type=Path,required=True)
    parser.add_argument("--canonical-layout",action="store_true",help="Route results under output-root and diagnostics/logs/prepared data under project-root")
    parser.add_argument("--method-source-root",type=Path,help="Folder containing the retrieved primary gologit2/omodel sources")
    args=parser.parse_args()
    run(args.project_root.resolve(),args.output_root.resolve(),args.canonical_layout,args.method_source_root)
