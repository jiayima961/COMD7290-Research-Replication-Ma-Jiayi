"""Independently recompute scaled-gradient and Hessian-step checks after a fit."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "analysis"))
from nested_logit import NestedBernoulli
CANDIDATE_SHA256 = hashlib.sha256((ROOT / "analysis/nested_logit.py").read_bytes()).hexdigest()


def run(path):
    fit = json.loads(path.read_text(encoding="utf-8"))
    theta = np.asarray(fit["parameters"])
    data = pd.read_stata(ROOT / "data/original/MedCon_Civility_actref.dta", convert_categoricals=False)
    for col in ("polsys","mediatype"):
        data[col] = data[col].map({1:1,2:3,3:2})
    data["socdiv"] = data["socdiv"].map({1:2,2:1})
    outcome = fit["outcome"]
    frame = data[["text_id","akteur_id",outcome,"polsys","socdiv","mediatype"]].dropna()
    model = NestedBernoulli(frame,outcome,points=fit["points_per_random_intercept"],null=len(theta)==3)
    cache = {}
    def objective(t):
        key = tuple(t)
        if key not in cache:
            cache[key] = -model.evaluate(t)
        return cache[key]
    d = len(theta)
    basis = np.eye(d)
    gradient = np.array([(objective(theta+2e-5*e)-objective(theta-2e-5*e))/(4e-5) for e in basis])
    hessians, summaries = {}, {}
    for step in (1e-4,2e-4,4e-4):
        hessian = np.empty((d,d))
        center = objective(theta)
        for i in range(d):
            hessian[i,i] = (objective(theta+step*basis[i])-2*center+objective(theta-step*basis[i]))/(step*step)
            for j in range(i):
                di,dj = step*basis[i],step*basis[j]
                hessian[i,j] = hessian[j,i] = (objective(theta+di+dj)-objective(theta+di-dj)-objective(theta-di+dj)+objective(theta-di-dj))/(4*step*step)
        eig = np.linalg.eigvalsh(hessian)
        covariance = np.linalg.inv(hessian) if eig.min()>0 else None
        summaries[step] = {"hessian_eigenvalues":eig.tolist(),"condition_number":float(np.linalg.cond(hessian)),
                           "scaled_gradient_g_cov_g":None if covariance is None else float(gradient@covariance@gradient),
                           "standard_errors":None if covariance is None else np.sqrt(np.diag(covariance)).tolist()}
        hessians[step] = hessian
        print(fit["model_id"], "curvature step", step, "minimum eigenvalue", eig.min(),flush=True)
    baseline = np.asarray(summaries[2e-4]["standard_errors"])
    step_change = {h:float(np.max(np.abs(np.asarray(v["standard_errors"])/baseline-1))) for h,v in summaries.items()}
    recorded_covariance = np.asarray(fit["covariance"])
    scaled_recorded = float(gradient@recorded_covariance@gradient)
    report = {"fit_path":str(path),"model_id":fit["model_id"],"candidate_sha256":CANDIDATE_SHA256,
              "gradient":gradient.tolist(),"gradient_infinity_norm":float(np.max(np.abs(gradient))),
              "scaled_gradient_using_saved_covariance":scaled_recorded,"scaled_gradient_threshold":1e-5,
              "scaled_gradient_check_passed":bool(scaled_recorded<1e-5),"step_checks":summaries,
              "max_relative_standard_error_changes_from_step_2e4":step_change,
              "max_difference_saved_vs_independent_hessian":float(np.max(np.abs(np.linalg.inv(recorded_covariance)-hessians[2e-4]))),
              "all_step_hessians_positive_definite":all(min(v["hessian_eigenvalues"])>0 for v in summaries.values()),
              "objective_evaluations":len(cache),"purpose":"Numerical acceptance verification of candidate finite-quadrature likelihood; not original Stata executable equivalence"}
    out = ROOT / "outputs/diagnostics/glmm"
    out.mkdir(parents=True,exist_ok=True)
    (out/(fit["model_id"]+"_independent_curvature.json")).write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:report[k] for k in ("model_id","gradient_infinity_norm","scaled_gradient_using_saved_covariance","scaled_gradient_check_passed","max_relative_standard_error_changes_from_step_2e4","all_step_hessians_positive_definite","objective_evaluations")},indent=2))


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--fit",type=Path,required=True)
    run(parser.parse_args().fit)
