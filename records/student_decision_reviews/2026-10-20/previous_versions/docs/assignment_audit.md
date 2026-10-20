# Assignment completion audit

Later follow-up on 20 October 2026. The user-requested dictionary and diagram
documentation is now complete. See the [dictionary guide](variable_dictionary.md)
and [model diagrams](model_diagram.md), including the source/domain/missingness
inventory, both numbered figures and the equation/code/matrix node map. Actual
codebook/archive conflicts are documented without changing author data. Student
diagram review and the final-report reference remain separate. The technical
documentation findings in the earlier audit below describe the prior state.

Follow-up on 20 October 2026. The matrix finding below has been resolved by the
user-requested documentation update. The [completed matrix](hypothesis_matrix.csv)
now contains 28 fully populated rows with a [reader guide](hypothesis_matrix.md).
Its 12 directional tests, three additional mixed-system comparisons and 13
supporting analyses are linked to saved code, outputs and diagnostics. The
original audit findings below remain as the record of what was observed before
this correction. No other audit item or student approval is closed by this update.

Checked on 20 October 2026 against all 21 pages of the teacher's assignment and
the saved project files. The individual final report was excluded. This audit
does not certify student understanding or acceptance and does not create a release.

## Overall finding

The principal computational work and its supporting evidence are saved. All 45
listed core artifacts exist. Saved records cover reliability, descriptives,
M1/M2/M3, predictions, diagnostics, comparison, independent checks, negative-test
recovery, clean reruns and country-deletion sensitivity. All 86 protected source
and existing numerical files still match the recorded hashes.

Several documentation and personal-review requirements remain incomplete. The
presence of a file or a successful earlier numerical audit does not establish
that every assignment requirement is finished. The earlier checklist overstated
the completeness of the central matrix and did not expose every stale document.

## Technical documentation that still needs completion

| Priority | Assignment requirement | Current finding | Work needed |
|---|---|---|---|
| 1 | Central hypothesis-to-evidence matrix, pp. 2–3 | docs/hypothesis_matrix.csv has 25 rows. Its 12 hypothesis rows contain results, but 13 supporting-analysis rows leave 11 specification fields blank. S1 still says not_yet_implemented even though it was run. | Complete the supporting rows using the existing source, execution and comparison records. Explain genuinely inapplicable fields rather than leaving them ambiguous. Correct S1's status and paths. Preserve the existing numerical outputs. |
| 2 | Own construction of the advanced-model diagram, pp. 4–5 | docs/model_diagram.mmd is an early AI draft. It gives the nested structure, but omits explicit category indicators, coding, separate outcome-specific parameters, estimation details and a complete link to executing code and matrix rows. Its note still calls resolved settings unresolved. A more detailed diagram map exists only inside a synthetic test case. | Produce a current study diagram and mapping using the actual specification. Number and title it as Figure 1. Obtain the student's review or reconstruction. The teacher also requires referring to it in the individual report, which was not inspected here. Do not relabel an AI diagram as an unaided student drawing. |
| 3 | Measurement dictionary, pp. 3–4 and 11–12 | Eight main-analysis rows have verification notes. Five auxiliary rows still contain pending mappings. Metadata inspection confirms that related evaluation, reference-construction, actor-characteristic and article-metadata fields exist in the author files. | Finish the codebook-to-column mapping and value-label checks. Distinguish variables used in the analyses from background fields. The missing work is documentation, not proof that the underlying columns are absent. |
| 4 | File-based recovery of an approved study state, pp. 5–6 and 14–15 | A genuine isolated first-skill recovery test and separate reviewer records exist. records/handoffs.md still describes the final approved-study handoff as pending and contains obsolete skill-2/skill-3 deferral text. | After actual student review, record a receiving session recovering the accepted specification and evidence versions from files. Preserve the earlier synthetic demonstration as such. This does not require another expensive full model fit merely to recover context. |
| 5 | Current navigation and dated approvals, pp. 5–6 and 13–15 | Some current worksheets retain old statements such as skill 2 being deferred or S1 being unfinished. The main README also calls the repository private, which no longer matches live GitHub metadata. | Update current navigation and checkpoint wording without changing historical receipts or inventing earlier approvals. Make the combined analysis/run_verified_replication.py command prominent in the teacher quickstart. |

The central diagram needs a source-to-equation-to-code mapping, not a particular
mandatory filename. A JSON specification file is likewise not a separate teacher
requirement when the saved equations and syntax are unambiguous.

## Sensitivity wording needs a clear decision

The six saved country deletions are a substantive influence analysis of M1. They
change the country composition while retaining the likelihood and predictor form.
They are correctly separated from the faithful reproduction and explicitly state
the changed sample. The teacher's wording on p. 13 asks for specification sensitivity.
An instructor may accept a justified sample-composition sensitivity, but the
audit cannot treat that interpretation as certain.

The already proposed country-indicator ordered-logit model would meet the
specification wording more directly by replacing national-category predictors
with country indicators. It has not been executed or accepted by the student.
If used to close this wording gap, it needs its own approved scope, saved fit,
diagnostics, estimates and comparison. It must not replace the original M1.
This is a proposed addition, not a newly completed result.

## Work that requires the student's own contribution

The assignment requires at least two cited foundational theoretical or
methodological sources to inform the reconstruction on p. 2. The record does not
yet contain the student's direct reading scopes and notes. Two source PDFs and
AI reading notes exist, but those do not establish personal reading. Add the
full references, pages or sections actually read, and a short explanation of what
each source contributes to the study. Record partial reading honestly.

The student supplied v1 and v2 theory explanations and both AI critiques are
saved. A separate preliminary student theory map and explicit acceptance of the
complete specification have not been recorded. A map can still be constructed
and reviewed now, but it must not be described as having preceded the AI advice.
The teacher asks for versioned approval before final estimation. D011 records
actual authorization to fit, but the files do not demonstrate a separate prior
review of the complete specification. Record the real chronology and present
review rather than backdating approval.

At least three consequential AI decisions require the student's acceptance or
correction with reasons under p. 11. records/skill3_decision_audit.md contains
seven technically checked choices, but every student-response field is pending.
After those decisions are supplied, update the relevant checkpoint and handoff
records. Technical passes cannot supply personal acceptance. Personal inspection
of the complex results and clean-setup access, together with oral-defence
preparation, also remains required under pp. 13–16.

## Documents and execution evidence already saved

| Requirement group | Current evidence |
|---|---|
| Theory, hypotheses and design | Student v1/v2, both critiques, docs/theory.md, docs/hypothesis_matrix.csv, docs/design_and_models.md and docs/execution_specification.md |
| Sources and environment | records/source_manifest.csv, sources/input_restore_manifest.json, requirements-lock.txt, environment.md and the teacher quickstart |
| Three reusable skills and controlled functions | .agents/skills/ and actual invocation, discovery, branch review and test records under records/ |
| Content-analysis statistics | Reliability, descriptives, ordinal tone, both nested binary models, probability summaries and marginal effects under outputs/reproduced/ |
| Numerical comparisons and interpretation | outputs/verification/comparison_all.csv, coverage, diagnostics, independent checks, interpretation audit and docs/limitations.md |
| Negative test and clean rebuild | Copied invalid-category detection and recovery, both clean-run receipts and analysis/run_verified_replication.py |
| Additional sensitivity | Six-country deletion plan, all six fits and 30 coefficient rows under outputs/verification/sensitivity/ |
| Follow-up design | docs/follow_up.md, a 418-word brief covering the question, hypothesis, existing sample, measurement, model and interpretation. The teacher does not require collecting new data or executing this future proposal. Confirm the final presentation occupies one page if exporting it. |
| Two technical Word documents | report/verification/01_results_comparison.docx and 02_python_stata_equivalence.docx, with editable sources and their existing page-review records |

The complete comparison retains unavailable targets and the invalid diagnostic
rather than claiming exact equality for everything. Independent binary checks
evaluate likelihood and curvature at fixed parameters. Independent optimization
was done for M1, not M2/M3 in another engine. Both clean runs reused the installed
environment. These documented boundaries do not imply that the core saved
statistical work is missing.

## GitHub access and final version information

Read-only GitHub checks on 20 October 2026 returned a public repository and main
commit e3f23cc71d9fe1c6bbe4528d68503fefcb895fd5. The releases list and tag-reference
list were empty. The permission endpoint returned read for fffchaobu. Because
the repository is public, that response alone does not establish collaborator
membership or acceptance of an invitation. The student should verify the
invitation or collaborator entry in the repository settings and record the
actual status. No invitation or visibility change was made by this audit.

The assessed version is the fixed repository snapshot the teacher will mark.
A tag is its readable label, a release packages that tagged version, and the
full commit identifier specifies the exact source and evidence snapshot. Pages
15–16 require a fixed tag, a named release and the full commit ID. Merely citing
the moving main branch or an arbitrary latest commit does not complete that task.

For now, leave assessed release and tag pending final freeze in the report.
After acceptance, choose the source/evidence commit, create its tag and named
release, and enter those real details in the access block. Attach the same
accepted report to the release and Moodle. Preserve the tag afterward and record
later corrections separately. No assessed release was created here.

The current working Word report and its versions remain excluded from this
audit. A root-level Word filename created by the student was not covered by the
older filename-specific ignore rule. The local ignore rule now covers all Word
files directly under report/, including its lock file, while retaining the two
technical Word reports in report/verification/ for sharing.

## Practical completion order

1. Complete the central matrix, measurement dictionary and current diagram package.
2. Supply actual reading notes, personal map or diagram review, and at least three decision responses.
3. Record specification review and decide how to satisfy the sensitivity wording.
4. Close the approved-study handoff and dated checkpoint records using actual actions.
5. Verify collaborator status and final access from a clean setup.
6. After accepting the report and repository, create the assessed tag/release, record its full commit and submit the identical report as instructed.

Deadline and grade weighting are announced on Moodle and are not available in
the supplied PDF. They still need checking there. A web app, deployment, multiple
AI providers, CI and AI recoding of the source texts are not mandatory additions.

Detailed machine-readable evidence is saved at
records/assignment_audit/2026-10-20/audit_evidence.json. This audit and its local
navigation updates have not been pushed to GitHub.

## Sources

Teacher-supplied COMD7290_assignment.pdf, pp. 1–16 and Option 3 on pp. 18–19.
SHA-256 0cd8bc6273af22288d13ad1e11f1c224322509e81b7c9ba16ff1faeaabe945fe.

GitHub official explanation of releases and tags was checked at
https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases
