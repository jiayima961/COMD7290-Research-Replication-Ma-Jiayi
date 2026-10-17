# COMD7290-Research Replication-Ma Jiayi

An individual statistics course project reproducing the content-analysis study by Löb, Rinke, Weinmann, and Wessler.

**Current stage: repository initialization. Research models have not been fitted and the final assignment is not complete.**

Selected article: Löb, C., Rinke, E. M., Weinmann, C., & Wessler, H. (2024). Unpacking the determinants of outrage and recognition in public discourse: Insights across socio-cultural divides, political systems, and media types. *The International Journal of Press/Politics, 29*(1), 273–294. https://doi.org/10.1177/19401612221084206

The article appeared online in 2022 and in its journal volume in 2024; these dates refer to the same article.

## Starting points

1. Read [project status](STATUS.md) for completed work, unresolved questions, decisions, and next steps.
2. Read the [assignment checklist](docs/assignment_checklist.md) and [repository structure and workflow](docs/github_structure_and_workflow.txt).
3. Review the draft [theory and hypotheses](docs/theory.md), [variable dictionary](docs/variable_dictionary.csv), and [design and models](docs/design_and_models.md). These require the student's own reconstruction, source checks, and approval.
4. Use the [hypothesis-to-evidence matrix](docs/hypothesis_matrix.csv) as the central index. The [analysis inventory](docs/analysis_inventory.csv) tracks descriptive, reliability, model, diagnostic, prediction, figure, and supplementary analyses.
5. Published comparison targets are in [outputs/published](outputs/published/). Newly computed results will be saved separately in [outputs/reproduced](outputs/reproduced/).

## Repository structure

```text
.agents/skills/   Three project-level skills
sources/         Source locations and access instructions; local/ holds local-only copies
docs/            Theory, hypotheses, measurement, models, checklists, and follow-up design
data/            original/ for unchanged inputs; prepared/ for derived analytical data
analysis/        Analysis implementation and execution plan
tests/           Data checks, model checks, and a harmless negative test
outputs/         Published targets, reproduced results, diagnostics, comparisons, and review
records/         Provenance, decisions, AI tasks, handoffs, checkpoints, and run logs
report/          Individual report outline and final submission checklist
tools/           Repository checks and source-download helper
```

## Local material check

With Python 3 available, run this command from the repository root:

```text
python tools/check_repository.py
```

This checks repository structure, CSV fields, and registered local-source checksums. It does not estimate statistical models. The final statistical environment and tested complete rerun command remain to be implemented; see [environment.md](environment.md) and [analysis/README.md](analysis/README.md).

## Access and submission status

- Project and local folder: `COMD7290-Research Replication-Ma Jiayi`
- GitHub repository name: `COMD7290-Research-Replication-Ma-Jiayi`
- Private repository: https://github.com/jiayima961/COMD7290-Research-Replication-Ma-Jiayi
- Instructor account: `fffchaobu`, checked against the assignment. **Do not send an invitation yet**, as requested by the user on 2026-10-17.
- Student name and identifier: to be supplied by the student; do not infer them from the login email.
- Final report, assessed tag, and release: not yet created. Initialization is not the final submission.
- Redistribution rights for source PDFs, author data, and author code remain under review. Originals are kept locally; access instructions are in sources/README.md and data/README.md.
- All project-authored files and filenames must be in English. The [language audit](records/language_audit.md) records the correction of the initial Chinese drafts.
