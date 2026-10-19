"""Check preservation and report exclusion before the authorized selective upload."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import ast,json,subprocess
ROOT=Path(__file__).resolve().parents[2]
def git(*args):return subprocess.run(['git',*args],cwd=ROOT,capture_output=True,check=True).stdout
baseline=json.loads((ROOT/'records/skill_invocations/2026-10-19_verify-and-package/baseline_manifest.json').read_text())
differences=[r['path'] for r in baseline if not (ROOT/r['path']).exists() or sha256((ROOT/r['path']).read_bytes()).hexdigest()!=r['sha256']]
paths=[p for p in git('ls-files','-z').decode().split('\0') if p]
final_paths=[p for p in paths if 'final_report' in p.lower() or p.startswith('report/local_review/')]
local_reports=['report/final_report_draft.md','report/final_report_review_2026-10-19.docx','report/local_review/previous_versions/final_report_before_editorial_revision.md']
ignored=all(subprocess.run(['git','check-ignore','-q',p],cwd=ROOT).returncode==0 for p in local_reports)
syntax=[]
for rel in ['tools/verification_package_audit.py','tools/maintenance/prepare_selective_sync.py','tools/maintenance/record_editorial_update.py', 'tools/maintenance/check_selective_sync.py']:
 ast.parse((ROOT/rel).read_text(encoding='utf-8'));syntax.append(rel)
checks=[
 {'name':'Original inputs and existing numerical outputs preserved','passed':not differences,'files':len(baseline),'differences':differences},
 {'name':'No individual report or review archive in the Git index','passed':not final_paths,'paths':final_paths},
 {'name':'Current and earlier local individual reports retained and ignored','passed':ignored and all((ROOT/p).exists() for p in local_reports)},
 {'name':'Both supporting technical Word reports included','passed':all(p in paths for p in ['report/verification/01_results_comparison.docx','report/verification/02_python_stata_equivalence.docx'])},
 {'name':'Changed maintenance Python files parse','passed':True,'files':syntax},
 {'name':'All-page local Word review complete','passed':json.loads((ROOT/'report/local_review/revision_receipt.json').read_text())['visual_review']=='passed'},
]
result={'checked_utc':datetime.now(timezone.utc).isoformat(),'checks':checks,'all_passed':all(c['passed'] for c in checks),'new_statistical_fits_run':False,'final_release_created':False}
dest=ROOT/'records/editorial_revision/2026-10-19/validation.json';dest.write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
assert result['all_passed']
