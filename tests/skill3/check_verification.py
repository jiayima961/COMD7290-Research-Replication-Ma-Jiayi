"""Independent source/data/ordinal verification and harmless negative recovery."""
from pathlib import Path
import importlib.util,json,hashlib
import numpy as np
import pandas as pd
import pyreadstat
from scipy import stats
from statsmodels.miscmodels.ordinal_model import OrderedModel

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/verification/independent_checks'
def main():
 OUT.mkdir(parents=True,exist_ok=True);checks=[]
 def check(name,passed,**details):
  checks.append(dict(check=name,passed=bool(passed),**details))
 # Separate raw reader and recodes, with original value-label metadata checked.
 rawpath=ROOT/'data/original/MedCon_Civility_item.dta'
 originalhash=hashlib.sha256(rawpath.read_bytes()).hexdigest()
 d,m=pyreadstat.read_dta(str(rawpath),apply_value_formats=False)
 country_labels=m.variable_value_labels['country']
 check('Country identifiers bound to original metadata',country_labels[3]=='LEB' and country_labels[4]=='SUI',labels=country_labels)
 auweb=d[(d.country==1)&(d.mediatype==3)]
 percentage=100*auweb.tone.eq(3).mean()
 check('Independent Australian website moderate percentage',percentage==1.,computed_percentage=percentage,denominator=len(auweb),reader='pyreadstat; raw website=3 and raw moderate tone=3')
 ref,_=pyreadstat.read_dta(str(ROOT/'data/original/MedCon_Civility_actref.dta'),apply_value_formats=False)
 check('Independent event and hierarchy counts',len(ref)==3770 and ref.actrefoutbin.sum()==192 and ref.actrefrecbin.sum()==196 and len(ref[['text_id','akteur_id']].drop_duplicates())==2453,
       reference_n=len(ref),outrage_events=int(ref.actrefoutbin.sum()),recognition_events=int(ref.actrefrecbin.sum()))
 # Fresh independent optimization and margins: no project likelihood/margin code.
 recoded=pd.DataFrame({'polsys':d.polsys.map({1:1,2:3,3:2}),'socdiv':d.socdiv.map({1:2,2:1}),'media':d.mediatype.map({1:1,2:3,3:2})})
 def matrix(frame):
  return np.column_stack([(frame[v].to_numpy()==level).astype(float) for v,level in [('polsys',2),('polsys',3),('socdiv',2),('media',2),('media',3)]])
 x=matrix(recoded);y=d.tone.to_numpy().astype(int)-1
 model=OrderedModel(y,x,distr='logit');fit=model.fit(method='bfgs',gtol=1e-9,maxiter=2000,disp=False)
 saved=json.loads((ROOT/'outputs/reproduced/models/ordinal/M1_model.json').read_text())
 check('Fresh independent ordered-logit MLE agrees',abs(fit.llf-saved['fit']['log_likelihood'])<1e-7 and max(abs(fit.params[:5]-np.array(saved['parameters'][:5])))<1e-6,
    independent_LL=float(fit.llf),maximum_slope_difference=float(max(abs(fit.params[:5]-np.array(saved['parameters'][:5])))),
    optimizer_return=bool(fit.mle_retvals['converged']),score_max_abs=float(max(abs(model.score(fit.params)))),scope='Independent optimization and parameterization of M1; not independent reoptimization of M2/M3.')
 cov=np.asarray(fit.cov_params());rows=[]
 savedames=pd.read_csv(ROOT/'outputs/reproduced/predictions/ordinal/M1_average_marginal_effects.csv')
 for var,level,label in [('polsys',2,'mixed'),('polsys',3,'majoritarian'),('socdiv',2,'contested'),('media',2,'website'),('media',3,'newspaper')]:
  a,b=recoded.copy(),recoded.copy();a[var]=level;b[var]=1;xa,xb=matrix(a),matrix(b)
  def effect(params):return (model.predict(params,exog=xa)-model.predict(params,exog=xb)).mean(axis=0)
  effect_value=effect(fit.params)
  gradient=np.column_stack([(effect(fit.params+np.eye(len(fit.params))[j]*1e-5)-effect(fit.params-np.eye(len(fit.params))[j]*1e-5))/2e-5 for j in range(len(fit.params))])
  se=np.sqrt(np.einsum('ki,ij,kj->k',gradient,cov,gradient))
  for category in range(5):
   savedrow=savedames[(savedames.term==('mediatype' if var=='media' else var))&(savedames.contrast==f'{level} versus 1')&(savedames.outcome==category)].iloc[0]
   estimate=effect_value[category];lo=estimate-1.959963984540054*se[category];hi=estimate+1.959963984540054*se[category]
   rows.append(dict(contrast=label,tone=category,estimate=estimate,se=se[category],ci_lower=lo,ci_upper=hi,
                    estimate_difference=estimate-savedrow.estimate,lower_difference=lo-savedrow.ci_lower,upper_difference=hi-savedrow.ci_upper))
 margins=pd.DataFrame(rows);margins.to_csv(OUT/'independent_ordinal_ames.csv',index=False)
 maxerr=float(np.max(abs(margins[['estimate_difference','lower_difference','upper_difference']].to_numpy())))
 check('All 25 ordinal AMEs and 50 CI endpoints independently reproduced',maxerr<1e-6,max_abs_difference=maxerr,method='Statsmodels fresh MLE, separate row-level predict, central-difference gradient, full covariance delta method')
 # Directly test boundary/error behavior, not wording in generated reports.
 spec=importlib.util.spec_from_file_location('verification',ROOT/'analysis/verify_and_package.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 check('Rounding mismatch cannot be hidden',module.classify(2.24,2.246459,2)=='discrepancy')
 check('Unavailable target cannot pass',module.classify(None,1.2,2)=='not_verifiable')
 check('Invalid fitted value cannot pass',module.classify(1.2,np.nan,2)=='not_verifiable')
 check('Exact integer comparison has no rounding allowance',module.classify(1700,1699,exact=True)=='discrepancy')
 # Harmless negative test on in-memory copy, followed by actual recovery.
 copied=d.copy(deep=True);copied.loc[copied.index[0],'tone']=99
 def validate_tone(frame):
  if not set(frame.tone.unique()).issubset({1,2,3,4,5}):raise ValueError('Invalid original tone category')
 detected=False
 try:validate_tone(copied)
 except ValueError:detected=True
 copied.loc[copied.index[0],'tone']=d.loc[d.index[0],'tone'];validate_tone(copied)
 recovered=bool(copied.tone.equals(d.tone))
 check('Harmless negative category test and recovery',detected and recovered,detection=detected,recovery=recovered,original_file_unchanged=hashlib.sha256(rawpath.read_bytes()).hexdigest()==originalhash)
 ledger=pd.read_csv(ROOT/'outputs/verification/comparison_all.csv')
 check('Comparison keys unique and unpublished targets not scored as agreement',not ledger.duplicated(['analysis_id','quantity']).any() and (ledger.loc[ledger.published_value.isna(),'comparison_status']=='not_verifiable').all())
 check('Seven recovered supplementary discrepancies retained',sum((ledger.analysis_id=='P1:AME')&(ledger.comparison_status=='discrepancy'))==7)
 (OUT/'checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
 print(json.dumps({'checks':len(checks),'passed':sum(c['passed'] for c in checks),'all_passed':all(c['passed'] for c in checks),'independent_AME_max_error':maxerr},indent=2))
 if not all(c['passed'] for c in checks):raise SystemExit(1)
if __name__=='__main__':main()
