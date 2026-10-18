"""Verify or restore registered research inputs without replacing existing files.

Offline checking is the default. --download retrieves only entries with a direct
URL or a registered ZIP member. Manual PDF inputs are reported as missing.
Historical source manifests and execution receipts are never rewritten.
"""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


def restore(root, entries, download=False):
    root = root.resolve()
    cache, results = {}, []
    for item in entries:
        path = (root / item['path']).resolve()
        if not path.is_relative_to(root):
            raise ValueError(f'Input path escapes project: {item["path"]}')
        status, error = 'missing_manual' if not item.get('url') else 'missing_downloadable', None
        if path.exists():
            status = 'verified' if path.is_file() and sha256(path.read_bytes()).hexdigest() == item['sha256'] else 'hash_mismatch'
        elif download and item.get('url'):
            try:
                url = item['url']
                if url not in cache:
                    with urlopen(Request(url, headers={'User-Agent': 'COMD7290-replication-input-restorer/1.0'}), timeout=45) as response:
                        cache[url] = response.read()
                raw = cache[url]
                if item.get('archive_member'):
                    with ZipFile(BytesIO(raw)) as archive:
                        matches = [name for name in archive.namelist() if Path(name).name == item['archive_member']]
                        if len(matches) != 1:
                            raise ValueError('Archive member missing or ambiguous')
                        raw = archive.read(matches[0])
                if sha256(raw).hexdigest() != item['sha256']:
                    raise ValueError('Retrieved version differs from registered SHA-256; no file written')
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open('xb') as stream:
                    stream.write(raw)
                status = 'restored_verified'
            except Exception as exc:
                status, error = 'download_failed', f'{type(exc).__name__}: {exc}'
        results.append({'path': item['path'], 'role': item['role'], 'status': status, 'error': error})
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--download', action='store_true')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'sources/input_restore_manifest.json').read_text(encoding='utf-8'))
    results = restore(ROOT, manifest['files'], args.download)
    counts = {key: sum(row['status'] == key for row in results) for key in sorted({r['status'] for r in results})}
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'download_requested': args.download,
              'counts': counts, 'files': results, 'existing_files_overwritten': False}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(counts))
    for row in results:
        if row['status'] not in {'verified', 'restored_verified'}:
            print(f'{row["status"]}: {row["path"]}')
    return 0 if all(r['status'] in {'verified', 'restored_verified'} for r in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
