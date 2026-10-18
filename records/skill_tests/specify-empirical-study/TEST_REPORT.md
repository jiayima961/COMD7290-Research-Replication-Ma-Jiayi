# First-skill preparation and test report

Date: 2026-10-18. Skill: `specify-empirical-study` version **1.0.1**. Final case specification: `forward-test-1.0.1`.

**Result: skill preparation and synthetic behavior testing completed after a documented review correction.** Official static validation passed; actual repository-cwd discovery passed; the named skill was invoked in an isolated fresh context; the corrected output passed the canonical specification validator and all 12 regression cases. Real student critique, scientific approval and research estimation remain pending.

## Scope and attribution

The student explicitly postponed their own preliminary theory explanation until the skill was ready. The test therefore uses an evaluator-created synthetic explanation, visibly labelled and preserved unchanged. It does not fabricate student authorship, foundational reading or acceptance. Canonical study drafts in the main `docs/` directory were preserved.

The existing project skill was revised using the installed [skill-creator guidance](E:/Codex/skills/.system/skill-creator/SKILL.md). Its responsibilities now cover source-based theory/gap reconstruction, six hypotheses and their mechanisms, actual variable coding, three original models, complete analysis coverage, an original diagram, personal-feedback boundaries and a traceable handoff. The [output contract](../../../.agents/skills/specify-empirical-study/references/output_contract.md) and [validator](../../../.agents/skills/specify-empirical-study/scripts/validate_specification.py) make key requirements checkable. The [usage guide](../../../docs/skill1_usage.md) explains the later real invocation.

## Discovery and actual invocation

| Evidence | Observed result | Record |
|---|---|---|
| Official `quick_validate.py` | Skill is valid | [Preflight checks](preflight_checks.json) |
| Installed Codex 0.160.1 app-server `skills/list` from repository cwd | All three project skills enabled, scope=repo; final skill hash recorded | [Discovery](discovery.json) |
| Same query from outer workspace `E:/Statistics with AI` | No nested project skills; expected directory negative control. Its raw status is failed because the probe expects all three | [Parent directory control](discovery_parent_folder.json) |
| Explicit named/full-path invocation | Native agent `/root/skill1_forward_test`, fork_turns=none, no model override; manually loaded the named skill | [Exact prompt](forward_test_prompt.txt), [runtime](runtime_record.json), [receipt](forward_case/records/specification_handoff.md) |
| File-based context recovery | Read case README, AGENTS, STATUS, decisions and input manifest; inspected original evidence without earlier canonical AI research drafts | [Handoff receipt](forward_case/records/specification_handoff.md) |

Discovery and manual full-path invocation are separate observations. Automatic discovery from the outer chat directory is not claimed. The native receipt did not expose an exact model identifier. The handoff retains observed command forms with repeated reads compacted; it is not a complete raw shell transcript. It also discloses the initial unwrapped RTK instruction read, followed by RTK-wrapped commands.

## Source-based inspection and outputs

Fourteen original case inputs are bound by SHA256: assignment, selected article, four codebooks, author analysis and reliability syntax, two analytical DTA files, two independent-rating workbooks and two cited foundations. The input hashes match. Source PDFs, code and data remain local and Git-ignored.

AI reading scopes are explicit: Sobieraj and Berry (2011), selected conceptual sections at PDF pages 1–5 and 7; Wolfe and Gould (1998), complete sg76 article at PDF/printed pages 24–27. These are separate from unknown human reading. Original source warnings and access gaps are retained.

| Substantive check | Source and finding |
|---|---|
| Theory and predictions | Article printed pp.274–278: all six original predictions retained; 12 coefficient targets separate outcome and medium; mixed-system contrasts remain exploratory |
| Actual measurement | Codebooks 1/2/5/8, author recodes and DTA metadata: ordinal item tone raw 1–5 becomes analysis 0–4; binary reference outcomes remain distinct; unmeasured mechanisms are not invented covariates |
| Model specification | Article Tables 3–4 and author syntax: M1 ordered logit with four thresholds; M2/M3 separate Bernoulli logits with actor/statement groups nested in items; no country random-effect hierarchy or joint outcome covariance |
| Reliability | Original rating workbooks and syntax: independent ratings retained, author identity weights recorded; consensus data are not substituted |
| Interpretation | Ordinal odds, conditional binary odds and probability contrasts distinguished; observational differences are not automatically causal effects; non-significance does not prove no association or adequate fit |
| Full coverage | Original diagnostics, alternative links, null models, probabilities, supplementary gaps and distinct future assignment checks retained after correction |
| Diagram and traceability | Original Mermaid source shows dummy variables/bases, levels, links, thresholds and separate variances; node map resolves to equations and matrix rows. Source inspected; no graphical rendering claimed |
| Human contribution and timing | Synthetic fixture byte-preserved, feedback separate, real human attestations false, ready_for_estimation=false. Published results were already available; no blinded prospective derivation claimed |

The case contains **14 specification documents**, **19 inventory IDs**, **29 matrix rows**, including **12 directional targets**. Start with [theory](forward_case/docs/theory.md), [hypothesis matrix](forward_case/docs/hypothesis_matrix.csv), [dictionary](forward_case/docs/variable_dictionary.csv), [models](forward_case/docs/design_and_models.md), [diagram](forward_case/docs/model_diagram.mmd) and [synthetic feedback](forward_case/docs/synthetic_draft_feedback.md). The [source-evidence table](forward_case/docs/source_evidence.csv), [reading record](forward_case/docs/foundational_reading.md), [unresolved decisions](forward_case/docs/unresolved_decisions.csv), [student worksheet](forward_case/docs/student_review.md) and [JSON specification](forward_case/docs/study_specification.json) retain provenance and pending decisions. These are test examples, not accepted student work.

## Observed failure and correction

The first blind invocation technically passed the initial validator, but evaluator inspection found a semantic coverage defect: N1 had become a null-model comparison, S1 a supplementary inventory and V1 software equivalence. This omitted the assignment's harmless statistical negative check, separate sensitivity analysis and independent descriptive/advanced numerical verification. The old validator checked ID presence without their meanings.

The initial artifacts were preserved byte-for-byte under [initial case snapshots](forward_case/records/iterations/initial/snapshot_manifest.json); initial discovery/regression receipts are in `iterations/initial/`. Skill 1.0.1 adds stable ID/type mappings, both V1 components and explicit not_run conclusions. The same agent applied this narrow review correction and retained an [ID crosswalk](forward_case/records/analysis_id_crosswalk.csv) and [correction receipt](forward_case/records/coverage_review_corrections.md). The revised case is a post-review iteration, not a second blind evaluation. Its proposed future sensitivity and negative-check designs remain unapproved plans.

## Final checks

- [Canonical validation](forward_case/records/specification_validation.json): technical_pass, zero errors; student-review and deferred-setting warnings remain.
- [Cross-file inspection](forward_case/records/output_consistency_check.json): all 17 checks pass, including mappings, not_run fields, unchanged inputs and initial snapshot identity.
- [Regression suite](validator_cases.json): **12/12 pass** — one valid specification plus eleven in-memory corruptions. It detects reversed H2b, continuous tone, incorrect nesting, consensus reliability input, changed weights, synthetic human approval, premature estimation readiness, changed source hash, repurposed analysis ID, missing advanced verification and a premature CSV conclusion. Research inputs were not altered.
- [Preflight](preflight_checks.json): repository material checks, canonical-draft preservation, original-input ignore rules and Git whitespace checks pass.
- [Delivery audit](deliverable_audit.json): local source preservation, English authored text and final file fingerprints.

Re-run the deterministic checks from the repository root:

```powershell
rtk proxy .venv/Scripts/python.exe tools/prepare_specification_test.py --case-root records/skill_tests/specify-empirical-study/forward_case
rtk proxy .venv/Scripts/python.exe .agents/skills/specify-empirical-study/scripts/validate_specification.py --root records/skill_tests/specify-empirical-study/forward_case --output records/skill_tests/specify-empirical-study/forward_case/records/specification_validation.json
rtk proxy .venv/Scripts/python.exe tests/skill1_specification/test_validator_cases.py --case-root records/skill_tests/specify-empirical-study/forward_case --output records/skill_tests/specify-empirical-study/validator_cases.json
```

The preparation helper restores only missing local original inputs with matching registered hashes; it does not overwrite authored outputs. The no-dependency skill validator uses Python's standard library. Re-running it does not repeat the independent agent behavior test or certify prose correctness.

## Remaining boundaries

No research model, reliability coefficient, numerical reproduction, statistical-pipeline negative check or sensitivity fit was executed. The specification corruption suite does not complete the assignment's N1. Fresh-context recovery does not constitute independent statistical verification. No checkpoint, student reading or scientific approval is marked complete. Three-level Python/Stata validation remains explicitly deferred to skill 2.

Unresolved matters include conflicting codebook numbers, undocumented upstream binary recodes, exact actor/statement identifiers, numeric versus factor coding in `omodel`, the pseudo-R2 naming discrepancy, missing standalone supplementary tables, and unpinned prediction/integration/software defaults. They remain visible for the appropriate next task.

After the student supplies their real preliminary explanation and reading notes, invoke this skill to preserve that contribution and provide source-linked personal critique. New materials in this task are saved locally; GitHub synchronization or submission is not claimed.
