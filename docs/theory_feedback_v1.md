# Feedback on the student's initial theory explanation

Date: 2026-10-18, Asia/Shanghai. Real personal-review invocation of `specify-empirical-study` 1.0.1. **AI feedback for student consideration; not an accepted revision.**

Input: [preserved student explanation v1](../records/student_inputs/2026-10-18_initial_theory_explanation_v1.txt). The student's wording is retained separately; none of the changes below has been inserted into that input. Detailed numerical/source checks and the invocation receipt are in [the review record](../records/skill_invocations/2026-10-18_specify-empirical-study_theory-review/README.md).

Locators below use the article's printed journal pages, with PDF pages in parentheses. This reviews the selected article, not the present-day political classification of its countries.

## Overall assessment

The explanation correctly identifies the topic, countries, media categories, distinction between item tone and directed actor references, and recognition's reference-only measurement. All ten quoted odds ratios match Tables 3 and 4. The deliberative and recognition discussion captures important normative foundations.

The main improvement is to move from a predominantly **results summary** to a **reconstruction of the scientific argument**. Assignment p.2 asks why the hypotheses follow from prior ideas, through which processes, under what conditions, and against which alternatives. Put the original predictions before the published findings, and keep later interpretations separate. This is a retrospective reconstruction with knowledge of results, not a preregistration or a new pre-results prediction.

## F01. Add a clear research gap and contribution

Add a short opening explanation of what earlier work left unresolved. The article identifies fragmented definitions of civility, relatively little attention to its positive side, and limited comparative understanding of its systemic determinants. It combines political context, religion-related social division and news production across six countries and three media types, and distinguishes two discourse outcomes at two measurement levels. It applies and integrates existing ideas and contributes toward a contingency account; it does not introduce two entirely new theories. Avoid claiming that no earlier research considered respect or recognition. Sources: pp.274-276 and 289 (PDF 2-4,17).

Suggested wording, **AI-authored example for adaptation**:

> Earlier research offers competing definitions of civility and often examines particular countries or media settings. This study combines a positive concept, recognition, with a negative concept, outrage, and compares how both relate to political institutions, divisions over secularism and forms of news production. Its contribution is to integrate these explanations in a comparative design, rather than to establish a new general theory of civility.

## F02. Distinguish normative foundations from explanatory mechanisms

Your two theory sections work as an account of the study's **normative foundations**, but they do not yet explain all three predictor sets. Deliberative democracy explains why civility matters; recognition theory helps define its positive dimension. To explain the six hypotheses, also reconstruct the following arguments from the article:

| Predictor | Authors' proposed process | Original observable prediction | Article locator |
|---|---|---|---|
| Political system | Power sharing makes accommodation and compromise more necessary; this can encourage recognition of opponents and restrain hostile communication | Majoritarian versus consensus: more outrage, less recognition | pp.276-277 (PDF 4-5), drawing on Lijphart and deliberation/institutional work |
| Division over secularism | Rival groups and parties defend identity boundaries; segmentation and social distance encourage hostility and make constructive engagement less likely | Contested versus stable secularism: more outrage, less recognition | p.277 (PDF 5), social-cleavage and divided-society arguments |
| News production | Professional norms, editorial oversight and gatekeeping may restrain outrage and encourage respectful treatment; weaker gatekeeping and audience incentives may encourage outrage in blogs | Each professional medium versus blogs: less outrage, more recognition | pp.277-278 (PDF 5-6) |

These mechanisms are the authors' theoretical explanations, not directly estimated mediators. The study does not measure a causal chain from institutional compromise, identity salience or gatekeeping to each communication act. Do not relabel the whole social-division argument as a formally tested social identity theory model without further source support.

A useful title for your last section is **"Normative foundations and explanatory mechanisms"**, followed by the two foundations and these three explanatory routes.

## F03. State all six hypotheses before assessing their results

The table separates the authors' original predictions from what the publication reports. No value here is a newly reproduced result.

| Hypothesis | Prediction | Analytical target | Published finding and appropriate interpretation |
|---|---|---|---|
| H1a | Majoritarian > consensus outrage | M1 item tone; M2 reference outrage | M1 OR=0.54, opposite to prediction; M2 comparison not significant. No consistent support |
| H1b | Consensus > majoritarian recognition | M3 reference recognition | Majoritarian-versus-consensus OR=0.58, not significant. Prediction not supported, rather than proven false |
| H2a | Contested > stable outrage | M1; M2 | M1 OR=1.69 supports the predicted association; M2 OR=0.88, not significant. Support is measurement-level specific |
| H2b | Contested < stable recognition | M3 | OR=2.20, significant in the opposite direction. Original prediction contradicted by the reported association |
| H3a | Blogs > each professional medium in outrage | M1; M2, separate website and newspaper contrasts | Both professional-media coefficients below one and significant in both outcomes; consistent with the prediction |
| H3b | Each professional medium > blogs in recognition | M3, separate website and newspaper contrasts | Website OR=1.99; newspaper OR=3.28, both significant; consistent with the prediction |

Sources: hypotheses pp.276-278; Tables 3-4 pp.283,286 (PDF 11,14). Model targets correspond to 12 separate directional coefficients. Mixed-system estimates are additional comparisons; the theory does not predict that mixed systems must lie between the other two types. Table 3 directly reports mixed-versus-consensus and majoritarian-versus-consensus contrasts. A claim about the significance of mixed-versus-majoritarian requires its own contrast and uncertainty; do not infer that test solely from two reference-category comparisons.

## F04. Correct the raw-country recognition ranking and flag the source ambiguity

Your sentence about recognition being descriptively highest in Lebanon and Switzerland and lowest in Australia and the USA follows the article's Discussion, p.288 (PDF 16). However, the Results, p.285 (PDF 13), explicitly report these **raw country proportions**:

| Country | Recognition proportion reported in Results |
|---|---|
| Australia | 2.8% |
| Switzerland | 3.0% |
| Germany | 5.3% |
| Turkey | 5.3% |
| United States | 5.5% |
| Lebanon | 18.0% |

Thus the quoted Discussion sentence cannot serve as an accurate raw-country ranking: Switzerland is among the lowest, and the USA is above it. Both passages were visually checked in the PDF. The political-system coefficients in Table 4 are adjusted model comparisons, not raw country percentages; their signs are compatible with lower recognition in majoritarian than consensus systems, but their uncertainty includes no difference. Whether the Discussion intended an adjusted interpretation is not established by its wording. Record the ambiguity rather than silently repairing the source.

Suggested replacement, **AI proposal**:

> Raw recognition proportions were highest in Lebanon and lowest in Australia and Switzerland. In the adjusted model, the political-system comparisons were not statistically significant. The Discussion's country-ranking wording differs from the raw proportions reported in the Results, so these should be kept distinct.

Also qualify "blogs were consistently the most outrage-prone": item-level raw proportions have a stated Lebanese exception, with 20% of newspaper items versus 14% of blog posts containing at least slight outrage (p.281, PDF 9). The reported adjusted media associations and reference-level descriptive pattern remain consistent with higher blog outrage. Avoid turning a pooled/model pattern into a claim about every country and every measure.

## F05. Keep odds ratios, probabilities and non-significance distinct

Your ten OR transcriptions are correct. Add their interpretation:

- M1 uses proportional-odds ordered logit. For a given threshold, compare the odds of an item being above it rather than at or below it, holding the other modeled predictors constant. Under the model, the same coefficient applies across thresholds. OR=0.17 means 83% lower **cumulative odds**, not 83 percentage points lower probability and not 83% lower mean outrage. The no-outrage versus any-outrage threshold is one such threshold.
- M2/M3 are separate binary multilevel logits. OR=3.28 for newspaper versus blog recognition is a conditional odds ratio, holding the other modeled predictors and random intercepts constant; it does not mean a 3.28-fold probability. Probability differences require an explicit prediction convention and baseline.
- "No statistically significant association was detected" is more precise than "political system had no effect." Non-significance is not evidence that the true association is exactly zero, especially in this limited country design.
- The lower-category observation belongs to **item-level tone probabilities**. Reference-level outcomes are binary, so they have no moderate-to-very-strong categories. Constant proportional odds can coexist with small absolute probability differences in rare upper categories.

Sources: analytic procedures pp.280-281, Table 3 and margins discussion pp.283-284, hierarchy and Table 4 pp.285-286 (PDF 8-9,11-14). These interpretation checks do not validate a Python implementation of the models.

## F06. Separate original predictions, later explanations and causal claims

Your discussion of divided societies producing more recognition is a reasonable account of the authors' Discussion. Label it a **post-result interpretation**. The original H2b predicted less recognition, using reduced compromise and constructive engagement as its rationale. The later salience/commonality explanation cannot be substituted for that original prediction to make it appear confirmed. The paper also did not distinguish ingroup from outgroup recognition in this analysis, so higher recognition does not by itself demonstrate improved relations across the divide. Source: p.288 (PDF 16).

Use "professional news items were associated with lower outrage and higher recognition" as your empirical conclusion. Attribute stronger language such as mitigation to the authors' interpretation. The observational comparison does not isolate gatekeeping as a cause; outlet selection, audience composition, article genre, speaker selection and country conditions are plausible competing explanations to consider, **reviewer-proposed alternatives rather than demonstrated causes**. Sources: selection pp.279-280; limitations p.289 (PDF 7-8,17).

Strengthen the limits: each political-system-by-division cell contains only one country. The many articles and references do not create many independent realizations of a national institutional system. Unobserved national differences may therefore be entangled with the contextual predictors. The topic, selected outlets and August 2015-July 2016 period further limit generalization. This is more specific than simply saying "six countries is a small sample."

## F07. Refine conceptual attribution and the meaning of the measures

Keep Honneth as an important intellectual source, but note that the article's particular recognition definition is attributed to **Maia (2014, p.17)**, with Honneth (1996) providing a broader foundation (article pp.275-276). Outrage's quoted definition is attributed to **Sobieraj and Berry (2011, p.20)**. These are the target article's attributions; this review does not claim to have inspected the original Honneth or Maia books.

Recognition and outrage are distinct concepts, not one bipolar score. An absence of coded outrage does not establish explicit recognition. The coding concerns communicative content and described gestures, not measured audience emotions or actual democratic improvement. Your word "generally" for outrage's normative harm is appropriate: the authors also acknowledge potential democratic value in some contexts, such as highlighting injustice (p.275).

## F08. Make the theory-to-analysis link explicit without starting implementation

For each mechanism, connect the prediction to an observed outcome and a named comparison: `polsys`, `socdiv` and `mediatype` jointly predict ordinal `tone` in M1; they jointly predict binary `actrefoutbin` in M2 and `actrefrecbin` in M3. Reference groups are consensus, stable secularism and blogs. The archive's tone 1-5 is recoded by the author to 0-4; do not confuse the stored codes with the article's scale. Actor-reference observations are nested in originating actor/statement groups within items, rather than in a country-media-item random hierarchy.

These details link a theory map to an analytical target. Exact implementation, uncertain coding bridges and three-level Python/Stata equivalence remain deferred. Source: article pp.278-281,285-286; author syntax lines 48-62,99,203,214-215,266-267.

## F09. Record foundational reading and student decisions truthfully

Discussing two theoretical labels is not the same as recording direct reading of two cited foundational works. Please eventually record the actual works, sections/pages read, and what you learned or questioned. No reading scope has yet been supplied, so this review marks it **unknown**, not "not read" and not "completed." Candidates named in the article include Lijphart on institutions and Honneth/Maia on recognition; their original text should be consulted for deeper claims. Existing local copies of Sobieraj/Berry (2011) and Wolfe/Gould (1998) are also possible theoretical/methodological readings. Their prior AI reading does not count as yours.

Your explanation is received before this particular critique. It is a real user-supplied contribution, but the project already contained AI explanations and published results; this record does not certify that it was composed before all AI exposure or without assistance. No separate student-created initial diagram was supplied. Keep its actual date and authorship when you create or submit one.

## Suggested order for your next version

1. Phenomenon, specific gap and contribution.
2. Normative definitions of outrage and recognition, with precise attribution.
3. The three explanatory mechanisms, followed by H1a-H3b.
4. Measurement units, outcomes and corresponding model comparisons.
5. Published results in a separate evaluation section.
6. Competing explanations, scope limits and two actual foundational-reading notes.

A revision can retain most of your accurate results summary by moving it to item 5. Revise the earlier sections in your own words and record which feedback you accept, modify or reject in [student_review.md](student_review.md). No acceptance, reading completion or model-fitting approval has been entered for you.
