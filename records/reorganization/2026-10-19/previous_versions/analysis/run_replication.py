"""Single Python-only rerun entry point. Logs each actual command; stops on failure."""
from datetime import datetime,timezone
from pathlib import Path
import argparse
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser();p.add_argument('--stage',choices=['all','data','reliability','ordinal','binary','summaries','checks'],default='all')
    a=p.parse_args()
    stages={
      'data':[['analysis/prepare_replication.py']],
      'reliability':[['analysis/reliability_reproduction.py','--project-root','.']],
      'ordinal':[['analysis/ordinal_reproduction.py','--project-root','.','--output-root','outputs/reproduced','--canonical-layout']],
      'binary':[['analysis/run_binary_models.py']],
      'summaries':[['analysis/binary_predictions.py'],['analysis/compare_replication.py']],
      'checks':[['tests/skill2/data_checks.py'],['tests/skill2/glmm_reference.py'],['tests/skill2/check_nested_logit.py']],
    }
    for mid in ['M2','M2_null','M3','M3_null']:
        fit=f'outputs/reproduced/models/{mid}_fit.json'
        stages['checks'].append(['tests/skill2/check_glmm_full_likelihood.py','--fit',fit])
        stages['checks'].append(['tests/skill2/check_glmm_fit_curvature.py','--fit',fit])
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    for stage,commands in stages.items():
        if a.stage not in ['all',stage]:continue
        for i,cmd in enumerate(commands):
            log=f'records/run_logs/skill2/reruns/{stamp}/{stage}_{i+1}'
            command=['rtk','proxy',sys.executable,'-X','utf8','tools/run_logged.py','--log',log,'--',sys.executable,'-X','utf8',*cmd]
            subprocess.run(command,cwd=ROOT,check=True)
    print('Requested stages completed. Review diagnostics; command completion is not exact historical-software equivalence.')
if __name__=='__main__':main()
