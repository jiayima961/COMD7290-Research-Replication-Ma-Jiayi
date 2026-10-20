"""Audit saved coursework evidence without reading the individual final report.

This documents presence, dated execution evidence and remaining course tasks.
It does not refit models, certify human understanding or submit anything.
"""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import csv,json,shutil,subprocess
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'records/assignment_audit/2026-10-20'
OUT.mkdir(parents=True,exist_ok=True)
for rel in ['.gitignore','docs/README.md','docs/assignment_checklist.md','records/access_status.md']:
    backup=OUT/'previous_versions'/rel
    if not backup.exists():
        backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,backup)
pdf=ROOT/'sources/local/COMD7290_assignment.pdf'
reader=PdfReader(pdf)
scratch=ROOT/'tmp/assignment_audit_2026-10-20';scratch.mkdir(parents=True,exist_ok=True)
for i,page in enumerate(reader.pages,1):
    (scratch/f'page_{i:02d}.txt').write_text(page.extract_text(),encoding='utf-8')
rows=list(csv.DictReader((ROOT/'docs/hypothesis_matrix.csv').open(encoding='utf-8-sig',newline='')))
fields=['theoretical_premise_mechanism','population_sampling','coding_unit_dependence',
 'constructs_indicators','measurement_coding_missing','estimand_parameter_contrast',
 'equation_syntax','estimator_settings','assumptions_intervals_diagnostics',
 'published_rule','dataset_spec_versions']
incomplete=[{'analysis_id':r['analysis_id'],'hypothesis_id':r['hypothesis_id'],
             'blank_fields':[k for k in fields if not r[k].strip()]} for r in rows
            if any(not r[k].strip() for k in fields)]
dictionary=list(csv.DictReader((ROOT/'docs/variable_dictionary.csv').open(encoding='utf-8-sig',newline='')))
baseline=json.loads((ROOT/'records/skill_invocations/2026-10-19_verify-and-package/baseline_manifest.json').read_text())
differences=[r['path'] for r in baseline if not (ROOT/r['path']).exists() or sha256((ROOT/r['path']).read_bytes()).hexdigest()!=r['sha256']]
assert not differences,differences
required=[
 'AGENTS.md','README.md','STATUS.md','records/source_manifest.csv','sources/input_restore_manifest.json',
 'docs/theory.md','docs/hypothesis_matrix.csv','docs/variable_dictionary.csv',
 'docs/design_and_models.md','docs/execution_specification.md','docs/model_diagram.mmd',
 'docs/analysis_inventory.csv','docs/limitations.md','docs/follow_up.md',
 'docs/student_review.md','records/handoffs.md','records/checkpoints.md',
 'records/skill3_decision_audit.md','records/access_status.md',
 '.agents/skills/specify-empirical-study/SKILL.md',
 '.agents/skills/reproduce-and-diagnose/SKILL.md','.agents/skills/verify-and-package/SKILL.md',
 'analysis/run_verified_replication.py','analysis/run_replication.py',
 'outputs/reproduced/reliability/reliability_coefficients.csv',
 'outputs/reproduced/descriptives/ordinal/item_descriptives.csv',
 'outputs/reproduced/descriptives/ordinal/reference_descriptives.csv',
 'outputs/reproduced/models/ordinal/ordinal_coefficients.csv',
 'outputs/reproduced/models/M2_fit.json','outputs/reproduced/models/M3_fit.json',
 'outputs/reproduced/predictions/ordinal/M1_predictive_margins.csv',
 'outputs/reproduced/predictions/binary_margins_ames.csv','outputs/reproduced/hypothesis_tests.csv',
 'outputs/verification/comparison_all.csv','outputs/verification/comparison_coverage.csv',
 'outputs/verification/independent_checks/checks.json','outputs/verification/interpretation_audit.md',
 'outputs/verification/sensitivity/country_deletion_coefficients.csv',
 'records/run_logs/skill3/clean_restart/receipt.json',
 'records/run_logs/skill3/verified_clean_restart/receipt.json',
 'records/skill_tests/verify-and-package/TEST_REPORT.md',
 'report/verification/01_results_comparison.docx',
 'report/verification/02_python_stata_equivalence.docx','requirements-lock.txt',
 'report/submission_checklist.md']
files=[{'path':rel,'exists':(ROOT/rel).is_file(),
         'bytes':(ROOT/rel).stat().st_size if (ROOT/rel).is_file() else None} for rel in required]
independent=json.loads((ROOT/'outputs/verification/independent_checks/checks.json').read_text())
clean=json.loads((ROOT/'records/run_logs/skill3/verified_clean_restart/receipt.json').read_text())
summary=json.loads((ROOT/'outputs/verification/summary.json').read_text())
evidence={
 'checked_utc':datetime.now(timezone.utc).isoformat(),'user_facing_date':'2026-10-20',
 'scope':'All 21 assignment pages and saved project evidence. Individual final report excluded.',
 'source':{'path':pdf.relative_to(ROOT).as_posix(),'sha256':sha256(pdf.read_bytes()).hexdigest(),'pages':len(reader.pages),
           'all_pages_text_reviewed':True,'visually_reviewed_pages':[3,14,15]},
 'source_parser_note':'Three wrong-pointing-object warnings. All 21 pages returned readable text. Initial console GBK encoding failed and was rerun with UTF-8.',
 'artifact_presence':files,'missing_listed_artifacts':[r['path'] for r in files if not r['exists']],
 'matrix':{'rows':len(rows),'wrong_width_rows':[r['analysis_id'] for r in rows if None in r or any(v is None for v in r.values())],
           'incomplete_support_rows':incomplete,'s1_entry':next(r for r in rows if r['analysis_id']=='S1')},
 'dictionary':{'verified_main_rows':sum('verified against actual' in r['verification_status'] for r in dictionary),
               'unverified_auxiliary_rows':[r['concept'] for r in dictionary if 'pending' in r['actual_data_variable']],
               'metadata_only_observation':{'observed_on':'2026-10-20','candidate_columns_present':
                 ['valenz_akteur','genuinekonstruierte_resp_akteur','rolle_allgemein','geschlecht','date_published','mediaoutlet'],
                 'interpretation':'Column names observed through pyreadstat metadata-only reads. This is not a complete codebook-to-value-label mapping.'}},
 'executed_evidence':{'independent_checks':len(independent),'independent_all_passed':all(r['passed'] for r in independent),
   'clean_returncode':clean['returncode'],'clean_numeric_comparisons_all_passed':all(r['numeric_exact'] for r in clean['numeric_comparisons']),
   'comparison_summary':summary,'protected_files_checked':len(baseline),'protected_changes':differences},
 'github_read_only_check':{'observation_date':'2026-10-20',
  'observation_source':'Actual read-only connector responses in this audit session. The script records this dated observation and does not refresh GitHub by itself.',
  'repository':'https://github.com/jiayima961/COMD7290-Research-Replication-Ma-Jiayi',
  'main_commit':'e3f23cc71d9fe1c6bbe4528d68503fefcb895fd5','visibility':'public',
  'releases':[],'tag_refs':[],'fffchaobu_permission_response':'read',
  'invitation_acceptance':'unverified. Public read permission does not establish collaborator membership or acceptance.',
  'methods':['GitHub get_repo','GitHub get_repo_collaborator_permission','GET releases','GET git/matching-refs/tags/','GET git/ref/heads/main'],
  'failed_request':'GET tags was rejected by the connector URL allowlist. Read-only Git matching-refs endpoint succeeded.'},
 'new_scientific_fits':False,'new_human_approvals':False,'final_report_read_or_edited':False,
 'github_mutations':False,'final_release_created':False}
(OUT/'audit_evidence.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
print(json.dumps({'assignment_pages':len(reader.pages),'listed_artifacts':len(files),
 'missing_listed_artifacts':evidence['missing_listed_artifacts'],
 'incomplete_support_matrix_rows':len(incomplete),'protected_files_unchanged':len(baseline),
 'final_report_excluded':True},indent=2))
