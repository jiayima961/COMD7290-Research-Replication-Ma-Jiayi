"""Download fixed author-provided materials; do not execute the downloaded code."""
from pathlib import Path
import csv
from datetime import datetime, timezone, timedelta
import hashlib
import sys
from urllib.parse import quote
from urllib.request import urlopen, Request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://medcon-doc.github.io/documentation/files/'
SOURCES = [
    ('codebook_01', '01_Content Analysis_Codebook – News Item Level.pdf', 'sources/local/codebook_01_news_item.pdf'),
    ('codebook_02', '02_Content Analysis_Codebook – Actor Identification.pdf', 'sources/local/codebook_02_actor_identification.pdf'),
    ('codebook_05', '05_Content Analysis_Codebook – Actor Level.pdf', 'sources/local/codebook_05_actor.pdf'),
    ('codebook_08', '08_Content Analysis_Codebook – Actor Reference Level.pdf', 'sources/local/codebook_08_actor_reference.pdf'),
    ('repro_package', 'Appendix - Content Analysis Repro Materials - STATA.zip', 'data/original/author_stata_reproduction.zip'),
    ('ratings_tone', 'Appendix - Repro Materials Reliability Content Analysis - Tone.xlsx', 'data/original/independent_ratings_tone.xlsx'),
    ('ratings_actref', 'Appendix - Repro Materials Reliability Content Analysis - Actor-reference.xlsx', 'data/original/independent_ratings_actor_reference.xlsx'),
    ('reliability_script', 'Appendix - Repro Materials Reliability Content Analysis Tone & Actor Reference Vars- STATA.do', 'sources/author_code/reliability_original.do'),
]

def main():
    manifest = ROOT / 'records/source_manifest.csv'
    with manifest.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames
        rows = list(reader)
    failed = False
    for source_id, filename, local_path in SOURCES:
        target = ROOT / local_path
        url = BASE + quote(filename)
        row = next((r for r in rows if r['source_id'] == source_id), None)
        if row is None:
            row = dict.fromkeys(fields, '')
            row['source_id'] = source_id
            rows.append(row)
        row.update(title=filename, url=url, local_path=local_path, redistribution='not confirmed;not tracked', source_locator='complete downloaded file')
        try:
            if target.exists():
                raw = target.read_bytes()
            else:
                with urlopen(Request(url, headers={'User-Agent':'COMD7290-source-inventory/1.0'}), timeout=25) as response:
                    raw = response.read()
                if filename.endswith('.pdf') and not raw.startswith(b'%PDF'):
                    raise ValueError('Expected PDF response')
                if filename.endswith(('.zip', '.xlsx')) and not raw.startswith(b'PK'):
                    raise ValueError('Expected ZIP/XLSX response')
                if filename.endswith('.do') and (b'<html' in raw[:200].lower() or not raw):
                    raise ValueError('Expected Stata text response')
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(raw)
            row.update(sha256=hashlib.sha256(raw).hexdigest(), retrieved_date=datetime.now(timezone(timedelta(hours=8))).date().isoformat(), version='as served;inspect file metadata/code header', status='available_local')
            print(f'AVAILABLE {source_id}: {len(raw)} bytes')
        except Exception as exc:
            row.update(status='download_failed', version=type(exc).__name__ + ': ' + str(exc))
            print(f'FAILED {source_id}: {exc}')
            failed = True
            # Avoid repeating the same blocked network operation for every file.
            break
    archive = ROOT / 'data/original/author_stata_reproduction.zip'
    if archive.exists():
        with zipfile.ZipFile(archive) as zipped:
            expected = {'MedCon_Civility_item.dta', 'MedCon_Civility_actref.dta', 'MedCon_Civility_an.do', 'readme.rtf'}
            members = {Path(info.filename).name: info for info in zipped.infolist() if not info.is_dir()}
            for name in sorted(expected):
                if name not in members:
                    print(f'NOT FOUND IN PACKAGE: {name}')
                    failed = True
                    continue
                folder = 'sources/author_code' if name.endswith(('.do', '.rtf')) else 'data/original'
                relative = folder + '/' + name
                output = ROOT / relative
                raw = zipped.read(members[name])
                if output.exists() and output.read_bytes() != raw:
                    raise RuntimeError(f'Existing original changed: {relative}')
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(raw)
                entry = dict.fromkeys(fields, '')
                entry.update(source_id='package_member_' + name, title=name, url=BASE+quote('Appendix - Content Analysis Repro Materials - STATA.zip'), local_path=relative, retrieved_date=datetime.now(timezone(timedelta(hours=8))).date().isoformat(), version='unmodified archive member', sha256=hashlib.sha256(raw).hexdigest(), status='available_local', redistribution='not confirmed;not tracked', source_locator=members[name].filename)
                rows = [r for r in rows if r['source_id'] != entry['source_id']]
                rows.append(entry)
                print(f'EXTRACTED {name}')
    with manifest.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return 1 if failed else 0

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
