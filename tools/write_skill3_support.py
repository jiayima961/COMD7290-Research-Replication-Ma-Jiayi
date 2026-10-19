"""Write dated verification support records from actual saved evidence."""
from pathlib import Path
import json,shutil
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def write(rel,text):
 p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')
def main():
 # Preserve the original inventory and retain every original analysis ID.
 original=ROOT/'records/skill_invocations/2026-10-19_verify-and-package/previous_versions/docs/analysis_inventory.csv'
 inv=pd.read_csv(original).fillna('')
 statuses={'D1':'reproduced_with_discrepancy','D2':'reproduced','R1':'reproduced_with_discrepancy','R2':'reproduced_with_discrepancy','M1':'reproduced_with_discrepancy','C1':'reproduced_with_discrepancy','C2':'reproduced_with_discrepancy','M2':'reproduced_with_discrepancy','M3':'reproduced','C3':'reproduced_with_discrepancy','P1':'reproduced_with_discrepancy','P2':'reproduced','A1':'not_verifiable','V1':'reproduced','N1':'reproduced','S1':'reproduced'}
 notes={
 'D1':'All Table 2 cells checked; Australian website moderate printed 11 versus data 1.',
 'D2':'All printed percentages agree; full graph cells computed; narrative ranking conflict separately recorded.',
 'R1':'All published point estimates/N agree; original reliability build unpinned; all-slot uncertainty equality not verifiable.',
 'R2':'Same published agreement; author-selected positional slots retain repeated coders/-99; benchmark-version labels differ.',
 'M1':'Slopes/SE/OR, N/LL and OR intervals agree; prose Nagelkerke label conflicts with McFadden value.',
 'C1':'WG numeric syntax agrees; generalized raw LR agrees but df/p cannot be certified owing to nonidentification/invalid probabilities.',
 'C2':'Original links executed; slope directions persist; mixed-system significance changes under probit.',
 'M2':'All b/SE agree; mixed OR and -2LL differ; historical finite-grid cause unresolved.',
 'M3':'Published main table and AMEs agree at printed precision; unprinted random variance targets remain unavailable.',
 'C3':'Recognition LR agrees; outrage LR differs; variance-boundary calibration unverified.',
 'P1':'Supplement recovered via cached primary page: 68/75 AME/CI cells within rounding, seven discrepancies; exact figure probability vector unpublished.',
 'P2':'All ten published AMEs and twenty interval endpoints agree; full unprinted probability/SE vectors computed.',
 'A1':'Available author code and primary tables inventoried. Complete unrounded historical logs/build-specific targets and current live appendix availability remain unavailable; no claim of exhaustive unavailable materials.',
 'V1':'Independent raw-reader counts, fresh statsmodels M1/AME checks and earlier nested likelihood/curvature checks pass; M2/M3 not independently reoptimized.',
 'N1':'Copied/in-memory invalid tone detected; restored valid copy reruns; original hashes preserved.',
 'S1':'Six prespecified M1 country deletions executed; separate sample influence question, not author-link/numerical sensitivity.'}
 inv['status']=inv.analysis_id.map(statuses)
 inv['coverage_note']=inv.analysis_id.map(notes)
 inv['comparison_target']='outputs/verification/comparison_all.csv'
 inv.loc[inv.analysis_id=='S1',['script_path','output_path','blocker']]=['analysis/skill3_sensitivity.py','outputs/verification/sensitivity/README.md','Student interpretation/acceptance pending, execution completed']
 inv.to_csv(ROOT/'docs/analysis_inventory.csv',index=False)
 write('outputs/verification/README.md','''# Complete verification evidence

Read report/verification/README.md for the ordered Word reports. comparison_all.csv
is the comprehensive numeric ledger; comparison_coverage.csv groups it; summary.json
counts comparison statuses. Counts are an inventory, not a replication probability.
The original outputs/comparison.csv is the unchanged 45-cell skill 2 subset.

independent_checks/ contains fresh raw-reader and independent ordinal-fit/margin
checks with a negative test and recovery. sensitivity/ contains the separate S1
country influence analysis. Saved model vectors/uncertainty without published
targets are explicitly not_verifiable for equality, even when calculated correctly.
''')
 write('outputs/review_report.md','''# Technical verification review

Material passport: ANALYZED from saved faithful outputs, with separately EXECUTED
fresh independent M1 and AME calculations, negative/recovery checks, six country
deletions and a full source/input-only clean refit. Original data and skill 2
numerical results were not overwritten. Student scientific acceptance is pending.

The complete review is report/verification/01_results_comparison.md and its DOCX;
software equivalence is report/verification/02_python_stata_equivalence.md and its
DOCX. Use outputs/verification/comparison_all.csv, not only the old 45-cell subset.

Core results agree at published precision with explicitly retained exceptions.
Thirteen numeric target entries differ, and one published LR p value cannot be
validated. Source labeling/table anomalies, unresolved numerical/postestimation
differences and diagnostic identification failures are distinguished. No remaining
difference is assigned to software alone without evidence. The generalized ordinal
LR is not accepted as regular inference, despite agreement of its raw statistic.

Evidence: independent checks outputs/verification/independent_checks/checks.json;
source review records/skill_tests/verify-and-package/independent_source_audit.md;
clean run records/run_logs/skill3/clean_restart/receipt.json; model checks
outputs/diagnostics/glmm/; coverage docs/analysis_inventory.csv; fallacy review
outputs/verification/interpretation_audit.md; human decisions
records/skill3_decision_audit.md. Technical completion does not complete the
student's personal reading, diagram, decision acceptance or release/submission.
''')
 write('docs/limitations.md','''# Evidence based limitations

| Domain | Demonstrated observation or possible threat | Implication | Evidence |
|---|---|---|---|
| Data access | Author-coded DTA/XLSX available; original text selection/recollection and recoding not repeated | Computational reproduction does not verify full data generation | sources/input_restore_manifest.json; data audit |
| Measurement | Tone has sparse upper categories; recognition does not separate ingroup/outgroup | Upper-category inference is fragile; recognition is not proof of cross-group respect | tone counts; article/codebooks |
| Reliability | 182 matched actor rows have repeated named coders; historical add-on build unpinned | Positional-slot agreement and version benchmark labels need qualification | reliability matching audit and version comparison |
| Design | Six countries with one country per institution-by-division cell | National differences may be entangled with contextual predictors; many articles are not many systems | article design; S1 |
| Analysis | Generalized ordinal diagnostic structurally nonidentified and allows seven negative unobserved-category probabilities | Its regular LR df/p cannot be certified; WG uses numeric RHS | ordinal diagnostics |
| Analysis | M2 likelihood/OR and seven ordinal AME/CI display discrepancies | Incomplete historical numerical equivalence; source/build causes remain possible rather than established | comparison_all.csv |
| Analysis | Two null random variances lie on boundaries | Ordinary regular chi-square calibration is unverified | Note 3 and binary likelihood comparison |
| Interpretation | Observational outlet/context comparison; mediator mechanisms not measured | Associations do not identify gatekeeping, compromise or identity salience as causes | execution specification and theory map |
| Reproducibility | Source/input-only rerun passed in reused environment; historical builds/logs absent | Demonstrates current-environment rerunning, not fresh-machine or historical-executable identity | clean-run receipt; environment lock |
| Source reporting | Australian Table 2 cell and R2 labels conflict; recognition prose rankings differ from raw results | Retain original values and distinguish strong error evidence from ambiguous narrative | independent source audit |
| External scope | Religion discourse, selected outlets and 2015–2016 sample | Generalization to other issues, platforms and periods remains untested | article sampling description |

S1 is a country-influence diagnostic of M1, not a repair for causal confounding or
an assessment of M2/M3 stability. All six deletions and their uncertainty are retained.
Possible selection, genre and audience explanations are plausible threats, not
empirically demonstrated causes in this dataset. Human reading, personal explanation
and final acceptance are separate from these technical limitations.
''')
 write('outputs/verification/interpretation_audit.md','''# Statistical interpretation audit

Date 2026-10-19. Primary spec and sources reviewed before synthesis. This records
eleven interpretation risks; it does not claim that every risk occurs in the data.

| Risk | Assessment for this study |
|---|---|
| Simpson reversal | Pooled, country-specific and adjusted results answer different questions. Lebanon's item pattern is an exception; a universal media claim is unsupported. No formal general Simpson paradox is asserted. |
| Ecological inference | Country classifications predict coded references/items; individual attitudes or institutions' causal effects cannot be inferred. Six countries remain six contexts. |
| Berkson or selection bias | Selected outlets/issue and only items with actor references may affect generalization; magnitude/direction not established. |
| Collider conditioning | Selecting reference-containing items could induce associations if inclusion depends on common causes; a causal graph/data are needed. No demonstrated collider claim. |
| Base rate neglect | Reference outcomes are about 5%; large ORs do not imply large probability changes. Report baseline convention and AMEs. |
| Regression to the mean | No before/after selection on extreme scores is central here; not established as an explanation. |
| Survivorship | Outlet/archive accessibility may omit discourse; no measured survivorship mechanism demonstrated. |
| Look elsewhere | Many contrasts/outcomes and sensitivity fits exist. Preserve the author's nominal tests; do not silently select significant contrasts or add unreported correction to faithful results. |
| Forking paths | Freeze source targets/tolerances and all six S1 deletions before judging outcomes; preserve corrections and all failed diagnostics. |
| Correlation and causation | Gatekeeping, power sharing and group salience are proposed explanations, not estimated causal mediators. Computational agreement does not establish them. |
| Reverse causation | Contemporaneous media content/selection may reflect mutually related political conditions; cross-sectional observational comparisons do not establish temporal direction. |

Non-significance is not zero; a confidence interval is not a posterior probability;
the OR is not a risk ratio or percentage-point effect. Higher-category small effects
can have intervals excluding zero. No post-result explanation is relabelled as an
original hypothesis or preregistered prediction. Multiple comparisons remain a
reporting limitation; no automatic generic OR-size threshold is treated as evidence.
''')
 write('records/skill3_decision_audit.md','''# Consequential AI decisions and student review

All technical source checks below were actually performed. The student has not
yet accepted or corrected these decisions. This is a completed AI technical audit
with pending human review, not three invented student approvals.

| ID | AI proposal or decision | Source based check and outcome | Implication | Student response |
|---|---|---|---|---|
| A01 | Preserve nested item and actor/statement random intercepts, seven-point frequentist marginal ML | Author syntax version16, item-specific actor construction and melogit intpoints(7); Stata16 manuals; independent integral/curvature checks | No country/media random hierarchy or simpler substitute; historical finite grid remains unpinned | Pending |
| A02 | Use prior-random-effect marginal standardized probabilities and discrete AMEs | Author margins calls; Stata16 postestimation docs distinguish margins from empirical-Bayes predict; saved convention and integration checks | Prediction estimand is explicit; not subject-conditioned probabilities or causal treatment effects | Pending |
| A03 | Retain a failed generalized ordinal assumption diagnostic rather than accept matching LR | Source Note1 and syntax versus absent website coefficient, rank22/24, negative probabilities; independent audit | Raw LR display agreement does not verify df14/p.07; interpretation needs qualification | Pending |
| A04 | Preserve author positional reliability slots and -99 coding | Original reliability script, XLSX column/matching audit; 182 repeated-coder actor rows and conditional uncertainty checks | Faithful reproduction retained; distinct named-person interpretation is limited | Pending |
| A05 | Correct the new verification draft's country label mapping | Actual DTA metadata: code3=LEB and code4=SUI; independent pyreadstat check detects/fixes initially swapped labels | Corrected comparison/sensitivity labels before delivery; no skill2 results/data changed. Prior draft preserved under invocation records | Pending |
| A06 | Do not force the supplementary seven AME/CI entries to match | Cached primary table, frozen .005 tolerance, fresh independent statsmodels fit and all 75 quantity checks | Retain discrepancies and uncertain source/postestimation causes; no retroactive wider tolerance | Pending |
| A07 | Run all six country deletions as a separate sensitivity | Assignment p13; plan saved before fits; all deletions retained with changed-sample estimand | Media direction stable within diagnostic; contextual significance varies; no cherry-picked preferred model | Pending |

For each item the student should record accept/correct, a reason in their own
words and any resulting change. A convenient response is A01 accept/correct ...,
A02 ..., A03 ...; the record is updated only after actual input. This task does not
infer personal reading, an unaided theoretical account or final scientific acceptance.
''')
 write('docs/follow_up.md','''# Follow up study proposal

AI-drafted one-page design for student review, 19 October 2026. No data collection,
preregistration, ethics approval or student acceptance is claimed.

**Question.** Does editorial review reduce hostile expression and increase explicit
recognition when the underlying religion-related message and speaker are held fixed?

**Derived hypothesis.** Hnew predicts that professionally edited versions of the
same submitted text will show lower coded outrage and more explicit recognition
than unedited versions. This tests an editorial mechanism that the original outlet
comparison could not isolate; it is a new prediction, not part of the original six.

**Design and sample.** Recruit consenting adult writers to respond to balanced,
matched religion-in-public-life prompts. Randomly allocate submitted texts within
prompt and language to a documented editorial-review process or a time-matched
formatting-only control. Preserve speaker identity and substantive position; record
editing intensity. Use multiple editors and independently blinded coders. The study
unit is the submitted text, with actor references nested within text. Randomization
supports a process contrast under this protocol, not the causal effect of an entire
national media system.

**Measurement.** Retain a preregistered ordinal outrage-tone code and binary explicit
outrage/recognition references, while adding ingroup/outgroup target and editing
fidelity codes. Pilot and revise ambiguous rules before the main sample; use separate
training and final independent-reliability samples. Report matching, missingness,
all reliability coefficients/uncertainty and adjudication separately.

**Precision and analysis.** Before recruitment, simulate text and reference outcomes
using pilot event rates and clustering. Choose the text count to target a 95% interval
half-width of 3 percentage points for the primary recognition probability contrast,
across plausible event rates and editor/text clustering. If this target is infeasible,
declare the feasible precision before collection; do not invent a powered sample N.
Preregister one primary outcome/contrast, ordered-logit tone as secondary with
assumption checks, and mixed binary models for references with text/editor effects
as supported by the crossed design. Report standardized probability differences and
intervals, all planned outcomes, missingness and prespecified multiplicity handling.

**Interpretation.** Improvement would support an editorial-process explanation under
the tested protocol. A null or imprecise result would limit that explanation without
proving outlet associations absent. Content distortion, unblinding or recognition
confined to ingroups would qualify the democratic interpretation. Generalization
still requires other topics, languages, editors and real publication settings.
''')
 write('records/checkpoints.md','''# Dated working checkpoints

| Checkpoint | Technical evidence as of 2026-10-19 | Human decision |
|---|---|---|
| A Feasibility | Sources/input access and Python installation documented; original coded data and full models executed | Reading/rights/access claims must remain specific; no blanket personal attestation |
| B Specification | Student v1/v2 and two reviews preserved; hypothesis matrix, dictionary, model map and exact execution spec exist | Complete-specification acceptance and student-owned diagram/reading record pending |
| C Execution and audit | Reliability, descriptives, M1/M2/M3/null fits, probabilities, diagnostics, independent checks, negative/recovery and comparison ledger executed | At least three source-checked AI decisions await personal acceptance/correction |
| D Completion | Full isolated clean refit passed; separate S1 and follow-up draft complete; skill3 reports and draft prepared | Final interpretation/acceptance, student ID, instructor-access check, fixed final commit/tag/release and identical submitted report pending |

These technical dates do not backfill student approvals. Full evidence is indexed
in report/verification/README.md and records/skill3_decision_audit.md.
''')
 write('report/skill3_submission_readiness.md','''# Submission readiness after skill 3

Completed technical work: source-by-source ledger, independent verification,
harmless negative/recovery test, full clean refit, separate country sensitivity,
one-page follow-up proposal, English comparison/equivalence documents, and saved
skill invocation/test evidence. See report/verification/README.md.

Remaining student/final-stage requirements:

1. Supply student ID and verify name/access details. No invitation was sent; current
   instructor access is unverified and must be checked by the student before submission.
2. Record the required foundational reading and personal understanding; retain the
   actual student diagram or explicitly review/revise the existing AI diagram.
3. Accept/correct at least three decisions in records/skill3_decision_audit.md and
   review the full specification, discrepancy interpretation, S1 and follow-up.
4. Revise report/final_report_draft.md in the student's own words, verify the body
   remains 1000–1200 words and apply APA7 formatting to the final assessed document.
   The two technical reference DOCX files are not substitutes for that individual report.
5. After actual acceptance, rebuild the final approved package, verify input restoration
   and instructor access, freeze a full commit and named tag/release, put that exact
   identity in the access block and submit the identical report as required.
6. Prepare personally for oral defence; see the question guide below. No agent can
   perform the student's personal defence or attest understanding.

Oral defence prompts: explain H2b prediction versus observed recognition; explain
an odds ratio versus a probability difference; draw reference/actor/item nesting;
explain why same seven nodes can differ numerically; identify the invalid generalized
diagnostic; distinguish coding reliability from validity; describe what S1 changes;
explain why software agreement does not identify gatekeeping as a cause.

No final tag, release, submission, visibility change or collaborator invitation is
created by this technical task. Do not mark assessed completion from an agent pass.
''')
 # Keep source access/failures explicit, with cached targets distinguished from downloads.
 write('records/skill_invocations/2026-10-19_verify-and-package/failures_and_corrections.md','''# Execution failures and corrections

- New S1 script initially had a missing closing parenthesis. It failed before
  fitting; syntax corrected and all six fits then ran. No research input changed.
- A new country-label draft swapped codes3/4. Original DTA metadata established
  3=LEB,4=SUI. Labels/target matching corrected, prior draft archived and independent
  metadata checks added. Skill2 numerical results remained unchanged.
- Primary supplement directory/no-slash downloads returned HTTP404. The web tool
  recovered a cached primary table (crawler metadata two years old); targets and
  access limits are explicit. No live download is fabricated.
- Word COM was unavailable inside the sandbox. A permission review timed out;
  a permitted retry exported documents. A Close/Quit by-reference error was fixed.
  Explicit hidden Word export commands succeeded. No desktop LibreOffice was used.
- Packaged renderer temporary writes failed under Windows sandbox temp. Renderer
  scratch was bound to the verified project tmp directory; canonical rasterization
  then succeeded. Visual QA is recorded separately after the final render.
''')
 write('records/source_access/skill3_sources.md','''# Skill 3 primary source access

Article/assignment/author inputs retain their registered hashes. Stata16 primary
manual URLs and cached hashes are in outputs/diagnostics/glmm/method_source_manifest.json.
The official reliability snapshot is already registered in the restoration manifest.

The web tool accessed the primary Additional Analyses index and cached paper page
on 2026-10-19:
https://medcon-doc.github.io/documentation/content-analysis/additional-analyses/civility-outrage_paper/

It supplied all 25 ordinal AMEs with 50 interval endpoints. Its metadata reported
an older crawl; direct HTTP requests with and without trailing slash returned404.
The 75 entries are an explicitly labelled transcription in
outputs/published/verification_targets.csv, independently checked in the source
audit. A current live HTML download/hash is not claimed. Source numbers are not
used to estimate any model. No earlier comparison omitted target is silently lost.
''')
 print('Support records written; original inventory IDs preserved:',len(inv))
if __name__=='__main__':main()
