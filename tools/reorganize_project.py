"""One-time, non-destructive 2026-10-19 layout migration; retain evidence."""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / 'records/reorganization/2026-10-19'
MOVES = {
    'docs/github_structure_and_workflow.txt': 'docs/guides/github_structure_and_workflow.txt',
    'docs/python_route_assessment.md': 'docs/guides/python_route_assessment.md',
    **{f'tools/{name}.py': f'tools/maintenance/{name}.py' for name in (
        'build_replication_notebook', 'finalize_skill2_documents', 'finish_skill2_record',
        'record_skill2_interruption', 'update_skill2_context')},
}


def inventory():
    result = {}
    for directory, folders, files in os.walk(ROOT):
        folders[:] = [p for p in folders if p not in {'.git', '.venv', '__pycache__', 'tmp'}]
        for name in files:
            path = Path(directory) / name
            if path.is_relative_to(RECORD):
                continue
            result[path.relative_to(ROOT).as_posix()] = sha256(path.read_bytes()).hexdigest()
    return result


def main():
    if (RECORD / 'before_sha256.json').exists():
        raise SystemExit('Migration was already recorded; do not repeat it.')
    RECORD.mkdir(parents=True, exist_ok=True)
    before = inventory()
    (RECORD / 'before_sha256.json').write_text(json.dumps(before, indent=2) + '\n', encoding='utf-8')
    # Preserve prior authored navigation and wrappers before updating them.
    backups = ['README.md', 'START_HERE.md', 'STATUS.md', 'AGENTS.md', 'environment.md',
               'analysis/README.md', 'analysis/run_replication.py', 'analysis/01_replication.ipynb',
               'tools/run_logged.py', 'Start_Jupyter_Notebook.cmd', '.gitignore', *MOVES]
    for relative in backups:
        source = ROOT / relative
        if source.is_file():
            target = RECORD / 'previous_versions' / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    for old, new in MOVES.items():
        source, target = (ROOT / old).resolve(), (ROOT / new).resolve()
        if not source.is_relative_to(ROOT) or not target.is_relative_to(ROOT) or target.exists():
            raise ValueError(f'Unsafe or occupied migration destination: {new}')
        target.parent.mkdir(parents=True, exist_ok=True)
        source.rename(target)
        if new.startswith('tools/maintenance/'):
            text = target.read_text(encoding='utf-8')
            target.write_text(text.replace('resolve().parents[1]', 'resolve().parents[2]'), encoding='utf-8')
    (RECORD / 'moves.json').write_text(json.dumps({
        'created_at_utc': datetime.now(timezone.utc).isoformat(), 'moves': MOVES,
        'excluded_from_inventory': ['.git', '.venv', '__pycache__', 'tmp'],
        'exclusion_reason': 'Runtime/cache directories left in place and not edited by this migration.',
        'deleted_files': [],
    }, indent=2) + '\n', encoding='utf-8')
    print(f'Inventoried {len(before)} files; preserved prior versions; moved {len(MOVES)} files; deleted none.')


if __name__ == '__main__':
    main()
