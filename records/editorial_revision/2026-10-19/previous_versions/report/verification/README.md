# Skill 3 verification documents

Read in this order. All documents are English. The technical review is distinct
from the student's final assessed acceptance.

1. **01_results_comparison.docx** — readable comparison of the entire reproduction,
   agreement levels, every discrepancy family and attribution limits. Its adjacent
   Markdown file is the editable source.
2. **02_python_stata_equivalence.docx** — assignment-specific justification,
   original/Python model settings, numerical validation and remaining equivalence
   limits. Its adjacent Markdown file is the editable source.
3. [Complete numeric ledger](../../outputs/verification/comparison_all.csv) — every
   comparison with original/reproduced values, differences, tolerances and sources.
   [Source targets](../../outputs/published/verification_targets.csv) are transcribed
   publication values, never fitting inputs. [Coverage](../../docs/analysis_inventory.csv)
   includes unverifiable targets rather than silently dropping them.
4. [Independent checks](../../outputs/verification/independent_checks/checks.json),
   [source audit](../../records/skill_tests/verify-and-package/independent_source_audit.md),
   [clean restart](../../records/run_logs/skill3/clean_restart/receipt.json), and
   [separate sensitivity](../../outputs/verification/sensitivity/README.md).
   The [skill 3 test report](../../records/skill_tests/verify-and-package/TEST_REPORT.md)
   links static validation, runtime discovery, independent checks, both full
   clean runs, source/forward review, preservation and final Word visual QA.
5. [AI decisions requiring student review](../../records/skill3_decision_audit.md),
   [follow-up design](../../docs/follow_up.md), [limitations](../../docs/limitations.md),
   [report draft](../final_report_draft.md) and [remaining submission steps](../skill3_submission_readiness.md).

The previous 45-cell outputs/comparison.csv remains unchanged for skill 2. Use
the complete ledger above for this review. No assessed release or instructor
invitation was created. No personal reading, diagram ownership, student ID or
scientific approval was supplied by the agent.

For one command that rebuilds all statistical and verification stages, use
analysis/run_verified_replication.py from a project copy. The original scientific
entry and saved skill 2 results remain unchanged. These latest skill 3 additions
are saved locally; GitHub has not been synchronized in this task.
