"""Preserve previous authored documents and bind existing scientific results."""
from pathlib import Path
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'records/skill_invocations/2026-10-19_verify-and-package'
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 if (OUT/'baseline_manifest.json').exists():
  raise SystemExit('Existing baseline preserved; do not overwrite.')
 paths=['AGENTS.md','README.md','START_HERE.md','STATUS.md','docs/analysis_inventory.csv',
        'docs/limitations.md','docs/follow_up.md','docs/assignment_checklist.md','docs/checkpoints.md',
        'outputs/review_report.md','.agents/skills/verify-and-package/SKILL.md',
        '.agents/skills/README.md','docs/skills/README.md','records/decisions.md','records/agent_records.md']
 for rel in paths:
  p=ROOT/rel
  if p.exists():
   dst=OUT/'previous_versions'/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
 protected=[]
 for folder in ['data/original','outputs/reproduced','outputs/diagnostics','sources/author_code']:
  for p in (ROOT/folder).rglob('*'):
   if p.is_file() and p.suffix not in ['.md']:
    protected.append({'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 (OUT/'baseline_manifest.json').write_text(json.dumps(protected,indent=2),encoding='utf-8')
 (OUT/'request.md').write_text('''# Actual skill 3 invocation

Date: 2026-10-19. User: Ma Jiayi. Skill: $verify-and-package.

The user requested comparison of every reproduced reliability, descriptive and formal hypothesis result with the original publication; an English Word comparison report; completion and testing of the third project skill and other assignment tasks; a documented justification for using Python to reproduce the Stata analysis; and economical reuse of completed evidence. Subsequent messages requested continuation after network interruptions.

Inputs: assignment PDF, article PDF, author syntax and data, execution specification, published targets, all skill 2 results and diagnostics, independent source audit. Read original specification and primary sources before implementation summaries. Source hashes are in records/source_manifest.csv and sources/input_restore_manifest.json.

Permitted actions: non-destructive local comparison, independent calculations, isolated full refitting, one separately labelled sensitivity, report/skill authoring and testing. No student approval, direct reading attestation, release, instructor invitation or final submission is inferred.

Execution: analysis/verify_and_package.py; analysis/skill3_sensitivity.py; tests/skill3/check_verification.py; tools/verification_clean_restart.py. Actual outcomes and commands are recorded separately; this request is not a success receipt.
''',encoding='utf-8')
 print('Archived',len(paths),'candidate documents; protected',len(protected),'scientific files.')
if __name__=='__main__':main()
