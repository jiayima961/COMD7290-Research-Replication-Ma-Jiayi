TEST ARTIFACT — isolated specification forward test; not scientific approval.

# Invocation, recovery and handoff receipt

Specification: forward-test-1.0.0; schema 1.0; artifact_kind=test. Output root: E:/Statistics with AI/COMD7290-Research Replication-Ma Jiayi/records/skill_tests/specify-empirical-study/forward_case. Only this root was written. No canonical study drafts were read. Raw inputs were not modified, recoded in place, published, committed or uploaded.

Final observed validation: **technical_pass**, zero errors; warnings only for pending real student approval and deferred settings. `ready_for_estimation=false`, models fitted by validator=false, statistical equivalence verified=false. The canonical validator was run before and after the final diagram/matrix edits. records/output_consistency_check.json additionally reports 12 passing cross-file checks, including not_run conclusions, source hashes, preserved fixture, diagram-node mappings and human false fields. No reviewer correction was needed to pass the canonical validator; source-driven corrections were the synthetic H2b direction and the fixture's measurement/nesting/reliability/inference claims. Exact delegated request and scope clarification are preserved in records/invocation_request.md.

Observed runtime: RTK 0.43.3; project Python 3.12.14; pandas3.0.6; openpyxl3.1.5. These were inspected, not installed or upgraded. The separate bundled Python ran pypdf extraction. Final additional commands: `rtk proxy <project python> tmp/check_outputs.py` and `rtk --version`.

## Explicit invocation and discovery evidence

Task received: “Independently forward-test a revised Codex project skill. Use $specify-empirical-study … reconstruct the selected paper's theory, six hypotheses, measurement dictionary and analytical specification from the original evidence; give source-linked feedback on the initial explanation in synthetic_initial_explanation.md.” Scope also required English test labels, no fitting/reliability/engine validation, two cited foundations, source hashes and the canonical validator. This is an explicit named invocation followed by manual reading of the canonical SKILL.md and references/output_contract.md. The agent did not observe native discovery in this isolated task. The parent reports a separate app-server discovery pass in discovery.json outside this root; that report is not substituted for locally observed invocation evidence.

Recovery occurred first from README.md,AGENTS.md,STATUS.md,records/decisions.md,input_manifest.json, after bootstrapping E:/Codex/RTK.md. The bootstrap used `Get-Content -LiteralPath E:\Codex\RTK.md` to learn the wrapper rule; every subsequent shell command used rtk. The real student had explicitly postponed their preliminary explanation; no clarification was requested or human evidence fabricated. The evaluator fixture is copied byte-for-byte to records/inputs/synthetic_initial_explanation.v1.md with provenance/hash, and feedback is separate.

## Sources and observed operations

The authoritative case input list is input_manifest.json, containing14 files. All14 SHA256 hashes matched (records/input_hash_check.json). The copied records/source_manifest.csv contains additional archive/readme/web-page rows that are not available within this case; none was falsely claimed inspected or assigned a fabricated hash. Source IDs, relative paths and hashes for actual originals are bound in docs/study_specification.json. The provided extraction text was used for page reading; critical original PDF scopes were independently re-extracted through pypdf (records/pdf_scope_check.json). Source scope is not a human reading attestation.

Observed shell command forms (all paths below resolved from this case root unless absolute):

```text
rtk read README.md AGENTS.md STATUS.md records/decisions.md input_manifest.json
rtk read <canonical skill>/SKILL.md
rtk read <canonical skill>/references/output_contract.md synthetic_initial_explanation.md input_metadata.json records/source_manifest.csv
rtk ls tmp/source_text/<source directories>
rtk read sources/author_code/MedCon_Civility_an.do sources/author_code/reliability_original.do
rtk read <canonical skill>/scripts/validate_specification.py
rtk read tmp/source_text/<page-specific article,assignment,codebook,and foundation files>
rtk rg -n <source locator patterns> tmp/source_text/COMD7290_assignment
rtk rg -n <recode/model/reliability patterns> sources/author_code
rtk proxy E:/Statistics with AI/COMD7290-Research Replication-Ma Jiayi/.venv/Scripts/python.exe tmp/probe_inputs.py
rtk proxy C:/Users/86150/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe tmp/check_pdf_pages.py
rtk proxy <project python> -c <read-only selected input_metadata JSON display>
rtk proxy <project python> tmp/build_test_specification.py
rtk proxy <project python> <canonical skill>/scripts/validate_specification.py --root <case root> --output <case root>/records/specification_validation.json
```

These are observed command forms with repeated page reads compacted, not a claim that ellipses were executed literally. The exact generating/check scripts are retained in tmp/. No statistical model code, reliability function, alternate engine, network research or dependency installation was run. Pandas read DTA domains/missing metadata and XLSX sheet/column headers only. Pypdf emitted three object-pointer warnings and returned the requested text. Authored outputs were written through apply_patch and the retained generator; planned analysis/*.py paths were not created.

## Produced files and scientific checks

docs/theory.md; variable_dictionary.csv; hypothesis_matrix.csv; analysis_inventory.csv; design_and_models.md; model_diagram.mmd; model_diagram_map.csv; source_evidence.csv; foundational_reading.md; student_review.md; unresolved_decisions.csv; study_specification.json; synthetic_draft_feedback.md; published_comparison_targets.csv. Records additionally retain the fixture version/provenance, hash report, PDF scope report and canonical validation JSON.

Substantive source checks: all six predictions retain their theory direction; 12 distinct directional coefficients are split by outcome and professional medium; mixed-system comparisons are exploratory. Tone raw1–5 differs from analysis0–4. The binary models are distinct nested actor/item logits, with no country hierarchy, measured mediator or cross-outcome covariance. Ratings and consensus data are kept separate; original identity reliability weights are retained. All inventory targets, including missing supplementary tables and deferred validation, remain visible and not_run. Published values are comparison-only; reproduced_values and discrepancy remain blank. The Mermaid source shows every dummy/base, observed outcome, link and separate variance; node IDs map to equations/matrix/planned paths. Mermaid source is authored, but no graphical renderer was invoked.

Two cited foundations were inspected with exact scope: Sobieraj/Berry selected full-text conceptual sections (PDF1–5,7), and Wolfe/Gould complete sg76(PDF/printed24–27). Human reading remains unknown. The target paper was read after publication; batching exposed early results before the theory document was drafted, so no blinded prospective derivation is claimed.

## Limits and next authorized work

This is an independent fresh-context behavior test, not independent statistical verification. No estimation or reliability coefficient was produced, and the Python three-level implementation was not verified. Human initial explanation, foundational reading attestation and specification acceptance all remain false/pending. A technical validator pass does not change those states or imply ready_for_estimation.

Source uncertainties: contradictory codebook numbers and undocumented upstream binary recodes; exact actor/statement semantics; numeric omodel versus factor model; pseudo-R² terminology; margins conventions; unpinned original build/add-ons/optimizer/integration defaults; variance-boundary/null LR details; rater import placeholders; missing standalone appendix tables; unlocated preregistration. Additional source access would be a later task. None blocks the independent source-supported specification claims.

Skill observation: no execution-blocking instruction defect was encountered. The validator checks presence, JSON invariants and selected CSV fields, but does not certify prose meaning, diagram rendering, actual human reading or numerical equivalence; those limitations are explicitly stated by the skill. Code inspection also shows it does not enforce every CSV scientific_conclusion value as not_run, so this test checks that condition substantively. No validator modification was made.

Next authorized handoff is review of these test artifacts by the evaluator. For a real study, the student's own preliminary explanation/readings and scientific decisions must be supplied separately. Skill2 may later validate original settings and equivalence only when authorized; this receipt supplies the specification, source versions and unresolved checks, and does not start that work.
