# Python route assessment

Historical feasibility assessment retained from before skill-2 execution.
Current calculations and remaining numerical-equivalence limits are documented
in `docs/replication_results.md` and `docs/execution_specification.md` from the
repository root. For current setup, use `docs/guides/teacher_quickstart.md`.

Assessed 2026-10-18. This is a feasibility assessment, not a completed reproduction or approval of a model specification.

## What the original authors used

The article's main text does not explicitly name the statistical software version. Its method section names Angrist as the coding tool, which is distinct from the statistical analysis engine. The clearest statistical-software evidence is the official reproduction code. `sources/author_code/MedCon_Civility_an.do`, dated 2021-04-24, specifies `version 16` at line 24. It uses Stata's `ologit`, `gologit2`, `omodel`, `melogit`, `margins`, and plotting commands. The separate reliability script also specifies `version 16` and requires `kappaetc`. A Stata compatibility declaration establishes the code's intended version; it does not identify the exact executable build originally used.

The code's multilevel fits contain two random-intercept grouping levels, `text_id` and a within-item actor identifier, above the binary actor-reference observations. The code specifies `intpoints(7)`. These are three-level binary logistic models, not ordinary binary logistic regressions.

The assignment, page 7, permits Python and other engines, but accepts a software change only with documented statistical equivalence. A notebook is the interface for reading explanations and executing cells; it does not determine the statistical estimator.

## Coverage and limits of the proposed foundation

| Task | Python foundation | Remaining verification |
| --- | --- | --- |
| Read author Stata files and value labels | `pandas`, `pyreadstat` | Preserve raw numeric values, labels, extended missing values, identifiers and source hashes. |
| Read independent-coder Excel files | `pandas`, `openpyxl` | Check sheets, matched units, coder columns, missingness and original script's path mappings. |
| Cleaning, descriptive summaries and charts | `numpy`, `pandas`, `scipy`, `matplotlib`, `seaborn` | Match analytical samples, category ordering and summary conventions. |
| Proportional-odds ordered logit | `statsmodels` `OrderedModel` | Match categorical reference groups, threshold parameterization, likelihood, covariance and predictions. Installation alone establishes none of these. |
| Ordered probit and complementary-log-log checks | `OrderedModel` supports logit/probit and custom continuous distributions | Check the complementary-log-log direction and parameterization against the author's `gologit2` implementation before using a custom distribution. |
| Proportional-odds diagnostics | Numerical and likelihood foundations are available | Reimplement and validate the particular `gologit2` likelihood-ratio and `omodel` checks; separate binary regressions are not automatically the same test. |
| Krippendorff alpha | `krippendorff` | Reconstruct original independent ratings and units; match the author's identity weights, corresponding to nominal disagreement for alpha, rather than silently changing to ordinal weights. |
| Complete `kappaetc` output | Only part is covered by the initial package set | Other agreement coefficients, multiple-rater conventions, conditional standard errors and confidence intervals still need validated implementations or the original engine. |
| Three-level binary random-intercept logistic fits | No equivalent implementation has yet been validated | Reproduce the frequentist estimator, seven-point integration setting, likelihood, random-effect variances, convergence and standard errors. |
| Probabilities, average marginal effects and intervals | Calculations can be written using the numerical foundation | Match contrasts, averaging sample, treatment of random effects, integration and uncertainty calculation. |

## Why installing a mixed-model package is insufficient

The installed `statsmodels` documentation describes its binomial mixed-model estimators as Bayesian. Those estimators introduce a different estimation procedure from the author's frequentist `melogit` analysis. `MixedLM` is a linear mixed model and does not supply the required binary-response model. Neither is an automatic replacement for the original analysis.

Python can remain the main environment for notebooks, data preparation, documentation, and checks. A pure-Python implementation of the advanced models is possible in principle, but requires additional implementation and numerical validation. If licensed Stata is available, using the author code as a comparison engine offers a practical way to check the translated analyses. Any Stata bridge also requires a working licensed Stata installation; installing a Python wrapper does not provide Stata.

Do not label the foundation environment a fully equivalent statistical environment. Resolve the advanced-model and reliability gaps before committing to an entirely Python-based final reproduction. Document any deliberately different estimator as an additional analysis, not the faithful reproduction.

## References inspected

- Assignment: local `sources/local/COMD7290_assignment.pdf`, page 7.
- Selected article: local `sources/local/Lob_et_al_2024.pdf`, method section (PDF page 8) and references (PDF page 22).
- Author materials: <https://medcon-doc.github.io/documentation/files/>; original local syntax remains unchanged.
- Ordered model documentation: <https://www.statsmodels.org/stable/generated/statsmodels.miscmodels.ordinal_model.OrderedModel.html>.
- Binomial mixed-model documentation: <https://www.statsmodels.org/stable/mixed_glm.html>.
- Stata multilevel logistic documentation: <https://www.stata.com/manuals/memelogit.pdf>. The current manual describes the command; exact original defaults still need checking against the intended Stata version.
- Krippendorff implementation: <https://pypi.org/project/krippendorff/>.
- Stata metadata access: <https://pyreadstat.readthedocs.io/en/latest/>.
- Jupyter installation: <https://jupyter.org/install>.
- Kernel registration: <https://ipython.readthedocs.io/en/stable/install/kernel_install.html>.
