"""Prepare reviewed Git-index content for connector transport when Git networking fails.

No network mutations occur here. Payload chunks stay in tmp, not the repository.
The index must already contain the intended sharing set. No Git filters are
bypassed: blobs are read from the index so normalized content and hashes agree.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]


def git(*args, input=None):
    return subprocess.run(['git',*args], input=input, cwd=ROOT, capture_output=True, check=True).stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--folder', default='tmp/github_upload')
    parser.add_argument('--read', type=int)
    parser.add_argument('--blob')
    parser.add_argument('--offset', type=int, default=0)
    parser.add_argument('--length', type=int, default=45000)
    args = parser.parse_args()
    folder = (ROOT/args.folder).resolve()
    if not folder.is_relative_to(ROOT/'tmp'):
        raise ValueError('Transport payloads must remain inside project tmp')
    if args.read is not None:
        print((folder/f'chunk_{args.read:03d}.json').read_text(encoding='utf-8'))
        return
    if args.blob:
        content = (folder/f'blob_{args.blob}.txt').read_text(encoding='utf-8')
        print(json.dumps({'slice':content[args.offset:args.offset+args.length], 'total_characters':len(content)},ensure_ascii=True))
        return
    folder.mkdir(parents=True, exist_ok=True)
    records = git('ls-files','--stage','-z').decode('utf-8').split('\0')
    entries, manifest, large, forbidden, token_hits, nonenglish = [], [], [], [], [], []
    for record in records:
        if not record:
            continue
        metadata, path = record.split('\t',1)
        mode, oid, stage = metadata.split()
        if stage != '0':
            raise ValueError('Unmerged index')
        raw = git('cat-file','blob',oid)
        if path.startswith(('.venv/','tmp/')) or path.endswith(('.dta','.xlsx','.pdf','.npy')) or (
            path.startswith(('data/original/','data/prepared/','sources/local/','sources/author_code/')) and not path.endswith('/README.md')):
            forbidden.append(path)
        content = raw.decode('utf-8')
        if re.search(r'(?:ghp_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{30,}|[?&]token=[A-Za-z0-9]{24,})', content):
            token_hits.append(path)
        if re.search('[\u4e00-\u9fff]',content):
            nonenglish.append(path)
        manifest.append({'path':path,'git_blob_sha':oid,'sha256':sha256(raw).hexdigest(),'bytes':len(raw)})
        if len(content)>45000:
            (folder/f'blob_{oid}.txt').write_text(content,encoding='utf-8')
            large.append({'path':path,'sha':oid,'mode':mode,'type':'blob','characters':len(content)})
            entries.append({'path':path,'mode':mode,'type':'blob','sha':oid})
        else:
            entries.append({'path':path,'mode':mode,'type':'blob','content':content})
    assert not forbidden, forbidden
    assert not token_hits, token_hits
    # Index removals are moves whose content remains present in the reviewed tree.
    removals = git('diff','--cached','--no-renames','--diff-filter=D','--name-only','-z').decode('utf-8').split('\0')
    entries += [{'path':p,'mode':'100644','type':'blob','sha':None} for p in removals if p]
    chunks, chunk, size = [], [], 0
    for entry in entries:
        length = len(json.dumps(entry,ensure_ascii=True))
        if chunk and size+length>60000:
            chunks.append(chunk);chunk=[];size=0
        chunk.append(entry);size+=length
    if chunk:
        chunks.append(chunk)
    for i, chunk in enumerate(chunks):
        (folder/f'chunk_{i:03d}.json').write_text(json.dumps(chunk,ensure_ascii=True),encoding='utf-8')
    result={'file_count':len(manifest),'total_bytes':sum(i['bytes'] for i in manifest),
            'index_tree_sha':git('write-tree').decode().strip(),'parent_sha':git('rev-parse','HEAD').decode().strip(),
            'chunks':len(chunks),'large_blobs':large,'removals':[p for p in removals if p],
            'forbidden_files':forbidden,'token_pattern_hits':token_hits,'files_containing_cjk':nonenglish,
            'files':manifest}
    (folder/'manifest.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='files'},indent=2))


if __name__=='__main__':
    main()
