# Research design and models: unapproved draft

## Observation production and units

This is an observational manual content analysis of the role of religion in public life. Items were published from August 2015 through July 2016. Countries and media outlets were selected for a comparative design; relevant texts were ranked computationally and screened by humans. This is not a random sample of all global media.

| Socio-cultural context | Majoritarian | Mixed | Consensus |
|---|---|---|---|
| Contested secularism | United States | Turkey | Lebanon |
| Stable secularism | Australia | Germany | Switzerland |

Published item N = 1,700: 600 newspaper items, 600 news-website items, and 500 blog posts. Actor-reference models report 3,770 directed references within 2,453 actor/statement units within 1,183 items. These are published counts, not locally recalculated results. Verify whether actor identifiers are unique only within items. Independently supplied coder ratings require separate matching and must not be replaced by consensus values.

## M1: item-level tone

Outcome: tone in {0, 1, 2, 3, 4}. Proportional-odds ordered logit, written using the upper-tail probability:

`logit[P(tone_i > k)] = alpha_k + beta' X_i, k = 0, 1, 2, 3`

X jointly includes political system, socio-cultural division, and media type. Reference groups are consensus democracy, stable secularism, and political blogs. If software uses the opposite cumulative direction, map threshold and coefficient signs before comparison. Reproduce proportional-odds diagnostics and the authors' probit and complementary-log-log checks. Preserve ordinal measurement in the faithful model.

## M2/M3: actor-reference outcomes

Fit separate three-level random-intercept binary-logit models for outrage and recognition:

`logit[P(Y_raj = 1 | u_j, v_aj)] = beta0 + beta' X_j + u_j + v_aj`

`u_j ~ Normal(0, sigma_item^2)` and `v_aj ~ Normal(0, sigma_actor^2)`.

Here r denotes a directed reference, a an originating actor/statement unit within an item, and j an item. Slopes are fixed. The outcomes are fitted separately; this is not a direct regression of outrage on recognition. These equations describe the intended model. Numeric coding, exact input names, estimation, integration, and interval conventions still require source-to-data verification.

## Resolve before estimation

- Actual variable names, binary value labels, special missing codes, identifiers/nesting, exclusions, and missing-data rules.
- Engine and extension versions, estimator, numerical integration/optimization, convergence, and interval settings.
- Reliability coefficients, measurement levels, distance weights, rating matches, and missing-rating handling.
- Random-effect treatment in predictions, the averaging population, and AME definitions. Distinguish log-odds, odds ratios, probabilities, and percentage-point differences.
- All supplementary analyses and paper/code conflicts. Specify tolerances before execution using reporting precision and numerical considerations.

Student approval: not recorded. Do not begin substantive estimation before review and approval of the specification.
