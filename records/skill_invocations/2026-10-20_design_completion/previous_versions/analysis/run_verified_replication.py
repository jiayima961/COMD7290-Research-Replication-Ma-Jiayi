"""One command rebuilds faithful results, full comparison, checks and sensitivity.

Run in a copy if existing evidence must be retained. DOCX editorial rendering and
human approval are separate; the command does not create an assessed release.
"""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def main():
 for script in ['analysis/run_replication.py','analysis/verify_and_package.py',
                'tests/skill3/check_verification.py','analysis/skill3_sensitivity.py']:
  subprocess.run([sys.executable,'-X','utf8',script],cwd=ROOT,check=True)
 print('All statistical stages, full comparison, independent verification and separate S1 completed; student acceptance remains pending.')
if __name__=='__main__':main()
