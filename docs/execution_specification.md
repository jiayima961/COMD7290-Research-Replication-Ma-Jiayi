# Source-bound Python execution specification

Version: source-faithful-python-1.0.0. Authorized by the student's explicit skill-2 request on 2026-10-18. This is a retrospective computational replication, not a preregistration. Human reading notes and a student-created diagram remain separate unfinished course tasks.

## Frozen substantive specification

Original inputs are bound by `records/source_manifest.csv`; prepared hashes and sample checks are in `outputs/diagnostics/data_audit.json`. Preserve author-prepared analytical data and independent reliability workbooks separately. Do not edit original files or select models by agreement with published coefficients.

Author syntax: `sources/author_code/MedCon_Civility_an.do`. Tone is recoded 1–5 to 0–4. Political-system codes map 1/2/3 to 1/3/2, secularism 1/2 to 2/1, and media 1/2/3 to 1/3/2. Baselines are consensus, stable secularism and blogs. Models use five category indicators, not linear trends in category numbers.

| Target | Exact statistical specification |
|---|---|
| M1 | Proportional-odds cumulative logistic model; four thresholds, five fixed slopes; maximum likelihood and observed-information covariance |
| M2 | Bernoulli logit for explicit actor-reference outrage; six fixed coefficients including intercept; independent Gaussian item and within-item actor random intercepts |
| M3 | Same nested model for explicit actor-reference recognition, fitted separately |
| Empty models | Same M2/M3 outcome, hierarchy and integration, intercept only |
| Reliability | Original independently coded columns, author-selected rater subsets, identity weights, conditional SEs, 95% intervals and probabilistic benchmarking; exact mapping/audits retained with results |
| Original checks | Generalized ordered-logit comparison; Wolfe–Gould test with the author's bare numeric RHS; proportional probit and complementary log-log alternatives |
| Predictions | Average over the observed analysis rows, changing one category; discrete changes against its reference. Binary predictions integrate over the prior random-effect distribution, with variance-parameter uncertainty included |

For M2/M3, references nest within originating actor/statement groups within items. Country and medium are fixed contextual predictors, not random grouping levels. Variance parameters are fitted by frequentist marginal maximum likelihood. Seven quadrature points per random-intercept dimension are retained in the configured primary calculation.

## Numerical settings and equivalence boundary

Stata `version 16` is a compatibility statement, not a pinned original executable build. The source omits explicit integration method, optimizer settings and prediction integration details. Stata 16 documentation identifies mean/variance adaptive Gauss–Hermite as the fitting default and prior-marginal predictions as the margins convention. Recovered primary documentation and independent checks are retained in the method records.

The Python engine uses recursive posterior mean/variance adaptation and seven nodes per dimension, a score-based BFGS starting search, then finite-difference BFGS refinement of the actual quadrature target. Observed-information covariance is calculated numerically. Optimizer implementation and convergence tolerances are explicitly Python implementation choices, not recovered author settings. No claim of identical internal Stata arithmetic is made. Damping changes the path to the adaptation fixed point, not the selected model.

Different adaptive-node constructions can have different finite-seven-node likelihoods despite estimating the same continuous model. Fixed-parameter independent integration checks and higher-node checks must accompany the model results. The primary binary prediction calculation explicitly uses tensor GH7; combined-normal GH7 and high-point predictions are saved as numerical comparisons because the historical prediction grid reduction is not fully documented.

Source-model fidelity, numerical convergence, agreement within printed rounding, and sensitivity to numerical integration are distinct checks. Passing one does not imply all others. Failed or nonidentified assumption diagnostics stay visible and cannot be used as ordinary valid chi-square tests.

## Hypothesis decisions

H1a: positive majoritarian slope in M1/M2; H1b: negative majoritarian slope in M3. H2a: positive contested slope in M1/M2; H2b: negative contested slope in M3. H3a: negative website and newspaper slopes in each of M1/M2; H3b: positive website and newspaper slopes in M3. These are 12 directional targets. Mixed-system coefficients are additional comparisons. Report coefficients, uncertainty and direction; do not rewrite the original prediction after observing its result.

Cross-software agreement establishes computational reproducibility under a specification. It does not by itself establish causal identification, coding validity, or robustness to all reasonable specifications.
