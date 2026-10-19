"""Audit skill 3 deliverables and evidence without refitting research models."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def main():
 checks=[]
 def add(name,passed,**details):checks.append(dict(check=name,passed=bool(passed),**details))
 baseline=json.loads((ROOT/'records/skill_invocations/2026-10-19_verify-and-package/baseline_manifest.json').read_text())
 differences=[r['path'] for r in baseline if not (ROOT/r['path']).exists() or hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()!=r['sha256']]
 add('Original inputs and preexisting numerical outputs unchanged',not differences,protected_files=len(baseline),differences=differences)
 d=pd.read_csv(ROOT/'outputs/verification/comparison_all.csv')
 add('All ledger identities unique',not d.duplicated(['analysis_id','quantity']).any(),rows=len(d))
 add('Missing targets cannot be agreement',d.loc[d.published_value.isna(),'comparison_status'].eq('not_verifiable').all())
 published=d[d.published_value.notna()]
 add('Published discrepancies retained',len(published)==376 and published.comparison_status.eq('discrepancy').sum()==13 and published.comparison_status.eq('not_verifiable').sum()==1)
 inv=pd.read_csv(ROOT/'docs/analysis_inventory.csv')
 old=pd.read_csv(ROOT/'records/skill_invocations/2026-10-19_verify-and-package/previous_versions/docs/analysis_inventory.csv')
 add('Inventory covers every original analysis ID exactly once',set(inv.analysis_id)==set(old.analysis_id) and not inv.analysis_id.duplicated().any() and inv.status.isin(['reproduced','reproduced_with_discrepancy','not_verifiable']).all())
 for rel in ['outputs/verification/independent_checks/checks.json','records/skill_tests/verify-and-package/runtime_discovery.json','records/run_logs/skill3/clean_restart/receipt.json']:
  v=json.loads((ROOT/rel).read_text())
  passed=all(r['passed'] for r in v) if isinstance(v,list) else v.get('status')=='passed' if 'status' in v else v.get('returncode')==0 and all(r.get('numeric_exact') for r in v['numeric_comparisons'])
  add('Saved actual evidence '+rel,passed)
 s=pd.read_csv(ROOT/'outputs/verification/sensitivity/country_deletion_coefficients.csv')
 add('All six planned country deletions executed',len(s)==30 and s.excluded_country.nunique()==6 and s.fit_status.eq('converged').all())
 text=(ROOT/'report/final_report_draft.md').read_text(encoding='utf-8').split('<!-- BODY START -->')[1].split('<!-- BODY END -->')[0]
 count=len(re.sub(r'^##.*$','',text,flags=re.M).split())
 add('Individual report draft body within required word range',1000<=count<=1200,word_count=count,count_rule='Whitespace-separated body tokens; headings/access/references excluded. Final student version must be recounted.')
 add('Both requested DOCX files exist',all((ROOT/'report/verification'/f'{name}.docx').stat().st_size>10000 for name in ['01_results_comparison','02_python_stata_equivalence']))
 summary=json.loads((ROOT/'outputs/verification/summary.json').read_text())
 add('Human acceptance and assessed release not fabricated',summary['student_acceptance']=='pending' and summary['final_release_created'] is False)
 # Numeric payloads from the clean pipeline beyond the five receipt exemplars.
 clean=ROOT/'tmp/skill3_clean_restart';result=[]
 for p in (ROOT/'outputs/reproduced').rglob('*.csv'):
  rel=p.relative_to(ROOT);q=clean/rel
  if not q.exists():result.append({'path':str(rel),'passed':False,'reason':'missing clean output'});continue
  a,b=pd.read_csv(p),pd.read_csv(q);cols=list(a.select_dtypes(include='number'))
  passed=a.shape==b.shape and list(a)==list(b) and np.allclose(a[cols],b[cols],atol=0,rtol=0,equal_nan=True)
  result.append({'path':rel.as_posix(),'passed':bool(passed)})
 add('All reproduced CSV numeric payloads exactly match clean refit',all(r['passed'] for r in result),files=len(result))
 # Final document review is a human-style visual inspection recorded separately.
 qa=json.loads((ROOT/'records/skill_tests/verify-and-package/document_qa.json').read_text())
 doc_bindings=all(hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==r['sha256'] and r['outcome']=='passed' for r in qa['documents'])
 add('Latest Word documents bound to completed all-page visual review',qa['all_pages_passed'] and doc_bindings and sum(r['page_count'] for r in qa['documents'])==14)
 access=json.loads((ROOT/'records/source_access/retrieval_metadata.json').read_text())
 excerpt=ROOT/access['preserved_excerpt']
 add('Cached supplement transcription bound with explicit original-HTML limitation',hashlib.sha256(excerpt.read_bytes()).hexdigest()==access['excerpt_sha256'] and access['original_http_body_sha256'] is None)
 # Parse the saved numeric excerpt independently of the reconciler constants.
 numeric_lines=[line for line in excerpt.read_text().splitlines() if '[' in line and re.match(r'^[+\-.0-9]',line)]
 triples=[tuple(map(float,m)) for line in numeric_lines for m in re.findall(r'([+-]?\d*\.\d+)\s*\[([+-]?\d*\.\d+),\s*([+-]?\d*\.\d+)\]',line)]
 target=pd.read_csv(ROOT/'outputs/published/verification_targets.csv').query("analysis_id == 'P1:AME'").set_index('quantity')
 parsed=[]
 for name,line_triples in zip(['mixed','majoritarian','contested','website','newspaper'],[triples[i:i+5] for i in range(0,len(triples),5)]):
  for category,values in enumerate(line_triples):
   for field,value in zip(['estimate','ci_lower','ci_upper'],values):parsed.append(target.loc[f'{name}:tone{category}:{field}','published_value']==value)
 add('All 75 cached numeric entries match transcribed comparison targets',len(triples)==25 and len(parsed)==75 and all(parsed))
 discovery=json.loads((ROOT/'records/skill_tests/verify-and-package/runtime_discovery.json').read_text())
 discovered=next(r for r in discovery['skills'] if r['name']=='verify-and-package')
 add('Runtime discovery binds the current skill file',discovered['sha256']==hashlib.sha256((ROOT/'.agents/skills/verify-and-package/SKILL.md').read_bytes()).hexdigest() and discovered['enabled'])
 clean2=ROOT/'tmp/skill3_verified_clean_restart'
 receipt2=json.loads((ROOT/'records/run_logs/skill3/verified_clean_restart/receipt.json').read_text())
 add('All-in-one entry completed in a second source/input-only tree',receipt2.get('returncode')==0 and all(r.get('numeric_exact') for r in receipt2.get('numeric_comparisons',[])))
 fresh=pd.read_csv(clean2/'outputs/verification/comparison_all.csv')
 ledger_fields=['analysis_id','quantity','published_value','reproduced_value','difference','tolerance','comparison_status','validation_status']
 ledger_same=d[ledger_fields].equals(fresh[ledger_fields])
 independent2=json.loads((clean2/'outputs/verification/independent_checks/checks.json').read_text())
 sensitivity2=pd.read_csv(clean2/'outputs/verification/sensitivity/country_deletion_coefficients.csv')
 cols=list(s.select_dtypes(include='number'))
 sensitivity_same=s.shape==sensitivity2.shape and np.allclose(s[cols],sensitivity2[cols],rtol=0,atol=0,equal_nan=True)
 add('Verified entry reproduces full ledger, independent checks and all sensitivity estimates',ledger_same and all(r['passed'] for r in independent2) and sensitivity_same,ledger_rows=len(fresh),independent_checks=len(independent2),sensitivity_rows=len(sensitivity2))
 record={'checked_utc':datetime.now(timezone.utc).isoformat(),'checks':checks,'all_checks_passed':all(r['passed'] for r in checks),'clean_csv_comparisons':result,
  'scientific_acceptance':'pending student review','final_submission_ready':False}
 out=ROOT/'records/skill_tests/verify-and-package/package_audit.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(record,indent=2),encoding='utf-8')
 print(json.dumps({'checks':len(checks),'all_passed':record['all_checks_passed'],'word_count':count,'protected_files':len(baseline),'clean_numeric_csvs':len(result),'failed':[r for r in checks if not r['passed']]},indent=2))
 if not record['all_checks_passed']:raise SystemExit(1)
if __name__=='__main__':main()
