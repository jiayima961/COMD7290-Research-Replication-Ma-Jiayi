"""Record the user's layout/upload scope without rewriting scientific evidence."""
from pathlib import Path
import shutil
ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / 'records/reorganization/2026-10-19/previous_versions'


def replace_file(relative, text):
    path = ROOT / relative
    backup = ARCHIVE / relative
    if path.exists() and not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)
    path.write_text(text, encoding='utf-8')


def main():
    path = ROOT / 'AGENTS.md'
    replace_file('AGENTS.md', path.read_text(encoding='utf-8') + '''
## Scope update — D012, 2026-10-19

The user authorizes non-destructive project reorganization, packaging the two
completed/tested skills for another agent, and updating the existing private
GitHub repository after local validation. Preserve every existing file, student
draft and completed run record; keep stable scientific-code/result paths and
archive prior versions of revised authored navigation/wrappers. Record moved
paths and verify unchanged statistical modules, inputs and numerical results.
Do not change published/reproduced values as part of cleanup. Use START_HERE.md
and docs/skills/README.md for the reader route. Both project skill packages
remain under .agents/skills; skill 3 is still a scaffold. RTK is a local optional
execution wrapper, not a requirement on the instructor's computer. Sharing
our code, aggregate results and records is authorized; excluded third-party
inputs and subject-level derived data retain access/restoration instructions.
No release, submission, visibility or collaborator change is requested.
''')
    path = ROOT / 'STATUS.md'
    value = path.read_text(encoding='utf-8').replace('Updated: 2026-10-18.', 'Updated: 2026-10-19.')
    value = value.replace('No latest-run upload, final release or submission has been performed.',
        'The D012 repository cleanup and latest-result synchronization are being verified; see records/reorganization/2026-10-19. No final release or submission has been performed.')
    value += '''
## Reader layout and reusable packages (D012)

- Use START_HERE.md and docs/skills/README.md to find both tested skill packages,
  their real invocations and test evidence. Skill 3 remains unfinished.
- Canonical scientific paths are stable. Auxiliary guides are in docs/guides;
  historical writers are in tools/maintenance. Previous versions and a move map
  are retained under records/reorganization/2026-10-19; no file was deleted.
- The runtime wrappers and notebook now support ordinary Python without RTK.
  tools/restore_inputs.py verifies/restores excluded exact-version inputs.
- This cleanup preserves the saved numerical work; it is not a new full refit.
'''
    replace_file('STATUS.md', value)
    replace_file('environment.md', '''# Software and execution environment

The user authorized a project-local Python/Jupyter environment and faithful
Python reproduction. Real analyses were completed on 2026-10-18. See
[replication results](docs/replication_results.md), [execution specification](docs/execution_specification.md)
and [teacher setup](docs/guides/teacher_quickstart.md).

- Tested system: Windows, 64-bit CPython 3.12.14.
- Project environment: `.venv/`, excluded from Git; recreate it on another machine.
- Direct packages: [requirements.txt](requirements.txt); full tested Windows lock:
  [requirements-lock.txt](requirements-lock.txt). Original installation used official PyPI.
- Text: UTF-8; existing CSVs may use a UTF-8 BOM for spreadsheet compatibility.
- RTK is optional. Standard Python runs the wrappers and notebooks. When found
  on PATH, the command logger uses RTK and records that actual command.

The direct package set provides NumPy/Pandas/SciPy, statsmodels/patsy,
pyreadstat/openpyxl, matplotlib/seaborn, krippendorff and Jupyter tools.
The three-level frequentist binary estimator is implemented in
[analysis/nested_logit.py](analysis/nested_logit.py); package installation alone
does not provide or validate that estimator.

For another Windows computer, follow the complete environment/input instructions
in [teacher_quickstart.md](docs/guides/teacher_quickstart.md). Run with the new
environment's Python. Do not copy this machine's `.venv`; it depends on the base
interpreter. The lock file includes Windows dependencies. Other systems require
their own environment resolution and renewed checks.

Open Jupyter with `Start_Jupyter_Notebook.cmd`, or `python -m notebook` from
the activated environment. The launcher binds to 127.0.0.1 and retains default
authentication. It keeps runtime/configuration caches in the project's `tmp/`.
The synthetic [environment notebook](analysis/00_environment_check.ipynb)
completed in a fresh kernel; the [replication notebook](analysis/01_replication.ipynb)
is an unexecuted interface to the saved statistical modules. Real research
execution evidence is in [records/run_logs/skill2](records/run_logs/skill2/).

The author analysis script specifies Stata 16 compatibility mode and seven
integration points. No Stata program was executed. Python implements the original
statistical likelihood and specified settings with independently checked numerical
calculations. Historical finite adaptive-grid details, original package builds,
and invalid generalized-ordinal diagnostics remain explicitly limited. Read the
execution specification before making an exact software-equivalence claim.

The [early Python route assessment](docs/guides/python_route_assessment.md) and
[original setup record](records/run_logs/python_environment_setup.md) are retained
as dated historical context. The [2026-10-19 checks](records/reorganization/2026-10-19/README.md)
cover relocation and portable execution, not another full research-model refit.
''')
    for relative, addition in {
      'sources/README.md': '''
## Restore exact-version inputs on another computer

[input_restore_manifest.json](input_restore_manifest.json) lists the required
original datasets, ZIP members, rating workbooks, codebooks, PDFs and archived
external method sources with SHA-256 values. Run `python tools/restore_inputs.py`
from the repository root for offline checking, or add `--download` to retrieve
registered direct sources. The tool never overwrites an existing file and never
changes the historical source manifest. Assignment/article copies need lawful
manual access; changed upstream versions are reported rather than accepted.
See [the teacher quickstart](../docs/guides/teacher_quickstart.md).

Original inputs and external method source files remain excluded from Git.
Subject-level prepared rating matrices, matching-row audits and conditional
influence arrays also remain local; rerun the reliability stage to recreate
them. Aggregate coefficient/benchmark tables, code, test summaries and provenance
are shared. Some historical GLMM documentation paths are under tmp; the
[method source manifest](../outputs/diagnostics/glmm/method_source_manifest.json)
records primary URLs/hashes. These PDFs are provenance, not runtime dependencies
of the saved Python likelihood engine.
''',
      'records/decisions.md': '''
## D012 — 2026-10-19: non-destructive layout and private GitHub synchronization

The user requests easy-to-find, agent-usable packages for tested skills 1 and 2,
a clearer project layout without any file deletion or broken tested programs,
and updating the existing GitHub repository after local completion. Preserve
the assignment's canonical directories and research artifacts; move auxiliary
guides/one-time writers, add reader indexes, archive revised authored originals
and verify hashes. Make RTK optional for portable execution and add exact-version
input restoration. Include own code, aggregate results and records; retain
excluded source/subject-level files locally with access/rebuild instructions.
No final release, submission, collaborator invitation or public visibility.
''',
      'records/agent_records.md': '''
## 2026-10-19 — Reader layout and reusable skill packaging

User request: preserve all existing files and tested behavior; make the two
completed skills and project easy for the instructor to use; synchronize the
private repository after checks. Applied skill-creator packaging principles,
retained canonical skill/scientific artifact paths, and added invocation guides.
Preservation, moves, portable-wrapper checks and upload evidence are recorded in
records/reorganization/2026-10-19. This task does not claim a new substantive fit
or completion of skill 3.
''',
      '.gitignore': '''
# Subject-level derived diagnostics remain local; aggregate checks are shared.
outputs/diagnostics/reliability/*__conditional_influence.npy
outputs/diagnostics/reliability/matching_row_audit.csv
''',
    }.items():
        path = ROOT / relative
        replace_file(relative, path.read_text(encoding='utf-8-sig') + addition)
    print('Updated current scope, environment, provenance and sharing notes; prior versions retained.')


if __name__ == '__main__':
    main()
