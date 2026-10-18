"""Update mutable navigation after preserving the preceding working drafts."""
from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[1]
before=root/'records/skill_invocations/2026-10-18_reproduce-and-diagnose/before'
paths=['README.md','STATUS.md','docs/analysis_inventory.csv','docs/hypothesis_matrix.csv','analysis/README.md']
for name in paths:
    dest=before/name;dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():shutil.copy2(root/name,dest)
p=root/'STATUS.md';text=p.read_text(encoding='utf-8-sig')
text=text.replace('Updated: 2026-10-18. Stage: student theory v2 reviewed; remaining refinements, reading notes and complete-specification approval are pending. Checkpoint A is not complete. Use START_HERE.md for the ordered document trail.',
'Updated: 2026-10-18. Stage: user-authorized skill-2 Python reproduction. See docs/replication_results.md for actual calculated results, numerical limitations and current fit status. Student reading/diagram attestations and final submission approval remain pending. Use START_HERE.md for navigation.')
start=text.index('## Remaining work');end=text.index('## Project identity')
text=text[:start]+'''## Current scope and remaining work

- D011 explicitly authorizes faithful Python-only data checks, reliability, descriptives, hypothesis fits and numerical verification. It supersedes earlier task-level no-fit/deferral limits. The source-bound specification is docs/execution_specification.md.
- Actual skill-2 results and limitations are indexed in docs/replication_results.md; completed numerical evidence must not be confused with earlier synthetic skill-1 fixtures.
- Historical finite-grid and reliability-build equivalence limits remain explicit. Do not claim a complete original-executable match merely because printed values agree.
- Complete skill 3, the separate justified substantive sensitivity analysis, student-owned reading/diagram records, final report and acceptance. Computational reproduction does not itself complete all course checkpoints.
- Keep the repository private and do not invite the instructor. No latest-run upload, final release or submission has been performed.
- All project-authored files remain English. Preserve original sources, earlier student submissions and completed historical evidence.

'''+text[end:]
p.write_text(text,encoding='utf-8')
p=root/'README.md';text=p.read_text(encoding='utf-8-sig')
if '**Current analysis results:**' not in text:
    text=text.replace('**Open [START_HERE.md](START_HERE.md) first.**','**Open [START_HERE.md](START_HERE.md) first.**\n\n**Current analysis results:** [Python replication results and evidence](docs/replication_results.md). The user has authorized and started real skill-2 analyses; consult this index for completed results and remaining numerical limitations.')
p.write_text(text,encoding='utf-8')
(root/'analysis/README.md').write_text('''# Python analysis entry points

Read [the results index](../docs/replication_results.md) and [execution specification](../docs/execution_specification.md).

Run all stages from the repository root:

```powershell
rtk proxy .venv/Scripts/python.exe -X utf8 analysis/run_replication.py
```

The same stages are available in `01_replication.ipynb`: data, reliability, ordinal, binary, summaries and checks. Use `--stage NAME` for one stage. Binary fitting can take substantial time. The runner saves command logs and stops on failure; diagnostics must still be inspected.

- prepare_replication.py: hash/domain/nesting checks and original-code recodes.
- reliability_reproduction.py: original selected independent-rating matrices, agreement coefficients and conditional uncertainty.
- ordinal_reproduction.py: descriptive tables, cumulative models, original diagnostics and predictions.
- nested_logit.py / run_binary_models.py: frequentist three-level Bernoulli models and their nulls with seven-point recursive adaptive integration.
- binary_predictions.py: prior-marginal probabilities and discrete AMEs with full-covariance delta uncertainty.
- compare_replication.py: comparison to separately stored published targets and 12 hypothesis targets.

The finite historical integration grid/build is not completely recovered. These limitations are recorded beside results rather than hidden by changing the model. The notebook is a runnable interface; execution evidence resides in records/run_logs/skill2.
''',encoding='utf-8')
print('Mutable navigation updated; preceding drafts preserved in the invocation record.')
