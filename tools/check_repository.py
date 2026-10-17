"""Check repository materials only; never fit statistical models or access the network."""
from pathlib import Path
import csv
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
warnings = []
for directory in ('.agents/skills', 'sources', 'docs', 'data/original', 'data/prepared', 'analysis', 'tests', 'outputs/published', 'outputs/reproduced', 'outputs/diagnostics', 'records/run_logs', 'report'):
    if not (ROOT / directory).is_dir():
        errors.append(f'Missing directory: {directory}')
for path, required in {
    'docs/hypothesis_matrix.csv': {'analysis_id','estimand_parameter_contrast','equation_syntax','approval_status'},
    'docs/analysis_inventory.csv': {'analysis_id','source_locator','status'},
    'docs/variable_dictionary.csv': {'measurement_type','missing_rule','verification_status'},
    'outputs/comparison.csv': {'published_value','reproduced_value','difference','tolerance','status'},
    'records/source_manifest.csv': {'url','sha256','redistribution','local_path'},
}.items():
    try:
        with (ROOT / path).open(encoding='utf-8-sig', newline='') as stream:
            reader = csv.DictReader(stream)
            if not required.issubset(reader.fieldnames or []):
                errors.append(f'Missing required CSV columns: {path}')
            list(reader)
    except (OSError, csv.Error) as exc:
        errors.append(f'{path}: {exc}')
manifest = ROOT / 'records/source_manifest.csv'
if manifest.exists():
    with manifest.open(encoding='utf-8-sig', newline='') as stream:
        for row in csv.DictReader(stream):
            if row['local_path'] and row['sha256']:
                path = ROOT / row['local_path']
                if path.is_file():
                    if hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256']:
                        errors.append(f'Checksum mismatch: {row["local_path"]}')
                elif row['redistribution'].startswith('not confirmed'):
                    warnings.append(f'Local-only source absent; follow access instructions: {row["local_path"]}')
                else:
                    errors.append(f'Registered source absent: {row["local_path"]}')
with (ROOT/'outputs/comparison.csv').open(encoding='utf-8-sig', newline='') as stream:
    for row in csv.DictReader(stream):
        if row['status']=='not_run' and row['reproduced_value']:
            errors.append('Unexecuted result must not contain a reproduced value')
for value in warnings:
    print('NOTE:',value)
for value in errors:
    print('ERROR:',value)
print(f'Material checks: {"FAILED" if errors else "PASSED"}; statistical analyses not executed by this tool.')
sys.exit(1 if errors else 0)
