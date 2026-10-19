# Comparison of published and reproduced statistical results

Prepared for Ma Jiayi and the COMD7290 instructor on 19 October 2026. This is an AI-assisted technical verification report for Löb et al. (2024), not the student's accepted final submission.

## Overall finding

The Python reproduction broadly recovers the article's main numerical and directional findings under the original statistical specification. It does not demonstrate complete equality with the historical Stata execution. Among the original 45 coefficient, standard-error and odds-ratio cells, 44 agree within the article's two-decimal display. The remaining M2 mixed-system odds ratio, several fit statistics, seven supplementary ordinal marginal-effect cells and two publication inconsistencies require explicit qualification. A problematic generalized ordinal diagnostic prevents certification of one published assumption test.

The complete ledger contains 1,798 quantity records. Of 376 entries with numeric publication targets, 334 agree within displayed rounding, 28 agree as published integers, 13 differ, and one published p value cannot be validated. Another 1,422 entries have no precise published numeric target; their calculations are saved, but equality cannot be tested. These heterogeneous, overlapping entries are an audit inventory, not independent replications or a statistical success rate.

"Within rounding" means the absolute difference is at most half the last displayed unit, fixed before comparison. Integer counts and significance tiers are checked exactly. Matching a rounded value does not establish equality of unavailable unrounded estimates. Validation of a calculation is separate from numerical agreement and substantive support for a hypothesis.

## Data and descriptive results

The analysis reconstructs 1,700 news items and 3,770 directed actor references in 2,453 originating actor or statement groups within 1,183 items. There are 192 coded outrage references and 196 recognition references. Required main-model fields produce no exclusions. Article tone codes 0–4 have counts 1,491, 159, 28, 17 and 5. Archive codes 1–5 were recoded using the author syntax; published and stored scales must not be confused.

All country/media and pooled Table 2 percentages agree at whole-percent precision except the Australian news-website moderate-outrage cell. The original table visibly prints 11, while one of 100 observations gives 1%. Its printed row sums to 110 despite a stated total of 100. This strongly supports an isolated table error, without establishing whether it arose during author preparation or production. Ordinary rounding can legitimately make another row sum to 101; such rows were not forced to sum to 100.

The printed reference-level descriptives reproduce: overall outrage is 5.0928% and recognition 5.1989%, rounding to 5.1% and 5.2%. Media and country percentages match their reported precision. The Discussion's recognition ranking differs from the raw Results: Switzerland is 3.0%, the USA 5.5% and Lebanon 18.0%. System-level interpretations and adjusted estimates must be distinguished from this raw country ranking. The discrepancy does not justify silently rewriting either passage.

## Independent coder reliability

All 30 published point coefficients and the five outcome sample sizes on the official main-stage reliability page agree at displayed precision. The calculations cover tone, valence, outrage, recognition and responsiveness, with six agreement coefficients for each. The author-selected all-slot analyses, conditional standard errors and intervals are also saved, but their complete numeric targets are not published on that page. They are computed results with an explicit verification limit.

Reliability uses independent-rating matrices rather than the consensus analytical data. The author-selected positional slots and nominal -99 category are retained. A matching audit finds 182 actor rows with repeated named coders; two slots do not automatically mean two distinct people. Removing them would change the faithful calculation. Historical reliability-package versions remain unpinned. Eight of 60 benchmark labels change under a documented newer convention, while the underlying point estimates do not. Direct independent alpha and influence-function checks support the translated calculations, not the validity of every coding decision.

## Main model comparisons

M1 is proportional-odds ordered logit for item tone. M2 and M3 are frequentist binary logits for reference outrage and recognition with independent Gaussian random intercepts for item and actor/statement within item. They use seven integration points per random intercept. Political system, socio-cultural division and media type are predictors; country and media are not random grouping levels. The table below shows published and reproduced ORs; full coefficients, SEs, intervals and fit quantities are in the ledger.

| Model | Contrast against reference | Published OR | Python OR |
|---|---|---:|---:|
| M1 | Mixed versus consensus | 1.49 | 1.487096 |
| M1 | Majoritarian versus consensus | 0.54 | 0.540495 |
| M1 | Contested versus stable secularism | 1.69 | 1.688141 |
| M1 | Website versus blog | 0.17 | 0.168464 |
| M1 | Newspaper versus blog | 0.28 | 0.281241 |
| M2 | Mixed versus consensus | 2.24 | 2.246459 |
| M2 | Majoritarian versus consensus | 0.68 | 0.678421 |
| M2 | Contested versus stable secularism | 0.88 | 0.875937 |
| M2 | Website versus blog | 0.23 | 0.230110 |
| M2 | Newspaper versus blog | 0.34 | 0.340450 |
| M3 | Mixed versus consensus | 0.94 | 0.939378 |
| M3 | Majoritarian versus consensus | 0.58 | 0.579169 |
| M3 | Contested versus stable secularism | 2.20 | 2.198739 |
| M3 | Website versus blog | 1.99 | 1.987046 |
| M3 | Newspaper versus blog | 3.28 | 3.276510 |

All 15 printed significance tiers agree. M1's five in-text OR confidence intervals agree after rounding. All ten binary AMEs and twenty interval endpoints reproduce the main article's displays. A binary OR compares conditional odds, while M1 compares cumulative odds across thresholds. Neither is a probability ratio or percentage-point difference. The AMEs are standardized probability differences under the documented prediction convention.

The M2 mixed OR rounds to 2.25 rather than 2.24. Printed b=.81 and OR=2.24 are mutually compatible at their respective rounding precision; this is not evidence of an arithmetic typo. M2 minus twice LL is 1326.556979 rather than 1326.48, a difference of .076979. M3 gives 1421.271116, agreeing with 1421.27. Numerical integration, optimization or historical build differences are possible M2 explanations. The original executable log is unavailable, so none is established as the cause.

The fitted random-intercept variances are 4.009099 and 3.248928 for M2, and 2.525380 and 1.022583 for M3, ordered as item then actor/statement. Covariance matrices, variance uncertainty, null estimates and diagnostics are retained. The article does not print corresponding variance targets, so their equality is not claimed.

## Supplementary marginal effects

The recovered official Additional Analyses table supplies 25 ordinal AMEs and 50 interval endpoints. Sixty-eight of its 75 entries agree with the predefined two-decimal rounding intervals. Seven narrowly exceed those intervals. The web tool recovered a cached primary representation; live requests returned 404, so current live availability is unverified. Values below are on the probability scale.

| Contrast and tone category | Quantity | Published | Python |
|---|---|---:|---:|
| Mixed and no outrage | Upper CI | -0.01 | -0.004590 |
| Mixed and strong outrage | AME | 0.01 | 0.004695 |
| Majoritarian and strong outrage | AME | -0.01 | -0.004545 |
| Contested and slight outrage | Lower CI | 0.02 | 0.014838 |
| Contested and strong outrage | AME | 0.01 | 0.004940 |
| Newspaper and moderate outrage | AME | -0.03 | -0.024511 |
| Newspaper and very strong outrage | AME | -0.01 | -0.004628 |

Each miss extends only .000060–.000489 beyond its rounding boundary, but it remains a discrepancy. Independent fresh statsmodels estimation and separately calculated predictions and delta intervals reproduce all 25 Python AMEs and 50 endpoints within 0.000000006. This makes a simple error in the project's margin implementation less likely. It does not identify whether the publication differences arose from historical postestimation settings, table transcription or production. Tolerances were not enlarged after observing the discrepancies.

The higher-category effects are often small, but "essentially nil" should not mean every interval includes zero. Several professional-media contrasts have small negative upper-category effects with intervals excluding zero. The complete probability vectors underlying Figures 1 and 3 are saved; graphical pixels are not exact numeric targets. Figure 2's country/media cells are also computed but not assigned invented exact publication values.

## Fit statistics and assumption checks

The item-model LL is -724.000387, agreeing with -724.00. McFadden R2 is .089014; Nagelkerke R2 is .131474. Thus Table 3's .09 McFadden label is supported numerically, while Results prose calling .09 Nagelkerke conflicts with the computed statistic. Neither is literally the percentage of outcome variance explained.

The Wolfe–Gould approximate statistic is 7.431063 with df=9 and p=.592333, reproducing 7.4, 9 and .59. This follows the author's bare numeric predictor syntax, which differs from the dummy-variable specification of M1. A non-significant diagnostic does not prove the assumption true for every relevant contrast.

The generalized-model raw LR is 22.535845, rounding to the reported 22.5. However, the unconstrained categorical model has nominal difference 15 rather than 14, information rank 22 of 24, an absent website slope and seven negative probabilities for unobserved categories. A finite regular unrestricted solution is not established. The published df=14 and p=.07 therefore cannot be certified as a regular chi-square test. Matching the raw statistic does not resolve this issue; a specific historical omission rule or typo remains unproven.

The author's alternative links preserve slope directions. Mixed-versus-consensus p changes from .03298 under logit to .14931 under probit and .01141 under complementary log-log. This qualifies the claim of similar substantive conclusions; not every significance decision is invariant. These original checks are distinct from the additional country sensitivity below.

For Note 3, the empty recognition mixed-versus-single-level LR is 91.222780, agreeing with 91.22. Outrage gives 154.763731 versus 154.95. Both random variances are zero on the null boundary, so ordinary regular chi-square calibration and the unrecovered historical mixture rule are not certified. Printed p<.000 is not a literal probability statement; any retained inferential statement needs valid calibration and reporting.

## Hypotheses and substantive interpretation

H1a receives no consistent support: majoritarian systems have significantly lower item tone outrage than consensus systems, opposite to prediction, and reference outrage is not significant. H1b's recognition comparison is not significant. H2a is supported for item tone but not reference outrage. H2b is contradicted by the significant positive recognition association. H3a and H3b are supported by the professional-media contrasts for both outrage measures and recognition. The mixed-system contrast is additional evidence, not an original directional H1 test. Non-significance does not establish an exactly zero association.

These are observational associations. Agreement across software does not demonstrate that gatekeeping, compromise or social identity salience caused them. Recognition does not distinguish ingroup from outgroup gestures, so more recognition need not show improved relations across a divide. At item level, Lebanon has more newspaper than blog outrage; the pooled media result should not be described as universal in every country and measure.

## Additional validation and sensitivity

A source/input-only isolated copy rebuilt all stages in fresh processes without loading saved estimates. It reused the installed Python environment rather than performing a fresh installation. Main coefficient tables, reliability coefficients and binary margins matched the original saved numerical payloads exactly. The clean-run receipt, commands and logs are retained. This demonstrates deterministic rerunning in this environment, not historical Stata equality.

Twelve new verification checks passed, including independent raw-data counts, a fresh M1 optimization and all ordinal AMEs/intervals, rounding-boundary behavior, unavailable-target handling, and a copied invalid-category negative test with recovery. Skill 2's independently implemented nested-likelihood integrals and observed-curvature checks supplement these checks. Fixed-parameter verification is not independent optimization of M2 or M3.

The separate S1 sensitivity deletes each country in turn, retaining M1's estimator and predictors. All six deletions were specified before fitting; none was chosen for its p value. Website ORs range .100–.208 and newspaper ORs .187–.346, with the same direction and p<.05 in all six fits. Contextual contrasts retain direction but reach p<.05 in only four of six fits each. Deletion changes the sample and target context mixture. It is an influence diagnostic, not another estimate of an identical population effect or proof of country-level causality.

## Scope and document trail

The six-country design has only one country in each political-system-by-division cell. Numerous articles do not create numerous independent institutional systems. Selected religion-related discourse, outlets and the 2015–2016 period limit generalization. Reproducing coded data does not repeat original text selection, coder training or measurement validation. Several historical software settings and unprinted vectors remain unverifiable.

Use outputs/verification/comparison_all.csv for original values, new values, differences, tolerances and evidence; docs/analysis_inventory.csv for coverage; outputs/verification/independent_checks/ for new tests; outputs/verification/sensitivity/ for S1; records/run_logs/skill3/clean_restart/ for the clean run; and records/skill3_decision_audit.md for human decisions still pending. All original data and skill 2 numerical files are preserved. Student reading, diagram ownership, personal acceptance, ID, instructor access and final release remain separate requirements.

## References

Löb, C., Rinke, E. M., Weinmann, C., & Wessler, H. (2024). Unpacking the determinants of outrage and recognition in public discourse: Insights across socio-cultural divides, political systems, and media types. The International Journal of Press/Politics, 29(1), 273–294. https://doi.org/10.1177/19401612221084206

Mediated Contestation in Comparative Perspective. (n.d.). Additional analyses for Löb et al. (2024). https://medcon-doc.github.io/documentation/content-analysis/additional-analyses/civility-outrage_paper/

Mediated Contestation in Comparative Perspective. (n.d.). Reliabilities. https://medcon-doc.github.io/documentation/content-analysis/reliabilities/

StataCorp. (2019). Stata 16 multilevel mixed-effects reference manual and postestimation documentation. https://www.stata.com/manuals16/me.pdf
