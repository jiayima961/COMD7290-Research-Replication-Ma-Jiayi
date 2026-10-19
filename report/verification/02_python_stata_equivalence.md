# Justification for reproducing Stata analyses in Python

Prepared for Ma Jiayi and the COMD7290 instructor on 19 October 2026. This AI-assisted methods statement accompanies the complete comparison report. It documents what is equivalent, how that was checked, and what remains unconfirmed.

## Basis for the software choice

The assignment explicitly permits switching statistical engines when statistical equivalence is documented (assignment p.7). Python was chosen to check whether the published analysis can be reproduced outside Stata and to make the likelihood and validation code inspectable. The user authorized this route and the project-local installation. This is a computational reproduction of the author-provided coded data, not new data collection or an independent replication of coding.

A statistical model is defined by its outcome distribution, predictors, observation structure, likelihood, estimator and target quantity. A software brand does not define it. Replacing the engine is defensible when these elements are preserved, transformations and defaults are explicit, and independent checks support the implementation. Merely using a similarly named command, matching p-value signs or obtaining a plausible table is insufficient. Numerical approximation and software-build equality require separate evidence.

## Original and reproduced specifications

The author's dated syntax specifies version 16. The original executable build and numerical logs were not recovered. The script's explicit settings take precedence over guesses about defaults. Stata was not run for this project.

| Component | Original target retained in Python |
|---|---|
| Samples and recodes | Same DTA/XLSX inputs with hashes; tone 1–5 to 0–4; author factor recodes; consensus, stable secularism and blogs as reference groups |
| M1 | Unweighted proportional-odds ordered-logit maximum likelihood; five dummy slopes and four ordered cutpoints; observed-information covariance and normal intervals |
| M2 and M3 | Separate Bernoulli/logit marginal maximum-likelihood models; fixed intercept plus five dummy slopes; independent Gaussian random intercepts for items and actor/statement groups nested within items |
| Integration | Seven quadrature points per random intercept; recursive mean/variance adaptive Gauss–Hermite implementation; null fits preserve the same hierarchy and setting |
| Probability summaries | Sample-standardized predictions, setting each focal category across estimation rows; binary predictions integrate over the random-effects distribution; discrete contrasts and full-covariance delta intervals |
| Reliability | Author-selected independent-rating slots and transformations; six identity-weight coefficients; conditional uncertainty and version-specific benchmark conventions documented separately |
| Author diagnostics | Bare-numeric Wolfe–Gould syntax, generalized categorical check and original alternative links retained; invalid inference reported visibly |

M1 uses P(Y ≤ j given x) = logistic(cutpoint j minus x beta), with common slopes across its four thresholds. M2/M3 use logit P(Y=1 given x, item effect, actor effect) = x beta plus item effect plus nested actor effect. Their likelihood integrates the Bernoulli product over both independent normal random-effect distributions. These are frequentist marginal likelihoods; Gaussian random-effect distributions are not Bayesian priors on the regression parameters.

The binary hierarchy is reference to actor/statement to item. It is not a country-to-media-to-item hierarchy. An ordinary logistic regression, a linear mixed model, a single random intercept or a Bayesian substitute would change the model. None replaces the faithful primary fits. The author's OR display option changes reporting, not estimation. No weights, clustered/robust covariance, random slopes or tuning options absent from the source were silently added.

## Implementation and independent evidence

The Python likelihoods use NumPy/SciPy, explicit recoding and recorded version pins. The ordered model supplies analytic derivatives; independent statsmodels estimation uses a different parameterization. Binary fitting uses an integrated-score warmup followed by optimization of the actual adaptive-quadrature target, with observed-information covariance. Final gradients and Hessian stability are checked rather than accepting the warmup message. These numerical algorithms are documented choices, not claims to reproduce Stata's undisclosed optimizer trajectory.

Validation has several distinct levels. Input checks establish exact source hashes, categories, cross-file joins and nesting. Independent raw readers confirm key counts and a disputed Table 2 percentage. Independent ordered-logit optimization recovers M1, and separately computed standardized probabilities, finite-difference gradients and covariance propagation recover all 25 ordinal AMEs and their 50 interval endpoints within 0.000000006. The earlier checks independently evaluate nested binary likelihoods at arbitrary and fitted parameters, compare integration approximations and examine curvature and step-size stability. They do not independently reoptimize M2/M3 in another engine.

The original 45 slope/SE/OR cells yield 44 display agreements. All five M1 OR intervals, all printed significance tiers, and all ten binary AMEs with their twenty interval endpoints agree at printed precision. Thirty published reliability coefficients and five sample sizes agree. A complete source/input-only rerun in fresh processes reproduces saved main tables exactly, using the existing environment. This is direct evidence of reproducibility within the documented Python environment.

## Equivalence limits

The same continuous likelihood and the same number of quadrature points do not guarantee the same finite-node adaptive grids. Historical Stata executable builds, optimizer stopping tolerances, numerical derivatives, adaptation internals and some prediction implementation details are unpinned. The original reliability add-on version and generalized-model omission rules are also unknown. Contemporary source snapshots document methods, not the authors' exact installed binaries.

The M2 mixed OR is 2.246459 rather than a value rounding to 2.24; M2 minus twice LL is 1326.556979 rather than 1326.48; and its empty-model LR differs from the printed value. Seven supplementary ordinal AME or interval cells narrowly miss the printed rounding intervals despite independent Python confirmation. These differences are retained. They cannot all be attributed to Stata-versus-Python numerical integration: M1 has no random-effects integration, and source table production is another possibility. Conversely, a small difference is not proof of a publication error.

The generalized ordinal assumption check has structural nonidentification and invalid unobserved-category probabilities. Its raw LR rounds to the article's number, but that does not validate the reported degrees of freedom or p value. This remains a model-diagnostic limitation rather than an engine-equivalence success. Boundary variance tests also need suitable calibration. No global claim of complete historical numerical equivalence is made.

## Appropriate conclusion and reporting language

The statistical specification is preserved, and substantial numerical agreement is demonstrated. This supports using Python for the assignment's computational reproduction with explicit limits, subject to the instructor's assessment. It does not prove every historical Stata quantity identical. Resolving the remaining computational discrepancies would require the original Stata build/logs, full parameter and covariance output, explicit integration options and prediction convention, followed by a direct comparison without changing the scientific specification.

Agreement between engines addresses implementation dependence under one specification. It does not establish causal identification, coding validity or general robustness. The separately labelled country-deletion sensitivity changes the sample and estimand and therefore answers a different influence question. Original alternative-link checks and numerical quadrature checks are reported separately. The student's final acceptance and personal understanding remain required.

## Sources and reproducibility records

COMD7290 assignment, p.7 and pp.10–13; author syntax sources/author_code/MedCon_Civility_an.do; docs/execution_specification.md; environment.md; requirements-lock.txt; outputs/diagnostics/glmm/method_source_manifest.json; records/run_logs/skill3/clean_restart/receipt.json; and outputs/verification/comparison_all.csv.

Löb, C., Rinke, E. M., Weinmann, C., & Wessler, H. (2024). Unpacking the determinants of outrage and recognition in public discourse: Insights across socio-cultural divides, political systems, and media types. The International Journal of Press/Politics, 29(1), 273–294. https://doi.org/10.1177/19401612221084206

StataCorp. (2019). Stata 16 melogit documentation. https://www.stata.com/manuals16/memelogit.pdf

StataCorp. (2019). Stata 16 melogit postestimation documentation. https://www.stata.com/manuals16/memelogitpostestimation.pdf

StataCorp. (2019). Stata 16 meglm postestimation documentation. https://www.stata.com/manuals16/memeglmpostestimation.pdf
