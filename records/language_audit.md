# English-language correction audit

Date: 2026-10-17.

The user required English in GitHub and local project-authored files. An audit found **35 tracked files containing Chinese**, plus the separate workflow TXT in the outer local project folder. The affected files covered navigation, research drafts, skill bodies, evidence records, directory notes, and student report/follow-up templates.

## Corrections

- Translated all 35 affected repository files into English.
- Renamed the repository workflow guide to `docs/github_structure_and_workflow.txt` and updated its README link.
- Replaced the separate local workflow guide with `COMD7290_GitHub_structure_and_workflow.txt` in the outer project folder.
- Added the English-language requirement to AGENTS.md and retained draft/pending labels and student-review requirements.
- Preserved numerical CSV contents and all original author/user-supplied research inputs byte for byte. Existing English formulas and source identifiers remain unchanged in meaning.
- This is an editorial correction, not statistical execution or completion of student-authored analysis.

## Translated repository files (current paths)

- `.agents/skills/reproduce-and-diagnose/SKILL.md`
- `.agents/skills/specify-empirical-study/SKILL.md`
- `.agents/skills/verify-and-package/SKILL.md`
- `README.md`
- `STATUS.md`
- `analysis/README.md`
- `data/README.md`
- `data/original/README.md`
- `data/prepared/README.md`
- `docs/assignment_checklist.md`
- `docs/design_and_models.md`
- `docs/follow_up.md`
- `docs/github_structure_and_workflow.txt`
- `docs/limitations.md`
- `docs/model_diagram.mmd`
- `docs/theory.md`
- `environment.md`
- `outputs/diagnostics/README.md`
- `outputs/published/README.md`
- `outputs/reproduced/README.md`
- `outputs/review_report.md`
- `records/access_status.md`
- `records/agent_records.md`
- `records/checkpoints.md`
- `records/decisions.md`
- `records/handoffs.md`
- `records/run_logs/README.md`
- `records/run_logs/initialization.md`
- `report/README.md`
- `report/report_outline.md`
- `report/submission_checklist.md`
- `sources/README.md`
- `sources/author_code/README.md`
- `sources/local/README.md`
- `tests/README.md`

## Validation scope

Local checks found no remaining Chinese characters in the 47 project-authored text documents or the separate workflow guide, and no broken relative Markdown links. The two dotfiles are already English. The repository material check passed, and all three translated skills passed the official quick_validate.py check. The 8 numerical CSV files and 14 original input files retained their SHA-256 hashes.

The uploaded GitHub tree must also be compared against the final local index before reporting synchronization complete. Original third-party data/code/documents and historical Git objects are preserved as sources/history rather than rewritten as project prose.
