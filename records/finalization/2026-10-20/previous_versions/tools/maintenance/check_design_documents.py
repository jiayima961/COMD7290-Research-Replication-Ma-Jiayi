"""Check completed measurement and model documentation without fitting models."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import csv
import json
import re
import xml.etree.ElementTree as ET
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
RECORD = ROOT / "records/skill_invocations/2026-10-20_design_completion"


def csvrows(rel):
    with (ROOT / rel).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8-sig"))


def main():
    checks = []

    def check(name, condition, **details):
        checks.append(dict(check=name, passed=bool(condition), **details))

    dictionary = csvrows("docs/variable_dictionary.csv")
    metadata = load("outputs/diagnostics/measurement/dataset_metadata.json")
    actual = {(a["dataset"], f["variable"]): (a, f) for a in metadata for f in a["fields"]}
    documented = {(r["dataset"], r["actual_data_variable"]) for r in dictionary if r["dataset"] != "derived"}
    check("All archive fields covered exactly once", documented == set(actual) and len(documented) == 138,
          observed_field_rows=len(documented))
    check("All dictionary IDs unique and fields populated", len(dictionary) == 144 and len({r["row_id"] for r in dictionary}) == 144
          and all(k is not None and isinstance(v, str) and v.strip() for r in dictionary for k, v in r.items()))
    check("Original dictionary contract columns retained", set("concept source_variable actual_data_variable unit measurement_type values_meaning reference_category missing_rule transformation source_locator verification_status raw_values_meaning".split()).issubset(dictionary[0]))
    check("Five unfinished auxiliary groups expanded into actual variables", {"bezug_akteur_id", "respobj_akteur", "valenz_akteur", "genuinekonstruierte_resp_akteur", "rolle_allgemein", "rolle_pol_land", "rolle_pol_level", "rolle_pol_inland_national", "rolle_pol_ausland_national", "parteizugehoerigkeit", "herkunft", "geschlecht", "religionszugehoerigkeit", "date_published", "mediaoutlet", "title", "rubrik", "laenge", "darstellungsform", "anfangsseite"}.issubset({v for _, v in documented}))
    check("No old uninspected auxiliary placeholder remains", all("pending author dataset" not in str(r) and "pending source/data inspection" not in str(r) for r in dictionary))
    defects = []
    for r in dictionary:
        if r["dataset"] == "derived":
            continue
        a, f = actual[(r["dataset"], r["actual_data_variable"])]
        if r["dataset_sha256"] != a["sha256"] or json.loads(r["observed_numeric_counts"]) != f.get("observed_numeric_counts", {}):
            defects.append(r["row_id"])
        if f"System missing={f['system_missing_n']}" not in r["missing_rule"] or f"blank strings={f['blank_string_n']}" not in r["missing_rule"]:
            defects.append(r["row_id"])
    check("Domains, missingness and input hashes match source metadata", not defects, mismatches=defects)
    derived = {r["actual_data_variable"] for r in dictionary if r["dataset"] == "derived"}
    check("All six actual grouping/design terms documented", derived == {"act_id", "mixed_vs_consensus", "majoritarian_vs_consensus", "contested_vs_stable", "website_vs_blog", "newspaper_vs_blog"})
    semantic = load("outputs/diagnostics/measurement/semantic_checks.json")
    check("Originator grouping distinction backed by aggregate check", semantic["origin_id_to_model_group_max_unique"] == 1 and semantic["model_group_to_origin_id_max_unique"] == 1)
    check("Observed source exceptions retained explicitly", semantic["joint_outrage_recognition_present_n"] == 1 and semantic["legacy_media_disagreements_under_expected_1newspaper_2website_3blog"] == 52
          and "52/1700" in (ROOT / "docs/variable_dictionary.md").read_text()
          and "One of 3770" in (ROOT / "docs/variable_dictionary.md").read_text())
    nodes = csvrows("docs/model_diagram_map.csv")
    registry = load("records/skill_invocations/2026-10-20_design_completion/diagram_registry.json")
    check("All diagram nodes mapped and populated", len(nodes) == 17 and {r["node_id"] for r in nodes} == {r["node_id"] for r in registry}
          and all(k is not None and isinstance(v, str) and v.strip() for r in nodes for k, v in r.items()))
    matrix_ids = {r["row_id"] for r in csvrows("docs/hypothesis_matrix.csv")}
    bad_paths, bad_matrix, bad_functions = [], [], []
    for r in nodes:
        bad_matrix.extend(v for v in r["matrix_row_ids"].split(" | ") if v not in matrix_ids)
        bad_paths.extend(p for p in r["planned_script_path"].split(" | ") if not (ROOT / p).is_file())
        for p, line, function in re.findall(r"([^| ]+\.py):(\d+) \(([^)]+)\)", r["executing_functions"]):
            content = (ROOT / p).read_text().splitlines()
            if not re.match(r"^(def|class) " + re.escape(function) + r"\b", content[int(line)-1]):
                bad_functions.append((p, line, function))
    check("Every node links to existing code and matrix rows", not bad_paths and not bad_matrix, missing_paths=bad_paths, missing_rows=bad_matrix)
    check("Function and line bindings match actual executing code", not bad_functions, mismatches=bad_functions)
    placements = load("records/skill_invocations/2026-10-20_design_completion/diagram_placements.json")
    for name, figure, expected in [("model_diagram", "Figure 1", {"POL", "SEC", "MED", "X", "M2U", "M2V", "M2ETA", "M2Y", "M3U", "M3V", "M3ETA", "M3Y", "CONFIG"}),
                                   ("model_diagram_m1", "Figure 2", {"X", "M1ETA", "M1C", "M1Y", "M1CONFIG"})]:
        svg = ET.parse(ROOT / f"docs/figures/{name}.svg").getroot()
        ids = {x.attrib["id"] for x in svg.iter() if "id" in x.attrib}
        mmd = (ROOT / f"docs/{name}.mmd").read_text()
        defined = set(re.findall(r'^\s+([A-Za-z][A-Za-z0-9_]*)\["', mmd, re.M))
        check(f"{figure} SVG/Mermaid node coverage", expected.issubset(ids) and defined == expected)
        image = Image.open(ROOT / f"docs/figures/{name}.png")
        check(f"{figure} raster dimensions match SVG export", image.size == (int(svg.attrib["width"]) * 2, int(svg.attrib["height"]) * 2), pixels=list(image.size))
        check(f"{figure} all node text fits its box", all(p["text_within_box"] and p["font_size"] >= 17 for p in placements[figure]))
    positions = {p["node_id"]: p for p in placements["Figure 1"]}
    check("M2/M3 matched diagram panels aligned", all(all(positions["M2"+suffix][k] == positions["M3"+suffix][k] for k in ["y", "width", "height"]) for suffix in ["U", "V", "ETA", "Y"]))
    for mid, outcome in [("M2", "actrefoutbin"), ("M3", "actrefrecbin")]:
        fit = load(f"outputs/reproduced/models/{mid}_fit.json")
        check(mid + " diagram agrees with saved fitted model", fit["outcome"] == outcome and fit["points_per_random_intercept"] == 7
              and fit["n_observations"] == 3770 and fit["n_items"] == 1183 and fit["n_actor_groups"] == 2453)
    m1 = load("outputs/reproduced/models/ordinal/M1_model.json")
    check("M1 diagram agrees with saved fitted model", m1["input_n"] == 1700 and len(m1["thresholds"]) == 4 and len(m1["parameters"]) == 9)
    broken = []
    for rel in ["docs/model_diagram.md", "docs/variable_dictionary.md", "docs/README.md", "START_HERE.md"]:
        for link in re.findall(r"\]\(([^)]+)\)", (ROOT / rel).read_text(encoding="utf-8")):
            if link.startswith(("http:", "https:")):
                continue
            if not ((ROOT / rel).parent / link.split("#", 1)[0]).resolve().exists():
                broken.append((rel, link))
    check("Reader guide and navigation links resolve", not broken, broken_links=broken)
    protected = load("records/skill_invocations/2026-10-20_design_completion/protected_manifest.json")
    changes = [r["path"] for r in protected if not (ROOT / r["path"]).exists() or sha256((ROOT / r["path"]).read_bytes()).hexdigest() != r["sha256"]]
    check("Existing source, analysis, test and numerical files unchanged", not changes, protected_files=len(protected), changes=changes)
    previous_matrix = RECORD / "previous_versions/docs/hypothesis_matrix.csv"
    check("Completed hypothesis matrix CSV preserved", previous_matrix.read_bytes() == (ROOT / "docs/hypothesis_matrix.csv").read_bytes())
    result = dict(checked_at_utc=datetime.now(timezone.utc).isoformat(),
                  status="passed" if all(c["passed"] for c in checks) else "failed", checks=checks,
                  dictionary_entries=len(dictionary), node_map_entries=len(nodes),
                  research_models_rerun=False, student_review_inferred=False,
                  final_report_read_or_modified=False, github_synchronized=False,
                  mermaid_engine_rendered=False,
                  rendering_scope="SVG and PNG generated from one node registry and drawing operations. Mermaid source structurally checked, no installed Mermaid renderer.")
    (RECORD / "validation.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"status": result["status"], "checks": len(checks), "passed": sum(c["passed"] for c in checks),
                      "dictionary_entries": len(dictionary), "diagram_nodes": len(nodes), "protected_files": len(protected),
                      "failures": [c for c in checks if not c["passed"]]}, indent=2))
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
