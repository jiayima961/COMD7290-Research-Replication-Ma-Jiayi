"""Prepare unchanged-author-data analyses with explicit domains and sample provenance."""
from pathlib import Path
from hashlib import sha256
import csv
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SPEC_VERSION = "source-faithful-python-1.0.0"
TERMS = ["intercept", "mixed_vs_consensus", "majoritarian_vs_consensus",
         "contested_vs_stable", "website_vs_blog", "newspaper_vs_blog"]

def design(frame, intercept=True):
    x = np.column_stack([np.ones(len(frame)), frame.polsys.eq(2), frame.polsys.eq(3),
                         frame.socdiv.eq(2), frame.mediatype.eq(2), frame.mediatype.eq(3)]).astype(float)
    return x if intercept else x[:, 1:]

def recode(frame):
    d = frame.copy()
    for name, domain in {"polsys": {1, 2, 3}, "socdiv": {1, 2}, "mediatype": {1, 2, 3}}.items():
        if d[name].isna().any() or not set(d[name].unique()).issubset(domain):
            raise ValueError(f"Invalid original values in {name}; stop before recoding.")
    d["polsys"] = d.polsys.map({1: 1, 2: 3, 3: 2})
    d["socdiv"] = d.socdiv.map({1: 2, 2: 1})
    d["mediatype"] = d.mediatype.map({1: 1, 2: 3, 3: 2})
    return d

def load_data(root=ROOT):
    root = Path(root)
    item = pd.read_stata(root / "data/original/MedCon_Civility_item.dta", convert_categoricals=False)
    ref = pd.read_stata(root / "data/original/MedCon_Civility_actref.dta", convert_categoricals=False)
    if item.text_idx.isna().any() or item.text_idx.duplicated().any() or item.text_id.duplicated().any():
        raise ValueError("Missing or duplicate original item identifier.")
    if ref.actref_idx.isna().any() or ref.actref_idx.duplicated().any():
        raise ValueError("Missing or duplicate directed-reference identifier.")
    linked=ref.merge(item[['text_idx','text_id','polsys','socdiv','mediatype','country']],on='text_idx',how='left',suffixes=('','_item'),validate='many_to_one',indicator=True)
    if not linked['_merge'].eq('both').all():
        raise ValueError("Reference links to an absent analytical item.")
    for field in ['text_id','polsys','socdiv','mediatype','country']:
        if not linked[field].eq(linked[field+'_item']).all():
            raise ValueError(f"Cross-file item/reference mismatch: {field}")
    if item.tone.isna().any() or not set(item.tone.unique()).issubset({1, 2, 3, 4, 5}):
        raise ValueError("Invalid original ordinal tone domain.")
    item = recode(item)
    item["tone"] = item.tone.astype(int) - 1
    ref = recode(ref)
    for y in ["actrefoutbin", "actrefrecbin"]:
        if ref[y].isna().any() or not set(ref[y].unique()).issubset({0, 1}):
            raise ValueError(f"Invalid Bernoulli outcome {y}.")
    if ref[["text_id", "akteur_id"]].isna().any().any():
        raise ValueError("Missing grouping identifier.")
    ref["act_id"] = ref.text_id.astype(str) + "_" + ref.akteur_id.astype(str)
    if ref.groupby("act_id", observed=True).text_id.nunique().max() != 1:
        raise ValueError("Concatenated actor identifier collision.")
    for v in ["polsys", "socdiv", "mediatype", "country"]:
        if ref.groupby("text_id", observed=True)[v].nunique().max() != 1:
            raise ValueError(f"Within-item context inconsistency: {v}")
    if np.linalg.matrix_rank(design(ref)) != 6 or np.linalg.matrix_rank(design(item, False)) != 5:
        raise ValueError("Main-model design matrix is rank deficient.")
    return item, ref

def prepare(root=ROOT):
    root = Path(root)
    item, ref = load_data(root)
    originals = []
    with (root / "records/source_manifest.csv").open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if row["local_path"] and row["sha256"]:
                p = root / row["local_path"]
                value = sha256(p.read_bytes()).hexdigest()
                originals.append({"path": row["local_path"], "sha256": value, "matches_manifest": value == row["sha256"]})
    if not all(r["matches_manifest"] for r in originals):
        raise ValueError("Original-file hash mismatch.")
    out = root / "data/prepared"
    out.mkdir(parents=True, exist_ok=True)
    ip = out / "item_analysis.csv"
    rp = out / "reference_analysis.csv"
    item[["text_idx", "text_id", "tone", "polsys", "socdiv", "mediatype", "country"]].to_csv(ip, index=False)
    columns = ["text_id", "akteur_id", "act_id", "actrefoutbin", "actrefrecbin", "polsys", "socdiv", "mediatype", "country"]
    if "actref_idx" in ref.columns: columns.insert(0, "actref_idx")
    ref[columns].to_csv(rp, index=False)
    groups = ref.groupby(["text_id", "akteur_id"], observed=True).size()
    audit = {"specification_version": SPEC_VERSION, "item_rows": len(item), "reference_rows": len(ref),
             "reference_items": ref.text_id.nunique(), "within_item_actor_groups": len(groups),
             "exclusions": 0, "exclusion_reason": "No missing/invalid required main-model fields in supplied analytical data",
             "identifier_checks": "Unique item and reference keys; all references join many-to-one to an item; context and text IDs agree across files",
             "actor_group_max_size": int(groups.max()), "item_group_max_size": int(ref.groupby("text_id").size().max()),
             "item_tone_counts": {str(k): int(v) for k, v in item.tone.value_counts().sort_index().items()},
             "reference_outcome_events": {y: int(ref[y].sum()) for y in ["actrefoutbin", "actrefrecbin"]},
             "reference_key_fields": [v for v in ref.columns if "idx" in v or "refobj" in v],
             "original_files": originals, "prepared_files": [{"path": str(p.relative_to(root)), "sha256": sha256(p.read_bytes()).hexdigest()} for p in [ip, rp]],
             "important_limit": "Supplied DTA files are already author-prepared consensus analytical inputs; upstream contradictory codebook numbering is not silently reconstructed."}
    dest = root / "outputs/diagnostics/data_audit.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(audit, indent=2, default=int) + "\n", encoding="utf-8")
    return audit

if __name__ == "__main__":
    print(json.dumps(prepare(), indent=2, default=int))
