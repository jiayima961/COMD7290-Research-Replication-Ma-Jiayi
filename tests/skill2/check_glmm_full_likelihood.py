"""Independent high-order full-data likelihood evaluation, without optimization.

Default evaluates both outcomes at arbitrary parameters. --fit reads a candidate
fit JSON and checks the fitted parameter vector without changing the fit artifact.
"""
from collections import Counter
import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd
from scipy.special import logsumexp, roots_hermitenorm

from glmm_reference import nested_quad

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "analysis"))
from nested_logit import NestedBernoulli
CANDIDATE_SHA256 = hashlib.sha256((ROOT / "analysis/nested_logit.py").read_bytes()).hexdigest()

OUT = ROOT / "outputs/diagnostics/glmm"


def high_order_log_likelihood(eta, item_variance, actor_variance, counts, points):
    nodes, weights = roots_hermitenorm(points)
    log_weights = np.log(weights) - .5*np.log(2*np.pi)
    predictor = eta + np.sqrt(item_variance)*nodes[:, None] + np.sqrt(actor_variance)*nodes[None, :]
    inner = [logsumexp(s*predictor-n*np.logaddexp(0, predictor)+log_weights[None, :], axis=1) for n,s in counts]
    return float(logsumexp(np.sum(inner, axis=0)+log_weights))


def independent_patterns(data, outcome, beta):
    patterns = Counter()
    for _, rows in data.groupby("text_id", sort=True):
        context = rows[["polsys", "socdiv", "mediatype"]].drop_duplicates()
        assert len(context) == 1
        p,s,m = context.iloc[0]
        x = np.array([1,p==2,p==3,s==2,m==2,m==3])
        eta = float(x[:len(beta)] @ beta)
        counts = tuple(sorted((len(actor), int(actor[outcome].sum())) for _,actor in rows.groupby("akteur_id", sort=True)))
        patterns[(eta, counts)] += 1
    return patterns


def run(fit_path=None):
    source = ROOT / "data/original/MedCon_Civility_actref.dta"
    data = pd.read_stata(source, convert_categoricals=False)
    for col in ["polsys", "mediatype"]:
        data[col] = data[col].map({1:1,2:3,3:2})
    data["socdiv"] = data["socdiv"].map({1:2,2:1})
    if fit_path:
        fit = json.loads(Path(fit_path).read_text(encoding="utf-8"))
        outcome = fit["outcome"]
        theta = np.array(fit["parameters"])
        null = len(theta) == 3
        label = fit["model_id"] + "_fitted_parameters"
        configs = [(outcome, theta, null, label)]
    else:
        theta = np.r_[[-1.4,.2,-.35,.45,-.1,.3], .5*np.log(.7), .5*np.log(1.3)]
        configs = [(outcome,theta,False,outcome+"_arbitrary_parameters") for outcome in ("actrefoutbin","actrefrecbin")]
    reports = []
    for outcome,theta,null,label in configs:
        frame = data[["text_id","akteur_id",outcome,"polsys","socdiv","mediatype"]].dropna()
        assert set(frame[outcome].unique()).issubset({0,1})
        beta, vi, va = theta[:-2], float(np.exp(2*theta[-2])), float(np.exp(2*theta[-1]))
        patterns = independent_patterns(frame, outcome, beta)
        evaluations = {}
        for points in (81,161,241):
            evaluations[points] = sum(count*high_order_log_likelihood(eta,vi,va,counts,points) for (eta,counts),count in patterns.items())
        candidate = {}
        for points in (7,11,21):
            model = NestedBernoulli(frame,outcome,points=points,null=null)
            ll = model.evaluate(theta)
            candidate[points] = {"log_likelihood": ll, "difference_from_reference_241":ll-evaluations[241], "adaptation":model.last_diagnostic}
        # Independent adaptive quadrature on extremes of predictor and grouping.
        keys = list(patterns)
        selected = list(dict.fromkeys([min(keys,key=lambda k:k[0]),max(keys,key=lambda k:k[0]),max(keys,key=lambda k:sum(c[0] for c in k[1]))]))
        selected_checks = []
        for eta,counts in selected:
            direct = nested_quad(eta,vi,va,counts)
            direct["eta"] = eta
            direct["actor_counts_n_s"] = counts
            direct["gh241_log_likelihood"] = high_order_log_likelihood(eta,vi,va,counts,241)
            direct["difference_gh241_from_quad"] = direct["gh241_log_likelihood"]-direct["log_likelihood"]
            selected_checks.append(direct)
        reference_converged = bool(abs(evaluations[241]-evaluations[161]) < 1e-7 and
                                   max(abs(d["difference_gh241_from_quad"]) for d in selected_checks) < 1e-7)
        report = {"label":label,"outcome":outcome,"fit_artifact":str(fit_path) if fit_path else None,
                  "theta":theta.tolist(),"item_variance":vi,"actor_variance":va,"null_model":null,
                  "source_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),
                  "candidate_sha256":CANDIDATE_SHA256,
                  "n_rows":len(frame),"n_items":frame.text_id.nunique(),"independent_patterns":len(patterns),
                  "high_order_full_log_likelihood":evaluations,"difference_241_from_161":evaluations[241]-evaluations[161],
                  "candidate_comparisons":candidate,"selected_quad_checks":selected_checks,
                  "reference_convergence_check_passed":reference_converged,
                  "status":"fixed_parameter_check_only_not_a_refit"}
        OUT.mkdir(parents=True,exist_ok=True)
        (OUT/(label+"_full_likelihood.json")).write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
        assert reference_converged, "Independent high-order reference has not passed convergence checks; inspect saved report"
        reports.append({"label":label,"high_order_log_likelihood":evaluations,"difference_241_from_161":report["difference_241_from_161"],
                        "candidate_errors":{q:d["difference_from_reference_241"] for q,d in candidate.items()},
                        "selected_quad_max_log_difference":max(abs(d["difference_gh241_from_quad"]) for d in selected_checks)})
    print(json.dumps(reports,indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fit",type=Path)
    args = parser.parse_args()
    run(args.fit)
