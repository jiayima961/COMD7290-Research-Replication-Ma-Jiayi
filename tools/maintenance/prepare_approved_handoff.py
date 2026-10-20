"""Bind current source/specification evidence for a file-only receiving session."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json
import shutil

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "records/handoffs/2026-10-20"
INPUTS = [
    "docs/execution_specification.md", "docs/design_and_models.md",
    "docs/hypothesis_matrix.csv", "docs/variable_dictionary.csv",
    "docs/model_diagram.mmd", "docs/model_diagram_m1.mmd", "docs/model_diagram_map.csv",
    "records/student_inputs/2026-10-18_revised_theory_explanation_v2.txt",
    "docs/limitations.md", "docs/follow_up.md", "records/skill3_decision_audit.md",
    "records/student_decision_reviews/2026-10-20/review.json",
    "records/source_manifest.csv", "sources/input_restore_manifest.json",
    "sources/author_code/MedCon_Civility_an.do", "sources/author_code/reliability_original.do",
    "data/original/MedCon_Civility_item.dta", "data/original/MedCon_Civility_actref.dta",
    "analysis/prepare_replication.py", "analysis/ordinal_reproduction.py",
    "analysis/nested_logit.py", "analysis/binary_predictions.py",
    "outputs/reproduced/models/ordinal/M1_model.json",
    "outputs/reproduced/models/M2_fit.json", "outputs/reproduced/models/M3_fit.json",
    "outputs/reproduced/hypothesis_tests.csv", "outputs/verification/summary.json",
    "outputs/verification/comparison_all.csv", "outputs/verification/independent_checks/checks.json",
    "outputs/verification/sensitivity/plan.json",
    "outputs/verification/sensitivity/country_deletion_summary.csv",
    "outputs/diagnostics/measurement/semantic_checks.json",
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for rel in ["records/handoffs.md", "records/checkpoints.md", "docs/student_review.md",
                "docs/assignment_checklist.md", "docs/assignment_audit.md", "docs/follow_up.md",
                "STATUS.md", "START_HERE.md", "records/decisions.md", "report/skill3_submission_readiness.md"]:
        previous = OUT / "previous_versions" / rel
        if not previous.exists():
            previous.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, previous)
    manifest = dict(prepared_at_utc=datetime.now(timezone.utc).isoformat(),
                    version="working-handoff-2026-10-20-v1",
                    binding="Current local working files, including uncommitted documentation. Not an assessed release or tag.",
                    inputs=[dict(path=p, sha256=sha256((ROOT / p).read_bytes()).hexdigest()) for p in INPUTS])
    path = OUT / "input_manifest.json"
    if path.exists():
        raise SystemExit("Manifest already exists. Do not replace a version submitted for student approval.")
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (OUT / "approvals.json").write_text(json.dumps(dict(
        status="awaiting_student_response", specification_approved=False,
        interpretation_sensitivity_proposal_approved=False, fresh_agent_test_authorized=False,
        chronological_boundary="Current retrospective approval only, never pre-fit approval.",
        final_report_or_submission_approved=False), indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"version": manifest["version"], "bound_inputs": len(INPUTS), "status": "prepared_for_review"}))


if __name__ == "__main__":
    main()
