"""Record the report-review boundary without publishing the individual report."""
from pathlib import Path
from datetime import datetime, timezone
import json, shutil
ROOT=Path(__file__).resolve().parents[2]
REC=ROOT/'records/editorial_revision/2026-10-19'
REC.mkdir(parents=True,exist_ok=True)
paths=['AGENTS.md','docs/follow_up.md','docs/assignment_checklist.md',
       'report/skill3_submission_readiness.md','report/verification/README.md',
       'tools/verification_package_audit.py']
for rel in paths:
    old=REC/'previous_versions'/rel
    if not old.exists():
        old.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,old)

p=ROOT/'AGENTS.md'
if 'Scope update D014' not in p.read_text(encoding='utf-8'):
    with p.open('a',encoding='utf-8') as f:f.write('''
## Scope update D014 on 2026-10-19

The user requests an English APA-formatted individual report revision and a
GitHub update of today's other materials. Keep every individual-report version,
its editable source, authoring script, review archive and QA images local during
student review. The two technical reports in report/verification are permitted
sharing material and are distinct from the individual report. Do not create a
final assessed release or tag, submit to Moodle, change visibility, or invite a
collaborator. Retain scientific discrepancies accurately while giving minor
numerical differences proportionate treatment in the report. The future research
proposal now uses existing item data and country indicators rather than requiring
a new editorial experiment. This extension is proposed, not executed.
''')

(ROOT/'docs/follow_up.md').write_text('''# Follow up analysis proposal

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
''',encoding='utf-8')

p=ROOT/'report/verification/README.md'
t=p.read_text(encoding='utf-8').replace('   [report draft](../final_report_draft.md) and [remaining submission steps](../skill3_submission_readiness.md).',
'   [remaining submission steps](../skill3_submission_readiness.md). The individual\n   report and its review versions remain local by the student’s request.')
t=t.replace('These latest skill 3 additions\nare saved locally; GitHub has not been synchronized in this task.',
'The latest skill 3 additions are included in the authorized GitHub update, with\nverification recorded under records/editorial_revision/2026-10-19. The individual\nreport, its source and its review archive are excluded from that update.')
p.write_text(t,encoding='utf-8')

p=ROOT/'report/skill3_submission_readiness.md';t=p.read_text(encoding='utf-8')
t=t.replace('4. Revise report/final_report_draft.md in the student\'s own words, verify the body\n   remains 1000–1200 words and apply APA7 formatting to the final assessed document.',
'''4. Review the local individual report in report/final_report_review_2026-10-19.docx
   and its editable report/final_report_draft.md source. The revised body contains
   1,110 words and has been formatted in APA7. These files and their prior versions
   are intentionally excluded from GitHub during the student's continuing review.
   Recount and rerender after further edits before final acceptance.''')
p.write_text(t,encoding='utf-8')
p=ROOT/'docs/assignment_checklist.md';t=p.read_text(encoding='utf-8')
t=t.replace('AI-assisted 1,046-word body draft prepared; student must revise, supply ID, check final APA formatting/word count and prepare oral defence. This is not final assessed submission',
'AI-assisted 1,110-word APA Word review copy saved locally and intentionally withheld from GitHub. Student review, ID, final access/release details and oral defence remain pending')
p.write_text(t,encoding='utf-8')
(ROOT/'report/README.md').write_text('''# Report reading order

1. Read [the technical comparison and methods documents](verification/README.md).
   Their two Word files are supporting evidence, not the assessed individual report.
2. Read [submission readiness](skill3_submission_readiness.md) for personal and final
   submission steps that still require the student's action.
3. On the original computer, open report/final_report_review_2026-10-19.docx for the
   latest individual report. Its editable source is report/final_report_draft.md.
   Every individual-report version and review artifact remains local while the
   student continues reviewing. These files are deliberately absent from GitHub.

The report folder is the designated location for report deliverables. Do not create
an assessed tag or release until the student accepts the report and verifies all
required access details. Historical technical receipts remain unchanged.
''',encoding='utf-8')
(REC/'README.md').write_text('''# Editorial revision and selective synchronization

The student authorized report editing and Word formatting on 19 October 2026,
followed by synchronization of today's other research files. The individual report,
all report draft versions, its editable source, authoring scripts and page-rendering
artifacts are withheld from GitHub. They remain available locally under report/.
The earlier report text is preserved only in the excluded report/local_review tree.

This record describes the boundary without reproducing the report. The other
research deliverables include the tested third skill, complete comparison ledger,
independent checks, clean-run records, sensitivity results and two technical Word
reports. Numerical reproduction outputs and earlier execution receipts are preserved.
The proposed follow-up now reuses existing item data with country indicators.
Its earlier experiment proposal is preserved in previous_versions. Neither proposed
follow-up has been executed. The completed S1 sensitivity remains separate.

The historical package audit contains a local-report word-count check. Its tool
now excludes the new table from that count and reports an explicit omission if the
individual report is unavailable in a GitHub copy. That omission does not certify
the report. Historical audit receipts are not rewritten by this editorial task.

GitHub verification is recorded in github_sync.json after the remote update is
checked. No final release, submission, collaborator invitation or visibility change
is performed.
''',encoding='utf-8')
print(json.dumps({'record':str(REC),'previous_versions_preserved':len(paths),'report_content_in_record':False}))
