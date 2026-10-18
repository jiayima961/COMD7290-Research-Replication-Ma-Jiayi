# Skill 1 evaluation plan

Prepared 2026-10-18 before reviewing forward-test outputs. Scope: preparation and test of `specify-empirical-study` only.

The actual student deferred their preliminary explanation and reading notes. The current evaluation uses an explicitly synthetic explanation in an isolated case. No personal feedback on a real student's explanation or acceptance of the canonical research specification is being recorded.

## Tests and evidence

1. Official skill-creator static validation checks metadata and scaffold validity. It is not a behavior test.
2. Query the installed Codex CLI 0.160.1 app-server's `skills/list` with the actual project cwd and forceReload. Retain relevant metadata, enabled state, scope and skill-file hashes in `discovery.json`. Discovery alone does not invoke a skill.
   Also check the parent workspace as a directory negative control. Its missing repository skills establish the need for the correct working directory or an explicit full-path invocation; this expected absence is not an automatic-discovery success.
3. Explicitly invoke the named skill in a fresh native Codex agent context, using raw source inputs and its own file-based context. Give it no earlier AI canonical drafts or evaluation answer. The permitted write path is `forward_case/`; the task ID and exact prompt are retained separately.
4. Inspect the produced theory, dictionary, matrix, equations, diagram, source/reading record, synthetic feedback and handoff against original sources. Check each target separately; file existence alone is not enough.
5. Run one positive specification check and eight deliberate in-memory corruptions: reversed author prediction, ordinal/continuous confusion, incorrect nesting, consensus reliability inputs, changed reliability weights, invented student approval, premature readiness and changed source hash. Record expected versus actual error codes and confirm input hashes are unchanged.
6. Preserve the fresh-context recovery receipt and source/version bindings. This is a workflow handoff demonstration and behavior check, not independent numerical or statistical verification.

## Pass criteria and limits

A pass requires real runtime discovery, actual explicit use of the skill, completed source-linked test outputs, successful technical validation, observed appropriate response to the synthetic mistakes, correctly rejected corruptions, and preserved originals. Foundational AI reading is recorded separately from unknown student reading. Original Stata specifications must be documented while Python three-level validation remains deferred to skill 2. No research results or completed study checkpoint may be invented.

The deterministic tests cannot establish the correctness of a theoretical interpretation or genuine human approval. A separate source-based substantive inspection is required. The assignment's independent descriptive/advanced-model calculations and statistical-pipeline negative test remain later tasks.

## Post-test amendment: observed coverage defect

The first blind invocation passed the initial validator, but the evaluator's substantive review found that several analysis IDs had changed meanings. In particular, null-model and supplementary tasks occupied N1/S1, omitting the assignment's harmless statistical negative check and separate sensitivity target; V1 covered software equivalence rather than both independent numerical checks. This is a real missed condition, not a successful coverage test. The initial artifacts/receipts are preserved under the case's `records/iterations/initial/` and this directory's `iterations/initial/`.

Version 1.0.1 therefore defines stable ID meanings and analysis_type fields, requires both V1 components, and enforces not_run scientific conclusions in the matrix. The independent agent receives this narrow review correction after its first blind pass. Add three deliberate corruptions to the original nine-case suite: repurposed N1 type, missing advanced verification component, and a premature matrix conclusion. Final expected suite: one positive and eleven negative cases. The corrected run is explicitly a post-review iteration, not a second blind evaluation.

## Attribution and guidance

Adapted the existing project skill using the installed `skill-creator` instructions at `E:/Codex/skills/.system/skill-creator/SKILL.md`. Runtime discovery and testing design were checked against official OpenAI documentation: <https://learn.chatgpt.com/docs/build-skills> and <https://developers.openai.com/blog/eval-skills>. No external skill has been represented as student-authored research.
