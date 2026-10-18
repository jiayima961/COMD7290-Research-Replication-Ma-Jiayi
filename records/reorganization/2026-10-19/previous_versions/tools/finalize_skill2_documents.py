"""Bind current study navigation to actual results, preserving earlier drafts."""
from pathlib import Path
import csv,json,shutil
import pandas as pd
root=Path(__file__).resolve().parents[1]
receipt=root/'records/skill_invocations/2026-10-18_reproduce-and-diagnose'
before=receipt/'before'
for name in ['docs/variable_dictionary.csv','docs/design_and_models.md','docs/hypothesis_matrix.csv','docs/analysis_inventory.csv']:
    dest=before/name;dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():shutil.copy2(root/name,dest)
inventory=pd.read_csv(root/'docs/analysis_inventory.csv').fillna('')
mapping={
'D1':('analysis/ordinal_reproduction.py','outputs/reproduced/descriptives/ordinal/item_descriptives.csv','computed',''),
'D2':('analysis/ordinal_reproduction.py','outputs/reproduced/descriptives/ordinal/reference_descriptives.csv','computed',''),
'R1':('analysis/reliability_reproduction.py','outputs/reproduced/reliability/reliability_coefficients.csv','computed_with_method_limits','historical benchmark build unpinned'),
'R2':('analysis/reliability_reproduction.py','outputs/reproduced/reliability/reliability_coefficients.csv','computed_with_matching_audit','positional slots and repeated named coders retained'),
'M1':('analysis/ordinal_reproduction.py','outputs/reproduced/models/ordinal/ordinal_coefficients.csv','validated',''),
'M2':('analysis/nested_logit.py','outputs/reproduced/models/M2_fit.json','computed_and_numerically_verified','historical finite-seven-point grid unresolved; M2 printed discrepancy retained'),
'M3':('analysis/nested_logit.py','outputs/reproduced/models/M3_fit.json','computed_and_numerically_verified','historical finite-seven-point grid unresolved'),
'C1':('analysis/ordinal_reproduction.py','outputs/diagnostics/ordinal/findings.md','partially_valid_diagnostic','generalized model nonidentified/invalid probabilities; ordinary LR inference not accepted'),
'C2':('analysis/ordinal_reproduction.py','outputs/reproduced/models/ordinal/ordinal_fit.csv','computed','mixed-system significance differs under probit'),
'C3':('analysis/compare_replication.py','outputs/diagnostics/binary_likelihood_comparisons.csv','statistics_computed_inference_limited','two random variances on null boundary; original mixture rule unrecovered'),
'P1':('analysis/ordinal_reproduction.py','outputs/reproduced/predictions/ordinal/M1_predictive_margins.csv','computed',''),
'P2':('analysis/binary_predictions.py','outputs/reproduced/predictions/binary_margins_ames.csv','computed_with_grid_checks','historical prediction finite-grid reduction unresolved'),
'A1':('docs/execution_specification.md','docs/replication_results.md','available_source_analyses_covered','supplementary numeric targets/build details not completely recovered; no exhaustive unavailable appendix claim'),
'V1':('tests/skill2/data_checks.py;tests/skill2/check_glmm_full_likelihood.py','outputs/diagnostics/data_independent_checks.json;outputs/diagnostics/glmm/','independent_descriptive_and_advanced_likelihood_checks_passed','independent fixed-parameter integral verification is not independent optimization'),
'N1':('tests/skill2/data_checks.py','outputs/diagnostics/data_independent_checks.json','detection_and_recovery_passed','synthetic copied input only'),
'S1':('not_yet_implemented','docs/limitations.md','pending_separate_substantive_sensitivity','original alternative links and numerical integration checks do not automatically replace the separate assignment sensitivity'),
}
for i,r in inventory.iterrows():
    script,out,status,limit=mapping[r.analysis_id]
    inventory.loc[i,['script_path','output_path','status','blocker']]=[script,out,status,limit]
    inventory.loc[i,'transformations']='See docs/execution_specification.md and actual branch source/settings records'
    inventory.loc[i,'coverage_note']='Actual execution coverage; preserve limitations and original hypothesis direction'
inventory.loc[inventory.analysis_id=='D2','source_locator']='Author code Analysis 3; article reference-level descriptive results'
inventory.loc[inventory.analysis_id=='P1','source_locator']='Author code Figure 2; article Figure 1'
inventory.loc[inventory.analysis_id=='P2','source_locator']='Author code Figure 4; article Figure 3'
inventory.to_csv(root/'docs/analysis_inventory.csv',index=False)
old=pd.read_csv(before/'docs/hypothesis_matrix.csv').fillna('')
hs=pd.read_csv(root/'outputs/reproduced/hypothesis_tests.csv')
rows=[]
for h in hs.to_dict('records'):
    row=old[old.hypothesis_id==h['hypothesis_id']].iloc[0].to_dict()
    mid=h['model_id'];row.update(analysis_id=mid,theoretical_premise_mechanism='Student v2 section 2; source mechanisms are proposed, not directly estimated mediators',
      predicted_relationship=f"{h['contrast']} contrast coefficient sign {h['predicted_sign']:+d}",
      measurement_coding_missing='Verified author recodes, binary domains, missingness and keys; see execution specification/data audit',
      estimand_parameter_contrast=h['contrast']+' versus original reference, conditional/cumulative log odds',
      equation_syntax='docs/execution_specification.md; sources/author_code/MedCon_Civility_an.do',
      estimator_settings='Observed-information ML; ordered logit' if mid=='M1' else 'Nested Bernoulli ML, recursive mean/variance adaptive GH7; historical grid unconfirmed',
      assumptions_intervals_diagnostics='95% normal Wald intervals; see branch diagnostics and independent verification',
      dataset_spec_versions='records/source_manifest.csv; docs/execution_specification.md',
      script_path='analysis/ordinal_reproduction.py' if mid=='M1' else 'analysis/nested_logit.py',
      output_path='outputs/reproduced/hypothesis_tests.csv',
      reproduced_values=f"b={h['beta']:.12g}; SE={h['se']:.12g}; OR={h['odds_ratio']:.12g}; p={h['p_value']:.12g}",
      discrepancy='outputs/comparison.csv; finite-grid caveat for M2/M3',scientific_conclusion=h['conclusion'],
      approval_status='execution explicitly authorized D011; final student interpretation pending')
    rows.append(row)
for r in inventory.to_dict('records'):
    if r['analysis_id'] in ['M1','M2','M3']:continue
    row={k:'' for k in old.columns};row.update(analysis_id=r['analysis_id'],hypothesis_id='not-numbered',source_locator=r['source_locator'],
      status_confirmatory_exploratory='measurement/descriptive/diagnostic/prediction/verification as inventoried',script_path=r['script_path'],output_path=r['output_path'],
      discrepancy=r['blocker'],scientific_conclusion=r['status'],approval_status='D011 execution authorization; final student interpretation pending')
    rows.append(row)
pd.DataFrame(rows,columns=old.columns).to_csv(root/'docs/hypothesis_matrix.csv',index=False)
d=pd.read_csv(root/'docs/variable_dictionary.csv').fillna('')
updates={0:('tone','raw 1-5; analysis 0 no outrage through 4 very strong outrage','subtract 1'),
1:('actrefoutbin','0 absence; 1 explicit outrage','none: author-prepared binary data'),
2:('actrefrecbin','0 absence; 1 explicit recognition','none: author-prepared binary data'),
3:('polsys','analysis 1 consensus; 2 mixed; 3 majoritarian','raw1/2/3 -> 1/3/2'),
4:('socdiv','analysis1 stable; 2 contested','raw1/2 -> 2/1'),
5:('mediatype','analysis1 blog; 2 website; 3 newspaper','raw1/2/3 -> 1/3/2'),
6:('country','1 Australia; 2 Germany; 3 Lebanon; 4 Switzerland; 5 Turkey; 6 USA','none'),
7:('akteur_id; text_id; constructed act_id','actor/statement identifier unique only within item','concatenate text_id and akteur_id for nested actor grouping')}
for i,(name,values,trans) in updates.items():
    d.loc[i,['actual_data_variable','values_meaning','transformation','missing_rule','verification_status']]=[name,values,trans,'no missing required main-model values; fail on invalid values','verified against actual author data/code; see outputs/diagnostics/data_audit.json']
d.to_csv(root/'docs/variable_dictionary.csv',index=False)
p=root/'docs/design_and_models.md';s=p.read_text(encoding='utf-8-sig').replace('# Research design and models: unapproved draft','# Research design and executed model specification')
s=s.replace('These are published counts, not locally recalculated results. Verify whether actor identifiers are unique only within items.','These counts were independently recalculated from original inputs. Actor identifiers are nested within items; the composite actor key is verified.')
s=s.replace('These equations describe the intended model. Numeric coding, exact input names, estimation, integration, and interval conventions still require source-to-data verification.','These equations describe the executed model. See [the execution specification](execution_specification.md) and [results index](replication_results.md) for verified input names, coding, numerical settings and the unresolved historical finite-grid details.')
s=s[:s.index('## Resolve before estimation')]+'''## Execution and interpretation status

The user explicitly authorized source-bound Python reproduction in D011. Current numerical results and uncertainty are saved; this is not a claim of preregistration or final student acceptance. See execution_specification.md for recovered settings and replication_results.md for differences and limitations. Independent ratings remain separate from consensus analytical data. Historical software builds and finite quadrature internals are incompletely pinned; no exact-executable equivalence is claimed.
'''
p.write_text(s,encoding='utf-8')
print('Updated canonical matrix (12 directional targets), inventory, verified focal dictionary and model navigation.')
