TEST ARTIFACT — source-based AI reconstruction; real student review pending.

# Design and analytical specification

Specification version: forward-test-1.0.1. All inference, reliability estimation, engine validation and human acceptance remain pending. The study is one comparative content-analysis study with two observation levels and three separate main models, not three independent studies.

## How observations were produced

The question is the public role of religion. Country selection crosses majoritarian (Australia stable, USA contested), mixed (Germany stable, Turkey contested) and consensus (Switzerland stable, Lebanon contested) systems. The design selects country categories; it does not randomly assign them. An expert survey (136 of 467 contacted; January 15–March 15, 2015) informed reach and opinion-leadership selection of at least two daily newspapers, five news websites and five blogs per country. Content from August 2015–July 2016 was purchased or crawled. Expert-informed topic modeling ranked candidate relevant articles, followed by manual validation until desired country/media quotas were reached. This is not a simple random sample of all national public discourse. [Article](../sources/local/Lob_et_al_2024.pdf), pp.279–280.

There are 1,700 items. Country/media cells usually contain 100, with Swiss blogs 27, Lebanese blogs 78 and Turkish blogs 95 (Table 2, p.282). The shared actor-reference file contains 3,770 reference rows within 1,183 item IDs. Table 4 reports 2,453 actors. These are prepared analytical files: the process from collected texts through all selection and coder data is not fully recreated here. Items absent from the actor-reference file must not be inserted as zero-valued references. Exact selection into that file and actor group count need an implementation audit, not an invented attrition account.

The article reports trained (near-)native coders in German and another source language, complete double coding, coder rotation and consensus adjudication of disagreements. The codebooks define an item-level actor list, placing the author first and distinguishing identifiable individuals and organized collectives (cb02 PDF pp.3–5). Actor characteristics are coded at publication time (cb05 §5.1, PDF pp.3–5). A reference is a directed originator–object constellation evaluated across the article, not necessarily every sentence or every mention (cb08 §8, PDF pp.3–5). The paper calls the intermediate grouping actor statements; code builds it from item ID and within-item actor code. Exact alignment of this grouping to original originator coding remains a check for skill 2. Country and media type are contextual categories, not random-effect levels.

Independent rating workbooks preserve rater-specific responses; consensus analytical DTA outcomes are a different product. The article's claim that adjudication removed major systematic error is an author interpretation, not a guarantee adopted here. No raw text recoding or new human data collection is authorized. Local originals stay unmodified and local; no additional corpus-access or redistribution permission is inferred from file possession.

## Variables, bases and fixed design vector

Use the author transformations in a separate prepared file: tone_raw−1; polsys raw 1/2/3→1/3/2; socdiv raw 1/2→2/1; mediatype raw 1/2/3→1/3/2. Verified DTA labels fix the meanings. After recoding, the fixed-effect vector x is [I(Mixed), I(Majoritarian), I(Contested secularism), I(News website), I(Newspaper)]. Bases are Consensus, Stable secularism and Blog. No pooling of newspapers and websites, interaction, extra country dummy, centering, z score, techcon/profor control or measured mediator is present in the main model syntax. All raw coded fields are inventoried in variable_dictionary.csv, with nonmodel metadata explicitly separated.

The focal archive fields have no system/extended missing values according to the metadata/read-only checks. Binary zero means absence, not missing. The PDF's recognition/outrage category tables use 1 No/2 Yes while examples use 1 Yes; valence and responsiveness have further contradictions and different archive domains. Preserve prepared binary fields, record their intended meanings, and do not infer an unobserved recode from integer order. The source code does not document their upstream creation. Codes −99 for unclear in other variables remain distinct. Estimation-time sample exclusions, if any, must be reported by skill 2.

## Equations and likelihoods

**M1, item tone (ordinal 0–4).** For k=0,1,2,3, logit Pr(Y_i≤k|x_i)=κ_k−x_iβ_1, with κ_0<κ_1<κ_2<κ_3. Set κ_−1=−∞ and κ_4=+∞. Category probability is F(κ_y−xβ_1)−F(κ_(y−1)−xβ_1), with F logistic; L_1 is the product over items of those probabilities. There is no separate intercept in xβ_1 because thresholds identify the location. A positive β raises the odds of being beyond each threshold. exp(β) is a common cumulative odds ratio, not a change of β units in tone. The model assumes proportional odds and conditional independence across items; possible outlet/country dependence is a limitation of this original specification.

Original syntax: `ologit tone i.polsys i.socdiv i.mediatype, or` (analysis_code lines 99 onward). No random intercept is fitted. H1a, H2a and the two H3a contrasts map to this model.

**M2/M3, directed references.** Let r be a reference, a its within-item originating actor/statement group, and j its news item. For q=2 (outrage) and q=3 (recognition), separately:

Y_raj^(q)|u_j^(q),v_aj^(q),x_j ~ Bernoulli(p_raj^(q)); logit(p_raj^(q))=α_q+x_jβ_q+u_j^(q)+v_aj^(q).

The scalar random intercepts have u_j^(q)~N(0,τ_item,q²) and v_aj^(q)~N(0,τ_actor,q²), independent across groups and between the two random-effect levels within a model. Conditional on these effects, reference outcomes are independent. Common slopes and independence of effects from predictors are distributional/model assumptions, not observed facts. Each outcome's marginal likelihood integrates its product of conditional Bernoulli probabilities over its item and nested actor intercept distributions. Specifically L_q=∏_j∫φ(u_j;0,τ_item,q²) ∏_a[∫φ(v_aj;0,τ_actor,q²)∏_r p_raj^y(1−p_raj)^(1−y)dv_aj]du_j.

Original ID syntax: `egen act_id = concat(text_id akteur_id), punct(_)`.

Original estimation syntax (separate calls):

```stata
melogit actrefoutbin i.polsys i.socdiv i.mediatype || text_id: || act_id: , intpoints(7) or
melogit actrefrecbin i.polsys i.socdiv i.mediatype || text_id: || act_id: , intpoints(7) or
```

exp(β_q) compares conditional odds at equal random intercepts. Each model has its own two variances and intercept, and does not estimate covariance between outrage and recognition. The codebook's mutually exclusive reference outcomes do not license treating them as independent outcomes in a joint likelihood; no joint likelihood is proposed. Marginal probabilities differ from conditional odds ratios. The simpler single-level logit drops the actor/item heterogeneity and conditional dependence modeled here.

## Original settings and unresolved defaults

The script is dated April 24, 2021 and declares Stata language `version 16`. It explicitly uses seven integration points for all empty/full mixed logits, reports odds ratios and repeats coefficient fits before margins. It does not pin the installed Stata build or add-on versions (gologit2, omodel, blindschemes, grc1leg2), integration method, optimizer, tolerances, iteration cap or starts. The likelihood families and normal random-intercept defaults above reconstruct the original commands; Python/Stata numerical equivalence and default auditing are explicitly deferred under I1; I1 is distinct from independent statistical verification V1. There are no priors or sampling chains in this frequentist syntax. Weights, robust/cluster variance options, interactions, standardization, lags and indirect-effect parameters are absent. Model-based standard errors are implied, but exact interval construction needs runtime confirmation; article CIs and marginsplot request 95%.

## Diagnostics, supplementary targets and interpretation

C1 compares gologit2 `npl` and `pl` models through LR test (five factor coefficients; published df=14). C1's second diagnostic preserves `omodel logit tone polsys socdiv mediatype` exactly, including its numeric rather than factor RHS (published df=9). It therefore must not be reported as automatically testing the identical factor design. Wolfe and Gould pp.24–27 explain the approximate test and warn that a nonsignificant result is not a goodness-of-fit certificate. C2 preserves proportional logit, probit and complementary log-log sensitivity. No diagnostic was executed here.

C3 records separate empty mixed logits, actor/item latent-scale ICCs and the published comparison with single-level null models; the supplied script does not include the explicit single-level LR commands. Variance-component nulls lie at a boundary, so their reference distribution requires review. For a logistic latent-scale convention, total latent variance is τ_item²+τ_actor²+π²/3: different actors in one item share τ_item²/total, and references in the same actor group share (τ_item²+τ_actor²)/total. These are latent-scale summaries, not the fraction of observed binary variance explained. F1 retains fit/ICC/pseudo-R² summaries separately. AIC=−2LL+2K penalizes parameter count; −2LL alone is not a model quality ranking across different outcomes or samples. Article p.281 calls .09 Nagelkerke R² whereas Table 3 labels it McFadden R²; do not silently equate these.

P1/P2 retain `margins polsys`, `margins socdiv`, `margins mediatype` and corresponding `margins, dydx(...)`. Conceptually compare category-specific predictions averaged over the observed covariates; factors imply discrete changes from bases. M1 requires all five outcome probabilities. M2/M3 require the precise Stata random-effect prediction convention, integration and interval method to be established in skill 2 because no `predict()` is supplied. An average marginal effect from this observational design is an adjusted probability contrast; the article's phrase “average treatment effect” does not establish causality.

Reliability R1/R2 use separate original rater files. `kappaetc` specifies identity weights, conditional SE, 95% intervals, probabilistic benchmarks and showscale; run coders 1/2 and all raters, with Ton_1–Ton_4 for tone and the recognition/outrage/valence/responsiveness families for references. Do not substitute ordinal weights without separately labeling a sensitivity analysis. Python handling of unmatched raters, blanks, special codes and Stata-import placeholders Q/AG/AW/BM/CC is unresolved. No agreement coefficient was computed here.

## Assignment checks and separate sensitivity

Post-review coverage correction, version forward-test-1.0.1: stable IDs now follow canonical skill contract1.0.1. C1 covers both original proportional-odds diagnostics with separate matrix rows C1_factor_lr and C1_numeric_approx_lr; C2 covers original alternative links; C3 covers null multilevel comparisons; A1 inventories supplementary access/coverage. F1 retains fit/variance summaries, I1 defers software equivalence, and E1 retains exploration. The initial blind iteration and its missed semantic coverage are preserved in records/iterations/initial/.

**V1 — independent statistical verification (not_run).** The assignment p.10 requires both an important descriptive quantity and a core advanced-model numerical quantity, independently implemented. Plan a reviewer calculation of count(actrefoutbin=1)/N from permitted original data independently of the implementer's D2 pipeline. Separately plan an independent implementation of the full M2 nested integrated Bernoulli log likelihood and score at a reviewed full-fit parameter vector, with the same two normal intercept levels and covariate design. The future reviewer must justify quadrature accuracy and comparison tolerances before evaluation. This is a central likelihood check, not another model chat or an environment/version check; its scope will not certify the entire model. No counting, likelihood calculation or verification is executed here; exact design awaits the appropriate later task and student review.

**N1 — statistical negative check and recovery (not_run).** Plan a disposable copied/synthetic statistical input with tone_analysis=5 outside the approved0–4 domain. The later data checks must reject it with the field/row identified, then pass after restoration, while original data and final outputs remain untouched and source hashes match. This failure/detection/recovery target comes from assignment pp.9–10. The canonical skill validator and output-file consistency checks performed here do not complete this statistical-input task.

**S1 — additional sensitivity (not_run).** After faithful reproduction and student review, a proposed separate leave-one-country-out influence analysis would retain each original model family,reference coding and nested hierarchy while omitting each country in turn. It would report all contextual estimates,uncertainty and largest absolute changes relative to the faithful fits. Article p.289 motivates this through the six-country,one-case-per-design-cell limitation; assignment p.13 requires a justified sensitivity beyond the original reproduction. Deleting a country changes the sampled population and estimand; this probes dependence on individual contexts and does not remedy country confounding. It is not the original C2 alternative-link analysis, and no preferred-significance selection or new causal claim is planned. Exact design and tolerances remain pending student review; no fits are authorized here.

## Traceability and review

Figure 1 is original AI-assisted Mermaid in model_diagram.mmd. The node map connects each observed predictor/outcome/variance to equations, M1–M3 and exact hypothesis row IDs; planned scripts do not exist and must not be described as executed. hypothesis_matrix.csv covers 12 directional targets and every inventory target; published_comparison_targets.csv contains source-transcribed comparison values only. Results remain not_run. student_review.md leaves the real student's map, reading notes, scientific decisions and acceptance blank/pending. This test does not approve estimation or complete skills 2/3.
