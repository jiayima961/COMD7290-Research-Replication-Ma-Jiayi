# Follow up analysis proposal

AI-drafted feasible extension for student review on 19 October 2026. This is a
new analysis proposal using existing data. No execution, preregistration or
student acceptance is claimed. The earlier editorial-experiment proposal is
preserved in records/editorial_revision/2026-10-19/previous_versions/docs/follow_up.md.

## Research question and theoretical purpose

Does the association between professional media and lower outrage remain when
stable differences among the six countries are represented more directly?
Professional norms and editorial review motivate the media prediction, but the
original observational comparison does not isolate those mechanisms. A country
indicator model provides an achievable check on that association with the
existing data and Python environment.

## Derived hypothesis and design

Hnew predicts lower ordinal outrage tone in news websites and newspapers than in
political blogs after accounting for country indicators. Retain the 1,700-item
sample, tone recode from archive codes 1–5 to 0–4, the blogs reference group and
the two separate professional-medium contrasts. Use the same proportional-odds
ordered-logit family as M1. Replace political-system and secularism-division
predictors with five country indicators and an identified reference country.
National categories must be replaced rather than added because they are
constant within country and cannot be independently estimated alongside a full
set of country indicators.

## Measurement and analysis plan

No recollection or new coding is needed. Recheck media coverage within each
country, required-field missingness, convergence and proportional-odds diagnostics
before interpretation. Retain all planned media contrasts. Report odds ratios,
95% confidence intervals and sample-standardized predicted probabilities over
all five tone categories. Average predictions over the same observed country
composition so the prediction convention is explicit. Compare these estimates
with the original M1 and the already executed S1 country-deletion analysis.
Preserve results under a new analysis ID without replacing the original models
or changing their published comparison targets. No prospective sample-size
calculation is needed because the existing sample is fixed. Uncertainty and
within-country media coverage will determine the precision of this extension.

## Interpretation and feasible next steps

Persistence of the media pattern would strengthen confidence that the association
is not wholly explained by stable differences across these six countries.
Attenuation or wide intervals would qualify its interpretation. Either outcome
remains observational and cannot establish that editorial gatekeeping caused the
pattern. The model also cannot identify independent political-system effects or
extend generalization beyond the selected countries, outlets, topic and period.
The first practical step is a coverage check followed by a separately recorded
fit. A focused request for original M2 estimation and prediction logs could
separately clarify historical numerical settings. No request has been sent.
