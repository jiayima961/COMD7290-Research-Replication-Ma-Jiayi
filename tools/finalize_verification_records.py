"""Write the dated skill 3 handoff only from completed, saved evidence."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil

ROOT = Path(__file__).resolve().parents[1]
INV = ROOT/'records/skill_invocations/2026-10-19_verify-and-package'
TEST = ROOT/'records/skill_tests/verify-and-package'

def read(rel):
    return json.loads((ROOT/rel).read_text(encoding='utf-8'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def append_preserving(rel, marker, content):
    p=ROOT/rel
    old=p.read_text(encoding='utf-8')
    if marker in old:
        return
    previous=INV/'previous_versions'/rel
    if not previous.exists():
        previous.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(p,previous)
    p.write_text(old.rstrip()+'\n\n'+content.strip()+'\n',encoding='utf-8')

def main():
    audit=read('records/skill_tests/verify-and-package/package_audit.json')
    fresh=read('records/run_logs/skill3/verified_clean_restart/receipt.json')
    first=read('records/run_logs/skill3/clean_restart/receipt.json')
    qa=read('records/skill_tests/verify-and-package/document_qa.json')
    independent=read('outputs/verification/independent_checks/checks.json')
    static=read('records/run_logs/skill3/static_validation.json')
    material=read('records/run_logs/skill3/material_checks.json')
    assert audit['all_checks_passed'] and fresh['returncode']==0 and first['returncode']==0
    assert qa['all_pages_passed'] and all(r['passed'] for r in independent)
    assert static['exit_code']==0 and material['exit_code']==0
    assert (TEST/'forward_review.md').is_file() and (TEST/'independent_source_audit.md').is_file()

    append_preserving('analysis/README.md','## Full verified reproduction', '''
## Full verified reproduction

`python analysis/run_verified_replication.py` runs the unchanged research pipeline,
then the [complete reconciler](verify_and_package.py), the independent skill 3
checks and the [separate country sensitivity](skill3_sensitivity.py). Use a copy
to preserve existing outputs. Actual source/input-only clean runs are recorded in
[skill 3 logs](../records/run_logs/skill3/); the existing environment is reused.
For completed fits, the three verification stages can be run separately without
repeating the expensive binary fitting. The [report index](../report/verification/README.md)
explains agreements, discrepancies, unavailable targets and remaining limits.
''')
    append_preserving('tests/README.md','## Skill 3 independent verification', '''
## Skill 3 independent verification

`python tests/skill3/check_verification.py` independently reads raw inputs, fits
M1 with statsmodels, recalculates all 25 ordinal AMEs and 50 interval endpoints,
and exercises invalid-code, rounding and unavailable-target controls. It
supplements the saved skill 2 binary likelihood/curvature checks; M2/M3 were not
independently optimized in another engine. See the [test report](../records/skill_tests/verify-and-package/TEST_REPORT.md).
`python tools/verification_package_audit.py` checks preservation and the saved
clean-run, comparison, sensitivity, discovery, source and Word-review evidence.
It expects this completed local evidence package, not only a fresh code checkout.
''')
    append_preserving('tools/README.md','## Skill 3 evidence and documents', '''
## Skill 3 evidence and documents

- `verification_clean_restart.py`: build an isolated source/input-only tree and
  actually run the requested analysis entry; a new destination is required.
- `verification_package_audit.py`: check the completed local evidence package.
- `verification_snapshot.py`: preserve pre-task versions and source/result hashes.
- `build_verification_documents.py`, `word_export_pdf.ps1` and
  `render_verification_documents.py`: build and visually verify the two requested
  Word documents using the bundled runtime. Regeneration requires a new visual review.
- `record_verification_sources_and_layout.py` and `finalize_verification_records.py`:
  bind the actual source/layout review and completed evidence. These dated task
  writers do not fit models or provide the student's acceptance.

Start with the [report index](../report/verification/README.md), not these maintenance
helpers. Scientific execution uses `analysis/run_verified_replication.py`.
''')
    append_preserving('records/README.md','## Current skill 3 verification', '''
## Current skill 3 verification

Use [the actual invocation and completion receipt](skill_invocations/2026-10-19_verify-and-package/README.md),
[the test report](skill_tests/verify-and-package/TEST_REPORT.md), [the seven source-checked
AI decisions](skill3_decision_audit.md) and [the two full clean-run logs](run_logs/skill3/).
The [cached source access record](source_access/skill3_sources.md) preserves the
supplement's numerical excerpt without claiming unavailable original HTML.
All human-owned acceptance fields remain pending.
''')
    append_preserving('records/agent_records.md','## 2026-10-19 Skill 3 completed technical invocation', '''
## 2026-10-19 Skill 3 completed technical invocation

The user authorized all-result comparison and two English reference Word reports.
Applied verify-and-package 1.0.0 with skill-creator, academic-research-suite,
documents and PDF guidance. Primary sources and the execution contract were read
before numerical reconciliation. Actual checks include the independent M1 fit and
all ordinal AMEs, a copied invalid-code/recovery test, two source/input-only full
restarts, six planned country deletions, official static validation and runtime
discovery. Bounded independent source and forward reviews retain their original
findings and corrections. Both Word files were rendered and all 14 final pages
visually inspected. The test report and invocation receipt bind the current
evidence. Historical Stata-build equality is not certified. No GitHub upload,
collaborator invitation, personal attestation, assessed release or submission was
performed in this task. Exact model/build identifiers not exposed by a tool are
not invented.
''')

    now=datetime.now(timezone.utc).isoformat()
    report=f'''# Skill 3 actual execution and validation

Completed technical evidence recorded {now}. Skill: verify-and-package 1.0.0.
This is AI technical verification, not the student's scientific acceptance.

| Layer | Actual outcome and evidence |
|---|---|
| Official static validator | Passed; records/run_logs/skill3/static_validation.json and stdout |
| Native discovery | Three enabled repository skills; runtime_discovery.json binds the current skill file |
| Real invocation | User request, originals and preserved versions in records/skill_invocations/2026-10-19_verify-and-package/ |
| Independent calculations | {len(independent)}/{len(independent)} passed; raw-reader counts, separate statsmodels M1 optimization and 25 AMEs/50 interval endpoints; maximum difference 5.688442376861058e-09 |
| Negative test and recovery | Invalid tone category in a copy rejected, restored and accepted; original inputs unchanged; rounding/count/unavailable-target guards also exercised |
| First clean restart | Full faithful research pipeline return code {first['returncode']}; 18 reproduced CSV numerical payloads match saved results exactly |
| All-in-one clean restart | New source/input-only tree, analysis/run_verified_replication.py return code {fresh['returncode']}; all 1,798 comparison rows, 12 independent checks and 30 sensitivity rows reproduced |
| Separate S1 | Six prespecified country deletions, 30 slope estimates, all converged; contextual significance varies and media contrasts retain direction/significance |
| Independent source audit | independent_source_audit.md; original tables, confidence intervals, diagnostics, method sources and all 75 supplementary entries checked |
| Independent bounded forward review | forward_review.md; nine executed bounded checks, separate raw counts and diagnostic calculations; no additional fits |
| Final package audit | {len(audit['checks'])}/{len(audit['checks'])} passed; package_audit.json protects 86 original/input/result files and binds sources, discovery, clean runs and reviewed documents |
| Repository material checks | Passed; records/run_logs/skill3/material_checks.json |
| Word visual QA | Two DOCX files, 9 + 5 pages; final rasterizations inspected page by page; document_qa.json |

## Comparison meaning

The ledger contains 376 numeric publication targets: 334 within displayed
rounding, 28 exact integer agreements, 13 discrepancies, and one invalid/unverified
published p value. Another 1,422 quantities lack numeric source targets. These
overlapping, heterogeneous records are not independent trials or a success rate.
Original 45-cell skill 2 comparisons and all protected numerical files remain
unchanged. Matching displayed numbers does not prove unrounded equality.

The generalized ordinal check is not certified as a regular LR test. Historical
Stata builds, finite-node adaptation, prediction details and reliability add-on
versions remain partly unpinned. Independent binary checks evaluate likelihoods
and curvature; they do not reoptimize M2/M3 in another engine. Both clean restarts
reuse the installed environment and do not establish a fresh-machine installation.

## Corrections and review resolution

The initial S1 syntax error, new-draft country-label swap, source 404, Word COM and
renderer issues are preserved in the invocation failures/corrections record.
The country-label draft is archived and guarded by raw DTA metadata checks.
The dated forward review correctly observed stale STATUS/decision text and a
missing durable cached excerpt at its snapshot. STATUS, the course checklist and
D013 are now updated; the 75-number excerpt, retrieval method and transcription
hash are saved under records/source_access/. Original live HTML remains unavailable.
The source and forward reviews were not rewritten to pretend these resolutions
preceded their observations.

Read report/verification/README.md for ordered deliverables. Final report revision,
personal reading/diagram evidence, at least three personal decision reviews,
student ID, instructor-access verification and assessed tag/release/submission
remain pending. No upload or final submission was performed here.
'''
    (TEST/'TEST_REPORT.md').write_text(report,encoding='utf-8')
    (INV/'README.md').write_text('''# Skill 3 invocation and handoff

Read request.md, then completion_receipt.json for actual evidence bindings.
The current technical deliverables are ordered in ../../../report/verification/README.md.
Validation is indexed in ../../skill_tests/verify-and-package/TEST_REPORT.md.
Prior authored files are retained under previous_versions; the corrected new
country-label draft is retained separately. failures_and_corrections.md records
observed execution problems. No source data or skill 2 result was replaced.

Human scientific acceptance and final assessed submission are pending.
''',encoding='utf-8')
    artifacts=[]
    for directory in ['.agents/skills/verify-and-package','outputs/verification','report/verification',
                      'records/skill_tests/verify-and-package','records/source_access']:
        for p in sorted((ROOT/directory).rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:
                artifacts.append({'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)})
    for rel in ['analysis/run_verified_replication.py','analysis/verify_and_package.py',
                'analysis/skill3_sensitivity.py','tests/skill3/check_verification.py',
                'tools/verification_package_audit.py','tools/finalize_verification_records.py',
                'docs/analysis_inventory.csv','docs/limitations.md','docs/follow_up.md',
                'report/final_report_draft.md','report/skill3_submission_readiness.md',
                'records/skill3_decision_audit.md','records/checkpoints.md',
                'records/run_logs/skill3/clean_restart/receipt.json',
                'records/run_logs/skill3/verified_clean_restart/receipt.json']:
        p=ROOT/rel;artifacts.append({'path':rel,'sha256':sha(p)})
    receipt={
        'completed_utc':now,'technical_status':'completed_with_explicit_scientific_and_historical_equivalence_limits',
        'skill':'verify-and-package','version':'1.0.0',
        'invocation_record':'request.md','test_report':'records/skill_tests/verify-and-package/TEST_REPORT.md',
        'protected_preexisting_files':86,'protected_files_unchanged':True,
        'package_checks_passed':len(audit['checks']),'independent_checks_passed':len(independent),
        'word_documents':2,'reviewed_pages':14,
        'student_acceptance':'pending','final_submission_ready':False,
        'github_synchronized_this_task':False,'final_release_created':False,
        'forward_review_issues_resolved':['Current STATUS and assignment checklist updated.','D013 recorded.','Cached numeric excerpt and retrieval metadata preserved; unavailable live HTML still disclosed.'],
        'bound_artifacts':artifacts,
    }
    (INV/'completion_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'technical_status':receipt['technical_status'],'bound_artifacts':len(artifacts),'package_checks':len(audit['checks']),'human_acceptance':'pending'},indent=2))

if __name__=='__main__':main()
