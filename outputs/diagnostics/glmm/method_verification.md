# Independent GLMM method and numerical verification

This is an AI-authored independent implementation check for the D011 Python-only reproduction. It does not certify original Stata executable equivalence, student review, or substantive specification sensitivity. No Stata executable was run. The reference writer did not fit the full study models or use published estimates to choose fixture parameters.

## Source-bound model and defaults

The author `MedCon_Civility_an.do` declares `version 16`, generates `act_id` from `text_id` and `akteur_id`, and fits separate reference outrage and recognition models with `|| text_id: || act_id:, intpoints(7)`. The full model adds `i.polsys i.socdiv i.mediatype`; each intercept-only null model uses the same hierarchy. The `or` option affects reporting.

| Convention | Primary source and locator | Finding |
|---|---|---|
| Conditional response / random effects | [Stata 16 melogit](https://www.stata.com/manuals16/memelogit.pdf), description and methods pp.1,7-8,22 | Bernoulli/logit conditional response, mean-zero Gaussian random effects; marginal maximum likelihood. |
| Random-effect covariance | Same, pp.4-5 | Default `covariance(independent)`. Here there is one random intercept at each nested level. |
| Estimation quadrature | Same pp.4,6; [Stata 16 meglm](https://www.stata.com/manuals16/memeglm.pdf), pp.7-8,26-28 | Default `mvaghermite` for nested models; seven points per random-effect level. Posterior mean/variance adaptation, initially zero mean and identity covariance; posterior orthogonalizing transformation is part of the documented formula. |
| Fixed-effect / variance covariance estimate | melogit pp.5-6 and meglm p.6 describe `vce(oim)` as the ordinary information-based choice; no robust/cluster option appears in author syntax | The candidate uses the inverse observed Hessian of its evaluated likelihood. The original internal transformed parameterization and exact derivative implementation are not recovered. |
| Optimizer | [Stata 16 maximize](https://www.stata.com/manuals16/rmaximize.pdf), pp.2-3 | General default Newton-Raphson, maximum300 iterations. General non-`ml` defaults are coefficient tolerance1e-6, log-likelihood tolerance1e-7 and scaled-gradient tolerance1e-5; `ml` defaults differ (1e-4 and0). The public melogit entry does not pin every internal override; these are documented general defaults, not a reproduced executable trace. |
| Inner adaptation stopping | Stata16 meglm pp.27-28 | Iterative moment updating is documented, but its internal stopping tolerance, damping, reuse of grids and precise hierarchical implementation are not exposed here. Candidate tolerance/damping/iteration limits must be recorded as Python implementation choices. |
| Bare `margins` prediction | [Stata 16 melogit postestimation](https://www.stata.com/manuals16/memelogitpostestimation.pdf), p.4 | Default mean response; `marginal` is assumed unless fixed-only specified. Empirical Bayes means/modes are disallowed with margins. |
| Random-effect integration for prediction | [Stata 16 meglm postestimation](https://www.stata.com/manuals16/memeglmpostestimation.pdf), pp.4-5 | Integrate the prediction over all random effects. Prediction quadrature points default to estimation value. Plain `predict` has a different conditional empirical-Bayes default; do not transfer it to bare `margins`. |
| Margins uncertainty | [Stata 16 margins](https://www.stata.com/manuals16/rmargins.pdf), pp.7,10,54 | Delta method by default, conditional on observed covariates; use full model covariance and derivative vector. Standard normal confidence intervals apply here. |

Exact official Stata16 PDFs were downloaded successfully despite the web reader being unable to open the direct URLs. Their original local files and SHA256 hashes are retained in `tmp/skill2_forward/glmm_verification/document_downloads.json`; the root's meglm16 hash is in `tmp/skill2_methods_download.json`. Downloads use no Stata licence or execution. Original executable build/update date is unpinned by `version 16`.

## Likelihood and verification target

For item j, actor a has n_ja Bernoulli rows and s_ja successes, with common fixed predictor eta_j. Let u and v be independent standard normals and sd_I and sd_A the item and actor standard deviations. The exact item contribution is

`L_j = integral phi(u) product_a [integral phi(v) exp{s_ja*(eta_j+sd_I*u+sd_A*v) - n_ja*log(1+exp(eta_j+sd_I*u+sd_A*v))} dv] du`.

The total row log likelihood is `sum_j log(L_j)`. There is no binomial combinatorial coefficient when grouping identical Bernoulli rows for calculation. Adding it would change reported log likelihood and information criteria. Sorting actor counts or combining identical item patterns with integer frequencies preserves this likelihood.

The reference implementation uses SciPy QUADPACK independently for each inner and outer integral over [-12,12] standard deviations (epsabs2e-13, epsrel2e-11). Since each conditional probability product is between0 and1, omitted normal-tail mass supplies a rigorous truncation bound. QUADPACK numerical errors are estimates, not certified bounds; inner errors are propagated conservatively as the sum of sampled maxima. A separate nonadaptive GH81/GH161 calculation agrees to a maximum likelihood difference1.23e-15 across the16 fixtures. Known reductions cover zero variances, a single actor's summed variances, and a symmetric single Bernoulli observation with probability1/2.

Real-data fixtures were selected only by hierarchy structure: a singleton, the first two-actor item, an item attaining the maximum reference count, and an item attaining the maximum actor count. Both outcomes are checked at arbitrary beta `[-1.4,0.2,-0.35,0.45,-0.1,0.3]`, item variance0.7 and actor variance1.3. These values are unrelated to candidate fits or printed targets.

## Hierarchical quadrature equivalence limit

Recursive integration is source supported. [Rabe-Hesketh, Skrondal and Pickles (2002)](https://journals.sagepub.com/doi/pdf/10.1177/1536867X0200200101), eqs.3-4 and pp.7-8, describes levelwise recursion and distinguishes computationally costly conditional moment adaptation from adaptation after posterior orthogonalization. This is methodological evidence, not proof of every Stata16 implementation detail.

The candidate implements conditional actor posterior mean/SD adaptation at every item node, followed by item posterior mean/SD adaptation. It is a valid numerical route to the same exact marginal likelihood. Public Stata16 formulas do not establish that this is the identical original finite seven-point grid. A small full-joint moment/Cholesky implementation in the reference is an alternate grid illustration, not an asserted reconstruction of Stata's hierarchical executable. It differs from the recursive seven-point result on three fixtures, so quadrature labels alone do not prove finite-grid equality. Do not infer that Stata exhaustively evaluates a full joint grid over all actors: hierarchical structure can be exploited.

The candidate's seven-point configuration remains distinct from higher-point numerical integration checks. Source/default recovery, same-model likelihood validation, numerical integration error, optimizer convergence, agreement with published estimates, and exact executable equivalence are separate claims.

## Prediction and confidence intervals

Under this random-intercept model the exact population probability is `E[expit(x beta + sqrt(var_I+var_A)*z)]` for standard normal z. Predictive margins set the requested factor category for every estimation row and average those probabilities using the reference-row empirical covariate distribution. A factor AME is the average category-versus-base discrete difference, not a continuous derivative. For covariance V of all fixed and variance parameters, delta SE is `sqrt(g' V g)`; numerical derivatives must include variance components. Margins and AMEs use estimate +/-1.95996398454*SE on their reported probability/difference scale.

An exact Gaussian-sum reduction does not prove finite-node equivalence. At eta=-1.4, variances0.7 and1.3, the independent integral is0.2630961531094776; combined-variance one-dimensional GH7 is0.2631499364543992 and separate-intercept tensor GH7 is0.2630966633811648. The original internal marginal prediction grid is not pinned by the inspected manuals. Record the Python choice and its higher-point check explicitly.

## Executable checks and outputs

From the repository root:

```powershell
rtk proxy .\.venv\Scripts\python.exe tests/skill2/glmm_reference.py
rtk proxy .\.venv\Scripts\python.exe tests/skill2/check_nested_logit.py
rtk proxy .\.venv\Scripts\python.exe tests/skill2/check_glmm_full_likelihood.py
```

The first command regenerates independent fixed-parameter references. The second imports the current production engine, binds its SHA256, checks7/11/21-point results, contrasts integrated scores with finite differences of the evaluated target on a mixed fixture, and verifies frequency compression and row-order invariance. The third independently reconstructs all item/actor counts from unchanged raw data and compares full-data fixed-parameter likelihoods with GH81/GH161/GH241, supplemented by QUADPACK contributions. All write only under `outputs/diagnostics/glmm/`. To check an existing fitted parameter vector without optimization, use the third command with `--fit <path-to-fit-json>`. Final-fit checks require separate subsequent evidence and are not implied by the arbitrary-parameter fixtures.

The final candidate source checked at this stage has SHA256 `ab8c609c131888d2a90b13737841fb6f6a636172a3cf669c3c8a76d8529c57e8`. Across16 fixtures, maximum absolute item log-likelihood errors versus independent integration at7/11/21 points are7.7573e-5,1.2862e-6,2.3185e-10. On the mixed fixture, the integrated score differs from the finite derivative of the adaptive approximate target by1.666e-5 at7 points and3.740e-11 at21 points; the candidate's numerical-derivative polish is therefore material.

At the arbitrary real-data vector above, independent full log likelihoods are -1256.8184911020662 (outrage) and -1269.761749615902 (recognition). GH161-to-GH241 changes are below1.9e-12 and selected QUADPACK item log-likelihood differences below2.3e-15. Candidate cumulative errors are approximately +0.00970/+0.00976 at7 points, -0.000103/-0.000102 at11 points and -1.9e-8 at21 points. These quantify finite-grid integration error at one vector; they are not estimates of fitted-coefficient error.

An initial fixture serialization tried to convert string `text_id` to float and failed before results were saved; it was corrected to preserve the author string. An attempted inline promotion command failed shell quoting before execution; promotion was rerun from a saved Python file. Obsolete checks loaded before a damping performance change were interrupted and replaced; redundant score Jacobians were restricted to the mixed fixture. Process-inventory attempts were unavailable under local Windows permissions and were not escalated. None changed source data or candidate code.
