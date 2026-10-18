"""Frequentist nested random-intercept Bernoulli ML with recursive mean-variance AGHQ.

Seven-point mean/variance adaptation is the source configuration. Likelihoods omit
binomial combination constants because the original observations are Bernoulli rows.
Identical item patterns can be frequency compressed without changing the likelihood.
"""
from collections import Counter
import json
from pathlib import Path
import time
import numpy as np
import pandas as pd
from numpy.polynomial.hermite_e import hermegauss
from scipy.optimize import minimize
from scipy.special import logsumexp, expit
from scipy.stats import norm
from statsmodels.tools.numdiff import approx_hess3, approx_fprime
from prepare_replication import ROOT, SPEC_VERSION, TERMS, design, load_data


class NestedBernoulli:
    def __init__(self, frame, outcome, points=7, null=False, compress=True,
                 adaptation_tolerance=2e-10, max_adaptation=400):
        self.outcome, self.points, self.null = outcome, points, null
        self.tolerance, self.max_adaptation = adaptation_tolerance, max_adaptation
        actor = frame.groupby(["text_id", "akteur_id"], observed=True, sort=True).agg(
            n=(outcome, "size"), s=(outcome, "sum"), polsys=("polsys", "first"),
            socdiv=("socdiv", "first"), mediatype=("mediatype", "first")).reset_index()
        patterns = Counter()
        for _, group in actor.groupby("text_id", sort=True):
            first = group.iloc[0]
            context = (int(first.polsys), int(first.socdiv), int(first.mediatype))
            pairs = tuple(sorted(zip(group.n.astype(int), group.s.astype(int))))
            key = (context, pairs) if compress else (context, pairs, str(first.text_id))
            patterns[key] += 1
        contexts, counts, ns, ss, actor_item, starts = [], [], [], [], [], []
        for j, (key, count) in enumerate(patterns.items()):
            contexts.append(key[0]); counts.append(count); starts.append(len(ns))
            for n, s in key[1]: ns.append(n); ss.append(s); actor_item.append(j)
        context_frame = pd.DataFrame(contexts, columns=["polsys", "socdiv", "mediatype"])
        self.X = np.ones((len(contexts), 1)) if null else design(context_frame)
        self.counts = np.array(counts)
        self.n, self.s = np.array(ns)[:, None], np.array(ss)[:, None]
        self.actor_item, self.starts = np.array(actor_item), np.array(starts)
        self.z, w = hermegauss(points)
        self.logw = np.log(w) - .5 * np.log(2 * np.pi)
        self.n_items = frame.text_id.nunique()
        self.n_actors = len(actor)
        self.n_rows = len(frame)
        self.evaluations = 0
        self.last_diagnostic = {}

    def _inner(self, eta, sigma, score=False):
        mu, sd = np.zeros_like(eta), np.ones_like(eta)
        n, s = self.n[..., None], self.s[..., None]
        converged = False
        for iteration in range(self.max_adaptation):
            v = mu[..., None] + sd[..., None] * self.z
            t = eta[..., None] + sigma * v
            logterms = s*t - n*np.logaddexp(0, t) + self.logw + np.log(sd)[..., None] + .5*(self.z**2-v*v)
            logint = logsumexp(logterms, axis=-1)
            w = np.exp(logterms-logint[..., None])
            newmu = np.sum(w*v, axis=-1)
            variance = np.sum(w*(v-newmu[..., None])**2, axis=-1)
            newsd = np.sqrt(np.maximum(variance, 1e-12))
            delta = max(np.max(np.abs(newmu-mu)), np.max(np.abs(newsd-sd)))
            damping = 1.0 if iteration < 20 else .5
            mu, sd = mu+damping*(newmu-mu), sd+damping*(newsd-sd)
            if delta < self.tolerance:
                converged = True
                break
        if not converged:
            raise ArithmeticError(f"Inner posterior moment adaptation did not converge; delta={delta}")
        v = mu[..., None]+sd[..., None]*self.z
        t = eta[..., None]+sigma*v
        logterms = s*t-n*np.logaddexp(0,t)+self.logw+np.log(sd)[...,None]+.5*(self.z**2-v*v)
        logint = logsumexp(logterms,axis=-1)
        if not score: return logint, iteration+1
        w = np.exp(logterms-logint[...,None])
        residual = s-n*expit(t)
        return logint, np.sum(w*residual,axis=-1), np.sum(w*residual*sigma*v,axis=-1), iteration+1

    def evaluate(self, theta, score=False, contributions=False):
        self.evaluations += 1
        p = self.X.shape[1]
        beta = np.asarray(theta[:p])
        sigma_item, sigma_actor = np.exp(theta[p:])
        eta = self.X @ beta
        mu, sd = np.zeros(len(eta)), np.ones(len(eta))
        converged = False
        maxinner = 0
        for iteration in range(self.max_adaptation):
            v = mu[:,None]+sd[:,None]*self.z
            delta = eta[:,None]+sigma_item*v
            inner, ni = self._inner(delta[self.actor_item], sigma_actor)
            maxinner = max(maxinner, ni)
            itemlog = np.add.reduceat(inner, self.starts, axis=0)
            logterms = itemlog+self.logw+np.log(sd)[:,None]+.5*(self.z**2-v*v)
            normalizer = logsumexp(logterms,axis=-1)
            w = np.exp(logterms-normalizer[:,None])
            newmu = np.sum(w*v,axis=-1)
            newsd = np.sqrt(np.maximum(np.sum(w*(v-newmu[:,None])**2,axis=-1),1e-12))
            diff = max(np.max(np.abs(newmu-mu)),np.max(np.abs(newsd-sd)))
            damping = 1.0 if iteration < 20 else .5
            mu, sd = mu+damping*(newmu-mu), sd+damping*(newsd-sd)
            if diff < self.tolerance:
                converged=True; break
        if not converged: raise ArithmeticError(f"Outer posterior adaptation failed: {diff}")
        v = mu[:,None]+sd[:,None]*self.z
        innerresult = self._inner((eta[:,None]+sigma_item*v)[self.actor_item],sigma_actor,score=score)
        inner = innerresult[0]
        itemlog = np.add.reduceat(inner,self.starts,axis=0)
        logterms=itemlog+self.logw+np.log(sd)[:,None]+.5*(self.z**2-v*v)
        normalizer=logsumexp(logterms,axis=-1)
        self.last_diagnostic={"outer_adaptation_iterations":iteration+1,"inner_adaptation_max_iterations":maxinner,
                              "moment_tolerance":self.tolerance,"points_per_level":self.points,
                              "compressed_item_patterns":len(self.counts),"adaptation_converged":True}
        ll = float(self.counts @ normalizer)
        if contributions: return normalizer
        if not score: return ll
        post=np.exp(logterms-normalizer[:,None])
        residual=np.add.reduceat(innerresult[1],self.starts,axis=0)
        actor_score=np.add.reduceat(innerresult[2],self.starts,axis=0)
        gbeta=self.X.T@(self.counts*np.sum(post*residual,axis=1))
        gu=np.sum(self.counts*np.sum(post*residual*sigma_item*v,axis=1))
        ga=np.sum(self.counts*np.sum(post*actor_score,axis=1))
        return ll,np.r_[gbeta,gu,ga]


def fit_model(frame,outcome,model_id,output_root=ROOT,points=7,null=False,start=None):
    model=NestedBernoulli(frame,outcome,points,null)
    p=model.X.shape[1]
    initial=np.zeros(p+2)
    initial[0]=np.log(frame[outcome].mean()/(1-frame[outcome].mean()))
    if start is not None: initial=np.array(start,float)
    t0=time.perf_counter(); trace=[]; rejected_trials=[]
    def integrated_objective(t):
        try:
            ll,g=model.evaluate(t,score=True)
            return -ll,-g
        except ArithmeticError as exc:
            rejected_trials.append({'parameters':t.tolist(),'reason':str(exc)})
            return np.inf,np.zeros_like(t)
    def callback(t):
        value=-model.evaluate(t)
        trace.append({"iteration":len(trace)+1,"negative_log_likelihood":value,"parameters":t.tolist()})
        if len(trace)%5==0: print(model_id,'warmup',len(trace),'nll',round(value,8),flush=True)
    print(model_id,'start', 'patterns',len(model.counts),'params',initial.tolist(),flush=True)
    # Integrated scores provide a fast starting search. Adaptive-node derivatives
    # are then included by numerical differentiation of the actual Q-point target.
    warm=minimize(integrated_objective,initial,jac=True,method='BFGS',callback=callback,
                  options={'gtol':2e-4,'maxiter':100})
    print(model_id,'score-search complete',warm.message,'nll',warm.fun,flush=True)
    objective=lambda t:-model.evaluate(t)
    refined=minimize(objective,warm.x,jac='3-point',method='BFGS',
                     options={'gtol':2e-5,'maxiter':100,'finite_diff_rel_step':1e-4})
    theta=refined.x
    grad=approx_fprime(theta,objective,epsilon=2e-5,centered=True)
    hess=approx_hess3(theta,objective,epsilon=2e-4)
    eig=np.linalg.eigvalsh(hess)
    cov=np.linalg.inv(hess) if eig.min()>0 else np.full_like(hess,np.nan)
    accepted=bool(np.linalg.norm(grad,np.inf)<.005 and eig.min()>1e-5 and np.all(np.isfinite(theta)))
    ll=model.evaluate(theta)
    se=np.sqrt(np.diag(cov)); z=theta/se
    term_names=(["intercept"] if null else TERMS)+["log_sd_item","log_sd_actor"]
    coefs=pd.DataFrame({'model_id':model_id,'outcome':outcome,'term':term_names,'estimate':theta,'se':se,
                        'z':z,'p_value':2*norm.sf(abs(z)),'ci95_lower':theta-1.95996398454*se,
                        'ci95_upper':theta+1.95996398454*se})
    coefs['odds_ratio']=np.where(np.arange(p+2)<p,np.exp(theta),np.nan)
    coefs['or_ci95_lower']=np.where(np.arange(p+2)<p,np.exp(theta-1.95996398454*se),np.nan)
    coefs['or_ci95_upper']=np.where(np.arange(p+2)<p,np.exp(theta+1.95996398454*se),np.nan)
    coefs['specification_version']=SPEC_VERSION
    coefs['status']='converged' if accepted else 'failed_validation'
    variances=np.exp(2*theta[p:])
    result={'model_id':model_id,'outcome':outcome,'specification_version':SPEC_VERSION,
            'family':'Bernoulli','link':'logit','estimator':'frequentist marginal maximum likelihood',
            'integration':'recursive mean-variance adaptive Gauss-Hermite','points_per_random_intercept':points,
            'parameter_names':term_names,'parameters':theta.tolist(),'covariance':cov.tolist(),
            'variance_item':float(variances[0]),'variance_actor':float(variances[1]),
            'variance_se':(2*variances*se[p:]).tolist(),
            'icc_same_item_different_actor':float(variances[0]/(sum(variances)+np.pi**2/3)),
            'icc_same_actor':float(sum(variances)/(sum(variances)+np.pi**2/3)),
            'log_likelihood':ll,'minus2_log_likelihood':-2*ll,'aic':-2*ll+2*len(theta),
            'n_observations':model.n_rows,'n_items':model.n_items,'n_actor_groups':model.n_actors,
            'converged_and_validated':accepted,'optimizer_success':bool(refined.success),
            'optimizer_message':str(refined.message),'warmup_message':str(warm.message),
            'gradient':grad.tolist(),'gradient_infinity_norm':float(np.linalg.norm(grad,np.inf)),
            'hessian_eigenvalues':eig.tolist(),'hessian_step':2e-4,
            'runtime_seconds':time.perf_counter()-t0,'likelihood_evaluations':model.evaluations,
            'initial_parameters':initial.tolist(),'adaptation':model.last_diagnostic,'trace':trace,
            'rejected_optimizer_trials':rejected_trials,
            'implementation_note':'Adaptive-grid finite-difference polish follows integrated-score warmup; warmup alone is not acceptance. Original build/internal quadrature details are unpinned; inspect separate independent integral and quadrature checks.',
            'research_data_transformed_in_place':False}
    out=Path(output_root)/'outputs/reproduced/models';out.mkdir(parents=True,exist_ok=True)
    coefs.to_csv(out/(model_id+'_coefficients.csv'),index=False)
    (out/(model_id+'_fit.json')).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(model_id,'done','accepted',accepted,'LL',ll,'runtime',result['runtime_seconds'],flush=True)
    if not accepted: raise ArithmeticError(f'{model_id} failed convergence/covariance validation; inspect saved artifact.')
    return result


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--model',choices=['M2','M3','M2_null','M3_null'],required=True)
    parser.add_argument('--points',type=int,default=7);parser.add_argument('--output-root',type=Path,default=ROOT)
    args=parser.parse_args();_,frame=load_data()
    y='actrefoutbin' if args.model.startswith('M2') else 'actrefrecbin'
    fit_model(frame,y,args.model,args.output_root,args.points,args.model.endswith('null'))
