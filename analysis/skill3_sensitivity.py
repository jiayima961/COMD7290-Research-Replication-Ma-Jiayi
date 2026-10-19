"""S1: country deletion diagnostic, separate from faithful author replication."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
import numpy as np
import pandas as pd
from scipy import stats
from ordinal_reproduction import prepare,design,group_ordinal,CommonOrdinal,fit_common

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs/verification/sensitivity'
NAMES=['mixed','majoritarian','contested','website','newspaper']
COUNTRIES={1:'Australia',2:'Germany',3:'Lebanon',4:'Switzerland',5:'Turkey',6:'United States'}
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 plan={'analysis_id':'S1','written_before_fitting_utc':datetime.now(timezone.utc).isoformat(),
 'question':'How dependent are M1 associations on retaining each of the six selected national contexts?',
 'rule':'Fit all six leave-one-country-out ordered logits with the original five dummy slopes, cutpoint ordering, ML and observed-information intervals. No deletion chosen after seeing estimates.',
 'assumption_changed':'The target sample and mix of national contexts change; not a new estimator of the same finite-sample estimand.',
 'scope':'Country influence diagnostic for ordinal M1 only. Not the authors alternative-link checks, not numerical integration sensitivity, not country-level causal identification.',
 'interpretation':'Report all coefficients, uncertainty, convergence and ranges. Do not choose a preferred deletion by p value or treat six fits as independent confirmation.',
 'student_acceptance':'pending'}
 if not (OUT/'plan.json').exists():
  (OUT/'plan.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
 rawpath=ROOT/'data/original/MedCon_Civility_item.dta'
 initial=hashlib.sha256(rawpath.read_bytes()).hexdigest()
 d=prepare(pd.read_stata(rawpath,convert_categoricals=False),tone=True)
 baseline=json.loads((ROOT/'outputs/reproduced/models/ordinal/M1_model.json').read_text())
 rows=[];fits=[]
 for country,name in COUNTRIES.items():
  s=d[d.country!=country];x,c=group_ordinal(design(s),s.tone.to_numpy(),5)
  result,cov,fit=fit_common(CommonOrdinal(x,c))
  if fit['status']!='converged':raise RuntimeError(f'Failed deletion {name}: {fit}')
  fits.append({'excluded_country':name,**{k:v for k,v in fit.items() if k!='information_eigenvalues'},'information_min_eigenvalue':float(min(fit['information_eigenvalues']))})
  for j,term in enumerate(NAMES):
   b=float(result.x[j]);se=float(np.sqrt(cov[j,j]));base=float(baseline['parameters'][j])
   rows.append({'analysis_id':'S1','excluded_country':name,'n':len(s),'contrast':term,'b':b,'se':se,
    'odds_ratio':float(np.exp(b)),'or_ci95_lower':float(np.exp(b-1.959963984540054*se)),
    'or_ci95_upper':float(np.exp(b+1.959963984540054*se)),'p_value':float(2*stats.norm.sf(abs(b/se))),
    'faithful_b':base,'difference_from_faithful_b':b-base,'same_sign':bool(np.sign(b)==np.sign(base)),'fit_status':fit['status']})
 pd.DataFrame(rows).to_csv(OUT/'country_deletion_coefficients.csv',index=False)
 pd.DataFrame(fits).to_csv(OUT/'country_deletion_fits.csv',index=False)
 summary=pd.DataFrame(rows).groupby('contrast').agg(min_OR=('odds_ratio','min'),max_OR=('odds_ratio','max'),same_sign_count=('same_sign','sum'),p_below_05_count=('p_value',lambda s:int((s<.05).sum())))
 summary.to_csv(OUT/'country_deletion_summary.csv')
 assert hashlib.sha256(rawpath.read_bytes()).hexdigest()==initial
 text=['# Separate country influence sensitivity','',
 'This AI-proposed sensitivity was planned before fitting and requires student review. All six countries were deleted in turn; no deletion was selected because of its result. The baseline remains the faithful M1 model. Each deletion changes the sample and target context mixture, so this is an influence diagnostic, not another estimate of an identical population quantity.','',
 '| Contrast | OR range over six deletions | Same direction | p below .05 |','|---|---:|---:|---:|']
 for term,r in summary.iterrows():text.append(f'| {term} | {r.min_OR:.3f} to {r.max_OR:.3f} | {int(r.same_sign_count)}/6 | {int(r.p_below_05_count)}/6 |')
 text+=['','Country contextual estimates can be sensitive to a single national setting because each political-system by division cell contains only one country. Article-level observations do not supply additional independent national institutional realizations. The p-value counts are descriptive stability summaries, not multiplicity-adjusted tests or a selection rule. Media contrasts remain associations; country deletion does not identify editorial gatekeeping as a cause. Full uncertainty and all deletion-specific results are in the adjacent CSV files.','',
 'Scope limit: this diagnostic evaluates M1 only and does not establish robustness of M2/M3, measurement validity, temporal generalizability or causal mechanisms.']
 (OUT/'README.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
 print(summary.to_string())
if __name__=='__main__':main()
