# Ordinal and descriptive reproduction findings

The original 1,700-item ordered-logit model converged: log likelihood -724.0003868022. All five coefficient/SE/odds-ratio rows round to Table 3 of the original article. No printed targets were used to fit the model.

| Contrast | Coefficient | SE | Odds ratio |
|---|---:|---:|---:|
| 2.polsys | 0.39682551 | 0.18609772 | 1.48709642 |
| 3.polsys | -0.61526971 | 0.21658082 | 0.54049510 |
| 2.socdiv | 0.52362794 | 0.15917765 | 1.68814102 |
| 2.mediatype | -1.78103114 | 0.20987468 | 0.16846435 |
| 3.mediatype | -1.26854311 | 0.18151806 | 0.28124106 |

The fitted null log likelihood is -794.7440389120. McFadden R-squared is 0.08901439, Cox-Snell R-squared is 0.07985851, and Nagelkerke R-squared is 0.13147351. The article text calls .09 Nagelkerke, whereas its Table 3 calls .09 McFadden. The newly computed values support the table's measure name; retain this source-label discrepancy.

The Wolfe-Gould test using the original numeric predictor RHS converged: chi-square 7.43106347, df 9, p 0.59233333. The independent historical dumping-severity example reproduced 3.72099572 (df 3, p .29321036), matching the STB42 rounded result.

The fully generalized categorical observed-category likelihood reached -712.7324642571; twice its difference from M1 is 22.53584509, matching the article's rounded 22.5. Its last website slope is exactly absent from observed likelihood contributions; the preceding website slope approaches minus infinity. The observed information has numerical rank 22 of 24 and 7 fitted probabilities for unobserved categories are negative. No regular chi-square p value is accepted. The article's df 14/p .07 cannot be certified from these data and unpinned software rules. This is a visible diagnostic failure, not a reason to simplify M1.

The original alternative-link likelihoods are -721.9131168045 (probit) and -724.4183707550 (gologit2 cloglog). All slope directions agree. The mixed-versus-consensus coefficient has a 95% interval crossing zero under probit, while logit and cloglog do not. Do not interpret the source's similar-substantive-conclusions statement as identical significance for every contrast.

Saved outputs contain full/null parameters, covariance, cutpoints, information, fit diagnostics, 40 predictive margins and 25 discrete AMEs with 95% delta intervals. Descriptives cover all original overall/country/media/country-by-media summaries and all five tone-category frequencies, including zero cells. All 13 meaningful implementation checks passed; all original inputs retained their SHA-256 hashes. No Stata was executed. Human reading and approval remain unattested.
