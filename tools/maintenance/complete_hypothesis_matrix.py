"""Complete the retrospective evidence map from saved specifications and results.

This task does not estimate models, change results, or supply student approval.
Run with --check to validate the current matrix without rewriting it.
"""
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
import argparse
import csv
import json
import math
import re
import shutil

ROOT = Path(__file__).resolve().parents[2]
RECORD = ROOT / "records/skill_invocations/2026-10-20_specify-empirical-study_matrix"
CSV = "docs/hypothesis_matrix.csv"
GUIDE = "docs/hypothesis_matrix.md"
MODEL_CODE = "sources/author_code/MedCon_Civility_an.do"
LEDGER = "outputs/verification/comparison_all.csv"
BASE_SPEC = "source-faithful-python-1.0.0"
ORD_SPEC = "ordinal-author-code-2021-python-forward-v1"
REL_SPEC = "author-reliability-2020-11-01__identity-conditional__python-v1"
MATRIX_VERSION = "executed-evidence-matrix-2026-10-20-v1"


def rows(path):
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def snapshot():
    RECORD.mkdir(parents=True, exist_ok=True)
    for rel in [CSV, "docs/README.md", "docs/assignment_checklist.md",
                "docs/assignment_audit.md", "records/agent_records.md"]:
        dest = RECORD / "previous_versions" / rel
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, dest)
    target = RECORD / "protected_manifest.json"
    if not target.exists():
        old = load("records/skill_invocations/2026-10-19_verify-and-package/baseline_manifest.json")
        paths = {entry["path"] for entry in old}
        paths.update(p.relative_to(ROOT).as_posix() for folder in ["analysis", "tests"]
                     for p in (ROOT / folder).rglob("*.py"))
        paths.update(r["local_path"] for r in rows("records/source_manifest.csv")
                     if r["local_path"] and (ROOT / r["local_path"]).is_file())
        write_json(target, [{"path": p, "sha256": digest(ROOT / p)} for p in sorted(paths)])


ITEM = ("Purposive six-country comparison of mediated discourse about religion in public life, "
        "August 2015-July 2016. Australia, Germany, Lebanon, Switzerland, Turkey and USA. "
        "N=1700 items from selected newspapers, websites and political blogs, not a probability sample of all media.")
REF = ITEM + " Reference analysis uses 3770 directed references in 2453 originating actor/statement groups in 1183 items."
ITEM_UNIT = "One news item. M1 treats items as independent likelihood units. Country conditions are shared fixed categories, not fitted random effects."
REF_UNIT = "One directed reference nested in an originating actor/statement group within an item. act_id=text_id plus akteur_id. Different directions are different references."
X = "X=(I(polsys=2), I(polsys=3), I(socdiv=2), I(mediatype=2), I(mediatype=3))"
CODING = ("Author recodes polsys raw 1/2/3 to 1/3/2, socdiv raw 1/2 to 2/1, "
          "mediatype raw 1/2/3 to 1/3/2. Analysis bases are consensus=1, stable secularism=1 and blog=1. "
          "Required fields have no missing values. Invalid categories stop preparation. No weights or imputation.")
ORD_EQ = "logit Pr(tone_i>k)=X_i beta-c_k for k=0,1,2,3, with c_0<c_1<c_2<c_3 and no separate free intercept. " + X
BIN_EQ = ("logit Pr(Y_raj=1|u_j,v_aj)=beta0+X_j beta+u_j+v_aj. "
          "u_j~N(0,sigma_item^2), v_aj~N(0,sigma_actor^2), mutually independent. " + X)
ORD_EST = ("Unweighted multinomial maximum likelihood, five common slopes and four ordered cutpoints. "
           "Python BFGS with analytic score/information, gtol=1e-9 and maxiter=1200, trust-exact refinement when needed. "
           "Observed-information covariance. Optimizer settings are implementation choices, not recovered Stata defaults.")
BIN_EST = ("Separate frequentist Bernoulli marginal ML models with two Gaussian random intercepts. "
           "Author intpoints(7). Python recursive mean/variance adaptive Gauss-Hermite, seven nodes per dimension, "
           "BFGS search/refinement and numerical observed-information covariance. "
           "Original Stata internal grid/build and optimizer tolerances were not pinned.")
ORD_DIAG = ("Proportional odds and independent item likelihood, finite ordered thresholds, valid category probabilities, "
            "small score and full-rank information. Normal two-sided 95% Wald intervals. C1 tests and C2 links retained. "
            "Only six national contexts, so this does not identify an institutional causal effect.")
BIN_DIAG = ("Conditional independence given independent Gaussian random intercepts, correct nesting and binary coding. "
            "Normal two-sided 95% Wald intervals, gradient/information checks, fixed-parameter independent integration "
            "and higher-node comparisons. Historical finite-seven-node equality remains unconfirmed.")
REVIEW = "Execution authorized by D011. This retrospective documentation update is requested on 2026-10-20. Final student scientific interpretation remains pending."


def versions(kind):
    paths = {"item": ["data/original/MedCon_Civility_item.dta"],
             "ref": ["data/original/MedCon_Civility_actref.dta"],
             "tone": ["data/original/independent_ratings_tone.xlsx"],
             "ratings": ["data/original/independent_ratings_actor_reference.xlsx"]}
    selected = paths.get(kind, paths["item"] + paths["ref"])
    spec = REL_SPEC if kind in {"tone", "ratings"} else ORD_SPEC if kind == "item" else BASE_SPEC
    return " | ".join([f"{p} SHA256={digest(ROOT / p)}" for p in selected] +
                      [f"spec={spec}", f"matrix={MATRIX_VERSION}", "source hashes in records/source_manifest.csv, environment in requirements-lock.txt"])


def result_text(r):
    return " | ".join(f"{label}={float(r[field]):.12g}" for label, field in
                      [("b", "estimate"), ("SE", "se"), ("OR", "odds_ratio"),
                       ("p", "p_value"), ("OR_CI95_lower", "or_ci95_lower" if "or_ci95_lower" in r else "or_ci_lower"),
                       ("OR_CI95_upper", "or_ci95_upper" if "or_ci95_upper" in r else "or_ci_upper")])


def main_rows(old):
    targets = {(r["model_id"], r["contrast"]): r for r in rows("outputs/published/model_targets.csv")}
    tests = {(r["model_id"], r["hypothesis_id"], r["contrast"]): r for r in rows("outputs/reproduced/hypothesis_tests.csv")}
    coefficients = {"M1": {r["term"]: r for r in rows("outputs/reproduced/models/ordinal/ordinal_coefficients.csv") if r["analysis_id"] == "M1"}}
    for mid in ["M2", "M3"]:
        coefficients[mid] = {r["term"]: r for r in rows(f"outputs/reproduced/models/{mid}_coefficients.csv")}
    terms = {"mixed": "2.polsys", "majoritarian": "3.polsys", "contested": "2.socdiv",
             "website": "2.mediatype", "newspaper": "3.mediatype"}
    contrasts = {"mixed": "mixed_vs_consensus", "majoritarian": "majoritarian_vs_consensus",
                 "contested": "contested_vs_stable", "website": "website_vs_blog", "newspaper": "newspaper_vs_blog"}
    premises = {
        "H1a": "Majoritarian concentration of power makes compromise less necessary, whereas consensus power sharing encourages accommodation. Proposed process, not a measured mediator.",
        "H1b": "Consensus power sharing makes accommodation and recognition of legitimate opponents more necessary. Proposed process, not a measured mediator.",
        "H2a": "Contested secularism heightens identity boundaries and social distance, which may encourage hostile communication. Proposed process, not a measured mediator.",
        "H2b": "Social segmentation and social distance in contested-secularism societies may inhibit constructive recognition across group boundaries. Proposed process, not a measured mediator.",
        "H3a": "Professional norms, editorial oversight and gatekeeping may restrain outrage compared with political blogs. These processes are not directly measured.",
        "H3b": "Professional news production may encourage respectful treatment and recognition compared with political blogs. These processes are not directly measured.",
    }
    new = []
    for oldrow in [r for r in old if r["analysis_id"] in {"M1", "M2", "M3"}]:
        mid, hid = oldrow["analysis_id"], oldrow["hypothesis_id"]
        contrast = next(c for c in ["majoritarian", "contested", "website", "newspaper"] if oldrow["predicted_relationship"].startswith(c))
        test = tests[mid, hid, contrast]
        sign = int(test["predicted_sign"])
        coef = coefficients[mid][terms[contrast] if mid == "M1" else contrasts[contrast]]
        row = dict(oldrow)
        row.update(row_id=f"{mid}_{hid}_{contrasts[contrast]}", comparison_key=contrasts[contrast],
                   theoretical_premise_mechanism=premises[hid],
                   source_locator=f"Article hypothesis {hid}, {'Table 3' if mid == 'M1' else 'Table 4'}. Author Analysis {'2' if mid == 'M1' else '4'} in {MODEL_CODE}",
                   status_confirmatory_exploratory="Author-stated directional hypothesis. Retrospective replication with results already known, not preregistered.",
                   predicted_relationship=f"{contrasts[contrast]} slope {'>0 and OR>1' if sign > 0 else '<0 and OR<1'} for {'ordinal tone' if mid == 'M1' else 'explicit outrage' if mid == 'M2' else 'explicit recognition'}.",
                   population_sampling=ITEM if mid == "M1" else REF,
                   coding_unit_dependence=ITEM_UNIT if mid == "M1" else REF_UNIT,
                   constructs_indicators=("Item outrage=tone, ordinal 0 no outrage to 4 very strong outrage. " if mid == "M1" else
                       f"{'Outrage=actrefoutbin' if mid == 'M2' else 'Recognition=actrefrecbin'}, binary 0 absent, 1 explicit presence. ") + "Predictors polsys, socdiv and mediatype enter jointly as five indicators.",
                   measurement_coding_missing=("tone=archive tone-1. " if mid == "M1" else "Author-prepared outcome retained as 0/1. No consensus codes used for reliability. ") + CODING,
                   estimand_parameter_contrast=f"beta for {contrasts[contrast]}, holding other modeled predictors constant. exp(beta) is {'a common cumulative odds ratio across four thresholds' if mid == 'M1' else 'a conditional odds ratio given both random intercepts'}. It is not a probability ratio or percentage-point change.",
                   equation_syntax=(ORD_EQ if mid == "M1" else BIN_EQ + f" Y={'actrefoutbin' if mid == 'M2' else 'actrefrecbin'}."),
                   estimator_settings=ORD_EST if mid == "M1" else BIN_EST,
                   assumptions_intervals_diagnostics=ORD_DIAG if mid == "M1" else BIN_DIAG,
                   published_rule="Retain original predicted sign and reported two-sided Wald uncertainty. Consistent with prediction only when direction agrees and p<.05. Non-significance does not prove zero association. No test of an unmeasured mechanism.",
                   dataset_spec_versions=versions("item" if mid == "M1" else "ref"),
                   script_path="analysis/ordinal_reproduction.py | analysis/compare_replication.py" if mid == "M1" else "analysis/run_binary_models.py | analysis/nested_logit.py | analysis/compare_replication.py",
                   output_path=("outputs/reproduced/hypothesis_tests.csv | outputs/reproduced/models/ordinal/ordinal_coefficients.csv | outputs/reproduced/models/ordinal/M1_model.json" if mid == "M1" else f"outputs/reproduced/hypothesis_tests.csv | outputs/reproduced/models/{mid}_coefficients.csv | outputs/reproduced/models/{mid}_fit.json"),
                   published_values_path="outputs/published/model_targets.csv",
                   reproduced_values=result_text(coef),
                   discrepancy="All published b/SE/OR cells for this contrast agree at displayed precision. See outputs/verification/comparison_all.csv. " + ("M1 fit-label/diagnostic and margin differences are documented in C1/P1." if mid == "M1" else "Historical integration details remain incompletely recovered. M2 mixed-OR and fit discrepancy belong to the additional comparison/C3, not this directional target."),
                   scientific_conclusion=test["conclusion"] + ". Observational association only, without causal or mediator identification.",
                   diagnostic_path="outputs/diagnostics/ordinal/findings.md | outputs/diagnostics/ordinal/implementation_checks.json" if mid == "M1" else "outputs/diagnostics/glmm/acceptance_review.md | outputs/diagnostics/glmm/candidate_comparison.csv",
                   approval_status=REVIEW)
        pub = targets[mid, contrast]
        row["published_values"] = f"b={pub['b']} | SE={pub['se']} | OR={pub['odds_ratio']} | reported p={pub['p_reported']}. Transcribed comparison targets, not estimates generated here."
        new.append(row)
    for mid in ["M1", "M2", "M3"]:
        row = next(r.copy() for r in new if r["analysis_id"] == mid)
        coef = coefficients[mid][terms["mixed"] if mid == "M1" else contrasts["mixed"]]
        pub = targets[mid, "mixed"]
        row.update(row_id=f"{mid}_additional_mixed_vs_consensus", hypothesis_id="not-numbered",
                   comparison_key="mixed_vs_consensus", status_confirmatory_exploratory="Additional published comparison, not a directional H1a/H1b test.",
                   source_locator=f"Article {'Table 3' if mid == 'M1' else 'Table 4'}, mixed versus consensus. Author Analysis {'2' if mid == 'M1' else '4'} in {MODEL_CODE}",
                   theoretical_premise_mechanism="Mixed institutions combine features of the two system types. The article does not hypothesize a required intermediate position or a directional mixed-system contrast.",
                   predicted_relationship="No original directional prediction for mixed versus consensus. Do not infer mixed versus majoritarian without a separate direct contrast and uncertainty.",
                   estimand_parameter_contrast="beta_mixed versus consensus, adjusted for socio-cultural division and media type. " + ("Common cumulative log odds and OR." if mid == "M1" else "Conditional log odds and OR given both random intercepts."),
                   published_rule="Report the coefficient and two-sided 95% interval as an additional comparison. Never count this comparison as support for H1a or H1b.",
                   published_values=f"b={pub['b']} | SE={pub['se']} | OR={pub['odds_ratio']} | reported p={pub['p_reported']}.",
                   reproduced_values=result_text(coef),
                   discrepancy=("b and SE agree. OR=2.246459 rounds to 2.25 rather than the printed 2.24. Historical finite-grid/rounding origin is unresolved, not a demonstrated typo." if mid == "M2" else "Published b/SE/OR agree at displayed precision."),
                   scientific_conclusion=("Mixed systems have higher item-level outrage than consensus in M1. This additional association is not H1a support and loses statistical significance under the original probit check." if mid == "M1" else "No statistically significant mixed-versus-consensus association detected. This is neither equality proof nor a directional hypothesis test."))
        new.append(row)
    return new


def supporting_rows(old):
    result = []

    def add(identifier, kind, claim, prediction, indicators, coding, estimand, equation, estimator, assumptions,
            rule, script, output, diagnostics, published, reproduced, discrepancy, conclusion, source, population=None, unit=None):
        row = next(r.copy() for r in old if r["analysis_id"] == identifier)
        row.update(row_id=identifier, comparison_key="multiple_saved_subtargets", hypothesis_id="not-numbered",
                   source_locator=source, status_confirmatory_exploratory=kind,
                   theoretical_premise_mechanism=claim, predicted_relationship=prediction,
                   population_sampling=population or ITEM, coding_unit_dependence=unit or ITEM_UNIT,
                   constructs_indicators=indicators, measurement_coding_missing=coding,
                   estimand_parameter_contrast=estimand, equation_syntax=equation,
                   estimator_settings=estimator, assumptions_intervals_diagnostics=assumptions,
                   published_rule=rule, dataset_spec_versions=versions("tone" if identifier == "R1" else "ratings" if identifier == "R2" else "ref" if identifier in {"D2", "C3", "P2"} else "both" if identifier in {"A1", "V1", "N1"} else "item"),
                   script_path=script, output_path=output, diagnostic_path=diagnostics,
                   published_values_path="outputs/reproduced/reliability/primary_website_comparison.csv" if identifier in {"R1", "R2"} else LEDGER if identifier not in {"V1", "N1", "S1"} else "Not applicable. Assignment-added check has no original numerical target.",
                   published_values=published, reproduced_values=reproduced, discrepancy=discrepancy,
                   scientific_conclusion=conclusion, approval_status=REVIEW if identifier != "S1" else "D013 authorized the separate sensitivity execution. Student acceptance and the specification-sensitivity wording decision remain pending.")
        result.append(row)

    add("D1", "Original descriptive analysis, not a directional hypothesis test.",
        "Describe the prevalence and intensity of item-level outrage before interpreting adjusted institutional and media associations.",
        "No directional hypothesis tested by an unadjusted frequency table or mean.",
        "tone ordinal 0-4, country nominal, mediatype nominal. Counts, mean, sample SD, range and five category percentages, overall and by country/media/country-by-media.",
        "tone=archive tone-1. " + CODING, "n_g, mean(tone|g), sample SD and Pr(tone=k|g), k=0..4, including zero cells.",
        "n_gk=sum I(group=g,tone=k). percent_gk=100*n_gk/n_g. mean_g=sum tone/n_g, sample variance denominator n_g-1.",
        "Unweighted finite-sample arithmetic on all 1700 valid items. No inferential intervals requested by the original summary commands.",
        "Check denominators, recodes, explicit zeros and total percentages. Descriptive means do not turn ordinal tone into a continuous regression outcome.",
        "Compare every printed Table 2 cell at its displayed precision. Keep unprinted summary/graph quantities unverified rather than treating them as matching.",
        "analysis/ordinal_reproduction.py",
        "outputs/reproduced/descriptives/ordinal/item_descriptives.csv | outputs/reproduced/descriptives/ordinal/item_tone_frequencies.csv | outputs/reproduced/descriptives/ordinal/item_tone_counts_country_media.csv | outputs/reproduced/descriptives/ordinal/item_tone_percent_country_media.csv",
        "outputs/diagnostics/ordinal/sample_audit.json | outputs/verification/independent_checks/checks.json",
        "Table 2 prints Australian website moderate outrage 11%. Published item N=1700. Full cell values in comparison ledger.",
        "N=1700, tone counts 0/1/2/3/4 = 1491/159/28/17/5. Mean=0.168235294118. Australian website moderate outrage=1%.",
        "125 of 126 printed Table 2 numeric cells agree. Australian website moderate 11% versus 1%, with the printed row summing to 110%, supports a reporting error.",
        "Outrage is uncommon and high-intensity tone is rare. Summaries describe the selected corpus, without a causal or hypothesis-level conclusion.",
        f"Article Table 2 and item descriptive Results. {MODEL_CODE}, Analysis 1 sum/bysort commands.")
    add("D2", "Original reference-level descriptive analysis.",
        "Separate explicit negative outrage from positive recognition. Absence of one does not establish presence of the other.",
        "No adjusted or directional hypothesis test from raw proportions.",
        "actrefoutbin and actrefrecbin, each binary 0 absent/1 present. Overall, country, media and country-by-media counts and proportions.",
        "Author-prepared binary outcomes unchanged. " + CODING,
        "Reference-weighted event count and mean of each 0/1 outcome within each reported group, not a proportion of articles or people.",
        "p_g=sum Y_r/n_g. Descriptive SD uses n_g-1. Calculate separately for outrage and recognition.",
        "Unweighted summaries of 3770 references. No original inferential interval for these summary commands.",
        "Keep reference, actor/statement and item denominators distinct. Nesting remains relevant for later inference, not an independence claim for descriptive arithmetic.",
        "Compare printed Results percentages at their precision. Do not read precise numeric values from graph pixels or equate raw country rankings with adjusted coefficients.",
        "analysis/ordinal_reproduction.py", "outputs/reproduced/descriptives/ordinal/reference_descriptives.csv",
        "outputs/diagnostics/data_audit.json | outputs/diagnostics/data_independent_checks.json",
        "Printed overall outrage=5.1% and recognition=5.2%. Country/media numerical targets are in the ledger.",
        "Outrage 192/3770=5.09283819629%. Recognition 196/3770=5.19893899204%. All 20 printed reference descriptive percentages agree at display precision.",
        "The Discussion recognition country ranking conflicts with raw Results proportions. Exact full graph probability values were not published.",
        "The two discourse measures have low overall prevalence. Keep raw descriptions separate from adjusted tests and recognition across versus within groups.",
        f"Article reference-level Results and descriptive Figure 2. {MODEL_CODE}, Analysis 3.", REF, REF_UNIT)

    rel_common = ("Six coefficients with identity weights, including for ordinal tone. Percent agreement, Brennan-Prediger, Cohen/Conger kappa, Scott/Fleiss, Gwet AC1 and Krippendorff alpha. "
                  "Conditional-on-rating-slot SE, Student-t 95% intervals, probabilistic Landis-Koch benchmarking. Two selected slots and all author-selected slots estimated separately.")
    rel_eq = ("Observed pair agreement p_a and method-specific expected agreement p_e yield chance-corrected (p_a-p_e)/(1-p_e), "
              "with the original method-specific alpha correction and Gwet chance rule. Exact formulas and conditional influence functions in analysis/reliability_reproduction.py coefficients().")
    for identifier, outcome, selection, pop, unit, values, mismatch in [
        ("R1", "Tone", "Ton_1/Ton_2 and Ton_1..Ton_4", "Original independent tone workbook, ton_codes sheet, author A1:J1701 import, 1700 rated news items.", "Rated news item with positional independent-rating slots, before consensus adjudication.",
         "Two-slot percent agreement=0.939376103590, alpha=0.740608396082. All six published tone coefficients and sample count match display precision. Full exact values are in reliability_coefficients.csv.",
         "Historical installed kappaetc build unpinned. Identity weighting is faithfully retained, not silently replaced by ordinal-distance weights. Published SE/all-slot targets are absent."),
        ("R2", "Reference valence, recognition, outrage and responsiveness", "Outcome-specific first two slots and all 14 fields, except responsiveness first five Q/AG/AW/BM/CC", "Original independent actor-reference rating workbook, matched sheet, author A1:HQ3865 import. Use outcome-specific valid rated subjects and saved sample audits rather than the final 3770-reference analytical denominator.", "Matched directed-reference rating subject with positional rater slots, before consensus adjudication.",
         "All 24 published first/second-slot reference coefficients and four sample counts match display precision. Exact outcome/selection-specific N, SE and intervals are in reliability_coefficients.csv.",
         "Some matched rows repeat a named human across positional slots. Matching and independence limitations are recorded. Historical benchmark build and all-slot/SE publication targets are unavailable.")]:
        add(identifier, "Original measurement reliability analysis.",
            "Independent coding agreement evaluates consistency of operational measurement, not truth of a substantive causal hypothesis.",
            "No directional institutional/media prediction. Assess original agreement measures and uncertainty without a newly invented pass threshold.",
            outcome + ". " + selection + ". " + rel_common,
            "Use original independent rating values, never final consensus codes. Blank/NaN ratings omitted according to the original coefficient rules, empty subjects removed and singletons handled method-specifically. Numeric -99 retained as a category because the author does not declare it missing. Exact columns in column_audit.csv.",
            "Each outcome/slot-selection agreement coefficient, observed/expected agreement, subject N, conditional SE/95% interval and benchmark-category probabilities.",
            rel_eq, rel_common + f" Source specification {REL_SPEC}. Recovered kappaetc 2.1.0 source translation, both historical/current benchmark variants saved.",
            "Check slot selections, missingness, matching/repeated humans, singleton influence rules, known answers and independent implementations. Conditional uncertainty pertains to the retained author rating matrix.",
            "Compare the primary website's first/second-slot six coefficients and N at their printed precision. Interpret coefficients with original probabilistic benchmarking. Unpublished uncertainty is not declared matched.",
            "analysis/reliability_reproduction.py | analysis/reliability_primary_comparison.py",
            "outputs/reproduced/reliability/reliability_coefficients.csv | outputs/reproduced/reliability/probabilistic_benchmarks.csv | outputs/reproduced/reliability/primary_website_comparison.csv",
            "outputs/diagnostics/reliability/sample_audit.json | outputs/diagnostics/reliability/column_audit.csv | outputs/diagnostics/reliability/matching_audit.json | outputs/diagnostics/reliability/checks.json",
            "Primary website two-slot agreement table, transcribed values and original sample counts in primary_website_comparison.csv. No published all-slot/SE targets.", values, mismatch,
            "Original agreement calculations are reproducible at reported precision. This supports coding consistency under the supplied rating design, not construct validity or proof of distinct independent humans in every slot.",
            f"sources/author_code/reliability_original.do, {'Item Level' if identifier == 'R1' else 'Actor-Reference Level'} kappaetc calls. Archived official reliability page in sources/local/skill2_methods/reliability/.", pop, unit)

    add("C1", "Original model-assumption diagnostics, not substantive hypothesis tests.",
        "M1 imposes equal slopes across outrage thresholds. Original diagnostics assess departures from this restriction.",
        "Diagnostic null is proportional odds for the specified RHS. Non-rejection does not prove proportional odds.",
        "Ordinal tone 0-4 and five dummy predictors for generalized LR. Wolfe-Gould uses three numeric-coded predictors instead, exactly as the author command.",
        "tone=archive tone-1. " + CODING + " Do not silently replace Wolfe-Gould numeric RHS with the five-indicator RHS.",
        "Twice unrestricted minus restricted log likelihood for factor-coded gologit2. Approximate Wolfe-Gould statistic for the original numeric RHS, df and p when valid.",
        "gologit2 tone i.polsys i.socdiv i.mediatype, npl versus pl. omodel logit tone polsys socdiv mediatype.",
        "Source-matched generalized observed-category likelihood and original independent-binary approximation. Original gologit2 omission/rank rules and package build unpinned.",
        "Check identification, information rank, boundary slopes and every design/category probability before regular LR inference. Generalized model rank 22/24 and negative probabilities invalidate a regular chi-square p value.",
        "Published Note 1 reports LR 22.5/df14/p.07 and Wolfe-Gould 7.4/df9/p.59. Do not treat a failed generalized likelihood as a valid accepted-assumption test.",
        "analysis/ordinal_reproduction.py",
        "outputs/diagnostics/ordinal/M1_gologit2_LR_diagnostic.csv | outputs/diagnostics/ordinal/M1_gologit2_npl_factor.json | outputs/diagnostics/ordinal/M1_Wolfe_Gould_numeric.csv",
        "outputs/diagnostics/ordinal/findings.md | outputs/diagnostics/ordinal/M1_gologit2_npl_all_design_probabilities.csv",
        "Generalized LR=22.5, df=14, p=.07. Wolfe-Gould=7.4, df=9, p=.59.",
        "Generalized raw LR=22.5358450903, nominal df difference=15, accepted p unavailable. Wolfe-Gould=7.43106346771, df=9, p=.592333326551.",
        "Generalized raw LR agrees but reported df/p cannot be certified. Seven design-category probabilities are negative. Numeric-RHS Wolfe-Gould matches, but is not the same five-indicator model.",
        "Retain M1 and report the assumption-check limitation. This does not establish that proportional odds is true or that the substantive findings are invalid.",
        f"Article Note 1. {MODEL_CODE}, Analysis 2 Diagnostics, gologit2 npl/pl and omodel commands.")
    add("C2", "Original alternative-link robustness checks.",
        "Assess whether substantive slope conclusions depend on logistic rather than probit or complementary-log-log response shape.",
        "Compare directions and reported uncertainty across the three original links, without changing the original hypotheses.",
        "Same tone and five category indicators as M1, all 1700 items.", "tone=archive tone-1. " + CODING,
        "Link-specific slopes, cutpoints, likelihood, SE and 95% intervals. Probit/cloglog slopes are not odds ratios and do not have the same numeric scale as logit.",
        "Logit F(z)=expit(z), probit F(z)=Phi(z), author cloglog F(z)=exp(-exp(-z)), with Pr(Y<=k)=F(c_k-X beta).",
        ORD_EST + " Fit original pl logit, probit and cloglog links separately.",
        "Same sample and common-slope restriction per link. Check score, full-rank information and probabilities. Compare slope sign and interval exclusion of zero, not raw slope equality across links.",
        "Published Note 2 states similar substantive conclusions. Evaluate each comparison, not an assumption that every significance flag is identical.",
        "analysis/ordinal_reproduction.py",
        "outputs/reproduced/models/ordinal/ordinal_coefficients.csv | outputs/reproduced/models/ordinal/ordinal_fit.csv | outputs/reproduced/models/ordinal/M1_probit_model.json | outputs/reproduced/models/ordinal/M1_cloglog_model.json",
        "outputs/diagnostics/ordinal/independent_statsmodels_probit.json | outputs/diagnostics/ordinal/independent_statsmodels_cloglog.json",
        "Note 2 qualitative similar-conclusions claim. No full published numerical coefficient table for these links was recovered.",
        "LL logit=-724.000386802, probit=-721.913116804, cloglog=-724.418370755. All five slope directions persist. Probit mixed-system p=.149309806, versus logit p=.032978070.",
        "Mixed-versus-consensus significance changes under probit. Full alternative-link numeric equality to Stata output is not verifiable without original logs.",
        "Directional patterns are similar, with a mixed-system significance qualification. Original alternative-link checks do not themselves supply the assignment-added S1 analysis.",
        f"Article Note 2. {MODEL_CODE}, Robustness tests with alternative link functions, gologit2 pl link(logit/probit/cloglog).")
    add("C3", "Original null/hierarchy comparisons and model-fit summaries.",
        "Empty nested models quantify dependence at item and actor/statement levels. Compare the full model with its nested intercept-only baseline separately.",
        "Not H1-H3. Null variance components equal zero for nested-versus-single-level comparison. Full-versus-nested-null tests jointly zero five fixed slopes.",
        "Separate actrefoutbin and actrefrecbin models, random item and nested actor/statement intercepts, intercept-only and full fixed-effects forms.",
        "Binary outcomes unchanged and composite act_id verified. " + CODING,
        "Variance components, latent-scale ICCs, LL/-2LL/AIC, nested-null versus single-intercept LR, and full versus nested-null LR with five added slopes.",
        BIN_EQ + " Empty model drops X beta. V=pi^2/3+sigma_item^2+sigma_actor^2. ICC_item=sigma_item^2/V, ICC_same_actor=(sigma_item^2+sigma_actor^2)/V. LR=2*(LL_larger-LL_smaller).",
        BIN_EST + " Single-level null LL computed directly from the observed binary event rate.",
        "Null variance components lie on the boundary. The original mixture calibration is unrecovered, so no regular chi-square p value is accepted for the variance test. Full-versus-nested-null fixed-slope LR uses df=5.",
        "Article Note 3 compares empty nested with single-level models. Keep that comparison distinct from adding covariates to an existing nested model. Compare reported LR values, not unsupported boundary p values.",
        "analysis/run_binary_models.py | analysis/nested_logit.py | analysis/compare_replication.py",
        "outputs/diagnostics/binary_likelihood_comparisons.csv | outputs/reproduced/models/M2_null_fit.json | outputs/reproduced/models/M3_null_fit.json | outputs/reproduced/models/M2_fit.json | outputs/reproduced/models/M3_fit.json",
        "outputs/diagnostics/glmm/M2_null_independent_curvature.json | outputs/diagnostics/glmm/M3_null_independent_curvature.json",
        "Original nested-null versus single-null LR outrage=154.95, recognition=91.22. Table 4 full -2LL outrage=1326.48, recognition=1421.27.",
        "Nested-null versus single-null LR outrage=154.763730882, recognition=91.222779532. Full -2LL M2=1326.55697919, M3=1421.27111607. Full-versus-nested-null LR M2=36.0272879263, M3=28.1673795113, df=5.",
        "Recognition LR/-2LL agree at print precision. Outrage LR/-2LL differ slightly, with historical quadrature/build origin unresolved. Boundary-test p calibration not certified.",
        "Retain the modeled dependence and full saved variance/ICC estimates. These fit comparisons are not separate causal tests of institutional or media mechanisms.",
        f"Article Note 3 and Table 4. {MODEL_CODE}, Analysis 4 empty models, estat icc and estat ic.", REF, REF_UNIT)

    add("P1", "Original M1 probability summaries and discrete average marginal effects.",
        "Translate ordinal cumulative-odds slopes into the five category probabilities to show where adjusted differences occur.",
        "No new hypothesis. Summarize all five category probabilities, including mixed-system and each professional-medium comparison, retaining original directional targets.",
        "M1 tone categories 0-4 and polsys/socdiv/mediatype category assignments, five nonreference contrasts and eight assigned category levels.",
        "Use the same M1 sample, coding and fit. Change one focal predictor for every row while retaining other observed covariates, rather than setting all covariates to their means.",
        "40 standardized category probabilities and 25 category-specific discrete average probability changes. AME is category-versus-base, not a derivative of nominal category numbers.",
        "p_k(a)=N^-1 sum_i [F(c_k-X_i(a)beta)-F(c_(k-1)-X_i(a)beta)]. AME_k(a)=p_k(a)-p_k(base), with outer thresholds infinite.",
        "Evaluate saved M1 ML and full covariance. Delta-method SE with full parameter covariance and normal untransformed 95% intervals.",
        "Verify probabilities sum to one and contrasts sum to zero across categories. Use the original standardization sample and keep uncertainty gradients. No causal treatment-effect claim.",
        "Compare 25 published supplementary AMEs and 50 interval endpoints at printed precision. Original figure probabilities are not supplied as an exact numeric vector.",
        "analysis/ordinal_reproduction.py",
        "outputs/reproduced/predictions/ordinal/M1_predictive_margins.csv | outputs/reproduced/predictions/ordinal/M1_average_marginal_effects.csv | outputs/reproduced/predictions/ordinal/M1_prediction_gradients.json",
        "outputs/verification/independent_checks/independent_ordinal_ames.csv | outputs/verification/independent_checks/checks.json",
        "All 75 published AME/CI targets in comparison ledger P1:AME. Exact figure probability/SE vector unavailable.",
        "40 probabilities and 25 AMEs computed with SE and intervals. 68/75 printed AME/CI cells agree and seven differ. Independent M1/AME calculation agrees to about 5.7e-9 across estimates/endpoints.",
        "Seven narrow supplementary AME/CI differences are retained. Unprinted figure probabilities cannot be classified as exactly reproduced. Independent calculation supports the Python values, without proving a particular Stata cause.",
        "Most probability differences concern no versus slight outrage. This statement applies to ordinal tone, not to intensity categories of the binary outcomes.",
        f"Article predictive Figure 1 and recovered supplementary AMEs. {MODEL_CODE}, Analysis 2 margins and margins,dydx commands for author Figure 2.")
    add("P2", "Original prior-marginal binary predictions and discrete AMEs.",
        "Translate conditional binary-logit coefficients into population-marginal reference probabilities, integrating over both random-intercept distributions.",
        "No new hypothesis. Report each original contrast in both outcome models, including additional mixed-system comparisons.",
        "M2 outrage and M3 recognition, eight assigned category probabilities and five nonreference discrete contrasts per outcome.",
        "Keep 3770 observed-reference weights and source recodes. Set one predictor for every reference, preserving other observed predictors. Integrate over prior Gaussian random effects, not empirical-Bayes effects or random effects fixed at zero.",
        "16 prior-marginal probabilities and 10 discrete AMEs, with full fixed/variance-parameter delta-method uncertainty.",
        "p(a)=N^-1 sum_r integral expit(beta0+X_r(a)beta+u+v) phi(u)phi(v) du dv. AME(a)=p(a)-p(base).",
        "Saved frequentist M2/M3 fits. Primary prediction tensor GH7 per intercept, full covariance central-difference delta method, normal 95% intervals. Combined-normal GH7/81/161 comparisons retained.",
        "Distinguish conditional OR, marginal probability and discrete change. Verify integration and sample weighting, include variance-parameter uncertainty, and retain unpinned historical prediction-grid reduction.",
        "Compare all ten published AMEs and twenty interval endpoints. Graph pixels and unprinted full SE/probability vectors are not exact comparison targets.",
        "analysis/binary_predictions.py",
        "outputs/reproduced/predictions/binary_margins_ames.csv",
        "outputs/diagnostics/binary_prediction_integration.csv | outputs/diagnostics/glmm/acceptance_review.md",
        "Ten original binary AMEs and twenty 95% endpoints recovered from the article and ledger M2:AME/M3:AME. Full exact probability vectors unavailable.",
        "16 probabilities plus 10 AMEs, each with SE and intervals, saved. All ten published AMEs and twenty interval endpoints match printed precision.",
        "Finite prediction-grid reduction was not documented historically. Primary estimates match published contrasts, but exact arithmetic equivalence for unprinted probabilities is unverified.",
        "Binary probability summaries support the same associational interpretation as M2/M3. Marginal changes do not prove causal gatekeeping or improved democratic relations.",
        f"Article predictive Figure 3 and AME text. {MODEL_CODE}, Analysis 4 margins/dydx for both outcomes and author Figure 4.", REF, REF_UNIT)

    add("A1", "Evidence-coverage inventory and source reconciliation.",
        "A full computational reproduction accounts for all relevant available analyses and exposes missing historical targets instead of selecting only successful cells.",
        "Not applicable as a directional prediction. Inventory every known item, reference, reliability, model, diagnostic and prediction target.",
        "Article tables/notes/figures, author analysis/reliability syntax, primary reliability and supplementary targets, recovered versus unavailable numerical values.",
        "Preserve source numbers separately from estimates. Use stable analysis_id/quantity keys, explicit precision and missing target markers, never zero-fill an unavailable target.",
        "Coverage disposition per analysis/quantity, displayed-value agreement, discrepancy or non-verifiability. Counts are heterogeneous evidence entries, not independent replication trials.",
        "Join published target and reproduced evidence by analysis_id/quantity. Compare exact integer targets exactly and displayed decimals against half one last displayed unit. Missing or invalid targets remain not_verifiable.",
        "Deterministic source inventory, target extraction and comparison. No statistical estimator or confidence interval for a completeness score.",
        "Check unique keys, primary source locators, target provenance and every known code section. Historical unrounded logs/builds and unavailable appendix targets remain explicit access limits.",
        "Account for all available target cells, preserving exceptions and unavailable evidence. Agreement at printed precision is not exact equality of unpublished estimates.",
        "analysis/verify_and_package.py",
        "docs/analysis_inventory.csv | outputs/verification/comparison_all.csv | outputs/verification/comparison_coverage.csv | outputs/verification/summary.json",
        "outputs/verification/interpretation_audit.md | records/skill_tests/verify-and-package/independent_source_audit.md",
        "376 numeric source targets registered. Source-specific numbers and locators in comparison_all.csv, not a newly published coverage statistic.",
        "1798 ledger rows. Of 376 numeric published targets, 362 agree at display/integer precision, 13 differ and one p value remains unverifiable. Another 1422 entries have no available numeric target.",
        "Original unrounded fits, some package builds, all-slot reliability uncertainty and exact figure vectors were not recovered. No claim of exhaustive inaccessible appendices.",
        "Every known available analysis has a disposition. Numeric agreement supports computational reproducibility within the recorded scope, not automatic theoretical or causal validation.",
        "Assignment pp.1 and 8-10, full coverage. Article Tables 1-4, Figures 1-3 and Notes 1-3. Both original author scripts and recovered official supplementary/reliability pages.",
        ITEM + " Independent rating workbooks are additional measurement evidence.", "One source analysis or numerical evidence entry. This is a document/coverage unit, not an independent sampled subject.")
    add("V1", "Assignment-added independent statistical verification.",
        "Separately implemented quantities can detect implementation errors that repeat runs of the same likelihood would reproduce.",
        "No new substantive prediction. Independent counts and model quantities should agree within documented numerical tolerances.",
        "Raw-data event/tone/hierarchy counts, Australian website moderate proportion, independent M1 optimization and all ordinal AMEs, M2/M3 fixed-parameter nested likelihood and curvature.",
        "Read original .dta with pyreadstat without value-format recoding. Separate M1 design/predict implementation. Evaluate saved M2/M3 parameters without copying project integration code. Original files unchanged.",
        "Count equality, independent M1 maximum-likelihood slopes/LL, all 25 AMEs/50 endpoints and fixed-parameter binary integrals/curvature. A check is not a new scientific estimand.",
        "Compare independent minus canonical quantities. M1 checks use abs(LL difference)<1e-7 and max slope/AME/CI difference<1e-6. Binary reference tests retain their own adaptive-integration tolerances.",
        "Independent raw-data arithmetic, statsmodels OrderedModel BFGS optimization and separate finite-difference delta method. Independent nested quadrature/curvature at fixed saved parameters.",
        "Inspect actual check receipts and tolerances. M2/M3 are not independently reoptimized in another engine. Software setup/import tests alone are insufficient.",
        "Assignment requires an important descriptive and a core advanced-model numerical check. Pass only actual numerical checks, not file presence or agreement with a copied published number.",
        "tests/skill2/data_checks.py | tests/skill2/check_glmm_full_likelihood.py | tests/skill2/check_glmm_fit_curvature.py | tests/skill3/check_verification.py",
        "outputs/diagnostics/data_independent_checks.json | outputs/verification/independent_checks/checks.json | outputs/verification/independent_checks/independent_ordinal_ames.csv",
        "outputs/diagnostics/glmm/M2_fitted_parameters_full_likelihood.json | outputs/diagnostics/glmm/M3_fitted_parameters_full_likelihood.json | outputs/diagnostics/glmm/M2_independent_curvature.json | outputs/diagnostics/glmm/M3_independent_curvature.json",
        "Not applicable. These are assignment-added numerical checks, not original article tests.",
        "Independent descriptive checks passed. Fresh M1 optimization and all ordinal AME/CI comparisons passed. Saved binary fixed-parameter likelihood/curvature checks passed within their recorded tolerances. Skill-3 receipt reports 12/12 checks.",
        "Independent binary integral/curvature checks do not establish independent M2/M3 optimization. Scope and finite-grid limits remain in their receipts.",
        "Checks support correctness of the tested calculations. They do not alone establish model validity, causal identification or exact unpublished Stata executable parity.",
        "Assignment p.10, independent statistical verification. Saved tests and dated check receipts are the direct execution evidence.",
        REF, "Count/model-check quantity calculated independently from original data or a fixed saved parameter vector, not a new sampled observational unit.")
    add("N1", "Assignment-added harmless negative statistical test and recovery.",
        "A reproducible pipeline must detect invalid inputs before estimation and recover without changing original evidence.",
        "Invalid copied category must raise ValueError, and a restored copy must produce the expected valid recode or domain check.",
        "Synthetic polsys invalid code 77 in the production recode check, plus in-memory original-data tone invalid code 99 in the later check.",
        "Mutate copied/synthetic objects only. Keep analytical source codes, hashes and canonical results unchanged. Restore copies from the untouched valid input.",
        "Detection flag, expected exception type and exact recovery flag, plus unchanged original SHA256. Not a hypothesis effect size.",
        "Inject invalid copied code, call production recode/domain check, catch ValueError, restore, rerun and compare with explicit source recode.",
        "Deterministic validation, no statistical fitting, confidence interval or p value.",
        "Test must reach the validation function, detect the intended failure and actually rerun recovery. Never mutate or delete source inputs or canonical result files.",
        "Assignment harmless failure/detection/recovery requirement, distinct from a skill-metadata corruption test.",
        "tests/skill2/data_checks.py | tests/skill3/check_verification.py",
        "outputs/diagnostics/data_independent_checks.json | outputs/verification/independent_checks/checks.json",
        "outputs/diagnostics/data_independent_checks.json | outputs/verification/independent_checks/checks.json",
        "Not applicable. No negative-test statistic is claimed in the original article.",
        "Copied polsys=77 and tone=99 errors were detected. Valid copies recovered and original-file hash checks passed.",
        "Not applicable as a numerical paper discrepancy. Failure injection occurs only in copies, not in the original research data.",
        "Demonstrates bounded detection and recovery for category errors. It does not prove the pipeline detects every possible data or modeling error.",
        "Assignment p.10, one harmless negative statistical failure/detection/recovery check.",
        "Controlled synthetic or in-memory copies associated with the original item data, not a newly recruited population.", "One injected invalid category and its restored test object. No inferential dependence model.")
    add("S1", "Assignment-added separate country-influence sensitivity, executed, student interpretation pending.",
        "Each political-system-by-division cell contains one country. Assess whether M1 associations depend heavily on retaining a single national context.",
        "No new prespecified directional substantive hypothesis. Report all six deletions, compare directions and uncertainty with faithful M1, without choosing a preferred result.",
        "Same ordinal tone and five dummy slopes as M1. Exclude each of the six countries once, yielding six changed-sample fits and 30 slope estimates.",
        "Apply original recodes, no reclassification or weights. Drop one country for each labeled fit. No deletion selected after observing its coefficient.",
        "Country-deletion-specific M1 slopes/ORs, intervals, differences from faithful beta and range/significance summaries. The sample/context mixture and thus estimand change.",
        ORD_EQ + " For deletion c, maximize the same likelihood over i with country_i != c.",
        ORD_EST + " Original likelihood/link retained for each of six country deletions. Plan saved before the fits.",
        "Check valid categories, ordered thresholds, small score and full-rank information for every deletion. 95% Wald intervals. Six p-count summaries are descriptive, not multiplicity-adjusted independent confirmations.",
        "Assignment p.13 asks for justified specification sensitivity. This completed check changes sample composition. A stricter model-specification interpretation remains unresolved, so it is not certified as closing that wording requirement.",
        "analysis/skill3_sensitivity.py",
        "outputs/verification/sensitivity/plan.json | outputs/verification/sensitivity/country_deletion_coefficients.csv | outputs/verification/sensitivity/country_deletion_fits.csv | outputs/verification/sensitivity/country_deletion_summary.csv",
        "outputs/verification/sensitivity/country_deletion_fits.csv | outputs/verification/sensitivity/README.md",
        "Not applicable. This is a replication-added sensitivity with faithful M1 as baseline, not an original article result.",
        "All six fits completed. All five slopes retain their original sign in 6/6 deletions. Website and newspaper p<.05 in 6/6, contextual contrasts in 4/6. Full OR ranges and intervals are saved.",
        "Changing the sample changes the target context mix. This is M1-only sample influence, not evidence for M2/M3 specification robustness or a newly executed country-fixed-effects model.",
        "Professional-media M1 associations persist across all six deletions. Contextual uncertainty varies by country. Student interpretation and the specification-sensitivity wording decision remain pending.",
        "Assignment p.13. outputs/verification/sensitivity/plan.json, dated before fitting. Separate from original C2 link checks and numerical integration diagnostics.")
    return result


def ledger_summary(identifier, ledger):
    def included(r):
        aid = r["analysis_id"]
        if identifier == "R1":
            return aid.startswith(("R:tone", "R_full:tone"))
        if identifier == "R2":
            return aid.startswith(("R:", "R_full:")) and not aid.startswith(("R:tone", "R_full:tone"))
        if identifier == "P2":
            return aid.startswith(("M2:AME", "M3:AME", "M2:prediction:", "M3:prediction:"))
        if identifier == "C2":
            return aid.startswith(("M1_probit:", "M1_cloglog:"))
        if identifier == "A1":
            return True
        return aid == identifier or aid.startswith(identifier + ":")
    selected = [r for r in ledger if included(r)]
    counts = {}
    for r in selected:
        status = r["comparison_status"]
        counts[status] = counts.get(status, 0) + 1
    return f"Ledger coverage for {identifier} = {json.dumps(counts, sort_keys=True)}. Detailed target values/locators remain in {LEDGER}."


def guide(matrix):
    lines = ["# Hypothesis-to-evidence matrix", "", "Updated on 20 October 2026.", "",
             "The [complete CSV](hypothesis_matrix.csv) is the canonical matrix. This page is its reader guide. "
             "Each CSV row preserves the teacher's six field groups on assignment p.3, from the theoretical claim through the executed evidence and scientific conclusion. "
             "Unique row IDs distinguish the 12 directional hypothesis targets, three additional mixed-system comparisons and 13 supporting-analysis rows.", "",
             "This is a retrospective documentation completion after the saved analyses. It does not claim that the completed matrix was approved before estimation. "
             "Published values are separately labelled comparison targets. Reproduced values come from saved Python results. No model was rerun and no source or estimate was changed for this update.", "",
             "## How to use the files", "",
             "1. Start with the hypothesis summary below, then find its row_id in the CSV.",
             "2. Read the row's design, coding, exact contrast, equation, estimator and evaluation fields together.",
             "3. Open the linked script, output and diagnostic paths to inspect the evidence. Paths are relative to the project root and use ` | ` when more than one file is needed.",
             "4. Compare the separately labelled source target and estimate. The [full comparison ledger](../outputs/verification/comparison_all.csv) retains every available target and its precision.", "",
             "In all main models the reference groups are consensus systems, stable secularism and political blogs. "
             "M1 estimates cumulative odds for ordinal item tone. M2 and M3 estimate conditional odds for binary outrage and recognition in separate nested models. "
             "Their odds ratios are not probability ratios. Professional websites and newspapers are tested separately against blogs.", "",
             "## Original directional hypotheses", "",
             "| Row ID | Original contrast and expected sign | Reproduced OR and 95% CI | Conclusion |",
             "|---|---|---|---|"]
    for r in matrix:
        if r["hypothesis_id"] != "not-numbered":
            values = dict(part.split("=", 1) for part in r["reproduced_values"].split(" | "))
            conclusion = r["scientific_conclusion"].split(".", 1)[0].replace("_", " ")
            lines.append(f"| {r['row_id']} | {r['predicted_relationship']} | {float(values['OR']):.3f} [{float(values['OR_CI95_lower']):.3f}, {float(values['OR_CI95_upper']):.3f}] | {conclusion} |")
    lines += ["", "H1a is unsupported overall, with the opposite significant direction in M1 and no significant reference-level association. "
              "H1b is not statistically supported. H2a is supported at item level only, while H2b has a significant association opposite to its prediction. "
              "Both professional-media contrasts support H3a and H3b. These substantive decisions agree with the original reported patterns.", "",
              "## Additional published comparisons", "",
              "The three rows labelled `M1_additional_mixed_vs_consensus`, `M2_additional_mixed_vs_consensus` and `M3_additional_mixed_vs_consensus` preserve the mixed-system coefficients. "
              "The article does not supply an original directional hypothesis for these comparisons. M1 shows higher outrage in mixed than consensus systems. "
              "M2 and M3 comparisons are not statistically significant. The small M2 mixed OR difference is recorded rather than counted as an H1a/H1b discrepancy.", "",
              "## Supporting analyses and their evidence", "",
              "| Row ID | Purpose and interpretation | Main saved evidence |", "|---|---|---|"]
    for r in matrix:
        if r["analysis_id"] not in {"M1", "M2", "M3"}:
            output = r["output_path"].split(" | ")[0]
            lines.append(f"| {r['row_id']} | {r['scientific_conclusion']} | [{Path(output).name}](../{output}) |")
    lines += ["", "A1 is the evidence inventory and retains unavailable historical quantities. V1 is independent numerical verification. "
              "N1 tests harmless failure detection and recovery on copies. These are not substantive hypotheses. "
              "S1 now correctly records the six completed country deletions. It remains a sample-influence sensitivity, so the teacher's stricter specification-sensitivity wording still needs a separate decision.", "",
              "## Completion and review status", "",
              "All 28 rows have populated claim, design, analytical target, specification, evidence and conclusion fields. "
              "Where an original target or inferential quantity is unavailable, the reason is explicit. This is more informative than leaving a cell blank or inventing a value. "
              "The 12 hypothesis targets were cross-checked against the saved coefficients, hypothesis-test file, published targets and comparison ledger. "
              "Every script, output and diagnostic path in the matrix was checked locally.", "",
              "Technical documentation completion does not supply student acceptance, direct-reading attestations or a prior approval date. "
              "The [dictionary](variable_dictionary.md), [diagrams](model_diagram.md) and other course requirements have their own evidence and review status. "
              "The [dated invocation record](../records/skill_invocations/2026-10-20_specify-empirical-study_matrix/README.md) preserves the previous CSV, source bindings, checks and changes.", ""]
    return "\n".join(lines)


def validate():
    matrix = rows(CSV)
    errors = []
    checked_paths = set()
    expected_ids = {r["analysis_id"] for r in rows("docs/analysis_inventory.csv")}
    if len(matrix) != 28 or len({r["row_id"] for r in matrix}) != 28:
        errors.append("Expected 28 unique row IDs.")
    if {r["analysis_id"] for r in matrix} != expected_ids:
        errors.append("Inventory coverage differs.")
    for r in matrix:
        for key, value in r.items():
            if key is None or not value or not value.strip():
                errors.append(f"{r.get('row_id')}: blank or malformed field {key}")
        for key in ["script_path", "output_path", "diagnostic_path", "published_values_path"]:
            if r[key].startswith("Not applicable"):
                continue
            for rel in r[key].split(" | "):
                p = (ROOT / rel).resolve()
                if not p.is_relative_to(ROOT) or not p.exists():
                    errors.append(f"{r['row_id']}: missing or out-of-root {key} {rel}")
                checked_paths.add(rel)
    tests = rows("outputs/reproduced/hypothesis_tests.csv")
    published = {(r["model_id"], r["contrast"]): r for r in rows("outputs/published/model_targets.csv")}
    ledger = rows(LEDGER)
    for r in matrix:
        if r["analysis_id"] not in {"M1", "M2", "M3"}:
            continue
        contrast = r["comparison_key"].split("_vs_", 1)[0]
        pub = published[r["analysis_id"], contrast]
        for label, key in [("b", "b"), ("SE", "se"), ("OR", "odds_ratio")]:
            if f"{label}={pub[key]}" not in r["published_values"]:
                errors.append(f"Published value mismatch {r['row_id']} {label}")
        coefpath = ("outputs/reproduced/models/ordinal/ordinal_coefficients.csv" if r["analysis_id"] == "M1"
                    else f"outputs/reproduced/models/{r['analysis_id']}_coefficients.csv")
        term = {"mixed": "2.polsys", "majoritarian": "3.polsys", "contested": "2.socdiv",
                "website": "2.mediatype", "newspaper": "3.mediatype"}[contrast] if r["analysis_id"] == "M1" else r["comparison_key"]
        coef = next(c for c in rows(coefpath) if c["term"] == term and c.get("analysis_id", r["analysis_id"]) == r["analysis_id"])
        if r["reproduced_values"] != result_text(coef):
            errors.append(f"Coefficient or interval mismatch {r['row_id']}")
    for identifier, aid in [("C3", "C3:M2"), ("C3", "C3:M3")]:
        source = next(r for r in ledger if r["analysis_id"] == aid and r["quantity"] == "empty_mixed_vs_single_LR")
        row = next(r for r in matrix if r["row_id"] == identifier)
        if source["published_value"] not in row["published_values"]:
            errors.append("C3 source target differs: " + aid)
    tone_alpha = next(r for r in rows("outputs/reproduced/reliability/reliability_coefficients.csv")
                      if r["outcome"] == "tone" and r["selection"] == "two_slots" and r["coefficient"] == "krippendorff_alpha")
    if f"{float(tone_alpha['estimate']):.12f}" not in next(r for r in matrix if r["row_id"] == "R1")["reproduced_values"]:
        errors.append("R1 alpha summary differs from saved estimate.")
    for t in tests:
        candidates = [r for r in matrix if r["analysis_id"] == t["model_id"] and r["hypothesis_id"] == t["hypothesis_id"] and r["comparison_key"].startswith(t["contrast"] + "_")]
        if len(candidates) != 1:
            errors.append(f"Missing/duplicate directional target {t}")
            continue
        r = candidates[0]
        parsed = dict(s.split("=", 1) for s in r["reproduced_values"].split(" | "))
        for label, key in [("b", "beta"), ("SE", "se"), ("OR", "odds_ratio"), ("p", "p_value")]:
            if not math.isclose(float(parsed[label]), float(t[key]), rel_tol=1e-10, abs_tol=1e-12):
                errors.append(f"Numeric mismatch {r['row_id']} {label}")
        direction = ">0" if int(t["predicted_sign"]) > 0 else "<0"
        if direction not in r["predicted_relationship"] or t["conclusion"] not in r["scientific_conclusion"]:
            errors.append(f"Direction or conclusion mismatch {r['row_id']}")
    for rel in re.findall(r"\]\(([^)]+)\)", (ROOT / GUIDE).read_text(encoding="utf-8")):
        if not ((ROOT / GUIDE).parent / rel).resolve().exists():
            errors.append("Broken reader-guide link: " + rel)
    unchanged = []
    for entry in load(str((RECORD / "protected_manifest.json").relative_to(ROOT))):
        if not (ROOT / entry["path"]).exists() or digest(ROOT / entry["path"]) != entry["sha256"]:
            errors.append("Protected input/code/result changed: " + entry["path"])
        else:
            unchanged.append(entry["path"])
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(), "matrix_version": MATRIX_VERSION,
              "status": "passed" if not errors else "failed", "rows": len(matrix), "directional_hypothesis_rows": len(tests),
              "additional_mixed_comparisons": sum(r["comparison_key"] == "mixed_vs_consensus" for r in matrix),
              "supporting_rows": sum(r["analysis_id"] not in {"M1", "M2", "M3"} for r in matrix),
              "columns": len(matrix[0]), "checked_unique_paths": len(checked_paths), "errors": errors,
              "protected_files_unchanged": len(unchanged), "research_models_rerun": False,
              "student_acceptance_inferred": False, "final_report_read_or_modified": False,
              "github_synchronized": False, "matrix_sha256": digest(ROOT / CSV),
              "evidence_bindings": [{"path": p, "sha256": digest(ROOT / p)} for p in sorted(checked_paths)
                                    if (ROOT / p).is_file()]}
    write_json(RECORD / "validation.json", result)
    print(json.dumps({k: v for k, v in result.items() if k != "evidence_bindings"}, indent=2))
    if errors:
        raise SystemExit(1)


def build():
    snapshot()
    old = rows(str((RECORD / "previous_versions" / CSV).relative_to(ROOT)))
    matrix = main_rows(old) + supporting_rows(old)
    ledger = rows(LEDGER)
    for row in matrix:
        if row["analysis_id"] not in {"M1", "M2", "M3", "V1", "N1", "S1"}:
            row["discrepancy"] += " " + ledger_summary(row["analysis_id"], ledger)
    original_fields = list(old[0])
    fields = ["row_id", "comparison_key"] + original_fields + ["published_values", "diagnostic_path"]
    with (ROOT / CSV).open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(matrix)
    (ROOT / GUIDE).write_text(guide(matrix), encoding="utf-8")
    validate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    validate() if args.check else build()
