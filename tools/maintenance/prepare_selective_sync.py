"""Inspect the sharing set and prepare normalized Git blobs for connector upload.

No network writes occur here. Individual-report materials are always excluded.
Use --stage-list before git add, then --payload to read reviewed index blobs.
"""
from pathlib import Path
from hashlib import sha256
import argparse, base64, json, re, subprocess
ROOT=Path(__file__).resolve().parents[2]
TMP=ROOT/'tmp/github_skill3_sync'

def git(*args):
    return subprocess.run(['git',*args],cwd=ROOT,capture_output=True,check=True).stdout

def forbidden(path):
    return ('final_report' in path.lower() or path.startswith(('report/local_review/','.venv/','tmp/'))
     or Path(path).suffix.lower() in {'.dta','.xlsx','.pdf','.npy','.pem','.key'}
     or any(path.startswith(s) and not path.endswith('/README.md') for s in
            ['data/original/','data/prepared/','sources/local/','sources/author_code/']))

def check(path,raw):
    assert not forbidden(path),path
    if path.endswith('.docx'):
        assert path in ['report/verification/01_results_comparison.docx','report/verification/02_python_stata_equivalence.docx'],path
        return
    text=raw.decode('utf-8')
    assert not re.search(r'(?:ghp_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{30,}|[?&]token=[A-Za-z0-9]{24,})',text),path
    # Do not publish report paragraphs through a helper or archive either.
    assert ('Civility is a central concern ' 'in democratic public discourse') not in text,path
    assert ('The broad agreement supports reproducibility ' 'of the main findings under') not in text,path

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--stage-list',action='store_true');ap.add_argument('--payload',action='store_true')
    ap.add_argument('--read-chunk',type=int);ap.add_argument('--read-blob')
    ap.add_argument('--offset',type=int,default=0);ap.add_argument('--length',type=int,default=100000)
    ap.add_argument('--read-manifest',action='store_true');args=ap.parse_args()
    TMP.mkdir(parents=True,exist_ok=True)
    if args.read_manifest:
        print((TMP/'manifest.json').read_text(encoding='utf-8'));return
    if args.read_chunk is not None:
        print((TMP/f'chunk_{args.read_chunk:03d}.json').read_text(encoding='utf-8'));return
    if args.read_blob:
        v=json.loads((TMP/f'blob_{args.read_blob}.json').read_text(encoding='utf-8'))
        if not v['path'].endswith('.docx'):
            v['content']=base64.b64decode(v['content']).decode('utf-8');v['encoding']='utf-8'
        v['total_characters']=len(v['content']);v['content']=v['content'][args.offset:args.offset+args.length]
        print(json.dumps(v,ensure_ascii=True));return
    if args.stage_list:
        modified=git('ls-files','-m','-z').decode().split('\0')
        others=git('ls-files','--others','--exclude-standard','-z').decode().split('\0')
        paths=sorted(set(p for p in modified+others if p and not forbidden(p)))
        for path in paths:check(path,(ROOT/path).read_bytes())
        (TMP/'stage_paths.nul').write_bytes(b'\0'.join(p.encode() for p in paths)+b'\0')
        (TMP/'stage_paths.json').write_text(json.dumps(paths,indent=2),encoding='utf-8')
        print(json.dumps({'selected_files':len(paths),'final_report_files_selected':0,'bytes':sum((ROOT/p).stat().st_size for p in paths)},indent=2));return
    if args.payload:
        changed=git('diff','--cached','--name-only','--diff-filter=ACM','-z').decode().split('\0')
        entries=[];blobs=[];manifest=[]
        for path in changed:
            if not path:continue
            raw=git('show',':'+path);check(path,raw)
            mode,oid,stage=git('ls-files','--stage','--',path).decode().split('\t',1)[0].split()
            manifest.append({'path':path,'git_blob_sha':oid,'sha256':sha256(raw).hexdigest(),'bytes':len(raw)})
            if path.endswith('.docx') or len(raw)>90000:
                payload={'sha':oid,'content':base64.b64encode(raw).decode(),'encoding':'base64','path':path}
                (TMP/f'blob_{oid}.json').write_text(json.dumps(payload),encoding='utf-8')
                blobs.append({'sha':oid,'path':path,'bytes':len(raw)})
                entries.append({'path':path,'mode':mode,'type':'blob','sha':oid})
            else:entries.append({'path':path,'mode':mode,'type':'blob','content':raw.decode('utf-8')})
        removed=[p for p in git('diff','--cached','--diff-filter=D','--name-only','-z').decode().split('\0') if p]
        assert not removed,removed
        chunks=[];chunk=[];size=0
        for entry in entries:
            length=len(json.dumps(entry,ensure_ascii=True))
            if chunk and size+length>95000:chunks.append(chunk);chunk=[];size=0
            chunk.append(entry);size+=length
        if chunk:chunks.append(chunk)
        for i,chunk in enumerate(chunks):(TMP/f'chunk_{i:03d}.json').write_text(json.dumps(chunk,ensure_ascii=True),encoding='utf-8')
        all_files=[]
        for record in git('ls-files','--stage','-z').decode().split('\0'):
            if not record:continue
            meta,path=record.split('\t',1);mode,oid,stage=meta.split();assert stage=='0'
            assert not forbidden(path),path
            all_files.append({'path':path,'sha':oid})
        result={'parent_sha':git('rev-parse','HEAD').decode().strip(),'index_tree_sha':git('write-tree').decode().strip(),
         'changed_files':len(manifest),'file_count':len(all_files),'chunks':len(chunks),'blobs':blobs,
         'changed_manifest':manifest,'files':all_files,'final_report_excluded':True}
        (TMP/'manifest.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k not in ['files','changed_manifest']},indent=2))

if __name__=='__main__':main()
