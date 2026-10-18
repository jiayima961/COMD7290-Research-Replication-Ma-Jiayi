"""Check meaningful specification failures on in-memory copies of the forward-test output."""
import argparse
import copy
from datetime import datetime, timezone
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / ".agents/skills/specify-empirical-study/scripts/validate_specification.py"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    module_spec = importlib.util.spec_from_file_location("specification_validator", VALIDATOR)
    validator = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(validator)
    case = args.case_root.resolve()
    baseline = json.loads((case / "docs/study_specification.json").read_text(encoding="utf-8-sig"))
    input_manifest = json.loads((case / "input_manifest.json").read_text(encoding="utf-8"))
    fingerprints = {item["path"]: sha256((case / item["path"]).read_bytes()).hexdigest()
                    for item in input_manifest["inputs"]}
    outcomes = []
    result = validator.validate(case, baseline)
    outcomes.append({"id": "positive_source_based_specification", "expected": "technical_pass_with_pending_human_review",
                     "observed": result["status"], "passed": result["status"] == "technical_pass"
                     and not result["ready_for_estimation"] and bool(result["warnings"]),
                     "errors": result["errors"]})

    def negative(identifier, expected_code, mutate):
        altered = copy.deepcopy(baseline)
        mutate(altered)
        actual = validator.validate(case, altered)
        codes = {error["code"] for error in actual["errors"]}
        outcomes.append({"id": identifier, "expected_error": expected_code, "observed_errors": sorted(codes),
                         "passed": actual["status"] == "failed" and expected_code in codes,
                         "ready_for_estimation": actual["ready_for_estimation"]})

    negative("reversed_original_prediction", "HYPOTHESIS_DIRECTION_OR_TARGET",
             lambda s: next(h for h in s["hypotheses"] if h["id"] == "H2b")["targets"][0].update(expected_beta_sign="positive"))
    negative("ordinal_tone_as_continuous", "TONE_MEASUREMENT",
             lambda s: next(v for v in s["variables"] if v["id"] == "tone").update(measurement_type="continuous"))
    negative("incorrect_country_media_article_hierarchy", "NESTING",
             lambda s: next(m for m in s["models"] if m["id"] == "M2").update(random_intercept_groups=["country", "mediatype", "text_id"]))
    negative("consensus_codes_as_independent_ratings", "RELIABILITY_INPUT",
             lambda s: s["reliability"].update(input_type="consensus_codes"))
    negative("ordinal_weights_substituted_for_author_identity_weights", "RELIABILITY_WEIGHTS",
             lambda s: s["reliability"].update(original_weights="ordinal"))
    negative("synthetic_input_as_real_student_approval", "SYNTHETIC_HUMAN_ATTRIBUTION",
             lambda s: s["human_review"].update(specification_approved=True))
    negative("premature_estimation_readiness", "PREMATURE_READINESS",
             lambda s: s.update(ready_for_estimation=True))
    negative("changed_source_fingerprint", "SOURCE_HASH_MISMATCH",
             lambda s: next(item for item in s["sources"] if item.get("relative_path")).update(sha256="0" * 64))
    negative("repurposed_required_analysis_id", "ANALYSIS_ID_MEANING",
             lambda s: next(item for item in s["coverage"] if item["analysis_id"] == "N1").update(analysis_type="null_multilevel_comparison"))
    negative("verification_missing_advanced_numerical_check", "INDEPENDENT_VERIFICATION_SCOPE",
             lambda s: next(item for item in s["coverage"] if item["analysis_id"] == "V1").update(components=["important_descriptive"]))
    original_csv_reader = validator.load_csv

    def premature_csv_conclusion(root, relative, errors):
        rows, fields = original_csv_reader(root, relative, errors)
        if relative == "docs/hypothesis_matrix.csv":
            rows = copy.deepcopy(rows)
            rows[0]["scientific_conclusion"] = "supported"
        return rows, fields

    with patch.object(validator, "load_csv", side_effect=premature_csv_conclusion):
        actual = validator.validate(case, copy.deepcopy(baseline))
    codes = {error["code"] for error in actual["errors"]}
    outcomes.append({"id": "premature_csv_scientific_conclusion", "expected_error": "PREMATURE_SCIENTIFIC_CONCLUSION",
                     "observed_errors": sorted(codes),
                     "passed": actual["status"] == "failed" and "PREMATURE_SCIENTIFIC_CONCLUSION" in codes,
                     "ready_for_estimation": actual["ready_for_estimation"]})
    final_fingerprints = {path: sha256((case / path).read_bytes()).hexdigest() for path in fingerprints}
    originals_preserved = fingerprints == final_fingerprints and all(
        fingerprints[item["path"]] == item["sha256"] for item in input_manifest["inputs"])
    report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(), "test_scope": "skill_1_specification_only",
              "validator_sha256": sha256(VALIDATOR.read_bytes()).hexdigest(),
              "baseline_specification_sha256": sha256((case / "docs/study_specification.json").read_bytes()).hexdigest(),
              "cases": outcomes, "unchanged_original_inputs": originals_preserved,
              "status": "passed" if all(item["passed"] for item in outcomes) and originals_preserved else "failed",
              "assignment_statistical_negative_test_completed": False,
              "research_models_fitted": False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
