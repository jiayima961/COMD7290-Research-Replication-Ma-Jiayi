# Research design and executed model specification

Documentation completed on 20 October 2026. Read the
[dictionary guide](variable_dictionary.md) and [complete field dictionary](variable_dictionary.csv)
for source fields, code categories, actual missingness and analysis roles.
[Figure 1](model_diagram.md) gives the separate M2/M3 nested models and Figure 2
the M1 companion. Their [node map](model_diagram_map.csv) binds the diagram
elements to these equations, actual executing functions and matrix row IDs.
This is a retrospective documentation update, not a prior student approval.

## Observation production and units

This is an observational manual content analysis of the role of religion in public life. Items were published from August 2015 through July 2016. Countries and media outlets were selected for a comparative design; relevant texts were ranked computationally and screened by humans. This is not a random sample of all global media.

| Socio-cultural context | Majoritarian | Mixed | Consensus |
|---|---|---|---|
| Contested secularism | United States | Turkey | Lebanon |
| Stable secularism | Australia | Germany | Switzerland |

Published item N = 1,700: 600 newspaper items, 600 news-website items, and 500 blog posts. Actor-reference models report 3,770 directed references within 2,453 actor/statement units within 1,183 items. These counts were independently recalculated from original inputs. Actor identifiers are nested within items; the composite actor key is verified. Independently supplied coder ratings require separate matching and must not be replaced by consensus values.

## M1: item-level tone

Outcome: tone in {0, 1, 2, 3, 4}. Proportional-odds ordered logit, written using the upper-tail probability:

`logit[P(tone_i > k)] = alpha_k + beta' X_i, k = 0, 1, 2, 3`

X jointly includes political system, socio-cultural division, and media type. Reference groups are consensus democracy, stable secularism, and political blogs. If software uses the opposite cumulative direction, map threshold and coefficient signs before comparison. Reproduce proportional-odds diagnostics and the authors' probit and complementary-log-log checks. Preserve ordinal measurement in the faithful model.

## M2/M3: actor-reference outcomes

Fit separate three-level random-intercept binary-logit models for outrage and recognition:

`logit[P(Y_raj = 1 | u_j, v_aj)] = beta0 + beta' X_j + u_j + v_aj`

`u_j ~ Normal(0, sigma_item^2)` and `v_aj ~ Normal(0, sigma_actor^2)`.

Here r denotes a directed reference, a an originating actor/statement unit within an item, and j an item. Slopes are fixed. The outcomes are fitted separately; this is not a direct regression of outrage on recognition. These equations describe the executed model. See [the execution specification](execution_specification.md) and [results index](replication_results.md) for verified input names, coding, numerical settings and the unresolved historical finite-grid details.

## Measurement-source checks on 20 October 2026

The supplied analytical fields and legacy metadata are not interchangeable.
The original main models use `mediatype`, not legacy `medientyp`, and `country`,
not legacy `land`. Their numbering and some category assignments differ. Exact
cross-tabs are retained in outputs/diagnostics/measurement/semantic_checks.json.
The replication preserves the analytical fields expressly chosen by the author.

The archive originator ID maps one-to-one to the model's composite actor groups.
The target actor identifier is documented separately and is not used as the
originating-actor random-effect group. One supplied reference has both binary
outcomes coded present despite the codebook's exclusivity instruction. The
original outcomes are fitted separately and that row is retained unchanged.
Conflicting codebook numbers for auxiliary valence and reference construction
are recorded explicitly, rather than silently imposing an unverified recode.

## Execution and interpretation status

The user explicitly authorized source-bound Python reproduction in D011. Current numerical results and uncertainty are saved; this is not a claim of preregistration or final student acceptance. See execution_specification.md for recovered settings and replication_results.md for differences and limitations. Independent ratings remain separate from consensus analytical data. Historical software builds and finite quadrature internals are incompletely pinned; no exact-executable equivalence is claimed.
