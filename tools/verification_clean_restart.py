"""Create an isolated source/input-only copy and actually refit the full pipeline.

Never reads saved estimates into the clean copy. Reuses the installed environment,
not notebook state. The canonical results are read only and remain unchanged.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import argparse,csv
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'tmp/skill3_clean_restart'
LOG = ROOT / 'records/run_logs/skill3/clean_restart'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    global DEST
    parser=argparse.ArgumentParser();parser.add_argument('--destination',type=Path,default=DEST);parser.add_argument('--entry',default='analysis/run_replication.py')
    args=parser.parse_args();DEST=args.destination.resolve()
    if not DEST.is_relative_to((ROOT/'tmp').resolve()):
        raise SystemExit('Clean destination must be within project tmp.')
    if args.entry!='analysis/run_replication.py':
        global LOG
        LOG=ROOT/'records/run_logs/skill3/verified_clean_restart'
    if DEST.exists():
        raise SystemExit('Clean-copy directory already exists; preserve it and select a new destination.')
    LOG.mkdir(parents=True, exist_ok=True)
    copied = []
    def copy(rel):
        src, dst = ROOT / rel, DEST / rel
        if not src.is_file() or '__pycache__' in src.parts:
            return
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied.append({'path':str(rel).replace('\\','/'),'sha256':digest(src)})
    for directory in ['analysis', 'tests', 'tools', '.agents/skills']:
        for src in (ROOT/directory).rglob('*'):
            copy(src.relative_to(ROOT))
    for rel in ['records/source_manifest.csv','outputs/published/model_targets.csv',
                'sources/input_restore_manifest.json','requirements-lock.txt','environment.md']:
        copy(Path(rel))
    for entry in json.loads((ROOT/'sources/input_restore_manifest.json').read_text())['files']:
        assert digest(ROOT/entry['path']) == entry['sha256'], entry['path']
        copy(Path(entry['path']))
    for entry in csv.DictReader((ROOT/'records/source_manifest.csv').open(encoding='utf-8-sig')):
        if entry.get('local_path'):copy(Path(entry['local_path']))
    for rel in ['outputs/diagnostics','outputs/reproduced','records/run_logs/skill2']:
        (DEST/rel).mkdir(parents=True, exist_ok=True)
    assert not list((DEST/'outputs/reproduced').rglob('*'))
    manifest = {'started_utc':datetime.now(timezone.utc).isoformat(),
        'isolated_root':str(DEST),'environment_reused':sys.executable,
        'scope':'Fresh process and source/input-only tree; no saved fits or notebook state. Not a fresh dependency installation.',
        'copied_files':copied,'command':[sys.executable,'-X','utf8',args.entry]}
    (LOG/'receipt.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    with (LOG/'stdout.log').open('w',encoding='utf-8') as out:
        proc=subprocess.run(manifest['command'],cwd=DEST,stdout=out,stderr=subprocess.STDOUT)
    manifest.update(finished_utc=datetime.now(timezone.utc).isoformat(),returncode=proc.returncode)
    if proc.returncode == 0:
        # Exact numerical payload comparison, ignoring provenance paths/times.
        import numpy as np
        import pandas as pd
        checks=[]
        for rel in ['outputs/reproduced/models/ordinal/ordinal_coefficients.csv',
                    'outputs/reproduced/models/M2_coefficients.csv','outputs/reproduced/models/M3_coefficients.csv',
                    'outputs/reproduced/predictions/binary_margins_ames.csv',
                    'outputs/reproduced/reliability/reliability_coefficients.csv']:
            if not (DEST/rel).is_file():
                checks.append({'path':rel,'error':'Expected file not found'});continue
            old,new=pd.read_csv(ROOT/rel),pd.read_csv(DEST/rel)
            cols=list(old.select_dtypes(include='number').columns)
            same=old.shape==new.shape and list(old.columns)==list(new.columns)
            exact=same and np.allclose(old[cols],new[cols],atol=0,rtol=0,equal_nan=True)
            close=same and np.allclose(old[cols],new[cols],atol=1e-8,rtol=1e-8,equal_nan=True)
            checks.append({'path':rel,'same_shape_schema':same,'numeric_exact':bool(exact),'numeric_within_1e_8':bool(close)})
        manifest['numeric_comparisons']=checks
    (LOG/'receipt.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in manifest.items() if k not in ['copied_files']},indent=2))
    raise SystemExit(proc.returncode)

if __name__=='__main__':
    main()
