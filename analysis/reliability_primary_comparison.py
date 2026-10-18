"""Post-fit comparison with an archived author website, kept separate from fitting."""
from __future__ import annotations
import argparse
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
import pandas as pd


class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables, self.table, self.row, self.cell = [], None, None, None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.table = []
        elif tag == "tr" and self.table is not None:
            self.row = []
        elif tag in ("th", "td") and self.row is not None:
            self.cell = ""

    def handle_data(self, data):
        if self.cell is not None:
            self.cell += data

    def handle_endtag(self, tag):
        if tag in ("th", "td") and self.cell is not None:
            self.row.append(" ".join(self.cell.split()))
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.table.append(self.row)
            self.row = None
        elif tag == "table" and self.table is not None:
            self.tables.append(self.table)
            self.table = None


def main(snapshot: Path, results: Path, diagnostics: Path | None = None, published: Path | None = None, log_root: Path | None = None):
    diagnostics = diagnostics or results
    published = published or results
    log_root = log_root or results
    published.mkdir(parents=True, exist_ok=True)
    log_root.mkdir(parents=True, exist_ok=True)
    parser = TableParser()
    parser.feed(snapshot.read_text(encoding="utf-8"))
    raw = parser.tables
    tone = next(table for table in raw if "Tone (item level)" in table[0])
    actor = next(table for table in raw if "Valence (actor reference level)" in table[0])
    rows = ["percent_agreement", "brennan_prediger", "cohen_conger_kappa", "scott_fleiss", "gwet_ac1", "krippendorff_alpha"]
    current = pd.read_csv(results / "reliability_coefficients.csv")
    audit = json.loads((diagnostics / "sample_audit.json").read_text(encoding="utf-8"))
    comparisons = []
    for outcome, table, col in [("tone", tone, 1), ("valence", actor, 1), ("recognition", actor, 2), ("outrage", actor, 3), ("responsiveness", actor, 4)]:
        for i, coef in enumerate(rows, start=1):
            published_value = float(table[i][col])
            selected = current[(current.outcome == outcome) & (current.selection == "two_slots") & (current.coefficient == coef)].iloc[0]
            computed = float(selected.estimate)
            comparisons.append({"analysis_id": selected.analysis_id, "outcome": outcome, "coefficient": coef,
                                "published_display": table[i][col], "published_numeric": published_value,
                                "computed_estimate": computed, "computed_rounded_2dp": round(computed, 2),
                                "difference_from_displayed_number": computed - published_value,
                                "matches_displayed_precision": abs(round(computed, 2) - published_value) < 1e-12,
                                "published_n_any_rating": int(table[7][col].replace(",", "")),
                                "computed_n_any_rating": audit[selected.analysis_id]["n_any_rating"],
                                "source_url": "https://medcon-doc.github.io/documentation/content-analysis/reliabilities/",
                                "source_locator": "Final Inter-Coder Reliability; first/second coder main-stage table",
                                "comparison_scope": "Two positional slots; the primary page does not publish all-slot estimates or SEs."})
    comparison = pd.DataFrame(comparisons)
    comparison.to_csv(results / "primary_website_comparison.csv", index=False)
    targets = comparison[["outcome", "coefficient", "published_display", "published_numeric", "published_n_any_rating", "source_url", "source_locator"]].copy()
    targets.to_csv(published / "official_website_targets.csv", index=False)
    assert comparison.matches_displayed_precision.all()
    assert (comparison.published_n_any_rating == comparison.computed_n_any_rating).all()
    evidence = {"status": "30_of_30_coefficients_match_primary_website_at_displayed_two_decimal_precision",
                "source_snapshot": str(snapshot.resolve()), "snapshot_sha256": hashlib.sha256(snapshot.read_bytes()).hexdigest(),
                "source_url": "https://medcon-doc.github.io/documentation/content-analysis/reliabilities/",
                "timing": "Source table retrieved only after independent implementation and actual fitting completed.",
                "source_tables_parsed": 2, "coefficient_targets": len(comparison),
                "sample_count_targets": 5, "sample_count_matches": 5,
                "se_or_interval_targets_available": False, "all_slot_targets_available": False,
                "original_software_build_equivalence": "not established"}
    (log_root / "primary_comparison_receipt.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(evidence["status"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--snapshot", type=Path, required=True)
    p.add_argument("--results", type=Path, required=True)
    p.add_argument("--diagnostics", type=Path)
    p.add_argument("--published", type=Path)
    p.add_argument("--log-root", type=Path)
    a = p.parse_args()
    main(a.snapshot, a.results, a.diagnostics, a.published, a.log_root)
