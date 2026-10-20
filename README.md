# COMD7290 Research Replication — Ma Jiayi

Final research repository for the Python reproduction of Löb et al. (2024),
*Unpacking the Determinants of Outrage and Recognition in Public Discourse*,
DOI https://doi.org/10.1177/19401612221084206. COMD7290 Option 3, content analysis.

**Read the [final individual report](report/COMD7290%20Individual%20Report%20for%20Research%20Replication.docx),
then use [START_HERE.md](START_HERE.md) to explore the evidence.**
The [final project status](STATUS.md) summarizes the completed work.

| Reader's question | Evidence |
| --- | --- |
| What was predicted and tested? | [Matrix guide](docs/hypothesis_matrix.md), [28-row matrix](docs/hypothesis_matrix.csv), [source-bound specification](docs/execution_specification.md) |
| How were variables and models defined? | [144-entry dictionary](docs/variable_dictionary.md), [two numbered model diagrams](docs/model_diagram.md), [equation/code map](docs/model_diagram_map.csv) |
| Where are the reusable agent skills? | [Skill guide](docs/skills/README.md), [specification](.agents/skills/specify-empirical-study/SKILL.md), [reproduction](.agents/skills/reproduce-and-diagnose/SKILL.md), [verification](.agents/skills/verify-and-package/SKILL.md) |
| Where are the statistical results? | [Results explanation](docs/replication_results.md), [outputs index](outputs/README.md), [hypothesis tests](outputs/reproduced/hypothesis_tests.csv) |
| How do the results compare with the article? | [Complete comparison ledger](outputs/verification/comparison_all.csv), [technical Word reports](report/verification/README.md) |
| What did the student and agents contribute? | [Student inputs and review trail](records/README.md), [three accepted decision reviews](records/skill3_decision_audit.md), [approved handoff](records/handoffs/2026-10-20/README.md) |
| How can another agent reproduce the work? | [Teacher quickstart](docs/guides/teacher_quickstart.md), [input restoration](sources/README.md), [environment](environment.md), [analysis guide](analysis/README.md) |

The reproduction covers independent-coder reliability, descriptive statistics,
ordinal item-level outrage, nested binary outrage and recognition, diagnostics,
predictions and marginal effects. The hypothesis conclusions agree with the
article. Of 376 numeric published targets, 362 agree at reported precision,
13 differ, and one diagnostic p value is not validated. Detailed comparisons
retain source inconsistencies and numerical qualifications. Computational
agreement does not establish causal effects.

All three skills have discovery, invocation and test evidence. The package also
includes independent numerical checks, error-detection and recovery evidence,
isolated clean reruns, six country-deletion influence fits, a follow-up proposal,
the student-approved working specification and a successful fresh-context handoff.

```text
.agents/skills/  Three reusable agent skills
docs/           Theory, matrix, dictionary, diagrams and analysis specification
analysis/       Python implementations, notebooks and rerun entry points
tests/          Specification and numerical checks
outputs/        Published targets, reproduced results and verification
records/        Student inputs, reviews, approvals, logs and handoff receipts
report/         Final individual report and two technical Word reports
sources/        Provenance and exact-version input-restoration instructions
data/           Local research inputs with tracked access instructions
tools/          Setup, restoration and maintenance utilities
```

After installing the pinned environment and restoring permitted exact-version
inputs, run from the repository root:

```powershell
python tools/restore_inputs.py
python tools/check_repository.py
python analysis/run_verified_replication.py
```

The last command performs the full statistical pipeline and verification and
can take substantial time. Preserve existing evidence before a new rerun.
Ordinary Python works without the optional local RTK wrapper.

Original third-party PDFs, author inputs and subject-level derived arrays stay
local where redistribution terms are unresolved. Access routes, exact hashes
and restoration instructions are supplied. The repository shares our code,
skills, aggregate results, documents and research records. The current repository
is public. Historical visibility statements describe their recorded dates.

The [20 October finalization record](records/finalization/2026-10-20/README.md)
documents this upload and the unchanged final report. Earlier versions are
retained in dated archives rather than deleted.
