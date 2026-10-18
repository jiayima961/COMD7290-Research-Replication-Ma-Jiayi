"""Verify preservation, current navigation, syntax and complete skill resources."""
import ast
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
RECORD = ROOT/'records/reorganization/2026-10-19'


def digest(path):
    return sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def main():
    before = json.loads((RECORD/'before_sha256.json').read_text(encoding='utf-8'))
    moves = json.loads((RECORD/'moves.json').read_text(encoding='utf-8'))['moves']
    preserved, changed, errors = [], [], []
    for old, expected in before.items():
        new = moves.get(old, old)
        path = ROOT/new
        archive = RECORD/'previous_versions'/old
        if digest(path) == expected:
            preserved.append({'old': old, 'current': new, 'preservation': 'identical'})
        elif path.is_file() and digest(archive) == expected:
            changed.append({'old': old, 'current': new, 'prior_bytes': archive.relative_to(ROOT).as_posix()})
        else:
            errors.append(f'Original is unaccounted for: {old}')
    protected = [p for p in before if
        p.startswith(('data/', 'sources/local/', 'sources/author_code/', 'records/skill_tests/',
                      'records/skill_invocations/', 'records/student_inputs/')) or
        (p.startswith('outputs/') and not p.endswith('README.md') and p != 'outputs/review_report.md') or
        (p.startswith('analysis/') and p not in {'analysis/README.md','analysis/run_replication.py','analysis/01_replication.ipynb'}) or
        p.startswith('.agents/skills/')]
    for relative in protected:
        if digest(ROOT/relative) != before[relative]:
            errors.append(f'Protected scientific/historical artifact changed: {relative}')
    required = [
        '.agents/skills/specify-empirical-study/SKILL.md',
        '.agents/skills/specify-empirical-study/references/output_contract.md',
        '.agents/skills/specify-empirical-study/scripts/validate_specification.py',
        '.agents/skills/reproduce-and-diagnose/SKILL.md',
        '.agents/skills/reproduce-and-diagnose/references/execution_contract.md',
        'analysis/run_replication.py', 'tests/skill1_specification/test_validator_cases.py',
        'tests/skill2/check_nested_logit.py', 'tools/restore_inputs.py',
        'docs/skills/README.md', 'sources/input_restore_manifest.json',
        'records/skill_tests/specify-empirical-study/TEST_REPORT.md',
        'records/skill_tests/reproduce-and-diagnose/TEST_REPORT.md',
    ]
    errors += [f'Missing required package resource: {p}' for p in required if not (ROOT/p).is_file()]
    pages = ['README.md','START_HERE.md','STATUS.md','environment.md','docs/README.md',
             'docs/skills/README.md','docs/guides/teacher_quickstart.md','analysis/README.md',
             'tests/README.md','outputs/README.md','outputs/reproduced/README.md',
             'outputs/diagnostics/README.md','records/README.md','sources/README.md',
             'tools/README.md','tools/maintenance/README.md','.agents/skills/README.md']
    links = []
    for relative in pages:
        page = ROOT/relative
        for target in re.findall(r'\]\(([^)]+)\)', page.read_text(encoding='utf-8')):
            if '://' in target or target.startswith(('#','mailto:')):
                continue
            destination = unquote(target.split('#')[0].strip('<>'))
            path = (page.parent/destination).resolve()
            links.append({'page': relative, 'target': target, 'exists': path.exists()})
            if not path.exists():
                errors.append(f'Broken reader link: {relative} -> {target}')
    syntax = []
    for folder in ['analysis','tests','tools','.agents/skills']:
        for path in (ROOT/folder).rglob('*.py'):
            try:
                ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
                syntax.append(path.relative_to(ROOT).as_posix())
            except SyntaxError as exc:
                errors.append(str(exc))
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'status': 'passed' if not errors else 'failed', 'deleted_files': [],
              'original_files_accounted_for': len(preserved)+len(changed),
              'unchanged_or_exactly_moved': len(preserved), 'revised_with_prior_bytes_retained': changed,
              'protected_scientific_historical_artifacts_unchanged': len(protected),
              'required_package_resources': required, 'current_reader_links': links,
              'python_files_syntax_checked': syntax, 'errors': errors,
              'full_research_rerun_performed': False}
    (RECORD/'verification.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k in {'status','original_files_accounted_for',
        'unchanged_or_exactly_moved','protected_scientific_historical_artifacts_unchanged','errors'}}, indent=2))
    print(f'Checked {len(links)} current navigation links and {len(syntax)} Python files.')
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
