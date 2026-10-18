"""Check source bindings and key Option 3 specification invariants, without fitting."""
import argparse
import csv
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

REQUIRED_DOCUMENTS = [
    "docs/theory.md", "docs/variable_dictionary.csv", "docs/hypothesis_matrix.csv",
    "docs/analysis_inventory.csv", "docs/design_and_models.md", "docs/model_diagram.mmd",
    "docs/model_diagram_map.csv", "docs/source_evidence.csv", "docs/foundational_reading.md",
    "docs/student_review.md", "docs/unresolved_decisions.csv", "records/specification_handoff.md",
]
MATRIX_FIELDS = set("analysis_id hypothesis_id source_locator status_confirmatory_exploratory "
                    "theoretical_premise_mechanism predicted_relationship population_sampling "
                    "coding_unit_dependence constructs_indicators measurement_coding_missing "
                    "estimand_parameter_contrast equation_syntax estimator_settings "
                    "assumptions_intervals_diagnostics published_rule dataset_spec_versions "
                    "script_path output_path published_values_path reproduced_values discrepancy "
                    "scientific_conclusion approval_status".split())
CORE_FIELDS = {"source_locator", "theoretical_premise_mechanism", "population_sampling",
               "coding_unit_dependence", "constructs_indicators", "measurement_coding_missing",
               "estimand_parameter_contrast", "equation_syntax", "estimator_settings",
               "assumptions_intervals_diagnostics", "published_rule", "dataset_spec_versions",
               "script_path", "output_path", "approval_status"}
EXPECTED_TARGETS = {
    "H1a": {(m, "majoritarian_vs_consensus", "positive") for m in ("M1", "M2")},
    "H1b": {("M3", "majoritarian_vs_consensus", "negative")},
    "H2a": {(m, "contested_vs_stable", "positive") for m in ("M1", "M2")},
    "H2b": {("M3", "contested_vs_stable", "negative")},
    "H3a": {(m, c, "negative") for m in ("M1", "M2")
            for c in ("website_vs_blog", "newspaper_vs_blog")},
    "H3b": {("M3", c, "positive") for c in ("website_vs_blog", "newspaper_vs_blog")},
}
EXPECTED_ANALYSIS_TYPES = {
    "D1": "item_descriptive", "D2": "reference_descriptive",
    "R1": "tone_reliability", "R2": "reference_reliability",
    "M1": "ordered_logit", "M2": "outrage_multilevel_logit",
    "M3": "recognition_multilevel_logit", "C1": "proportional_odds_diagnostics",
    "C2": "original_alternative_links", "C3": "null_multilevel_comparison",
    "P1": "ordinal_predictions", "P2": "binary_predictions",
    "A1": "supplement_inventory", "V1": "independent_statistical_verification",
    "N1": "statistical_negative_check", "S1": "additional_sensitivity",
}


def load_csv(root, relative, errors):
    try:
        with (root / relative).open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            return list(reader), set(reader.fieldnames or [])
    except (OSError, csv.Error) as exc:
        errors.append({"code": "CSV_UNREADABLE", "detail": f"{relative}: {exc}"})
        return [], set()


def validate(root, specification=None):
    root = Path(root).resolve()
    errors, warnings = [], []

    def require(condition, code, detail):
        if not condition:
            errors.append({"code": code, "detail": detail})

    if specification is None:
        try:
            specification = json.loads((root / "docs/study_specification.json").read_text(encoding="utf-8-sig"))
        except (OSError, ValueError) as exc:
            return {"status": "failed", "errors": [{"code": "SPEC_UNREADABLE", "detail": str(exc)}],
                    "warnings": [], "ready_for_estimation": False}
    spec = specification
    require(spec.get("schema_version") == "1.0", "SCHEMA_VERSION", "Expected specification schema 1.0.")
    require(bool(spec.get("spec_version")), "SPEC_VERSION", "A specification version is required.")
    require(spec.get("artifact_kind") in ("study", "test"), "ARTIFACT_KIND", "Identify study or test.")
    for relative in REQUIRED_DOCUMENTS:
        path = root / relative
        require(path.is_file() and path.stat().st_size > 0, "DOCUMENT_MISSING", relative)

    sources = spec.get("sources", [])
    source_ids = [item.get("source_id") for item in sources]
    require(len(source_ids) == len(set(source_ids)), "SOURCE_DUPLICATE", "Source IDs must be unique.")
    require(bool(sources), "SOURCES_MISSING", "Bind inspected local original inputs.")
    for item in sources:
        if not item.get("relative_path"):
            require(bool(item.get("availability_note")), "SOURCE_GAP_UNDECLARED", str(item.get("source_id")))
            continue
        path = (root / item["relative_path"]).resolve()
        require(path.is_relative_to(root), "SOURCE_OUTSIDE_ROOT", item["relative_path"])
        if not path.is_relative_to(root):
            continue
        require(path.is_file(), "SOURCE_UNAVAILABLE", item["relative_path"])
        if path.is_file():
            require(sha256(path.read_bytes()).hexdigest() == item.get("sha256"),
                    "SOURCE_HASH_MISMATCH", item["relative_path"])

    hypotheses = spec.get("hypotheses", [])
    ids = [h.get("id") for h in hypotheses]
    require(set(ids) == set(EXPECTED_TARGETS) and len(ids) == 6,
            "HYPOTHESIS_COVERAGE", "Exactly the six stated hypotheses need separate entries.")
    for hypothesis in hypotheses:
        identifier = hypothesis.get("id")
        for field in ("premise", "mechanism", "prediction", "source_locator"):
            require(bool(hypothesis.get(field)), "HYPOTHESIS_FIELD", f"{identifier}: {field}")
        targets = hypothesis.get("targets", [])
        observed = {(t.get("model_id"), t.get("comparison"), t.get("expected_beta_sign")) for t in targets}
        require(observed == EXPECTED_TARGETS.get(identifier, set()), "HYPOTHESIS_DIRECTION_OR_TARGET",
                f"{identifier}: preserve author prediction, outcome coverage and model coefficient direction.")
        for target in targets:
            require(all(target.get(f) for f in ("predictor", "estimand", "source_locator")),
                    "TARGET_UNSPECIFIED", str(identifier))

    variables = {v.get("id"): v for v in spec.get("variables", [])}
    tone = variables.get("tone", {})
    require(tone.get("measurement_type") == "ordinal" and tone.get("analysis_unit") == "news_item",
            "TONE_MEASUREMENT", "Tone is ordinal at item level, not continuous or reference-level.")
    require(tone.get("raw_values") == [1, 2, 3, 4, 5] and tone.get("analysis_values") == [0, 1, 2, 3, 4],
            "TONE_RECODE", "Distinguish archive tone 1-5 from the author's analysis tone 0-4.")
    for name in ("actrefoutbin", "actrefrecbin"):
        variable = variables.get(name, {})
        require(variable.get("measurement_type") == "binary" and variable.get("analysis_unit") == "directed_actor_reference",
                "BINARY_MEASUREMENT", name)
        require(variable.get("analysis_values") == [0, 1], "BINARY_DOMAIN", name)
    for variable in variables.values():
        require(all(variable.get(f) for f in ("actual_data_variable", "source_locator", "missing_rule", "verification_status")),
                "VARIABLE_EVIDENCE", str(variable.get("id")))

    models = {m.get("id"): m for m in spec.get("models", [])}
    require(set(models) == {"M1", "M2", "M3"}, "MODEL_COVERAGE", "Keep three distinct main models.")
    expected_refs = {"polsys": "Consensus", "socdiv": "Stable secularism", "mediatype": "Blog"}
    for identifier, model in models.items():
        require(set(model.get("predictors", [])) == {"polsys", "socdiv", "mediatype"},
                "MODEL_PREDICTORS", f"{identifier}: no invented controls or measured mediators.")
        require(model.get("reference_categories") == expected_refs, "REFERENCE_CATEGORIES", identifier)
        require(model.get("link") == "logit", "MODEL_LINK", identifier)
        require(all(model.get(f) for f in ("equation", "original_syntax", "original_settings", "source_locator", "implementation_status")),
                "MODEL_SETTINGS", identifier)
        if identifier == "M1":
            require(model.get("family") == "ordered_logistic" and model.get("outcome") == "tone",
                    "ORDINAL_MODEL", "M1 must retain the ordered outcome.")
            require(model.get("random_intercept_groups") == [], "ORDINAL_RANDOM_EFFECTS", "Do not invent item-model random effects.")
        else:
            outcome = "actrefoutbin" if identifier == "M2" else "actrefrecbin"
            require(model.get("family") == "bernoulli" and model.get("outcome") == outcome,
                    "BINARY_MODEL", identifier)
            require(model.get("random_intercept_groups") == ["text_id", "act_id"],
                    "NESTING", "Actor/statement groups are nested in items; countries are not the random-effect hierarchy.")
    reliability = spec.get("reliability", {})
    require(reliability.get("input_type") == "independent_coder_ratings" and
            reliability.get("preserve_independent_ratings") is True,
            "RELIABILITY_INPUT", "Consensus codes do not estimate independent-coder reliability.")
    require(reliability.get("original_weights") == "identity", "RELIABILITY_WEIGHTS", "Match author identity weights; do not silently substitute ordinal weights.")

    rows, fields = load_csv(root, "docs/hypothesis_matrix.csv", errors)
    require(MATRIX_FIELDS.issubset(fields), "MATRIX_COLUMNS", "Retain all assignment Table 1 fields.")
    require({r.get("hypothesis_id") for r in rows}.issuperset(EXPECTED_TARGETS), "MATRIX_HYPOTHESES", "Missing hypothesis rows.")
    for index, row in enumerate(rows, 1):
        require(all(row.get(f, "").strip() for f in CORE_FIELDS), "MATRIX_SPEC_EMPTY", f"Row {index}")
        require(not row.get("reproduced_values", "").strip() and not row.get("discrepancy", "").strip(),
                "UNEXECUTED_RESULT", f"Row {index}: do not label copied or imagined values as reproduced.")
        require(row.get("scientific_conclusion", "").strip() == "not_run",
                "PREMATURE_SCIENTIFIC_CONCLUSION", f"Row {index}: this pre-estimation specification has no research conclusion.")
    inventory, _ = load_csv(root, "docs/analysis_inventory.csv", errors)
    inventory_ids = {r.get("analysis_id") for r in inventory}
    require(inventory_ids.issuperset(EXPECTED_ANALYSIS_TYPES),
            "ANALYSIS_COVERAGE", "Keep descriptive, reliability, diagnostics, supplementary and validation targets.")
    coverage = spec.get("coverage", [])
    coverage_ids = {c.get("analysis_id") for c in coverage}
    matrix_ids = {r.get("analysis_id") for r in rows}
    require(inventory_ids.issubset(coverage_ids) and inventory_ids.issubset(matrix_ids),
            "COVERAGE_ALIGNMENT", "Every inventory target needs a matrix and JSON coverage entry.")
    for identifier, analysis_type in EXPECTED_ANALYSIS_TYPES.items():
        for name, entries in (("inventory", inventory), ("JSON coverage", coverage)):
            matching = [entry for entry in entries if entry.get("analysis_id") == identifier]
            require(len(matching) == 1 and matching[0].get("analysis_type") == analysis_type,
                    "ANALYSIS_ID_MEANING", f"{name} {identifier}: preserve {analysis_type}, not merely the ID.")
    verification = next((entry for entry in coverage if entry.get("analysis_id") == "V1"), {})
    require({"important_descriptive", "core_advanced_model"}.issubset(verification.get("components", [])),
            "INDEPENDENT_VERIFICATION_SCOPE", "V1 must plan both descriptive and advanced-model checks; software setup alone does not qualify.")

    human = spec.get("human_review", {})
    if spec.get("artifact_kind") == "test":
        require(not any(human.get(k) for k in ("initial_explanation_received", "foundational_readings_attested", "specification_approved")),
                "SYNTHETIC_HUMAN_ATTRIBUTION", "Test inputs are not real student contributions or approval.")
    ready = bool(spec.get("ready_for_estimation"))
    require(not ready or (human.get("specification_approved") and human.get("initial_explanation_received")
                         and human.get("foundational_readings_attested") and not spec.get("deferred")),
            "PREMATURE_READINESS", "Human review and deferred implementation requirements must be resolved before readiness.")
    if not human.get("specification_approved"):
        warnings.append("Student specification approval remains pending; this is not a completed research checkpoint.")
    if spec.get("deferred"):
        warnings.append("Deferred original-setting/implementation questions remain visible for the next authorized task.")
    return {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
            "spec_version": spec.get("spec_version"), "artifact_kind": spec.get("artifact_kind"),
            "status": "failed" if errors else "technical_pass",
            "errors": errors, "warnings": warnings, "ready_for_estimation": ready and not errors,
            "research_models_fitted_by_validator": False, "statistical_equivalence_verified": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--spec", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    spec = json.loads(args.spec.read_text(encoding="utf-8-sig")) if args.spec else None
    result = validate(args.root, spec)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
