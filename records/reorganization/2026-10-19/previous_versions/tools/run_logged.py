"""Run an explicit local analysis command and retain real stdout/stderr/runtime evidence."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import time

def main():
    p=argparse.ArgumentParser();p.add_argument('--log',type=Path,required=True)
    p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args()
    cmd=a.command[1:] if a.command and a.command[0]=='--' else a.command
    if not cmd: p.error('An explicit command is required after --.')
    a.log.parent.mkdir(parents=True,exist_ok=True)
    started=datetime.now(timezone.utc).isoformat();t=time.perf_counter()
    record={'command':['rtk','proxy']+cmd,'cwd':str(Path.cwd()),'started_at_utc':started,'status':'running'}
    a.log.with_suffix('.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    with a.log.with_suffix('.stdout.txt').open('w',encoding='utf-8') as out, a.log.with_suffix('.stderr.txt').open('w',encoding='utf-8') as err:
        process=subprocess.Popen(['rtk','proxy']+cmd,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',errors='replace',
                                 creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        for line in process.stdout:
            out.write(line);out.flush();print(line,end='',flush=True)
        code=process.wait()
    record.update(finished_at_utc=datetime.now(timezone.utc).isoformat(),runtime_seconds=time.perf_counter()-t,
                  exit_code=code,status='completed' if code==0 else 'failed')
    a.log.with_suffix('.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    if code: print(a.log.with_suffix('.stderr.txt').read_text(encoding='utf-8'),file=sys.stderr)
    return code
if __name__=='__main__':raise SystemExit(main())
