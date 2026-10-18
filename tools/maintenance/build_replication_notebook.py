"""Build a readable, unexecuted notebook that calls the canonical analysis modules."""
from pathlib import Path
import nbformat
root=Path(__file__).resolve().parents[2]
n=nbformat.v4.new_notebook()
n.cells=[nbformat.v4.new_markdown_cell('# Python replication\n\nRead `../docs/replication_results.md` first. Each cell calls the saved modules. Historical finite-quadrature and reliability-build equivalence limits remain explicit. Full binary fits can take time. This notebook is a runnable interface; actual execution evidence is in the run logs.'),
nbformat.v4.new_code_cell('from pathlib import Path\nimport sys, subprocess\nroot = Path.cwd()\nif root.name == "analysis": root = root.parent\nassert (root / "analysis/run_replication.py").exists()\nprint(root, sys.executable)'),
nbformat.v4.new_code_cell('def run_stage(stage):\n    subprocess.run([sys.executable, "-X", "utf8", "analysis/run_replication.py", "--stage", stage], cwd=root, check=True)')]
for stage in ['data','reliability','ordinal','binary','summaries','checks']:
    n.cells.append(nbformat.v4.new_code_cell(f'run_stage("{stage}")'))
n.metadata['kernelspec']={'display_name':'Python 3','language':'python','name':'python3'}
nbformat.validate(n)
nbformat.write(n,root/'analysis/01_replication.ipynb')
print('Notebook saved and schema validated; not executed a second time.')
