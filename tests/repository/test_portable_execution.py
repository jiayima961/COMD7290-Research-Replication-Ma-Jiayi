"""Exercise portable process transport and input restoration without refitting models."""
from datetime import datetime, timezone
from contextlib import nullcontext
from hashlib import sha256
import importlib.util
from io import BytesIO
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch
from zipfile import ZipFile
import nbformat

ROOT = Path(__file__).resolve().parents[2]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    checks = []
    (ROOT/'tmp').mkdir(exist_ok=True)
    with nullcontext(tempfile.mkdtemp(prefix='comd7290-portability-', dir=ROOT/'tmp')) as directory:
        temporary = Path(directory)
        environment = dict(os.environ, PATH='', PYTHONUTF8='1')
        # Empty PATH models a reader without RTK. Python is addressed absolutely.
        for code, expected in [('print("portable-success")', 0), ('import sys; print("expected-negative",file=sys.stderr); sys.exit(7)', 7)]:
            log = temporary / f'without_rtk_{expected}'
            result = subprocess.run([sys.executable, str(ROOT/'tools/run_logged.py'), '--log', str(log),
                                     '--', sys.executable, '-c', code], env=environment,
                                    capture_output=True, text=True, encoding='utf-8')
            if not log.with_suffix('.json').exists():
                raise AssertionError(f'Command did not create a receipt: {result.stdout}\n{result.stderr}')
            receipt = json.loads(log.with_suffix('.json').read_text(encoding='utf-8'))
            assert result.returncode == receipt['exit_code'] == expected
            assert receipt['command'][0] == sys.executable
            assert receipt['status'] == ('completed' if expected == 0 else 'failed')
            if expected:
                assert 'expected-negative' in log.with_suffix('.stderr.txt').read_text(encoding='utf-8')
            checks.append({'check': f'actual command without RTK, exit {expected}', 'passed': True})
        runner = load('portable_runner', 'analysis/run_replication.py')
        with patch.object(sys, 'argv', ['run_replication.py']), patch.object(runner.subprocess, 'run') as run:
            runner.main()
        assert len(run.call_args_list) >= 10
        assert all(call.args[0][0] == sys.executable and call.kwargs['cwd'] == ROOT for call in run.call_args_list)
        assert all('rtk' not in call.args[0] for call in run.call_args_list)
        checks.append({'check': 'all stage commands use the same interpreter and repository cwd',
                       'commands_inspected': len(run.call_args_list), 'passed': True})
        restorer = load('portable_restore', 'tools/restore_inputs.py')
        good = b'independent input fixture\n'
        entry = {'path': 'data/original/input.txt', 'sha256': sha256(good).hexdigest(),
                 'role': 'synthetic_fixture', 'url': 'https://example.invalid/source.zip', 'archive_member': 'input.txt'}
        archive = BytesIO()
        with ZipFile(archive, 'w') as stream:
            stream.writestr('package/input.txt', good)
        with patch.object(restorer, 'urlopen', return_value=BytesIO(archive.getvalue())):
            assert restorer.restore(temporary, [entry], True)[0]['status'] == 'restored_verified'
        assert restorer.restore(temporary, [entry])[0]['status'] == 'verified'
        target = temporary / entry['path']
        target.write_bytes(b'existing different version')
        with patch.object(restorer, 'urlopen') as network:
            assert restorer.restore(temporary, [entry], True)[0]['status'] == 'hash_mismatch'
            assert not network.called
        assert target.read_bytes() == b'existing different version'
        checks.append({'check': 'ZIP restoration, exact hash, and existing-file mismatch refusal', 'passed': True})
        bad = dict(entry, path='bad_version.txt', sha256='0'*64, archive_member=None)
        with patch.object(restorer, 'urlopen', return_value=BytesIO(good)):
            assert restorer.restore(temporary, [bad], True)[0]['status'] == 'download_failed'
        assert not (temporary / bad['path']).exists()
        checks.append({'check': 'changed upstream content is rejected before writing', 'passed': True})
        try:
            restorer.restore(temporary, [dict(entry, path='../outside.txt')])
        except ValueError:
            pass
        else:
            raise AssertionError('Escaping path was accepted')
        checks.append({'check': 'input destination cannot escape selected project', 'passed': True})
    notebook = nbformat.read(ROOT/'analysis/01_replication.ipynb', as_version=4)
    nbformat.validate(notebook)
    for cell in notebook.cells:
        if cell.cell_type == 'code':
            compile(cell.source, '<notebook-cell>', 'exec')
    assert '"rtk"' not in '\n'.join(c.source for c in notebook.cells)
    checks.append({'check': 'notebook schema and code syntax; portable runner invocation', 'passed': True})
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'status': 'passed',
              'checks': checks, 'research_models_refitted': False,
              'network_used': False, 'historical_outputs_overwritten': False}
    path = ROOT/'records/reorganization/2026-10-19/portable_execution.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(f'Portable execution: {len(checks)} checks passed. No research fit or real download performed.')


if __name__ == '__main__':
    main()
