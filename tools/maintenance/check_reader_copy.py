"""Smoke-test a shareable-file copy in isolation, using existing local inputs."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
RECORD = ROOT/'records/reorganization/2026-10-19'


def main():
    listing = subprocess.run(['git','-c','core.quotepath=false','ls-files','--cached','--others','--exclude-standard','-z'],
        cwd=ROOT, capture_output=True, check=True).stdout.decode('utf-8')
    paths = sorted({p for p in listing.split('\0') if p and (ROOT/p).is_file()})
    forbidden = [p for p in paths if p.startswith(('.venv/','tmp/','sources/local/skill2_methods/'))
                 or (p.startswith(('data/original/','data/prepared/','sources/local/','sources/author_code/'))
                     and not p.endswith('/README.md'))
                 or p.endswith('.npy') or p.endswith('matching_row_audit.csv')]
    assert not forbidden, forbidden
    root = Path(tempfile.mkdtemp(prefix='reader-copy-', dir=ROOT/'tmp')).resolve()
    assert root.is_relative_to(ROOT/'tmp')
    for relative in paths:
        source, target = ROOT/relative, root/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    commands = []
    environment = dict(os.environ, PATH='', PYTHONUTF8='1')

    def run(arguments, expected=0):
        command = [sys.executable,'-X','utf8',*arguments]
        result = subprocess.run(command, cwd=root, env=environment, capture_output=True,
                                text=True, encoding='utf-8')
        commands.append({'command': command, 'cwd': str(root), 'exit_code': result.returncode,
                         'stdout': result.stdout, 'stderr': result.stderr})
        assert result.returncode == expected, result.stderr + result.stdout

    # A reader can inspect and check structure without excluded originals.
    run(['tools/check_repository.py'])
    run(['tools/restore_inputs.py'], expected=1)
    # Simulate lawful restoration from this machine's hash-verified registered copies.
    manifest = json.loads((root/'sources/input_restore_manifest.json').read_text(encoding='utf-8'))
    for item in manifest['files']:
        target = root/item['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT/item['path'], target)
    run(['tools/restore_inputs.py'])
    run(['analysis/run_replication.py','--stage','data'])
    run(['tests/skill2/data_checks.py','--project-root','.', '--output','records/reader_data_checks.json'])
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'status':'passed',
              'shareable_files_copied':len(paths), 'isolated_root':str(root),
              'excluded_raw_or_subject_level_candidates':forbidden, 'rtk_on_child_path':False,
              'commands':commands, 'inputs_restored_from_existing_lawful_local_copies':True,
              'fresh_dependency_installation_tested':False, 'full_statistical_refit_performed':False,
              'original_project_results_overwritten':False}
    (RECORD/'reader_copy.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'Reader copy passed: {len(paths)} shareable files; honest absent-input handling; actual data stage and independent data checks without RTK.')


if __name__ == '__main__':
    main()
