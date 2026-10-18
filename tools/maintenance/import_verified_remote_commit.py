"""Import a connector-created Git commit locally after exact tree verification.

Use the GitHub GET git/commits response saved as JSON, not a summary. No files
or index entries are reset. Hash/tree/parent checks must all match before refs
advance. This is an alternative transport for the authorized repository sync.
"""
import argparse
from datetime import datetime
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]


def git(*args, input=None):
    return subprocess.run(['git',*args], input=input, cwd=ROOT, capture_output=True, check=True).stdout


def identity(person):
    time = datetime.fromisoformat(person['date'].replace('Z','+00:00'))
    return f'{person["name"]} <{person["email"]}> {int(time.timestamp())} {time.strftime("%z")}'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('json_file',type=Path)
    args = parser.parse_args()
    commit = json.loads(args.json_file.read_text(encoding='utf-8'))
    if commit['tree']['sha'] != git('write-tree').decode().strip():
        raise ValueError('Remote tree differs from the reviewed local index')
    old = git('rev-parse','HEAD').decode().strip()
    if [p['sha'] for p in commit['parents']] != [old]:
        raise ValueError('Remote parent differs from current local HEAD; no refs changed')
    rows = [f'tree {commit["tree"]["sha"]}',f'parent {old}',
            'author '+identity(commit['author']),'committer '+identity(commit['committer'])]
    signature = commit.get('verification',{}).get('signature')
    if signature:
        rows.append('gpgsig '+signature.rstrip('\n').replace('\n','\n '))
    raw = ('\n'.join(rows)+'\n\n'+commit['message']).encode('utf-8')
    # GitHub commit messages normally have a final newline in the object.
    candidates = [raw] if raw.endswith(b'\n') else [raw+b'\n',raw]
    for candidate in candidates:
        actual = git('hash-object','-t','commit','--stdin',input=candidate).decode().strip()
        if actual == commit['sha']:
            git('hash-object','-w','-t','commit','--stdin',input=candidate)
            break
    else:
        raise ValueError('Could not reconstruct exact Git object; refs left unchanged')
    branch = git('symbolic-ref','HEAD').decode().strip()
    git('update-ref',branch,commit['sha'],old)
    git('update-ref','refs/remotes/origin/main',commit['sha'])
    print(f'Imported verified remote commit {commit["sha"]}; working files/index unchanged.')


if __name__ == '__main__':
    main()
