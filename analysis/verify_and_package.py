"""Source-ledger reconciliation; reads saved scientific results without refitting.

Run after analysis/run_replication.py. Published numbers below are comparison
targets only, never model inputs. Missing targets are not treated as matches.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json
import numpy as np
import pandas as pd
from scipy import stats

ROOT=Path(__file__).resolve().parents[1]
COUNTRIES={1:'Australia',2:'Germany',3:'Lebanon',4:'Switzerland',5:'Turkey',6:'United States'}
CONTRASTS=['mixed','majoritarian','contested','website','newspaper']
TERMS1=['2.polsys','3.polsys','2.socdiv','2.mediatype','3.mediatype']
TERMSB=['mixed_vs_consensus','majoritarian_vs_consensus','contested_vs_stable','website_vs_blog','newspaper_vs_blog']
APPENDIX='https://medcon-doc.github.io/documentation/content-analysis/additional-analyses/civility-outrage_paper/'

def classify(original,reproduced,decimals=None,exact=False):
    if original is None or pd.isna(original):return 'not_verifiable'
    if not np.isfinite(reproduced):return 'not_verifiable'
    tolerance=0.0 if exact else .5*10.**(-decimals)
    if abs(float(reproduced)-float(original)) <= tolerance+1e-12:
        return 'exact_integer_agreement' if exact else 'within_published_rounding'
    return 'discrepancy'

def reconcile(root=ROOT,out=None):
    root=Path(root).resolve();out=Path(out or root/'outputs/verification').resolve();out.mkdir(parents=True,exist_ok=True)
    rows=[];used=set()
    def add(aid,quantity,original,value,source,evidence,decimals=2,exact=False,explanation='',cause='not_assigned',confidence='not_applicable',validation='comparison_only'):
        key=(aid,quantity)
        if key in used:raise ValueError(f'Duplicate comparison identity: {key}')
        used.add(key)
        val=None if value is None or pd.isna(value) else float(value)
        status=classify(original,np.nan if val is None else val,decimals,exact)
        rows.append(dict(analysis_id=aid,quantity=quantity,published_value=original,reproduced_value=val,
             difference=None if original is None or val is None else val-float(original),
             tolerance=None if original is None else (0 if exact else .5*10.**(-decimals)),
             comparison_status=status,source_locator=source,reproduced_evidence=evidence,
             comparison_rule='no published numeric target' if original is None else ('exact integer count' if exact else f'absolute difference <= half of one unit in the {decimals}-decimal display'),
             explanation=explanation,cause_category=cause,cause_confidence=confidence,validation_status=validation))
    def csv(rel):return pd.read_csv(root/rel)
    def js(rel):return json.loads((root/rel).read_text(encoding='utf-8'))
    # Tables 3 and 4: retain the original 45-cell comparison unchanged.
    for r in csv('outputs/comparison.csv').to_dict('records'):
        why='Agreement is at printed precision; original unrounded estimates are unavailable.'
        cause='display_rounding';confidence='demonstrated'
        if not r['within_display_rounding']:
            why='M2 mixed OR rounds to 2.25 rather than 2.24. Rounded source b=.81 is compatible with OR=2.24; a typo is not established. Historical finite-grid/optimization differences remain a possible explanation.'
            cause='unresolved_numerical_difference';confidence='possible_not_proven'
        add(r['model_id'],r['contrast']+':'+r['quantity'],r['published_value'],r['reproduced_value'],r['source_locator'],'outputs/comparison.csv',explanation=why,cause=cause,confidence=confidence,validation='validated_faithful_fit_historical_grid_unconfirmed' if r['model_id']!='M1' else 'validated_faithful_fit')
    target=csv('outputs/published/model_targets.csv')
    for mid in ['M1','M2','M3']:
        rel='outputs/reproduced/models/ordinal/ordinal_coefficients.csv' if mid=='M1' else f'outputs/reproduced/models/{mid}_coefficients.csv'
        coef=csv(rel)
        if mid=='M1':coef=coef.query("analysis_id=='M1' and scale=='slope'")
        for contrast,term in zip(CONTRASTS,TERMS1 if mid=='M1' else TERMSB):
            r=coef.loc[coef.term==term].iloc[0]
            p=float(r.p_value)
            actual=3 if p<.001 else 2 if p<.01 else 1 if p<.05 else 0
            src=target[(target.model_id==mid)&(target.contrast==contrast)].iloc[0].p_reported
            wanted={'<.001':3,'<.01':2,'<.05':1,'not significant at .05':0}[src]
            add(mid,contrast+':significance_tier',wanted,actual,'Article Table 3' if mid=='M1' else 'Article Table 4',rel,exact=True,explanation='0 none; 1 p<.05; 2 p<.01; 3 p<.001. Matching stars alone is not numerical or model validation.')
    m1=js('outputs/reproduced/models/ordinal/M1_model.json')
    add('M1','N',1700,m1['input_n'],'Article Table 3 p.283','outputs/reproduced/models/ordinal/M1_model.json',exact=True)
    add('M1','log_likelihood',-724.00,m1['fit']['log_likelihood'],'Article Table 3 p.283','outputs/reproduced/models/ordinal/M1_model.json')
    add('M1','McFadden_R2',.09,m1['mcfadden_r2'],'Article Table 3 p.283','outputs/reproduced/models/ordinal/M1_model.json',explanation='Numerical value supports the Table 3 label; this is not literal explained outcome variance.')
    add('M1','prose_Nagelkerke_R2',.09,m1['nagelkerke_r2'],'Article Results p.281','outputs/reproduced/models/ordinal/M1_model.json',explanation='Nagelkerke=.131474 while McFadden=.089014. Table/prose measure-label conflict; production origin not established.',cause='source_label_conflict',confidence='strong_direct_evidence')
    bounds=[[1.03,2.14],[.35,.83],[1.24,2.31],[.11,.25],[.20,.40]]
    coef=csv('outputs/reproduced/models/ordinal/ordinal_coefficients.csv').query("analysis_id=='M1' and scale=='slope'")
    for term,contrast,bd in zip(TERMS1,CONTRASTS,bounds):
        r=coef.loc[coef.term==term].iloc[0]
        for quantity,original,value in [('OR_CI95_lower',bd[0],r.or_ci_lower),('OR_CI95_upper',bd[1],r.or_ci_upper)]:
            add('M1',contrast+':'+quantity,original,value,'Article Results pp.281–283','outputs/reproduced/models/ordinal/ordinal_coefficients.csv')
    for mid in ['M2','M3']:
        rel=f'outputs/reproduced/models/{mid}_fit.json';fit=js(rel)
        for label,key,wanted in [('items','n_items',1183),('actor_statement_groups','n_actor_groups',2453),('references','n_observations',3770)]:
            add(mid,'N_'+label,wanted,fit[key],'Article Table 4 p.286',rel,exact=True)
        add(mid,'minus2_log_likelihood',1326.48 if mid=='M2' else 1421.27,fit['minus2_log_likelihood'],'Article Table 4 p.286',rel,
            explanation='M2 differs by .076979; original executable log and adaptive-grid internals are not recovered. No specific cause is proven.' if mid=='M2' else 'Agrees at displayed precision.',
            cause='unresolved_numerical_difference' if mid=='M2' else 'display_rounding',confidence='possible_not_proven' if mid=='M2' else 'demonstrated')
        for key in ['variance_item','variance_actor','icc_same_item_different_actor','icc_same_actor','aic','gradient_infinity_norm']:
            add(mid,key,None,fit[key],'Not numerically reported in Table 4',rel,explanation='Calculated and saved; cannot certify numerical equality without an original target.')
        for i,name in enumerate(fit['parameter_names']):
            add(mid,'full_parameter:'+name,None,fit['parameters'][i],'Full unrounded parameter vector not published',rel)
            add(mid,'parameter_SE:'+name,None,np.sqrt(fit['covariance'][i][i]),'Full unrounded covariance/SE vector not published',rel)
        for i,se in enumerate(fit['variance_se']):
            add(mid,'variance_SE:'+str(i),None,se,'Random-intercept variance SE not published',rel)
    # Table 2: all 18 country-media distributions and three pooled rows.
    table2={1:[[78,16,4,1,1],[97,2,11,0,0],[100,0,0,0,0]],2:[[74,14,6,4,2],[96,4,0,0,0],[89,11,0,0,0]],
      4:[[93,4,4,0,0],[97,3,0,0,0],[95,4,0,1,0]],3:[[86,6,4,3,1],[85,14,1,0,0],[80,12,5,2,1]],
      5:[[54,39,2,5,0],[93,7,0,0,0],[86,10,4,0,0]],6:[[81,16,1,2,0],[99,1,0,0,0],[98,2,0,0,0]]}
    pct=csv('outputs/reproduced/descriptives/ordinal/item_tone_percent_country_media.csv')
    for country,media_rows in table2.items():
        for medium,values in enumerate(media_rows,1):
            r=pct[(pct.country==country)&(pct.mediatype==medium)].iloc[0]
            aid=f'D1:{COUNTRIES[country]}:medium{medium}'
            for category,original in enumerate(values):
                anomaly=country==1 and medium==2 and category==2
                add(aid,'tone'+str(category)+'_percent',original,r[str(category)],'Article Table 2 p.282','outputs/reproduced/descriptives/ordinal/item_tone_percent_country_media.csv',decimals=0,
                 explanation='The visually checked source prints 11; raw data give 1. Printed row sums to 110 although its total is 100. Strong evidence of an isolated publication-table error; no erratum identifies production origin.' if anomaly else 'Whole-percent rounding; some independently rounded rows sum to 101.',
                 cause='likely_source_table_error' if anomaly else 'display_rounding',confidence='strong_direct_evidence' if anomaly else 'demonstrated')
            add(aid,'total_percent',100,sum(float(r[str(j)]) for j in range(5)),'Article Table 2 p.282','outputs/reproduced/descriptives/ordinal/item_tone_percent_country_media.csv',decimals=0)
    # Calculate pooled rows from original data, not from rounded country percentages.
    raw=pd.read_stata(root/'data/original/MedCon_Civility_item.dta',convert_categoricals=False)
    raw['medium']=raw.mediatype.map({1:1,2:3,3:2});raw['y']=raw.tone-1
    for medium,values in enumerate([[75,18,3,3,1],[95,5,0,0,0],[91,7,2,1,0]],1):
        s=raw[raw.medium==medium]
        for j,original in enumerate(values):
            add(f'D1:pooled:medium{medium}','tone'+str(j)+'_percent',original,100*(s.y==j).mean(),'Article Table 2 p.282','data/original/MedCon_Civility_item.dta; independent pandas aggregation',decimals=0)
        add(f'D1:pooled:medium{medium}','total_percent',100,100.,'Article Table 2 p.282','data/original/MedCon_Civility_item.dta',decimals=0)
    # Article reference descriptives and all graph-only country-by-media cells.
    ref=csv('outputs/reproduced/descriptives/ordinal/reference_descriptives.csv')
    source_maps={'actrefoutbin':{'overall':[5.1],'mediatype':[7.7,4.1,3.8],'country':[3.8,7.8,4.5,3.7,8.8,3.0]},
                 'actrefrecbin':{'overall':[5.2],'mediatype':[3.2,5.2,7.0],'country':[2.8,5.3,18.0,3.0,5.3,5.5]}}
    for outcome,maps in source_maps.items():
        for group,values in maps.items():
            for j,original in enumerate(values,1):
                term='overall' if group=='overall' else f'{group}={j}'
                r=ref[(ref.outcome==outcome)&(ref.grouping==group)&(ref.term==term)].iloc[0]
                add(f'D2:{outcome}',term+':percent',original,100*r.estimate,'Article Results pp.284–285','outputs/reproduced/descriptives/ordinal/reference_descriptives.csv',decimals=1)
    for r in ref.to_dict('records'):
        for q in ['n','missing_n','estimate','sd','min','max']:
            add(f'D2:{r["outcome"]}:{r["term"]}',q,None,r[q],'Figure 2 or author descriptive syntax; full numeric summaries not published','outputs/reproduced/descriptives/ordinal/reference_descriptives.csv')
    # Official reliability page: 30 point values and five non-repeated sample sizes.
    rel='outputs/reproduced/reliability/primary_website_comparison.csv';reliability=csv(rel)
    for r in reliability.to_dict('records'):
        add('R:'+r['analysis_id'],r['coefficient'],r['published_numeric'],r['computed_estimate'],r['source_url']+' '+r['source_locator'],rel)
    for aid,g in reliability.groupby('analysis_id'):
        r=g.iloc[0];add('R:'+aid,'n_any_rating',r.published_n_any_rating,r.computed_n_any_rating,'Official reliability page main-stage first/second slot table',rel,exact=True)
    for r in csv('outputs/reproduced/reliability/reliability_coefficients.csv').to_dict('records'):
        for q in ['estimate','se','ci95_low','ci95_high','df','n_expected','n_observed','n_rating_slots','n_categories']:
            if q=='estimate' and r['selection']=='two_slots':continue
            add('R_full:'+r['analysis_id']+':'+r['coefficient'],q,None,r[q],'Official page has no corresponding all-slot point or uncertainty target','outputs/reproduced/reliability/reliability_coefficients.csv',
                explanation='All author-selected slots and conditional uncertainty are computed; original package build unpinned. Two positional slots need not be two different named humans; repeated coders and -99 nominal categories are retained per author syntax.')
    # Binary AMEs and 20 interval endpoints in the main article.
    bpub={'M2':[[.03,-.00,.06],[-.01,-.04,.02],[-.00,-.02,.01],[-.05,-.07,-.02],[-.04,-.06,-.01]],
          'M3':[[-.00,-.03,.03],[-.02,-.05,.01],[.03,.01,.05],[.02,.00,.04],[.04,.02,.06]]}
    bp=csv('outputs/reproduced/predictions/binary_margins_ames.csv')
    order=[('polsys',2),('polsys',3),('socdiv',2),('mediatype',2),('mediatype',3)]
    for mid in ['M2','M3']:
        for contrast,(pred,level),published in zip(CONTRASTS,order,bpub[mid]):
            r=bp[(bp.model_id==mid)&(bp.predictor==pred)&(bp.level==level)&(bp.statistic=='discrete_ame')].iloc[0]
            for q,original in zip(['estimate','ci95_lower','ci95_upper'],published):
                add(mid+':AME',contrast+':'+q,original,r[q],'Article pp.286–287','outputs/reproduced/predictions/binary_margins_ames.csv',explanation='Prior random-effect marginal standardized discrete contrast. Negative zero is display, not an exact zero; observational quantity, not identified treatment effect.')
    for r in bp.to_dict('records'):
        for q in ['estimate','se','ci95_lower','ci95_upper']:
            if r['statistic']=='discrete_ame' and q!='se':continue
            add(f'{r["model_id"]}:prediction:{r["predictor"]}:{r["level"]}:{r["statistic"]}',q,None,r[q],'Figure 3 does not print full probability and SE vectors','outputs/reproduced/predictions/binary_margins_ames.csv')
    # Recovered primary supplement, numeric cells in row-major category order.
    apub=[[[ -.05,-.09,-.01],[.03,.00,.06],[.01,.00,.01],[.01,.00,.01],[.00,-.00,.00]],
          [[ .05,.02,.09],[-.04,-.06,-.01],[-.01,-.01,-.00],[-.01,-.01,-.00],[.00,-.00,.00]],
          [[-.05,-.08,-.02],[.04,.02,.06],[.01,.00,.01],[.01,.00,.01],[.00,-.00,.00]],
          [[ .19,.15,.23],[-.14,-.17,-.11],[-.03,-.04,-.02],[-.02,-.03,-.01],[-.01,-.01,-.00]],
          [[ .16,.12,.20],[-.12,-.15,-.08],[-.03,-.04,-.01],[-.02,-.02,-.01],[-.01,-.01,-.00]]]
    oa=csv('outputs/reproduced/predictions/ordinal/M1_average_marginal_effects.csv')
    for contrast,(pred,level),cats in zip(CONTRASTS,order,apub):
        for category,values in enumerate(cats):
            r=oa[(oa.term==pred)&(oa.contrast==f'{level} versus 1')&(oa.outcome==category)].iloc[0]
            for q,original in zip(['estimate','ci_lower','ci_upper'],values):
                add('P1:AME',f'{contrast}:tone{category}:{q}',original,r[q],APPENDIX+' Average Marginal Effects table; cached primary page accessed 2026-10-19','outputs/reproduced/predictions/ordinal/M1_average_marginal_effects.csv',
                   explanation='Live URL returned 404; cached primary table is the comparison source. Seven cells narrowly miss the displayed rounding interval. Different postestimation numerics, transcription or table production remain possibilities; cause not established. Do not widen tolerance after seeing results.',
                   cause='unresolved_postestimation_or_source_difference',confidence='possible_not_proven')
    for rel in ['outputs/reproduced/predictions/ordinal/M1_predictive_margins.csv','outputs/reproduced/descriptives/ordinal/item_descriptives.csv']:
        for i,r in enumerate(csv(rel).to_dict('records')):
            for q in (['estimate','se','ci_lower','ci_upper'] if 'predictions' in rel else ['n','missing_n','estimate','sd','min','max']):
                add('P1:probabilities' if 'predictions' in rel else 'D1:full_summary',f'row{i}:{q}',None,r[q],'Graph-only or author descriptive syntax; no exact numeric target',rel)
    # Ordinal alternative slopes and cutpoints and likelihoods are saved, no printed exact vector.
    for r in csv('outputs/reproduced/models/ordinal/ordinal_coefficients.csv').to_dict('records'):
        if r['analysis_id']=='M1' and r['scale']=='slope':continue
        for q in ['estimate','se','ci_lower','ci_upper','p_value']:
            add(r['analysis_id']+':full',r['term']+':'+q,None,r[q],'Note 2 or unprinted cutpoints; no precise parameter table recovered','outputs/reproduced/models/ordinal/ordinal_coefficients.csv')
    for q in ['lr_vs_null','lr_df','lr_p_value','cox_snell_r2']:
        add('M1',q,None,m1[q],'Fit quantity not numerically reported','outputs/reproduced/models/ordinal/M1_model.json')
    wg=js('outputs/diagnostics/ordinal/M1_Wolfe_Gould_numeric.json')
    for q,orig,dec,exact in [('chi_square',7.4,1,False),('df',9,0,True),('p_value',.59,2,False)]:
        add('C1:Wolfe_Gould',q,orig,wg[q],'Article Note 1 p.290','outputs/diagnostics/ordinal/M1_Wolfe_Gould_numeric.json',decimals=dec,exact=exact,explanation='Replicates author bare numeric RHS polsys socdiv mediatype, rather than M1 factor-dummy RHS.')
    gen=js('outputs/diagnostics/ordinal/M1_gologit2_npl_factor.json')
    for q,orig,val,dec in [('raw_LR',22.5,gen['raw_twice_log_likelihood_difference'],1),('nominal_df',14,15,0),('p_value',.07,None,2)]:
        add('C1:generalized',q,orig,val,'Article Note 1 p.290','outputs/diagnostics/ordinal/M1_gologit2_npl_factor.json',decimals=dec,exact=q=='nominal_df',
          explanation='No regular LR inference accepted: structural nonidentification, rank 22/24 and seven negative unobserved-category probabilities. Raw LR agreement does not validate df14 or p=.07. Omission/build rules unrecovered; typo attribution unproven.',cause='diagnostic_identification_failure',confidence='demonstrated_for_current_design',validation='inference_not_verified')
    for r in csv('outputs/diagnostics/binary_likelihood_comparisons.csv').to_dict('records'):
        mid=r['model_id']
        add('C3:'+mid,'empty_mixed_vs_single_LR',154.95 if mid=='M2' else 91.22,r['nested_null_vs_single_null_lr'],'Article Note 3 p.291','outputs/diagnostics/binary_likelihood_comparisons.csv',
            explanation='M2 numeric difference retained. Two variance components are zero on the null boundary; ordinary regular chi-square inference and original mixture calibration are not certified. Printed p<.000 is not literal probability.',cause='unresolved_numerical_and_boundary_inference',confidence='boundary_issue_demonstrated_cause_of_difference_unknown')
        for q in ['full_ll','nested_null_ll','single_level_null_ll','full_vs_nested_null_lr','full_vs_nested_null_df','full_vs_nested_null_p']:
            add('C3:'+mid,q,None,r[q],'Author model comparison; full precision targets not published','outputs/diagnostics/binary_likelihood_comparisons.csv')
    frame=pd.DataFrame(rows)
    frame.to_csv(out/'comparison_all.csv',index=False)
    targets=frame[frame.published_value.notna()].drop(columns=['reproduced_value','difference','comparison_status','validation_status'])
    # Generated transcription is separate from computation and clearly labelled.
    (root/'outputs/published').mkdir(parents=True,exist_ok=True)
    target_path=root/'outputs/published/verification_targets.csv' if out==root/'outputs/verification' else out/'verification_targets.csv'
    targets.to_csv(target_path,index=False)
    coverage=frame.groupby(['analysis_id','comparison_status']).size().unstack(fill_value=0)
    coverage.to_csv(out/'comparison_coverage.csv')
    summary={'generated_utc':datetime.now(timezone.utc).isoformat(),'ledger_rows':len(frame),
       'published_numeric_rows':int(frame.published_value.notna().sum()),
       'comparison_status_counts':frame.comparison_status.value_counts().to_dict(),
       'scope':'Cells are heterogeneous and not independent trials. Do not turn counts into a statistical replication success probability.',
       'student_acceptance':'pending','final_release_created':False}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    return frame,summary

def main():
    p=argparse.ArgumentParser();p.add_argument('--project-root',type=Path,default=ROOT);p.add_argument('--output-root',type=Path)
    a=p.parse_args();_,summary=reconcile(a.project_root,a.output_root);print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
