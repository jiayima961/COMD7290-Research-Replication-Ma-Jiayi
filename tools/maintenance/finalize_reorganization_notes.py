"""Finalize layout-validation notes while retaining prior narrative versions."""
from pathlib import Path
import shutil
ROOT = Path(__file__).resolve().parents[2]
RECORD = ROOT/'records/reorganization/2026-10-19'


def main():
    path = ROOT/'outputs/review_report.md'
    backup = RECORD/'previous_versions/outputs/review_report.md'
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)
    path.write_text('''# Consolidated verification report — final synthesis pending

Skill-2 independent data counts, harmless copied-input rejection/recovery,
likelihood fixtures, saved-vector gradient and curvature checks have been
executed. See [the results explanation](../docs/replication_results.md),
[diagnostics](diagnostics/README.md) and [actual skill-2 test report](../records/skill_tests/reproduce-and-diagnose/TEST_REPORT.md).

This file is reserved for skill 3's later consolidated review. It is not a new
independent full-model refit or final acceptance. The report must state reviewer
roles, source/specification versions, exact calculations, discrepancies,
unverified scope and the student's decisions. Repeating the same script is not
independent verification. Historical finite-grid/build identity remains limited.

The former initialization placeholder is preserved in the reorganization archive.
''', encoding='utf-8')
    (RECORD/'validation_summary.md').write_text('''# Layout and portability validation

Date: 2026-10-19 (Asia/Shanghai). The task reorganizes and shares existing work;
it does not change the statistical formulas or refit the complete study.

| Check | Actual outcome and evidence |
| --- | --- |
| No lost originals; protected scientific artifacts | [verification.json](verification.json): every inventoried file is identical, moved, or revised with original bytes archived; numerical results/data/skill evidence remain unchanged |
| Current navigation and Python syntax | verification.json lists resolved links and parsed Python files |
| Complete skill resources | Both canonical packages, contracts, validator, project modules and test reports checked; package versions remain 1.0.1 and 1.1.0 |
| Official skill frontmatter validator | `.venv/Scripts/python.exe -X utf8 E:/Codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-directory>` returned `Skill is valid!` for both packages |
| Skill-1 substantive regression | [skill1_regression.json](skill1_regression.json): 12/12 cases passed; historical case inputs unchanged |
| Registered source inputs | [input_verification.json](input_verification.json): 24/24 present with exact expected hashes |
| Independent study counts and harmless rejection/recovery | [data_independent_checks.json](data_independent_checks.json): four checks passed; 196 recognition and 192 outrage events among 3,770 references |
| Ordinary Python, logger failures, source-version refusal | [portable_execution.json](portable_execution.json): seven meaningful checks; no live downloads or research fits |
| Reader copy | [reader_copy.json](reader_copy.json): copied only shareable candidates, checked honest missing-input reporting, restored registered local copies, executed the data stage and independent data checks with RTK absent from child PATH |
| Repository material schemas/checks | `python tools/check_repository.py` passed locally and in the isolated shareable copy |
| Git whitespace | `git diff --check` passed before synchronization |

The first portable-test attempt used the sandbox's system temporary folder and
could not read its child receipt/clean up that restricted folder. The test was
changed to use a new isolated directory under the project's tmp; it passed.
An initial official-validator attempt used the bundled base interpreter, which
lacked PyYAML. Running with the already-installed project environment passed;
no new dependency installation was needed.

Ordinary Git network transport failed (local DNS/thread and then connection
reset). The working GitHub connector is used for the authorized private-repository
update. Remote files and branch identity will be verified after upload. No
visibility change, invitation, release or final submission is authorized here.

The reader-copy check reuses the existing Python environment and lawful local
input copies. It is not a fresh dependency installation, a live-download test,
a new agent's substantive skill invocation, or a full clean statistical refit.
Original execution/discovery reports remain the evidence of the earlier work.
''', encoding='utf-8')
    print('Consolidation status and actual cleanup checks saved; previous placeholder preserved.')


if __name__ == '__main__':
    main()
