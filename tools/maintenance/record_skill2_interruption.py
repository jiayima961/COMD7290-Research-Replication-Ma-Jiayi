"""Annotate interrupted attempts without deleting original command/output evidence."""
from pathlib import Path
from datetime import datetime,timezone
import json
root=Path(__file__).resolve().parents[2]
folder=root/'records/run_logs/skill2'
for name in ['M3_engine_candidate','M2_engine_damped','M3_engine_damped','M3_null','M2_null_trial_rejection']:
    p=folder/(name+'.json')
    if not p.exists():continue
    data=json.loads(p.read_text())
    if data.get('status')=='running':
        data['previous_status']='running'
        data['status']='interrupted_not_accepted'
        data['interruption_note']=('Prior session/usage interruption; no completed fit artifact accepted.' if name=='M3_engine_candidate' else 'Stopped with session interrupt to avoid redundant slow fits after the adaptive-damping performance revision. Separate final batch uses the same statistical model and seven points.')
        data['annotated_at_utc']=datetime.now(timezone.utc).isoformat()
        p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print('Interrupted attempts annotated; existing stdout/stderr retained.')
