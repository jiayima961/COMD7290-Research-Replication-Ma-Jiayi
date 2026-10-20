# Hypothesis-to-evidence matrix

Updated on 20 October 2026.

The [complete CSV](hypothesis_matrix.csv) is the canonical matrix. This page is its reader guide. Each CSV row preserves the teacher's six field groups on assignment p.3, from the theoretical claim through the executed evidence and scientific conclusion. Unique row IDs distinguish the 12 directional hypothesis targets, three additional mixed-system comparisons and 13 supporting-analysis rows.

This is a retrospective documentation completion after the saved analyses. It does not claim that the completed matrix was approved before estimation. Published values are separately labelled comparison targets. Reproduced values come from saved Python results. No model was rerun and no source or estimate was changed for this update.

## How to use the files

1. Start with the hypothesis summary below, then find its row_id in the CSV.
2. Read the row's design, coding, exact contrast, equation, estimator and evaluation fields together.
3. Open the linked script, output and diagnostic paths to inspect the evidence. Paths are relative to the project root and use ` | ` when more than one file is needed.
4. Compare the separately labelled source target and estimate. The [full comparison ledger](../outputs/verification/comparison_all.csv) retains every available target and its precision.

In all main models the reference groups are consensus systems, stable secularism and political blogs. M1 estimates cumulative odds for ordinal item tone. M2 and M3 estimate conditional odds for binary outrage and recognition in separate nested models. Their odds ratios are not probability ratios. Professional websites and newspapers are tested separately against blogs.

## Original directional hypotheses

| Row ID | Original contrast and expected sign | Reproduced OR and 95% CI | Conclusion |
|---|---|---|---|
| M1_H1a_majoritarian_vs_consensus | majoritarian_vs_consensus slope >0 and OR>1 for ordinal tone. | 0.540 [0.354, 0.826] | significant opposite direction |
| M1_H2a_contested_vs_stable | contested_vs_stable slope >0 and OR>1 for ordinal tone. | 1.688 [1.236, 2.306] | consistent with prediction |
| M1_H3a_website_vs_blog | website_vs_blog slope <0 and OR<1 for ordinal tone. | 0.168 [0.112, 0.254] | consistent with prediction |
| M1_H3a_newspaper_vs_blog | newspaper_vs_blog slope <0 and OR<1 for ordinal tone. | 0.281 [0.197, 0.401] | consistent with prediction |
| M2_H1a_majoritarian_vs_consensus | majoritarian_vs_consensus slope >0 and OR>1 for explicit outrage. | 0.678 [0.262, 1.756] | not statistically supported |
| M2_H2a_contested_vs_stable | contested_vs_stable slope >0 and OR>1 for explicit outrage. | 0.876 [0.486, 1.579] | not statistically supported |
| M2_H3a_website_vs_blog | website_vs_blog slope <0 and OR<1 for explicit outrage. | 0.230 [0.107, 0.494] | consistent with prediction |
| M2_H3a_newspaper_vs_blog | newspaper_vs_blog slope <0 and OR<1 for explicit outrage. | 0.340 [0.166, 0.699] | consistent with prediction |
| M3_H1b_majoritarian_vs_consensus | majoritarian_vs_consensus slope <0 and OR<1 for explicit recognition. | 0.579 [0.297, 1.130] | not statistically supported |
| M3_H2b_contested_vs_stable | contested_vs_stable slope <0 and OR<1 for explicit recognition. | 2.199 [1.355, 3.567] | significant opposite direction |
| M3_H3b_website_vs_blog | website_vs_blog slope >0 and OR>1 for explicit recognition. | 1.987 [1.065, 3.708] | consistent with prediction |
| M3_H3b_newspaper_vs_blog | newspaper_vs_blog slope >0 and OR>1 for explicit recognition. | 3.277 [1.766, 6.080] | consistent with prediction |

H1a is unsupported overall, with the opposite significant direction in M1 and no significant reference-level association. H1b is not statistically supported. H2a is supported at item level only, while H2b has a significant association opposite to its prediction. Both professional-media contrasts support H3a and H3b. These substantive decisions agree with the original reported patterns.

## Additional published comparisons

The three rows labelled `M1_additional_mixed_vs_consensus`, `M2_additional_mixed_vs_consensus` and `M3_additional_mixed_vs_consensus` preserve the mixed-system coefficients. The article does not supply an original directional hypothesis for these comparisons. M1 shows higher outrage in mixed than consensus systems. M2 and M3 comparisons are not statistically significant. The small M2 mixed OR difference is recorded rather than counted as an H1a/H1b discrepancy.

## Supporting analyses and their evidence

| Row ID | Purpose and interpretation | Main saved evidence |
|---|---|---|
| D1 | Outrage is uncommon and high-intensity tone is rare. Summaries describe the selected corpus, without a causal or hypothesis-level conclusion. | [item_descriptives.csv](../outputs/reproduced/descriptives/ordinal/item_descriptives.csv) |
| D2 | The two discourse measures have low overall prevalence. Keep raw descriptions separate from adjusted tests and recognition across versus within groups. | [reference_descriptives.csv](../outputs/reproduced/descriptives/ordinal/reference_descriptives.csv) |
| R1 | Original agreement calculations are reproducible at reported precision. This supports coding consistency under the supplied rating design, not construct validity or proof of distinct independent humans in every slot. | [reliability_coefficients.csv](../outputs/reproduced/reliability/reliability_coefficients.csv) |
| R2 | Original agreement calculations are reproducible at reported precision. This supports coding consistency under the supplied rating design, not construct validity or proof of distinct independent humans in every slot. | [reliability_coefficients.csv](../outputs/reproduced/reliability/reliability_coefficients.csv) |
| C1 | Retain M1 and report the assumption-check limitation. This does not establish that proportional odds is true or that the substantive findings are invalid. | [M1_gologit2_LR_diagnostic.csv](../outputs/diagnostics/ordinal/M1_gologit2_LR_diagnostic.csv) |
| C2 | Directional patterns are similar, with a mixed-system significance qualification. Original alternative-link checks do not themselves supply the assignment-added S1 analysis. | [ordinal_coefficients.csv](../outputs/reproduced/models/ordinal/ordinal_coefficients.csv) |
| C3 | Retain the modeled dependence and full saved variance/ICC estimates. These fit comparisons are not separate causal tests of institutional or media mechanisms. | [binary_likelihood_comparisons.csv](../outputs/diagnostics/binary_likelihood_comparisons.csv) |
| P1 | Most probability differences concern no versus slight outrage. This statement applies to ordinal tone, not to intensity categories of the binary outcomes. | [M1_predictive_margins.csv](../outputs/reproduced/predictions/ordinal/M1_predictive_margins.csv) |
| P2 | Binary probability summaries support the same associational interpretation as M2/M3. Marginal changes do not prove causal gatekeeping or improved democratic relations. | [binary_margins_ames.csv](../outputs/reproduced/predictions/binary_margins_ames.csv) |
| A1 | Every known available analysis has a disposition. Numeric agreement supports computational reproducibility within the recorded scope, not automatic theoretical or causal validation. | [analysis_inventory.csv](../docs/analysis_inventory.csv) |
| V1 | Checks support correctness of the tested calculations. They do not alone establish model validity, causal identification or exact unpublished Stata executable parity. | [data_independent_checks.json](../outputs/diagnostics/data_independent_checks.json) |
| N1 | Demonstrates bounded detection and recovery for category errors. It does not prove the pipeline detects every possible data or modeling error. | [data_independent_checks.json](../outputs/diagnostics/data_independent_checks.json) |
| S1 | Professional-media M1 associations persist across all six deletions. Contextual uncertainty varies by country. Student interpretation and the specification-sensitivity wording decision remain pending. | [plan.json](../outputs/verification/sensitivity/plan.json) |

A1 is the evidence inventory and retains unavailable historical quantities. V1 is independent numerical verification. N1 tests harmless failure detection and recovery on copies. These are not substantive hypotheses. S1 now correctly records the six completed country deletions. It remains a sample-influence sensitivity, so the teacher's stricter specification-sensitivity wording still needs a separate decision.

## Completion and review status

All 28 rows have populated claim, design, analytical target, specification, evidence and conclusion fields. Where an original target or inferential quantity is unavailable, the reason is explicit. This is more informative than leaving a cell blank or inventing a value. The 12 hypothesis targets were cross-checked against the saved coefficients, hypothesis-test file, published targets and comparison ledger. Every script, output and diagnostic path in the matrix was checked locally.

Technical documentation completion does not supply student acceptance, direct-reading attestations or a prior approval date. The [dictionary](variable_dictionary.md), [diagrams](model_diagram.md) and other course requirements have their own evidence and review status. The [dated invocation record](../records/skill_invocations/2026-10-20_specify-empirical-study_matrix/README.md) preserves the previous CSV, source bindings, checks and changes.
