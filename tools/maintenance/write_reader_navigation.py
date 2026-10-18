"""One-time reader-navigation update for the 2026-10-19 non-destructive migration."""
import csv
from hashlib import sha256
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / 'records/reorganization/2026-10-19/previous_versions'

DOCUMENTS = {
'README.md': '''# COMD7290 Research Replication — Ma Jiayi

Python reproduction of Löb et al., *Unpacking the Determinants of Outrage and Recognition in Public Discourse*, DOI [10.1177/19401612221084206](https://doi.org/10.1177/19401612221084206). COMD7290 Option 3, content analysis. This is work in progress, with completed skills 1 and 2; it is not the final submission.

**Start with [START_HERE.md](START_HERE.md).** To use the tested skills, open this repository as the agent's working folder and follow the [skill guide](docs/skills/README.md). The actual skill packages are in [.agents/skills/](.agents/skills/).

| Reader's question | Go to |
| --- | --- |
| What was predicted, and how was it tested? | [Hypothesis matrix](docs/hypothesis_matrix.csv) → [execution specification](docs/execution_specification.md) → [analysis code](analysis/README.md) → [hypothesis tests](outputs/reproduced/hypothesis_tests.csv) → [results and limitations](docs/replication_results.md) |
| Where are the two tested skills? | [Skill 1: theory/specification](.agents/skills/specify-empirical-study/SKILL.md), [Skill 2: reproduce/diagnose](.agents/skills/reproduce-and-diagnose/SKILL.md), [invocation instructions and test evidence](docs/skills/README.md) |
| Where are the numerical results? | [Results index](outputs/README.md), [published-versus-reproduced table](outputs/comparison.csv) |
| What did the student write and how did AI respond? | [Ordered review trail](records/README.md) |
| How can I run this on my computer? | [Setup and rerun guide](docs/guides/teacher_quickstart.md), [input access and verification](sources/README.md), [environment](environment.md) |
| What remains? | [Current status](STATUS.md), [assignment checklist](docs/assignment_checklist.md) |

```text
.agents/skills/  Agent-discoverable skill packages
docs/           Theory, hypotheses, model specifications, reviews and guides
data/           Original and prepared data (local; access instructions tracked)
sources/        Source provenance and input-restoration manifest
analysis/       Statistical Python modules and notebook entry points
tests/          Specification and numerical verification programs
outputs/        Published targets, reproduced results and diagnostics
records/        Student inputs, actual invocations, tests and execution logs
report/         Final-report preparation (unfinished)
tools/          Setup, input restoration, logging and repository checks
tmp/, .venv/    Local runtime/cache files, excluded from Git
```

The saved results include independent-coder reliability, descriptives, M1 ordinal tone, M2/M3 nested binary models, predictions and 12 directional hypothesis targets. Of 45 published coefficient/SE/OR cells, 44 match printed rounding; the remaining discrepancy is retained. Historical Stata integration details and reliability-package builds are not fully recovered. See [the results explanation](docs/replication_results.md) before interpreting agreement as robustness.

Quick rerun after setting up Python and restoring inputs, from the repository root:

```powershell
python tools/restore_inputs.py
python tools/check_repository.py
python analysis/run_replication.py --stage data
python analysis/run_replication.py
```

Use the Python interpreter from the project's activated environment. Ordinary Python works without RTK; when RTK is available, the logging helper uses it automatically. The full run can take substantial time and updates canonical analysis outputs; preserve a copy for a new independent rerun. The notebook [analysis/01_replication.ipynb](analysis/01_replication.ipynb) invokes the same stages. Saved historical logs remain the evidence of the completed original runs.

Author data, third-party PDFs/method files and subject-level derived arrays remain local where redistribution is unresolved. Their access routes, exact hashes and restoration instructions are included; the repository supplies our skill packages, code, aggregate results, tests and records. No Stata licence is needed for the Python calculations.

The [2026-10-19 reorganization record](records/reorganization/2026-10-19/README.md) maps old paths to new paths and verifies preserved files. No existing file was deleted. The repository remains private; no collaborator invitation, release or submission is part of this update.
''',
'START_HERE.md': '''# Start here

Read this project in the following order. Current scientific results are in the main folders; earlier tests and student versions are retained as evidence.

1. **Purpose and progress:** [README](README.md), [STATUS](STATUS.md), [course checklist](docs/assignment_checklist.md).
2. **Student theory and feedback:** [student v1](records/student_inputs/2026-10-18_initial_theory_explanation_v1.txt) → [feedback 1](docs/theory_feedback_v1.md) → [student v2](records/student_inputs/2026-10-18_revised_theory_explanation_v2.txt) → [feedback 2](docs/theory_feedback_v2.md). Check the [records index](records/README.md) for receipts and attribution.
3. **Theory to test:** [theory](docs/theory.md), [hypothesis matrix](docs/hypothesis_matrix.csv), [variables](docs/variable_dictionary.csv), [design](docs/design_and_models.md), [execution specification](docs/execution_specification.md). The [model diagram](docs/model_diagram.mmd) is an AI-assisted draft pending student review.
4. **Use the skills:** [two tested skills, supporting files, invocation examples and evidence](docs/skills/README.md). Skill 3 is still a scaffold. Open the repository root, rather than its parent folder, for native skill discovery.
5. **Inspect results:** [results explanation](docs/replication_results.md) → [results folders](outputs/README.md) → [comparison table](outputs/comparison.csv) → [12 hypothesis tests](outputs/reproduced/hypothesis_tests.csv) → [diagnostics](outputs/diagnostics/README.md).
6. **Rerun:** [teacher quickstart](docs/guides/teacher_quickstart.md) → [inputs](sources/README.md) → [analysis entry points](analysis/README.md) → [verification programs](tests/README.md).
7. **Understand the work trail:** [records index](records/README.md), [decisions](records/decisions.md), [execution logs](records/run_logs/), [reorganization map/checks](records/reorganization/2026-10-19/README.md).
8. **Finish the assignment later:** [limitations](docs/limitations.md), [follow-up](docs/follow_up.md), [report guide](report/README.md), [submission checklist](report/submission_checklist.md). Human reading attestations, final scientific acceptance, skill 3 and a separate substantive sensitivity analysis remain pending.

New reviews and runs should use the next version or a new dated record. Do not overwrite earlier student inputs or historical execution receipts.
''',
'docs/README.md': '''# Study documents

The following files are the canonical study documents. Their paths stay stable because the skill contracts and analysis programs refer to them.

| Purpose | Files |
| --- | --- |
| Theory and student review | [theory](theory.md), [feedback v1](theory_feedback_v1.md), [feedback v2](theory_feedback_v2.md), [student review worksheet](student_review.md) |
| Hypotheses and coverage | [hypothesis matrix](hypothesis_matrix.csv), [analysis inventory](analysis_inventory.csv) |
| Variables and models | [dictionary](variable_dictionary.csv), [design](design_and_models.md), [execution specification](execution_specification.md), [diagram](model_diagram.mmd) |
| Results and interpretation | [replication results](replication_results.md), [limitations](limitations.md), [follow-up](follow_up.md) |
| Course requirements | [assignment checklist](assignment_checklist.md) |
| Use the project | [skill guide](skills/README.md), [teacher quickstart](guides/teacher_quickstart.md), [folder/workflow guide](guides/github_structure_and_workflow.txt), [early Python route assessment](guides/python_route_assessment.md), [skill-1 usage](skill1_usage.md) |

The early route assessment records feasibility questions before skill-2 execution. Use the execution specification and replication-results document for the current numerical status.
''',
'docs/skills/README.md': '''# Use the two tested project skills

Open the **whole repository root** as your agent's working folder. Copying only a SKILL.md is insufficient: these are project skills that use the repository's documents, code, tests and inputs. No global skill installation or account credentials are required. The canonical packages are under `.agents/skills/`, as required by the assignment.

| Skill | Complete package and supporting project files | Evidence of actual use |
| --- | --- | --- |
| 1. Theory, variables and models (`specify-empirical-study`, 1.0.1) | [SKILL.md](../../.agents/skills/specify-empirical-study/SKILL.md), [output contract](../../.agents/skills/specify-empirical-study/references/output_contract.md), [validator](../../.agents/skills/specify-empirical-study/scripts/validate_specification.py), [test-input helper](../../tools/prepare_specification_test.py), [12 regression cases](../../tests/skill1_specification/test_validator_cases.py); canonical documents are indexed in [docs](../README.md) | [Forward-test report](../../records/skill_tests/specify-empirical-study/TEST_REPORT.md), [first real theory review](../../records/skill_invocations/2026-10-18_specify-empirical-study_theory-review/), [second real theory review](../../records/skill_invocations/2026-10-18_specify-empirical-study_theory-review_v2/) |
| 2. Data checks, reproduction and diagnosis (`reproduce-and-diagnose`, 1.1.0) | [SKILL.md](../../.agents/skills/reproduce-and-diagnose/SKILL.md), [execution contract](../../.agents/skills/reproduce-and-diagnose/references/execution_contract.md), [analysis modules](../../analysis/README.md), [numerical tests](../../tests/README.md), [execution specification](../execution_specification.md), [input instructions](../../sources/README.md) | [Execution/test report](../../records/skill_tests/reproduce-and-diagnose/TEST_REPORT.md), [native discovery](../../records/skill_tests/reproduce-and-diagnose/discovery.json), [real invocation and receipt](../../records/skill_invocations/2026-10-18_reproduce-and-diagnose/), [run logs](../../records/run_logs/skill2/) |

For Codex, explicitly select the skill or send one of these prompts from the repository root:

```text
Use $specify-empirical-study from .agents/skills/specify-empirical-study.
Review the supplied theory explanation against the registered sources.
Preserve the student input, save new feedback as a new version, and record the invocation.
Do not invent student approvals or completed readings.
```

```text
Use $reproduce-and-diagnose from .agents/skills/reproduce-and-diagnose.
Read docs/execution_specification.md, check the registered input hashes, and
reproduce the original Python analyses. Preserve the existing evidence in a copy
before a new run, save all results and diagnostics, and disclose unresolved
historical-software settings. Use analysis/run_replication.py as the entry point.
```

If another agent framework does not discover `.agents/skills`, explicitly ask it to read the appropriate SKILL.md and its linked contract, then follow those instructions in this repository. That is manual loading, not evidence of native discovery. The skill-1 validator example uses `rtk proxy`; an agent without RTK can run the identical validator with `python <skill-path>/scripts/validate_specification.py ...`.

Restore source inputs and set up Python using the [teacher quickstart](../guides/teacher_quickstart.md) before requesting a full reproduction. Each skill states its inputs, procedure, outputs, validation and stopping rules. Reading the package or passing static validation alone does not prove successful scientific use.

[Skill 3](../../.agents/skills/verify-and-package/SKILL.md) remains a scaffold for later verification and final packaging. It must not be presented as a third completed/tested skill. This folder is a reader guide; `.agents/skills/` is the only canonical skill installation in the repository.
''',
'docs/guides/teacher_quickstart.md': '''# Setup and rerun on another computer

1. Clone the private repository with an authorized GitHub account and open its root folder in the agent. Start with [the skill guide](../skills/README.md). Do not open only the parent folder or copy only the skill entry files.
2. Install Python 3.12 and create an environment. These Windows commands assume the Python launcher is installed:

```powershell
py -3.12 -m venv .venv
.venv/Scripts/python.exe -m pip install --index-url https://pypi.org/simple -r requirements-lock.txt
.venv/Scripts/python.exe -m pip check
.venv/Scripts/Activate.ps1
```

If activation is unavailable, replace `python` below with `.venv/Scripts/python.exe`. The lock records the tested Windows environment. Other operating systems need a separately resolved environment and renewed checks. [environment.md](../../environment.md) describes the original machine. RTK is optional.

3. Obtain lawful copies of the assignment and article; place them at `sources/local/COMD7290_assignment.pdf` and `sources/local/Lob_et_al_2024.pdf`. File names alone do not establish the expected version. The manifests give exact hashes. If your copy differs, record and investigate that difference rather than disabling hash checks.
4. Restore registered author datasets, independent ratings, codebooks and archived method sources:

```powershell
python tools/restore_inputs.py --download --report records/run_logs/input_restoration.json
python tools/restore_inputs.py
python tools/check_repository.py
```

The first command requests network downloads only from the manifest's direct URLs and extracts named ZIP members. Existing files are never overwritten. Downloads must match saved SHA-256 values before being written. A changed/unavailable upstream version causes a recorded failure; obtain the registered version lawfully and keep the mismatch visible. The page snapshot may change over time and may need to be supplied from a lawful archived copy. The original student's computer already has these sources. Repository code and aggregate results can be inspected without them; source-dependent validation and refitting require them.

5. Run selected stages or all stages from the repository root:

```powershell
python analysis/run_replication.py --stage data
python analysis/run_replication.py --stage reliability
python analysis/run_replication.py --stage ordinal
python analysis/run_replication.py --stage binary
python analysis/run_replication.py --stage summaries
python analysis/run_replication.py --stage checks
```

`python analysis/run_replication.py` runs all stages in that order. Full nested-model fits can take substantial time. Preserve a copy of the repository/results before a new independent run because canonical output names are reused; dated wrapper logs are created for each run. No Stata executable is used. Do not accept a failed convergence/identification diagnostic as a successful fit.

6. For notebooks, install/register the project kernel and launch from this environment:

```powershell
python -m ipykernel install --sys-prefix --name comd7290-python --display-name "Python (COMD7290 - Ma Jiayi)"
python -m notebook
```

On Windows the root `Start_Jupyter_Notebook.cmd` is an alternative. Open [01_replication.ipynb](../../analysis/01_replication.ipynb); it calls the same modules. The environment notebook uses synthetic data. Neither notebook's mere presence is evidence of a completed research run.

7. Read [replication results](../replication_results.md), [comparison.csv](../../outputs/comparison.csv), [hypothesis_tests.csv](../../outputs/reproduced/hypothesis_tests.csv), and [diagnostics](../../outputs/diagnostics/README.md). Historical finite-grid/build identity remains unresolved even where printed values agree.

To reconstruct the archived skill-1 test inputs after restoring canonical sources, use `python tools/prepare_specification_test.py --case-root records/skill_tests/specify-empirical-study/forward_case`. Then use the regression command in [tests/README.md](../../tests/README.md). New test results belong in new dated paths, not over the historical receipts.
''',
'analysis/README.md': '''# Analysis entry points

Read [the execution specification](../docs/execution_specification.md), [results explanation](../docs/replication_results.md) and [setup/input instructions](../docs/guides/teacher_quickstart.md).

Run from the repository root with the project Python environment:

```powershell
python analysis/run_replication.py
python analysis/run_replication.py --stage data
```

RTK is optional. The same stages are available in [01_replication.ipynb](01_replication.ipynb). The runner logs commands and stops on failure. A full run replaces canonical numerical outputs; copy the existing result set before an independent rerun. Binary fitting can take substantial time.

| Stage | Programs | Saved outputs |
| --- | --- | --- |
| data | prepare_replication.py | Local data/prepared; outputs/diagnostics/data_audit.json |
| reliability | reliability_reproduction.py | outputs/reproduced/reliability; outputs/diagnostics/reliability |
| ordinal | ordinal_reproduction.py | Descriptives; models/ordinal; predictions/ordinal; diagnostics/ordinal |
| binary | run_binary_models.py, nested_logit.py | M2/M3 full/null fits, coefficients and covariance |
| summaries | binary_predictions.py, compare_replication.py | Binary margins/AMEs; comparison.csv; hypothesis_tests.csv |
| checks | tests/skill2 programs | Independent data/likelihood/curvature diagnostics |

[00_environment_check.ipynb](00_environment_check.ipynb) is a synthetic environment check. [01_replication.ipynb](01_replication.ipynb) is an unexecuted interface to the real saved modules; actual study execution evidence is in [records/run_logs/skill2](../records/run_logs/skill2/). These distinctions must survive reuse.

The statistical model modules and saved numerical results were preserved during the directory cleanup. Historical finite-grid and package-build identity remains limited; see the execution specification rather than interpreting code portability as exact original executable parity.
''',
'outputs/README.md': '''# Numerical results

Start with [the results explanation](../docs/replication_results.md), then use this map. These are actual saved Python calculations, not unexecuted templates.

| Result | Location |
| --- | --- |
| Original published targets | [published](published/) |
| 45 coefficient/SE/OR comparisons (44 within printed rounding) | [comparison.csv](comparison.csv) |
| 12 directional hypothesis targets | [hypothesis_tests.csv](reproduced/hypothesis_tests.csv) |
| Reliability: 60 coefficient rows and 720 benchmark rows | [reliability](reproduced/reliability/) |
| Item/reference counts and proportions | [descriptives](reproduced/descriptives/) |
| M1 ordinal and M2/M3 binary full/null fits | [models](reproduced/models/) |
| Probabilities and discrete marginal effects | [predictions](reproduced/predictions/) |
| Independent checks, convergence, integration and failed diagnostics | [diagnostics index](diagnostics/README.md) |

Published values and reproduced values are separate. Unidentified generalized ordinal diagnostics and the M2 discrepancy remain visible. Subject-level rating matrices/influence arrays stay local and are regenerated by the reliability script; aggregate reliability tables and method checks are shared. No existing local result was deleted during reorganization.
''',
'outputs/reproduced/README.md': '''# Reproduced results

These folders contain completed Python calculations. See [the results index](../README.md) and [interpretation/limits](../../docs/replication_results.md).

- [reliability](reliability/): independent-coder coefficients, uncertainty and probabilistic benchmarks.
- [descriptives](descriptives/): sample counts and outcome distributions.
- [models](models/): M1 ordinal and M2/M3 binary full/null artifacts, coefficient/covariance tables and fit diagnostics.
- [predictions](predictions/): ordinal and binary probabilities/AMEs.
- [hypothesis_tests.csv](hypothesis_tests.csv): all 12 directional author-hypothesis targets, including opposite-direction and non-significant results.

The published comparison targets are in [../published](../published/). Do not replace a reproduced estimate with its target to remove a discrepancy.
''',
'outputs/diagnostics/README.md': '''# Numerical and data diagnostics

- [data_audit.json](data_audit.json): source/sample construction; [data_independent_checks.json](data_independent_checks.json): independent counts plus invalid-code rejection/recovery.
- [reliability](reliability/): known-answer and independent checks, selections, missingness and source-method provenance. Subject-level matching/influence artifacts remain local and can be rebuilt.
- [ordinal](ordinal/): original-link fits, gradients/probabilities and the retained invalid/unidentified generalized-model diagnostics.
- [glmm](glmm/): independent likelihood fixtures, finite-grid comparisons, final-vector gradients and observed-curvature checks for M2/M3 and null models.
- [binary_likelihood_comparisons.csv](binary_likelihood_comparisons.csv): full/null comparison quantities.
- [binary_prediction_integration.csv](binary_prediction_integration.csv): prior-marginal prediction integration checks.

Read [replication_results.md](../../docs/replication_results.md) for what passed, what failed, and which historical settings remain unrecovered. Passing numerical checks does not establish exact Stata-build equivalence or causal identification.
''',
'records/README.md': '''# Records in reading order

| Order | Material | Location |
| --- | --- | --- |
| 1 | Student's original theory explanation | [v1](student_inputs/2026-10-18_initial_theory_explanation_v1.txt) |
| 2 | First feedback and its actual invocation | [feedback](../docs/theory_feedback_v1.md), [record](skill_invocations/2026-10-18_specify-empirical-study_theory-review/) |
| 3 | Student's revised explanation | [v2](student_inputs/2026-10-18_revised_theory_explanation_v2.txt) |
| 4 | Second feedback and its actual invocation | [feedback](../docs/theory_feedback_v2.md), [record](skill_invocations/2026-10-18_specify-empirical-study_theory-review_v2/) |
| 5 | Skill 1 forward test and regression evidence | [test report](skill_tests/specify-empirical-study/TEST_REPORT.md) |
| 6 | Skill 2 real reproduction and verification | [invocation](skill_invocations/2026-10-18_reproduce-and-diagnose/), [test report](skill_tests/reproduce-and-diagnose/TEST_REPORT.md), [runtime logs](run_logs/skill2/) |
| 7 | Directory cleanup, preserved versions and post-move checks | [2026-10-19 reorganization](reorganization/2026-10-19/README.md) |
| 8 | Current decisions and handoffs | [decisions](decisions.md), [agent record](agent_records.md), [handoffs](handoffs.md), [checkpoints](checkpoints.md) |

[source_manifest.csv](source_manifest.csv) identifies original research inputs and hashes. [sources/input_restore_manifest.json](../sources/input_restore_manifest.json) adds reproducible access paths for archived external methods. Earlier commands and absolute paths in completed receipts describe the original computer; they are historical evidence, not current installation requirements.

Keep old student inputs and completed execution receipts unchanged. `reorganization/.../previous_versions` is an archive of replaced navigation/wrappers, not a competing current result set. Rebuilding study outputs does not establish that the student read a foundational text or approved the analysis.
''',
'tests/README.md': '''# Verification programs

These programs test different claims; a structural check alone is not evidence of a successful statistical reproduction. Saved original test evidence is under [records/skill_tests](../records/skill_tests/) and [outputs/diagnostics](../outputs/diagnostics/).

| Programs | Purpose |
| --- | --- |
| skill1_specification/test_validator_cases.py | 12 meaningful specification cases, including wrong hypothesis direction, hierarchy and reliability inputs |
| skill2/data_checks.py | Independent raw counts and copied invalid-code rejection/recovery |
| skill2/glmm_reference.py, check_nested_logit.py | Independently integrated likelihoods and structural fixtures |
| skill2/check_glmm_full_likelihood.py | Independent saved-vector likelihood and gradient checks |
| skill2/check_glmm_fit_curvature.py | Observed-Hessian steps and covariance/score checks |
| repository/test_portable_execution.py | Runner transport, source restoration, notebook entry points and relocation checks |

After restoring archived case inputs, run skill-1 regression without replacing earlier evidence:

```powershell
python tests/skill1_specification/test_validator_cases.py --case-root records/skill_tests/specify-empirical-study/forward_case --output records/run_logs/skill1_new_regression.json
python tests/repository/test_portable_execution.py
```

`python analysis/run_replication.py --stage checks` reruns the numerical/data checks against restored inputs and saved fits and writes canonical diagnostic files. Use a separate project copy for an independent rerun if you need to retain the present artifacts byte-for-byte. The reorganization record distinguishes post-cleanup smoke tests from the original substantive verification.
''',
'tools/README.md': '''# Project utilities

| Utility | Purpose |
| --- | --- |
| restore_inputs.py | Offline hash check; optional verified download/extraction without overwriting existing files |
| check_repository.py | Material structure, CSV schemas and registered source hashes; no fitting |
| run_logged.py | Real command/stdout/stderr/runtime capture; RTK optional |
| prepare_specification_test.py | Restore ignored source copies for the archived skill-1 forward case |
| probe_skill_discovery.py | Read-only local Codex app-server discovery probe; requires an installed Codex runtime |
| check_python_environment.py | Synthetic environment checks |
| fetch_sources.py | Original acquisition helper retained for historical reproducibility; prefer restore_inputs.py for another computer because it does not revise the historical manifest |
| reorganize_project.py | One-time 2026-10-19 non-destructive migration; refuses a repeat |
| maintenance/ | Historical document/checkpoint writers and notebook builder |

Run current analysis through [analysis/run_replication.py](../analysis/run_replication.py). The maintenance writers contain historical content and can overwrite current narrative files; inspect them before explicitly using one. They are retained because the user requested no file deletion. Their project-root calculation was updated after relocation.
''',
'tools/maintenance/README.md': '''# One-time maintenance helpers

These are preserved historical helpers, separated from the utilities a reader should normally run. Their path calculation follows the new directory. Earlier logs retain the old command paths; see [the migration map](../../records/reorganization/2026-10-19/moves.json).

- build_replication_notebook.py rebuilds the unexecuted notebook interface from the current saved modules.
- finalize_skill2_documents.py and finish_skill2_record.py wrote the 2026-10-18 result narrative/receipts. Do not use them to regenerate a new run's evidence or current navigation.
- record_skill2_interruption.py and update_skill2_context.py wrote historical interruption/context updates.
- write_reader_navigation.py produced the 2026-10-19 reader guides and input-restoration manifest.

No statistical estimation formula was changed as part of moving these files. Use the canonical analysis runner for study calculations.
''',
'.agents/skills/README.md': '''# Project skill packages

The two completed and tested packages are [specify-empirical-study](specify-empirical-study/SKILL.md) and [reproduce-and-diagnose](reproduce-and-diagnose/SKILL.md). Their supporting contracts/scripts are inside these folders; study code and evidence stay at the repository paths linked from them.

See [the invocation and evidence guide](../../docs/skills/README.md). Open the entire repository root for discovery. [verify-and-package](verify-and-package/SKILL.md) is an unfinished third-skill scaffold and is not included in the claim of two completed skills.
''',
'records/reorganization/2026-10-19/README.md': '''# Non-destructive reorganization — 2026-10-19

The user requested two reusable/tested skills, a clearer project layout with no deleted files, and synchronization to the private GitHub repository after local checks.

The assignment's `docs / data / analysis / tests / outputs / records` structure and `.agents/skills` discovery paths are retained. Auxiliary guides moved to docs/guides; one-time writers moved to tools/maintenance. Stable scientific document, code, numerical-result, student-input and historical-receipt paths were preserved. Canonical statistical formulas and existing numerical results were not altered. Logging/notebook/launcher transport now supports ordinary Python when RTK is absent.

- [moves.json](moves.json): every old/new path and excluded untouched runtime directories.
- [before_sha256.json](before_sha256.json): pre-change file fingerprints.
- [previous_versions](previous_versions/): originals of replaced navigation/wrappers and moved helpers. These are historical copies, not current instructions.
- verification.json and validation logs (created after edits): preservation, references, package completeness and portable execution checks.

No original file was deleted. Where an authored file was revised, its prior bytes remain in previous_versions; moves retain the file under its new path. Original data/PDF/method inputs and subject-level derived arrays remain local under existing access restrictions; the GitHub payload supplies access and exact-version restoration instructions. Runtime directories were left in place and were not repackaged.

The existing completed skill invocations and saved model results remain the evidence of research execution. The cleanup checks only establish that layout and transport changes preserve use; they do not constitute a new full independent refit or final course completion. Remote synchronization evidence is recorded separately after the upload.
''',
}


def main():
    before = json.loads((ROOT / 'records/reorganization/2026-10-19/before_sha256.json').read_text(encoding='utf-8'))
    for relative, content in DOCUMENTS.items():
        path = ROOT / relative
        backup = ARCHIVE / relative
        if relative in before and path.is_file() and not backup.exists():
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, backup)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
    files = []
    with (ROOT / 'records/source_manifest.csv').open(encoding='utf-8-sig', newline='') as stream:
        for row in csv.DictReader(stream):
            if not row['local_path'] or not row['sha256']:
                continue
            manual = row['source_id'] in {'assignment', 'selected_article'}
            files.append({'path': row['local_path'], 'sha256': row['sha256'],
                          'url': None if manual else row['url'], 'role': row['source_id'],
                          'access_note': row['url'] if manual else 'Original source; no redistribution licence inferred.',
                          'archive_member': row['source_locator'] if row['source_id'].startswith('package_member_') else None})
    method = ROOT / 'sources/local/skill2_methods'
    recovery = json.loads((method / 'ordinal/source_recovery.json').read_text(encoding='utf-8'))
    for item in recovery['sources']:
        path = method / 'ordinal' / item['file']
        files.append({'path': path.relative_to(ROOT).as_posix(), 'sha256': sha256(path.read_bytes()).hexdigest(),
                      'url': item['url'], 'role': 'ordinal_primary_method'})
    for filename, url in [
        ('kappaetc_2.1.0.ado', 'http://fmwww.bc.edu/repec/bocode/k/kappaetc.ado'),
        ('kappaetc_2.1.0.sthlp', 'http://fmwww.bc.edu/repec/bocode/k/kappaetc.sthlp'),
        ('official_reliabilities_2026-10-18.html', 'https://medcon-doc.github.io/documentation/content-analysis/reliabilities/')]:
        path = method / 'reliability' / filename
        files.append({'path': path.relative_to(ROOT).as_posix(), 'sha256': sha256(path.read_bytes()).hexdigest(),
                      'url': url, 'role': 'reliability_primary_method_or_postfit_comparison'})
    path = ROOT / 'sources/input_restore_manifest.json'
    path.write_text(json.dumps({'schema_version': 1, 'created_date': '2026-10-19',
        'purpose': 'Restore excluded exact-version inputs; do not infer rights or execute Stata sources.',
        'historical_build_limit': 'These method snapshots are inspected sources, not proof of the authors installed original builds.',
        'files': files}, indent=2) + '\n', encoding='utf-8')
    print(f'Wrote {len(DOCUMENTS)} reader guides and {len(files)} exact-version restoration entries.')


if __name__ == '__main__':
    main()
