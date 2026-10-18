"""Prior-marginal probabilities and discrete AMEs with full-covariance delta SEs.

Seven-point tensor GH is explicit; historical Stata prediction grid reduction is
unrecovered. High-point combined-normal calculations quantify integration error.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from numpy.polynomial.hermite_e import hermegauss
from scipy.special import expit
from statsmodels.tools.numdiff import approx_fprime
from prepare_replication import ROOT, load_data, design, SPEC_VERSION

def probability(theta, x, points=7, representation='tensor'):
    z,w=hermegauss(points); w=w/np.sqrt(2*np.pi)
    eta=x@theta[:6]; su,sa=np.exp(theta[6:])
    if representation=='tensor':
        return np.sum(expit(eta[:,None,None]+su*z[None,:,None]+sa*z[None,None,:])*w[None,:,None]*w[None,None,:],axis=(1,2))
    return expit(eta[:,None]+np.hypot(su,sa)*z)@w

def run(root=ROOT):
    root=Path(root); _,df=load_data(root)
    contexts=df.groupby(['polsys','socdiv','mediatype']).size().reset_index(name='n')
    weights=contexts.n.to_numpy()/len(df)
    rows=[]; checks=[]
    for mid in ['M2','M3']:
        fit=json.loads((root/f'outputs/reproduced/models/{mid}_fit.json').read_text())
        if not fit['converged_and_validated']: raise ValueError('Unvalidated model input')
        theta=np.array(fit['parameters']); cov=np.array(fit['covariance'])
        for var,levels in [('polsys',[1,2,3]),('socdiv',[1,2]),('mediatype',[1,2,3])]:
            matrices={level:design(contexts.assign(**{var:level})) for level in levels}
            for level in levels:
                for kind in ['probability','discrete_ame']:
                    if kind=='discrete_ame' and level==1: continue
                    def f(t,points=7,rep='tensor'):
                        val=weights@probability(t,matrices[level],points,rep)
                        if kind=='discrete_ame': val-=weights@probability(t,matrices[1],points,rep)
                        return float(val)
                    estimate=f(theta); grad=approx_fprime(theta,f,epsilon=1e-5,centered=True)
                    se=float(np.sqrt(grad@cov@grad))
                    exact=f(theta,161,'combined'); exact81=f(theta,81,'combined'); alt7=f(theta,7,'combined')
                    rows.append(dict(model_id=mid,outcome=fit['outcome'],predictor=var,level=level,reference_level=1,statistic=kind,
                        estimate=estimate,se=se,ci95_lower=estimate-1.95996398454*se,ci95_upper=estimate+1.95996398454*se,
                        scale='probability' if kind=='probability' else 'probability_difference',
                        convention='prior marginal; empirical reference-row weighting; tensor GH7 per intercept',
                        specification_version=SPEC_VERSION,status='computed_historical_finite_grid_unconfirmed'))
                    checks.append(dict(model_id=mid,predictor=var,level=level,statistic=kind,tensor7=estimate,combined7=alt7,
                        combined81=exact81,combined161=exact,tensor7_minus_161=estimate-exact,combined81_minus_161=exact81-exact))
    dest=root/'outputs/reproduced/predictions'; dest.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_csv(dest/'binary_margins_ames.csv',index=False)
    pd.DataFrame(checks).to_csv(root/'outputs/diagnostics/binary_prediction_integration.csv',index=False)
    print('Saved',len(rows),'binary margins/AMEs and integration comparisons.')

if __name__=='__main__':run()
