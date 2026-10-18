"""Independent raw-data descriptive verification (V1) and safe negative test (N1).

Uses pyreadstat to count raw records directly, without the ordinal implementation
or canonical preparation loader. The preparation recode function is imported
only for a copied synthetic invalid-domain detection and recovery test.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
import time

import pandas as pd
import pyreadstat


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(project_root, output):
    started = time.perf_counter()
    root = Path(project_root).resolve()
    output = Path(output).resolve()
    item_path = root / "data/original/MedCon_Civility_item.dta"
    reference_path = root / "data/original/MedCon_Civility_actref.dta"
    sources = {"item": {"path": str(item_path), "sha256": sha(item_path)},
               "reference": {"path": str(reference_path), "sha256": sha(reference_path)}}

    # Separate raw-file reader and direct Boolean counts; no ordinal helpers.
    item, item_meta = pyreadstat.read_dta(str(item_path), apply_value_formats=False)
    reference, reference_meta = pyreadstat.read_dta(str(reference_path), apply_value_formats=False)
    ref_csv = root / "outputs/reproduced/descriptives/ordinal/reference_descriptives.csv"
    tone_csv = root / "outputs/reproduced/descriptives/ordinal/item_tone_frequencies.csv"
    saved_reference = pd.read_csv(ref_csv)
    saved_tone = pd.read_csv(tone_csv)
    checks = []
    for outcome in ["actrefrecbin", "actrefoutbin"]:
        values = reference[outcome]
        nonmissing = int(values.notna().sum())
        events = int(values.eq(1).sum())
        nonevents = int(values.eq(0).sum())
        proportion = events / nonmissing
        row = saved_reference.loc[(saved_reference.grouping == "overall") &
                                  (saved_reference.outcome == outcome)].iloc[0]
        checks.append({"assignment_check": "V1", "check": f"Direct raw {outcome} counts versus saved descriptive CSV",
                       "reader": "pyreadstat.read_dta; value formats disabled", "raw_n": len(reference),
                       "raw_nonmissing_n": nonmissing, "raw_event_n": events, "raw_nonevent_n": nonevents,
                       "raw_proportion": proportion, "saved_n": int(row.n), "saved_proportion": float(row.estimate),
                       "absolute_difference": abs(proportion-float(row.estimate)),
                       "raw_binary_value_labels": reference_meta.variable_value_labels.get(outcome, {}),
                       "passed": nonmissing == len(reference) == events+nonevents == int(row.n)
                                 and abs(proportion-float(row.estimate)) < 1e-14})

    raw_counts = {str(level-1): int(item.tone.eq(level).sum()) for level in range(1,6)}
    overall = saved_tone.loc[saved_tone.grouping == "overall"]
    saved_counts = {str(int(row.outcome)): int(row.n) for row in overall.itertuples()}
    checks.append({"assignment_check": "V1", "check": "Direct archive tone 1-5 counts versus saved analysis tone 0-4 frequencies",
                   "raw_item_n": len(item), "raw_counts_with_explicit_subtract_one_labels": raw_counts,
                   "saved_counts": saved_counts,
                   "passed": raw_counts == saved_counts and sum(raw_counts.values()) == len(item)})

    # Import the production validator only for this negative test. No research
    # input is changed, and the synthetic original remains available for recovery.
    preparation_path = root / "analysis/prepare_replication.py"
    spec = importlib.util.spec_from_file_location("tested_prepare_replication", preparation_path)
    preparation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(preparation)
    synthetic_original = pd.DataFrame({"polsys": [1,2,3], "socdiv": [1,2,1], "mediatype": [1,2,3]})
    unchanged_copy = synthetic_original.copy(deep=True)
    invalid_copy = synthetic_original.copy(deep=True)
    invalid_copy.loc[1,"polsys"] = 77
    detected = False
    exception = None
    try:
        preparation.recode(invalid_copy)
    except ValueError as exc:
        detected = True
        exception = str(exc)
    recovered = preparation.recode(synthetic_original.copy(deep=True))
    expected = pd.DataFrame({"polsys": [1,3,2], "socdiv": [2,1,2], "mediatype": [1,3,2]})
    recovery_ok = recovered.equals(expected)
    synthetic_original_unchanged = synthetic_original.equals(unchanged_copy)
    checks.append({"assignment_check": "N1", "check": "Production recode rejects a synthetic copied invalid domain, then recovers from untouched synthetic original",
                   "tested_function": "analysis.prepare_replication.recode", "tested_script_sha256": sha(preparation_path),
                   "injected_error": {"copy_row_zero_based": 1, "variable": "polsys", "invalid_value": 77},
                   "detected": detected, "exception_type": "ValueError" if detected else None,
                   "exception_message": exception, "recovery_matches_explicit_source_recode": recovery_ok,
                   "synthetic_original_unchanged": synthetic_original_unchanged,
                   "actual_recovered_values": recovered.to_dict(orient="list"),
                   "expected_recovered_values": expected.to_dict(orient="list"),
                   "passed": detected and recovery_ok and synthetic_original_unchanged})

    originals_unchanged = {name: sha(Path(details["path"])) == details["sha256"] for name,details in sources.items()}
    all_passed = all(check["passed"] for check in checks) and all(originals_unchanged.values())
    result = {"purpose": "V1 independent direct raw-data descriptive check; N1 harmless invalid-domain detection and recovery",
              "timestamp_utc": datetime.now(timezone.utc).isoformat(), "script": str(Path(__file__).resolve()),
              "script_sha256": sha(Path(__file__).resolve()), "command": [sys.executable, str(Path(__file__).resolve()),
                       "--project-root", str(root), "--output", str(output)],
              "runtime_seconds": time.perf_counter()-started, "python": platform.python_version(),
              "packages": {"pandas":pd.__version__, "pyreadstat":pyreadstat.__version__},
              "source_bindings": sources,
              "comparison_bindings": [{"path":str(path),"sha256":sha(path)} for path in [ref_csv,tone_csv]],
              "original_file_hashes_unchanged": originals_unchanged, "checks": checks,
              "all_passed": all_passed, "ordinal_implementation_imported": False,
              "research_models_rerun": False, "original_inputs_modified": False}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"all_passed":all_passed,"checks":len(checks),
                      "recognition": f"{checks[0]['raw_event_n']}/{checks[0]['raw_nonmissing_n']}",
                      "outrage": f"{checks[1]['raw_event_n']}/{checks[1]['raw_nonmissing_n']}",
                      "negative_test_detected":detected,"recovery_passed":recovery_ok,"output":str(output)},indent=2))
    if not all_passed:
        raise SystemExit(1)
    return result


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root",type=Path,default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output",type=Path)
    arguments=parser.parse_args()
    run(arguments.project_root,arguments.output or arguments.project_root/"outputs/diagnostics/data_independent_checks.json")
