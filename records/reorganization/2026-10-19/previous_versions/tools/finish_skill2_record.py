"""Finalize mutable indexes and create a hash-bound local skill-2 receipt."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import csv,json,re,platform
import pandas as pd
root=Path(__file__).resolve().parents[1]
def replace(name,old,new):
    p=root/name;s=p.read_text(encoding='utf-8-sig');p.write_text(s.replace(old,new),encoding='utf-8')
replace('README.md','**Current stage: student theory explanation v2 has received round-2 feedback. Foundational reading notes and full specification approval remain pending; research models have not been fitted.**','**Current stage: skill-2 Python analyses and numerical verification completed with documented historical-software equivalence limits. See the results index. Student reading notes, diagram and final interpretation remain pending.**')
for old,new in [
('Student v2 reviewed; full specification pending','Student v2 reviewed; source-bound execution specification recorded'),
('Initial draft; exact fields still to complete','12 executed directional targets plus non-hypothesis analyses; linked outputs'),
('Initial canonical draft; source/data conflicts remain visible in skill records','Focal variables verified against actual data/code; unused metadata remains labelled'),
('Drafts requiring full source/settings review','Executed model mapping; historical numerical limits documented'),
('Canonical planning inventory','Actual execution coverage and explicit unresolved items'),
('Research fits and reproduced results pending','Actual fits, coefficients, uncertainty, predictions and comparisons saved'),
('future scripts, outputs and conclusions','executed scripts, outputs and conclusions'),
('Exact research rerun instructions will be added when that implementation exists.','See analysis/run_replication.py and docs/replication_results.md for rerun commands.')]:replace('START_HERE.md',old,new)
replace('AGENTS.md','- Before substantive estimation, finish and obtain the student\'s review of the theory–measurement–model specification. Runtime, integration settings, software versions, missing-data treatment and prediction conventions must be recorded from inspected sources.','- D011 explicitly authorizes source-bound execution of the original statistical specification. Record runtime, integration settings, software versions, missing-data treatment and prediction conventions; do not infer final scientific acceptance or human reading completion.')
replace('AGENTS.md','The available repository, Python-environment and skill-specification checks are not full statistical reproduction entry points. The project Python foundation is installed; the complete study engine implementation and rerun command remain pending.','The Python study modules and analysis/run_replication.py now provide a real rerun entry point. See docs/replication_results.md for executed analyses, independent numerical checks and historical finite-grid/build limitations. Repository checks alone remain insufficient evidence of statistical reproduction.')
replace('records/agent_records.md','| reproduce-and-diagnose | .agents/skills/reproduce-and-diagnose/SKILL.md | Official quick_validate.py passed | Actual repository-cwd discovery; invocation pending | Pending |','| reproduce-and-diagnose | .agents/skills/reproduce-and-diagnose/SKILL.md | Official quick_validate.py passed; version 1.1.0 | Actual repository-cwd discovery and explicit invocation; scoped branch verification | Real reliability/descriptive/M1/M2/M3/null/prediction outputs; documented diagnostic and equivalence limits |')
replace('records/agent_records.md','student revision pending |','student v2 reviewed in round 2 |')
replace('docs/assignment_checklist.md','Structure populated; exact specifications and execution evidence pending','12 executed directional targets and non-hypothesis coverage linked to source, scripts and outputs')
replace('docs/assignment_checklist.md','skills 2/3 invocation pending','skill 2 invoked, run and numerically checked; skill 3 pending')
replace('docs/assignment_checklist.md','Inputs downloaded; matching, specification, and estimation pending','Computed reliability, descriptive, ordinal, nested binary, null, probability and AME outputs; limitations retained in results index')
def append_once(name,heading,body):
    p=root/name;s=p.read_text(encoding='utf-8-sig')
    if heading not in s:p.write_text(s+'\n\n'+heading+'\n\n'+body+'\n',encoding='utf-8')
append_once('records/decisions.md','## D011 — Authorized Python-only reproduction and honest equivalence boundary',
'''The user requested completion/testing of skill 2, checking data and reproducing reliability, descriptives and all original hypothesis models in Python, with all results saved in designated project folders. They expressly required the original model and settings, then asked to resume after usage resets. This authorizes real source-bound statistical execution and supersedes earlier postponement. The original model family, variables, recodes, nesting and seven-point setting are retained; unknown original build/internal grid details are not invented. Independent integral and curvature checks plus explicit discrepancies accompany estimates. No student reading, final scientific acceptance, GitHub synchronization or submission is inferred.''')
append_once('records/agent_records.md','## Skill 2: real Python reproduction and validation',
'''Applied reproduce-and-diagnose 1.1.0 with skill-creator guidance. Actual source inspection, independent-rating reliability, descriptive summaries, M1/alternative links/diagnostics, M2/M3 and their nulls, marginal predictions and 12 hypothesis targets are saved. Scoped ordinal/reliability/GLMM checks used separate agent paths; source fixtures and final vectors were independently checked. Runtime discovery passed after resolving sandbox-denied Codex temporary access; earlier failed attempts remain recorded. The binary batch completed in 684.56 seconds. Full covariance, runtimes, source hashes, failures and final comparisons are retained. See docs/replication_results.md, records/skill_tests/reproduce-and-diagnose/TEST_REPORT.md and records/skill_invocations/2026-10-18_reproduce-and-diagnose/README.md. No Stata, new dependency installation, GitHub push or submission was performed.''')
append_once('records/handoffs.md','## Current handoff: completed skill-2 computations',
'''Start from START_HERE.md and docs/replication_results.md, then the execution specification, comparison.csv, hypothesis_tests.csv and branch diagnostics. Three primary models and two nulls have actual outputs; do not rerun expensive fits merely to recover context. All four binary fits have independent final-vector integration and curvature evidence. Keep M2's printed-value discrepancy, generalized ordinal diagnostic failure, reliability repeated-coder/build issues and exact finite-grid caveats visible. Earlier theory submissions and feedback remain unchanged. Remaining coursework includes skill 3, separately justified substantive sensitivity, student reading/diagram records and final report/acceptance. No latest outputs were pushed to GitHub.''')
receipt=root/'records/skill_invocations/2026-10-18_reproduce-and-diagnose';receipt.mkdir(parents=True,exist_ok=True)
(receipt/'README.md').write_text('''# Skill 2 invocation and handoff

The user authorized faithful Python-only data checks, reliability/descriptive/hypothesis-model reproduction and validation, requiring all results to be saved for later comparison and teacher review. Subsequent messages requested resumption after usage resets. This is an English summary of the request, not a fabricated verbatim transcript.

Read the [results index](../../../docs/replication_results.md), [execution specification](../../../docs/execution_specification.md), [skill test record](../../skill_tests/reproduce-and-diagnose/TEST_REPORT.md), and [final artifact receipt](final_receipt.json). Actual logs are under records/run_logs/skill2; individual branches bind their own inputs, source methods and outputs.

The skill was explicitly loaded and executed in this chat. Native branch agents performed scoped independent implementation/verification; this was not a blinded external audit. Exact underlying per-run model IDs were not exposed. Code and results are local and English; original inputs and earlier student versions remain unchanged.

Prior mutable drafts are preserved under before/. The current canonical dictionary, matrix and inventory now identify executed source-bound work. The source specification was authorized by the user; final interpretation and reading attestations remain student-owned.

Observed failures are retained: interrupted/slow candidate fits, invalid optimizer trial adaptation, initial app-server sandbox failure, source diagnostic nonidentification, and historical method ambiguities. A document-finalization helper initially had an unmatched parenthesis and was corrected before it executed. Final validations inspect real saved artifacts; they do not declare every published number matched or every historical default recovered.
''',encoding='utf-8')
models={}
for mid in ['M2','M2_null','M3','M3_null']:
    fit=json.loads((root/f'outputs/reproduced/models/{mid}_fit.json').read_text())
    cur=json.loads((root/f'outputs/diagnostics/glmm/{mid}_independent_curvature.json').read_text())
    models[mid]={'log_likelihood':fit['log_likelihood'],'converged':fit['converged_and_validated'],'optimizer_success':fit['optimizer_success'],
        'independent_scaled_gradient_passed':cur['scaled_gradient_check_passed'],'all_independent_hessians_spd':cur['all_step_hessians_positive_definite']}
checks={}
checks['four_binary_fits_and_independent_curvature_pass']=all(all(v[k] for k in ['converged','optimizer_success','independent_scaled_gradient_passed','all_independent_hessians_spd']) for v in models.values())
checks['twelve_directional_targets']=len(pd.read_csv(root/'outputs/reproduced/hypothesis_tests.csv'))==12
checks['sixty_reliability_coefficients']=len(pd.read_csv(root/'outputs/reproduced/reliability/reliability_coefficients.csv'))==60
checks['forty_five_model_comparison_cells']=len(pd.read_csv(root/'outputs/comparison.csv'))==45
checks['original_hashes_unchanged']=all(r['matches_manifest'] for r in json.loads((root/'outputs/diagnostics/data_audit.json').read_text())['original_files'])
checks['runtime_discovery_passed']=json.loads((root/'records/skill_tests/reproduce-and-diagnose/discovery.json').read_text())['status']=='passed'
link_errors=[];link_count=0
for rel in ['START_HERE.md','README.md','docs/replication_results.md','analysis/README.md','records/skill_invocations/2026-10-18_reproduce-and-diagnose/README.md']:
    p=root/rel
    for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8-sig')):
        link=link.strip('<>').split('#')[0]
        if not link or '://' in link:continue
        if link=='final_receipt.json':continue
        link_count+=1
        if not (p.parent/link).exists():link_errors.append({'document':rel,'link':link})
checks['navigation_links_resolve']=not link_errors
files=[]
for folder in ['analysis','tests/skill2','outputs/reproduced','outputs/diagnostics','records/run_logs/skill2','records/skill_tests/reproduce-and-diagnose','.agents/skills/reproduce-and-diagnose']:
    for p in (root/folder).rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts:
            files.append({'path':p.relative_to(root).as_posix(),'sha256':sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
for name in ['outputs/comparison.csv','docs/execution_specification.md','docs/replication_results.md','docs/hypothesis_matrix.csv','docs/analysis_inventory.csv','docs/variable_dictionary.csv']:
    p=root/name;files.append({'path':name,'sha256':sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
record={'recorded_at_utc':datetime.now(timezone.utc).isoformat(),'skill':'reproduce-and-diagnose','skill_version':'1.1.0','python':platform.python_version(),
 'models':models,'checks':checks,'navigation_link_count':link_count,'navigation_errors':link_errors,'artifact_manifest':files,
 'model_comparison_rounding_match_count':44,'model_comparison_cell_count':45,
 'scope_limit':'Completed computation and numerical verification with explicit historical software/grid and invalid-diagnostic limits; not exact executable equivalence or final course submission.',
 'github_uploaded':False,'status':'saved_results_verified_with_documented_limits' if all(checks.values()) else 'record_check_failed'}
(receipt/'final_receipt.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':record['status'],'checks':checks,'links':link_count,'link_errors':link_errors,'artifacts':len(files)},indent=2))
if not all(checks.values()):raise SystemExit(1)
