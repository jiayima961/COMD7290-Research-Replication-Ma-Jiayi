"""Save source metadata and categorical summaries without exporting subject rows."""
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
import csv
import json
import shutil
import pandas as pd
import pyreadstat

ROOT = Path(__file__).resolve().parents[2]
RECORD = ROOT / "records/skill_invocations/2026-10-20_design_completion"
OUT = ROOT / "outputs/diagnostics/measurement"


def main():
    RECORD.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    changed = ["AGENTS.md", "STATUS.md", "START_HERE.md", "docs/README.md", "docs/variable_dictionary.csv",
               "docs/model_diagram.mmd", "docs/design_and_models.md", "docs/hypothesis_matrix.csv",
               "docs/hypothesis_matrix.md", "docs/analysis_inventory.csv", "docs/assignment_checklist.md",
               "docs/assignment_audit.md", "docs/follow_up.md", "records/agent_records.md", "records/decisions.md",
               "tools/maintenance/complete_hypothesis_matrix.py", "analysis/run_verified_replication.py"]
    for rel in changed:
        dest = RECORD / "previous_versions" / rel
        if (ROOT / rel).exists() and not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, dest)
    baseline = RECORD / "protected_manifest.json"
    if not baseline.exists():
        paths = []
        for folder in ["data/original", "sources", "outputs", "analysis", "tests"]:
            paths.extend(p for p in (ROOT / folder).rglob("*") if p.is_file() and
                         "__pycache__" not in p.parts and p.suffix not in {".png", ".tiff", ".emf"})
        data = [{"path": p.relative_to(ROOT).as_posix(), "sha256": sha256(p.read_bytes()).hexdigest()}
                for p in sorted(paths)]
        baseline.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    audits = []
    summary = []
    frames = {}
    for level, fname in [("item", "MedCon_Civility_item.dta"), ("reference", "MedCon_Civility_actref.dta")]:
        path = ROOT / "data/original" / fname
        d, m = pyreadstat.read_dta(str(path), apply_value_formats=False)
        frames[level] = d
        fields = []
        for name in m.column_names:
            s = d[name]
            nonmissing = s.dropna()
            numeric = m.readstat_variable_types.get(name) != "string"
            if numeric:
                nonmissing = pd.to_numeric(nonmissing, errors="raise")
            entry = {"variable": name, "label": m.column_names_to_labels.get(name),
                     "storage": m.readstat_variable_types.get(name), "format": m.original_variable_types.get(name),
                     "system_missing_n": int(s.isna().sum()), "blank_string_n": int(s.eq("").sum()) if not numeric else 0,
                     "unique_nonmissing_n": int(nonmissing.nunique()),
                     "value_labels": m.variable_value_labels.get(name, {})}
            if numeric:
                entry["min"] = float(nonmissing.min()) if len(nonmissing) else None
                entry["max"] = float(nonmissing.max()) if len(nonmissing) else None
                if nonmissing.nunique() <= 40:
                    entry["observed_numeric_counts"] = {str(k): int(v) for k, v in nonmissing.value_counts().sort_index().items()}
            fields.append(entry)
            summary.append({"dataset": level, **{k: entry[k] for k in ["variable", "label", "storage", "format", "system_missing_n", "blank_string_n", "unique_nonmissing_n"]}})
        audits.append({"dataset": level, "path": path.relative_to(ROOT).as_posix(),
                       "sha256": sha256(path.read_bytes()).hexdigest(), "rows": len(d), "fields": fields,
                       "user_missing_codes_metadata": m.missing_user_values})
    (OUT / "dataset_metadata.json").write_text(json.dumps(audits, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    with (OUT / "field_inventory.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)
    ref, item = frames["reference"], frames["item"]
    origin = ref.resp_akteur_akteur_id.astype(str)
    group = ref.text_id.astype(str) + "_" + ref.akteur_id.astype(str)
    pair = pd.DataFrame({"origin": origin, "group": group})
    semantic = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_hashes": {a["dataset"]: a["sha256"] for a in audits},
        "origin_id_to_model_group_max_unique": int(pair.groupby("origin").group.nunique().max()),
        "model_group_to_origin_id_max_unique": int(pair.groupby("group").origin.nunique().max()),
        "target_id_unique": int(ref.respobj_akteur.nunique()),
        "joint_outrage_recognition_present_n": int(((ref.actrefoutbin == 1) & (ref.actrefrecbin == 1)).sum()),
        "reference_n": len(ref),
        "item_n": len(item),
        "recognition_by_valence": pd.crosstab(ref.valenz_akteur, ref.actrefrecbin).to_dict(),
        "outrage_by_valence": pd.crosstab(ref.valenz_akteur, ref.actrefoutbin).to_dict(),
        "legacy_media_vs_analysis_media": pd.crosstab(item.medientyp, item.mediatype).to_dict(),
        "legacy_media_disagreements_under_expected_1newspaper_2website_3blog": int(
            (item.medientyp.map({1: 2, 2: 3, 3: 1}) != item.mediatype).sum()),
        "legacy_country_vs_analysis_country": pd.crosstab(item.land, item.country).to_dict(),
        "scope": "Aggregate source-description checks only. No data recoding, correction or model fitting.",
    }
    (OUT / "semantic_checks.json").write_text(json.dumps(semantic, indent=2) + "\n", encoding="utf-8")
    selected = {"resp_akteur_akteur", "resp_akteur_akteur_id", "respobj_akteur", "bezug_akteur_level", "bezug_akteur_id",
                "genuinekonstruierte_resp_akteur", "valenz_akteur", "rolle_allgemein", "rolle_pol_land", "rolle_pol_level",
                "rolle_pol_inland_national", "rolle_pol_ausland_national", "herkunft", "parteizugehoerigkeit",
                "religionszugehoerigkeit", "geschlecht", "land", "medientyp", "medientitel", "rubrik",
                "darstellungsform", "laenge", "anfangsseite", "date_published", "mediaoutlet", "tone"}
    print(json.dumps([{ "dataset": a["dataset"], "fields": [f for f in a["fields"] if f["variable"] in selected]}
                      for a in audits], indent=2))


if __name__ == "__main__":
    main()
