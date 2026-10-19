# COMD7290 Research Replication — Ma Jiayi

Python reproduction of Löb et al., *Unpacking the Determinants of Outrage and Recognition in Public Discourse*, DOI [10.1177/19401612221084206](https://doi.org/10.1177/19401612221084206). COMD7290 Option 3, content analysis. All three skills now have implemented workflows and execution/test evidence. Student acceptance and final submission requirements remain pending.

**Start with [START_HERE.md](START_HERE.md).** To use the tested skills, open this repository as the agent's working folder and follow the [skill guide](docs/skills/README.md). The actual skill packages are in [.agents/skills/](.agents/skills/).

| Reader's question | Go to |
| --- | --- |
| What was predicted, and how was it tested? | [Hypothesis matrix](docs/hypothesis_matrix.csv) → [execution specification](docs/execution_specification.md) → [analysis code](analysis/README.md) → [hypothesis tests](outputs/reproduced/hypothesis_tests.csv) → [results and limitations](docs/replication_results.md) |
| Where are the three skills? | [Skill 1](.agents/skills/specify-empirical-study/SKILL.md), [Skill 2](.agents/skills/reproduce-and-diagnose/SKILL.md), [Skill 3](.agents/skills/verify-and-package/SKILL.md), [invocation instructions and evidence](docs/skills/README.md) |
| Where are the numerical results? | [Results index](outputs/README.md), [complete comparison ledger](outputs/verification/comparison_all.csv), [Word report index](report/verification/README.md) |
| What did the student write and how did AI respond? | [Ordered review trail](records/README.md) |
| How can I run this on my computer? | [Setup and rerun guide](docs/guides/teacher_quickstart.md), [input access and verification](sources/README.md), [environment](environment.md) |
| What remains? | [Current status](STATUS.md), [assignment checklist](docs/assignment_checklist.md) |

```text
.agents/skills/  Agent-discoverable skill packages
docs/           Theory, hypotheses, model specifications, reviews and guides
data/           Original and prepared data (local; access instructions tracked)
sources/        Source provenance and input-restoration manifest
analysis/       Statistical Python modules and notebook entry points
tests/          Specification and numerical verification programs
outputs/        Published targets, reproduced results and diagnostics
records/        Student inputs, actual invocations, tests and execution logs
report/         Final-report preparation (unfinished)
tools/          Setup, input restoration, logging and repository checks
tmp/, .venv/    Local runtime/cache files, excluded from Git
```

The saved results include independent-coder reliability, descriptives, M1 ordinal tone, M2/M3 nested binary models, predictions and 12 directional hypothesis targets. Of 45 published coefficient/SE/OR cells, 44 match printed rounding; the remaining discrepancy is retained. Historical Stata integration details and reliability-package builds are not fully recovered. See [the results explanation](docs/replication_results.md) before interpreting agreement as robustness.

Skill 3 adds the [complete source comparison and Python/Stata justification](report/verification/README.md), fresh independent M1/margin checks, an isolated full clean refit and a [separate country influence sensitivity](outputs/verification/sensitivity/README.md). All 376 numeric target entries are accounted for: 362 agree at their stated display/integer precision, 13 differ and one LR p value remains unverified. Full unprinted quantities are explicitly distinguished. [Student decisions](records/skill3_decision_audit.md) and the [final-stage checklist](report/skill3_submission_readiness.md) remain visible.

Quick rerun after setting up Python and restoring inputs, from the repository root:

```powershell
python tools/restore_inputs.py
python tools/check_repository.py
python analysis/run_replication.py --stage data
python analysis/run_replication.py
```

Use the Python interpreter from the project's activated environment. Ordinary Python works without RTK; when RTK is available, the logging helper uses it automatically. The full run can take substantial time and updates canonical analysis outputs; preserve a copy for a new independent rerun. The notebook [analysis/01_replication.ipynb](analysis/01_replication.ipynb) invokes the same stages. Saved historical logs remain the evidence of the completed original runs.

Author data, third-party PDFs/method files and subject-level derived arrays remain local where redistribution is unresolved. Their access routes, exact hashes and restoration instructions are included; the repository supplies our skill packages, code, aggregate results, tests and records. No Stata licence is needed for the Python calculations.

The [2026-10-19 reorganization record](records/reorganization/2026-10-19/README.md) maps old paths to new paths and verifies preserved files. No existing file was deleted. The repository remains private; no collaborator invitation, release or submission is part of this update.
