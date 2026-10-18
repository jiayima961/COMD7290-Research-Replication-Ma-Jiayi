# COMD7290-Research Replication-Ma Jiayi

An individual statistics course project reproducing the content-analysis study by Löb, Rinke, Weinmann, and Wessler.

**Open [START_HERE.md](START_HERE.md) first.** It links the current work, the chronological student/AI review history, study files and supporting records in reading order.

**Current stage: student theory explanation v2 has received round-2 feedback. Foundational reading notes and full specification approval remain pending; research models have not been fitted.**

Selected article: Löb, C., Rinke, E. M., Weinmann, C., & Wessler, H. (2024). Unpacking the determinants of outrage and recognition in public discourse: Insights across socio-cultural divides, political systems, and media types. *The International Journal of Press/Politics, 29*(1), 273–294. https://doi.org/10.1177/19401612221084206

The article appeared online in 2022 and in its journal volume in 2024; these dates refer to the same article.

## Starting points

1. Read [project status](STATUS.md) for completed work, unresolved questions, decisions, and next steps.
2. Read the [assignment checklist](docs/assignment_checklist.md) and [repository structure and workflow](docs/github_structure_and_workflow.txt).
3. Review the draft [theory and hypotheses](docs/theory.md), [variable dictionary](docs/variable_dictionary.csv), and [design and models](docs/design_and_models.md). These require the student's own reconstruction, source checks, and approval.
4. Use the [hypothesis-to-evidence matrix](docs/hypothesis_matrix.csv) as the central index. The [analysis inventory](docs/analysis_inventory.csv) tracks descriptive, reliability, model, diagnostic, prediction, figure, and supplementary analyses.
5. Published comparison targets are in [outputs/published](outputs/published/). Newly computed results will be saved separately in [outputs/reproduced](outputs/reproduced/).
6. For skill 1 preparation, test evidence and the later personal-feedback workflow, see [skill 1 usage](docs/skill1_usage.md), [the test report](records/skill_tests/specify-empirical-study/TEST_REPORT.md) and [the evaluation plan](records/skill_tests/specify-empirical-study/evaluation_plan.md). Isolated test examples are separate from the student's canonical study specification.
7. The current [student explanation v2](records/student_inputs/2026-10-18_revised_theory_explanation_v2.txt), [round-2 feedback](docs/theory_feedback_v2.md) and [revision progress](docs/student_review.md) record the second personal review. Both review rounds are ordered in [START_HERE.md](START_HERE.md), separately from the synthetic case.

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

For the Python/Jupyter foundation, see [environment.md](environment.md) and [Python route assessment](docs/python_route_assessment.md). The local launcher is `Start_Jupyter_Notebook.cmd`; the synthetic environment notebook is `analysis/00_environment_check.ipynb`. The installation record is separate from research-analysis results.

With the project Python environment available, run this command from the repository root:

```powershell
rtk proxy .\.venv\Scripts\python.exe tools/check_repository.py
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
