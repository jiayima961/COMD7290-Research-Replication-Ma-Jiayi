# Technical verification review

Material passport: ANALYZED from saved faithful outputs, with separately EXECUTED
fresh independent M1 and AME calculations, negative/recovery checks, six country
deletions and a full source/input-only clean refit. Original data and skill 2
numerical results were not overwritten. Student scientific acceptance is pending.

The complete review is report/verification/01_results_comparison.md and its DOCX;
software equivalence is report/verification/02_python_stata_equivalence.md and its
DOCX. Use outputs/verification/comparison_all.csv, not only the old 45-cell subset.

Core results agree at published precision with explicitly retained exceptions.
Thirteen numeric target entries differ, and one published LR p value cannot be
validated. Source labeling/table anomalies, unresolved numerical/postestimation
differences and diagnostic identification failures are distinguished. No remaining
difference is assigned to software alone without evidence. The generalized ordinal
LR is not accepted as regular inference, despite agreement of its raw statistic.

Evidence: independent checks outputs/verification/independent_checks/checks.json;
source review records/skill_tests/verify-and-package/independent_source_audit.md;
clean run records/run_logs/skill3/clean_restart/receipt.json; model checks
outputs/diagnostics/glmm/; coverage docs/analysis_inventory.csv; fallacy review
outputs/verification/interpretation_audit.md; human decisions
records/skill3_decision_audit.md. Technical completion does not complete the
student's personal reading, diagram, decision acceptance or release/submission.
