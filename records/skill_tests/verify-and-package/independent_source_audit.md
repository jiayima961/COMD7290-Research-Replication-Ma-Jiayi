# Independent primary-source audit

Date: 2026-10-19. Scope: read the original `docs/execution_specification.md` before implementation reports; inspect the article, author syntax, saved numeric results, and selected diagnostics. No models were fitted and no canonical outputs were changed. PDF page 10/Table 2 was rendered in memory and visually checked; other article passages were checked in the page-specific extraction. This is an independent audit, not student approval.

## Source agreement and omissions

At the initial audit, `outputs/comparison.csv` contained 45 comparisons: five slopes times coefficient, SE, and OR times three models. Its 44/45 rounding agreement was correct **for that restricted inventory**, not a comprehensive replication score. Table 2, sample/fit rows, significance markers, in-text confidence intervals, ten binary AMEs and their intervals, and notes 1-3 need explicit comparison entries or clearly linked narrative verdicts.

| Source target | Audit finding |
|---|---|
| Table 2, p.282 (PDF p.10) | The Australian website row visibly prints 97, 2, **11**, 0, 0, total 100. Saved data percentages are 97, 2, **1**, 0, 0. The printed cells sum to 110. This is strong evidence of an isolated publication-table error; its production origin is unknown. Other country/media row percentages agree after whole-percent rounding. Rounding can legitimately yield totals of 101, as for Swiss blogs; do not force every rounded row to sum to 100. |
| Table 3, p.283 (PDF p.11) | All 15 coefficient/SE/OR cells agree within displayed rounding. N=1,700 and LL=-724.00 agree. Every printed significance tier agrees, including contested secularism p=.001003, which belongs to ** rather than ***. The five in-text OR confidence intervals on pp.281-283 also agree after rounding. |
| Table 4, p.286 (PDF p.14) | All coefficients/SEs and nine of ten ORs agree. M2 mixed OR=2.246459 rounds to 2.25, outside the printed 2.24 interval. All significance tiers agree. N(items/actors/references)=1,183/2,453/3,770 matches. M2 -2LL=1326.556979 differs from 1326.48 by +.076979; M3=1421.271116 agrees with 1421.27. |
| Binary in-text AMEs, pp.286-287 (PDF pp.14-15) | All ten AMEs and all twenty interval endpoints round to the article. For M2, mixed=.028217, majoritarian=-.009981, contested=-.004025, website=-.047029, newspaper=-.037675. For M3, corresponding estimates are -.002821, -.021394, .028974, .020928, .043030. Rounded negative zero does not mean an exact zero effect. |
| Reference descriptives, pp.284-285 | Overall outrage 5.0928% and recognition 5.1989%, media summaries, and country summaries reproduce the stated one-decimal percentages. No population inference follows from this arithmetic agreement. |

Numeric evidence: `outputs/reproduced/descriptives/ordinal/item_tone_percent_country_media.csv`, `reference_descriptives.csv`; `outputs/reproduced/models/ordinal/ordinal_coefficients.csv`, `M1_model.json`; `outputs/reproduced/models/M2_coefficients.csv`, `M3_coefficients.csv`, and their fit JSONs; `outputs/reproduced/predictions/binary_margins_ames.csv`.

## Conflicts and attribution limits

1. **R-squared labeling conflict.** Article p.281 calls .09 Nagelkerke R-squared; Table 3 calls .09 McFadden R-squared and also includes a percent label. Using saved full LL=-724.000387, null LL=-794.744039, and N=1,700 yields McFadden=.089014 and Nagelkerke=.131474. Thus the numerical .09 supports the McFadden interpretation; retain the prose conflict explicitly. Neither statistic is literally the percentage of observed outcome variance explained. The source alone does not prove who introduced the label error.

2. **Do not declare the M2 OR a typo.** Printed b=.81 and OR=2.24 are mathematically compatible when both derive from an unrounded coefficient in their respective rounding intervals. The Python b=.809355 is simply on the other side of the OR rounding boundary. The small OR and likelihood discrepancies are consistent with numerical integration/optimization differences, but no recovered original executable log establishes their cause. Keep the M2 fit discrepancy separate from the M2 OR discrepancy.

3. **Note 1 is not fully validated.** Article p.290 reports LR=22.5, df=14, p=.07. Saved unconstrained-factor diagnostic gives raw 22.535845 but nominal df=15, rank 22 of 24, and seven negative category probabilities across observed covariate combinations (minimum -.011083). Matching the raw LR does not validate a regular chi-square test or the proportional-odds assumption. The reason for the published df=14 cannot confidently be assigned to a typo. The separate Wolfe-Gould statistic 7.431063, df=9, p=.592333 reproduces 7.4/9/.59, **under the author's bare numeric RHS**, not the indicator specification used in M1. Author code lines 90-95 preserve this distinction.

4. **Note 2 is qualified, not universally invariant.** Article p.290 says probit and complementary log-log yield very similar substantive conclusions; author code lines 138-144 defines these checks. Focal hypothesis directions persist. However, mixed-versus-consensus p=.03298 under logit changes to .14931 under probit (.01141 under complementary log-log). Do not say every significance decision survives alternative links.

5. **Note 3 retains a numerical difference and boundary caveat.** Article p.291 reports empty mixed versus single-level LR values: recognition 91.22 and outrage 154.95. Saved values are 91.222780 and 154.763731. Recognition matches; outrage does not. The latter shares M2's unresolved finite-grid issue but is not proved to arise from it. With two variances zero under the null, ordinary regular chi-square calibration is not established. Stata 16's three-level example labels its chi-square test conservative (melogit postestimation pp.11-12). Printed p<.000 is not a literal probability statement.

6. **Narrative claims need interpretation.** Article pp.283-284 describes higher-category AMEs as essentially nil: they are small in magnitude, but several exclude zero (website moderate=-2.87 percentage points, strong=-1.80). Article p.288 describes Switzerland among the highest recognition countries, whereas p.285 reports Swiss recognition=3.0%, below the USA=5.5%. This may reflect system-level aggregation, not the same country-level ordering. The article's 'average treatment effect' wording on p.286 does not establish causal identification; the computed quantities are standardized model contrasts in observational data.

## Model evidence and software equivalence

Author code line 24 specifies `version 16`; lines 48-62 recode tone and factors; lines 99-123 use proportional-odds logit and factor margins. Line 203 constructs within-item actor IDs; lines 208-222 and 260-274 fit separate nested Bernoulli-logit models with seven integration points. Country and medium are not random grouping levels. The `or` option changes display, not estimation. No robust/cluster VCE, weights, random slopes, Bayesian prior on parameters, or optimizer tuning appears.

Primary Stata 16 manuals support independent Gaussian random effects, marginal ML, default mean/variance adaptive Gauss-Hermite quadrature and observed-information inference (`memelogit`, pp.3-6); `margins` assumes random-effect marginal predictions (`memelogit postestimation`, p.4), whereas plain `predict` uses empirical-Bayes conditioning. These are substantively different estimands. Saved cached manuals and their hashes are inventoried in `outputs/diagnostics/glmm/method_source_manifest.json`.

Same likelihood family, hierarchy, predictors, and estimand establish statistical-specification equivalence. They do not establish identical finite-node grids, optimizer paths, derivatives, executable builds, or arithmetic. Python's optimizer and recursive adaptation are documented implementation choices. Existing fixed-parameter checks and higher-node comparisons support numerical reliability without identifying historical Stata internals.

Recommended bounded follow-ups: expand the comparison inventory; retain all disagreements and source conflicts; separately label alternative-link sensitivity and integration sensitivity; if an original Stata run becomes available, compare full/null likelihoods, variance components, covariance matrix, and explicit marginal predictions before blaming software. `binary_prediction_integration.csv` already shows tensor-GH7 versus high-point AME differences below .00004 probability units, far smaller than the article's .01 AME display precision. That fixed-parameter result does not prove refitted high-node coefficients are identical.

## Follow-up: recovered ordinal AME supplement

The primary [Additional Analyses page, Average Marginal Effects table](https://medcon-doc.github.io/documentation/content-analysis/additional-analyses/civility-outrage_paper/) was independently retrieved through the web tool's cached representation on 2026-10-19. The tool reported a crawl age of "2.0 years ago"; this audit did not establish current live HTTP availability or an original HTML digest. The parent audit reported live requests returned 404. No documents were rendered in this follow-up.

The table's five contrasts follow mixed, majoritarian, contested secularism, website, and newspaper; its five outcomes run from no to very strong outrage. All **75 numbers** (25 AMEs and 50 CI endpoints) were compared with `outputs/reproduced/predictions/ordinal/M1_average_marginal_effects.csv`. The rule was an absolute difference at most .005 for each two-decimal source number; signed zero was treated numerically as zero. **68 agree; seven disagree**, comprising five estimates and two interval endpoints:

| Contrast versus its baseline | Outcome | Quantity | Published | Reproduced | Distance outside source rounding interval |
|---|---|---|---:|---:|---:|
| Mixed versus consensus | No outrage | Upper CI | -.01 | -.004590240129 | .000409759871 |
| Mixed versus consensus | Strong outrage | AME | .01 | .004695478702 | .000304521298 |
| Majoritarian versus consensus | Strong outrage | AME | -.01 | -.004544912315 | .000455087685 |
| Contested versus stable secularism | Slight outrage | Lower CI | .02 | .014837859194 | .000162140806 |
| Contested versus stable secularism | Strong outrage | AME | .01 | .004940434748 | .000059565252 |
| Newspaper versus blog | Moderate outrage | AME | -.03 | -.024511280637 | .000488719363 |
| Newspaper versus blog | Very strong outrage | AME | -.01 | -.004627995357 | .000372004643 |

These narrowly miss rounding boundaries; none is an exact-boundary tie. They preserve effect directions and do not establish a changed significance decision. Source cells printed with a zero endpoint are insufficient to recover that decision independently. No recovered original margins log establishes whether manual or repeated rounding, different saved estimates, standardization, or another step produced the differences. Binary-model quadrature cannot by itself explain discrepancies in this ordinal M1 table. Retain the seven discrepancies instead of enlarging the display tolerance or declaring them typos. No fitting or canonical-result edits were performed.
