"""Compare freshly fitted estimates with separately stored published targets."""
import json
import numpy as np
import pandas as pd
from scipy.special import xlogy,xlog1py
from scipy.stats import chi2
from prepare_replication import ROOT,load_data

MAP={'mixed':'mixed_vs_consensus','majoritarian':'majoritarian_vs_consensus','contested':'contested_vs_stable','website':'website_vs_blog','newspaper':'newspaper_vs_blog'}
ORD={'mixed':'2.polsys','majoritarian':'3.polsys','contested':'2.socdiv','website':'2.mediatype','newspaper':'3.mediatype'}
def run():
    target=pd.read_csv(ROOT/'outputs/published/model_targets.csv')
    ordinal=pd.read_csv(ROOT/'outputs/reproduced/models/ordinal/ordinal_coefficients.csv')
    rows=[]; hypotheses=[]
    for r in target.to_dict('records'):
        mid=r['model_id']
        if mid=='M1':
            v=ordinal[(ordinal.analysis_id==mid)&(ordinal.term==ORD[r['contrast']])].iloc[0]
        else:
            data=pd.read_csv(ROOT/f'outputs/reproduced/models/{mid}_coefficients.csv')
            v=data[data.term==MAP[r['contrast']]].iloc[0]
        for quantity,key in [('b','estimate'),('se','se'),('odds_ratio','odds_ratio')]:
            value=float(v[key]); published=float(r[quantity]); difference=value-published
            rows.append(dict(model_id=mid,contrast=r['contrast'],quantity=quantity,published_value=published,reproduced_value=value,
                difference=difference,within_display_rounding=abs(difference)<.005000001,display_tolerance=.005,tolerance=.005,
                status='computed_within_printed_rounding' if abs(difference)<.005000001 else 'computed_discrepancy_retained',
                comparison_rule='two-decimal printed rounding interval; not a model-validity test',source_locator=r['source_locator'],
                reproduction_status='same_statistical_model; historical_finite_grid_unconfirmed' if mid!='M1' else 'validated_model_reproduction'))
        contrast=r['contrast']; h=None; direction=None
        if contrast=='majoritarian':h='H1b' if mid=='M3' else 'H1a';direction=-1 if mid=='M3' else 1
        elif contrast=='contested':h='H2b' if mid=='M3' else 'H2a';direction=-1 if mid=='M3' else 1
        elif contrast in ['website','newspaper']:h='H3b' if mid=='M3' else 'H3a';direction=1 if mid=='M3' else -1
        if h:
            beta=float(v['estimate']);p=float(v['p_value']);sign=np.sign(beta)==direction
            conclusion='consistent_with_prediction' if sign and p<.05 else ('significant_opposite_direction' if not sign and p<.05 else 'not_statistically_supported')
            hypotheses.append(dict(hypothesis_id=h,model_id=mid,contrast=contrast,predicted_sign=direction,beta=beta,se=float(v['se']),odds_ratio=float(v['odds_ratio']),p_value=p,
                conclusion=conclusion,scope='associational; original directional target; two-sided reported Wald uncertainty'))
    pd.DataFrame(rows).to_csv(ROOT/'outputs/comparison.csv',index=False)
    pd.DataFrame(hypotheses).to_csv(ROOT/'outputs/reproduced/hypothesis_tests.csv',index=False)
    _,frame=load_data();lr=[]
    for mid,y in [('M2','actrefoutbin'),('M3','actrefrecbin')]:
        full=json.loads((ROOT/f'outputs/reproduced/models/{mid}_fit.json').read_text())
        null=json.loads((ROOT/f'outputs/reproduced/models/{mid}_null_fit.json').read_text())
        mu=frame[y].mean(); ll0=float(np.sum(xlogy(frame[y],mu)+xlog1py(1-frame[y],-mu)))
        lr.append(dict(model_id=mid,full_ll=full['log_likelihood'],nested_null_ll=null['log_likelihood'],single_level_null_ll=ll0,
            full_vs_nested_null_lr=2*(full['log_likelihood']-null['log_likelihood']),full_vs_nested_null_df=5,
            full_vs_nested_null_p=chi2.sf(2*(full['log_likelihood']-null['log_likelihood']),5),
            nested_null_vs_single_null_lr=2*(null['log_likelihood']-ll0),
            nested_vs_single_p_status='not_regular_chi_square; two_variances_on_boundary; original_mixture_rule_unrecovered',
            source_minus2ll=1326.48 if mid=='M2' else 1421.27,reproduced_minus2ll=full['minus2_log_likelihood']))
    pd.DataFrame(lr).to_csv(ROOT/'outputs/diagnostics/binary_likelihood_comparisons.csv',index=False)
    print('Saved',len(rows),'coefficient comparisons and',len(hypotheses),'hypothesis targets.')
if __name__=='__main__':run()
