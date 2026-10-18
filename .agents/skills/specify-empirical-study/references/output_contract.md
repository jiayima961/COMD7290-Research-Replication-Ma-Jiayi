# Specification output contract

Use relative paths below inside the explicitly assigned output root. In a test root, all generated text must identify itself as a test artifact. Preserve existing human contributions and extend existing records rather than replacing them.

## Documents

- `docs/theory.md`: phenomenon, gap, contribution, concepts, mechanisms, H1a-H3b derivations, competing explanations, boundaries and provenance. No invented student voice or completed reading.
- `docs/variable_dictionary.csv`: concept, source_variable, actual_data_variable, unit, measurement_type, raw_values_meaning, values_meaning, reference_category, missing_rule, transformation, source_locator, verification_status. Additional useful columns are allowed.
- `docs/hypothesis_matrix.csv`: preserve the project's existing Table 1 columns. Add a unique row_id if splitting targets. Every distinct directional coefficient/contrast has a separate row. Include non-hypothesis targets. Before estimation, keep reproduced_values/discrepancy empty and scientific_conclusion explicitly not_run.
- `docs/analysis_inventory.csv`: analysis_id, analysis_type, source_locator, target, starting_inputs, model, transformations, script_path, output_path, comparison_target, status, blocker, coverage_note. Supplementary/unavailable targets remain visible. Preserve the established ID meanings below rather than silently repurposing IDs.
- `docs/design_and_models.md`: observation production, sample design, equations/syntax, target parameters, assumptions and rationale, original settings versus unresolved/deferred settings, prediction conventions, diagram/model/matrix links, and review status.
- `docs/model_diagram.mmd`: original diagram, Figure 1 number/title, node identifiers and explanatory note. Keep separate intercept variances for the two outcome models; do not imply an estimated cross-outcome covariance.
- `docs/model_diagram_map.csv`: node_id, construct_or_parameter, measurement_or_distribution, equation_or_syntax, analysis_id, matrix_row_ids, planned_script_path, source_locator. Planned files must be labelled planned if they do not yet exist.
- `docs/source_evidence.csv`: evidence_id, source_id, locator, supported_claim, evidence_type, verification_status. Keep direct evidence, inference and unresolved interpretation distinct.
- `docs/foundational_reading.md`: at least two cited candidates with complete verified bibliographic identifiers where accessible; exact inspected scope and AI interpretation; separate human read_scope/notes left unknown until supplied. Unavailable access is a gap, not a completed reading.
- `docs/student_review.md`: empty human-owned initial map/explanation and reading/decision fields, or links to unchanged supplied versions; AI work and pending status plainly labelled. No prefabricated acceptance.
- `docs/unresolved_decisions.csv`: issue_id, source_locator, question, current_evidence, consequence, owner, status. Include human contributions and deferred skill-2 implementation settings as appropriate.
- `records/specification_handoff.md`: source/specification versions, permitted scope, files, observed commands, checks, limitations and next authorized task. Identify tests as tests and do not assert independent statistical verification.

The hypothesis matrix keeps these Table 1 fields:

```text
analysis_id,hypothesis_id,source_locator,status_confirmatory_exploratory,theoretical_premise_mechanism,predicted_relationship,population_sampling,coding_unit_dependence,constructs_indicators,measurement_coding_missing,estimand_parameter_contrast,equation_syntax,estimator_settings,assumptions_intervals_diagnostics,published_rule,dataset_spec_versions,script_path,output_path,published_values_path,reproduced_values,discrepancy,scientific_conclusion,approval_status
```

## Machine-readable summary: docs/study_specification.json

Use schema_version `1.0`, a spec_version, artifact_kind (`test` or `study`), student_initial_explanation_status, student_reading_status, student_approval_status, and ready_for_estimation (false unless actual authorized approval and all model requirements are evidenced).

Required top-level arrays/objects:

- `sources`: entries with source_id, relative_path, sha256 and role for inspected local original inputs. Local input paths are relative to this output root. Missing sources need an explicit availability note rather than a fabricated checksum.
- `hypotheses`: entries with id, premise, mechanism, prediction, source_locator, targets. Targets contain model_id, predictor, comparison, expected_beta_sign (`positive` or `negative`), estimand, and source_locator. Define comparisons in the model's parameter direction, not an ambiguous verbal direction.
- `variables`: entries with id, actual_data_variable, measurement_type, analysis_unit, raw_values, analysis_values, transformation, missing_rule, source_locator, verification_status. Use arrays for finite numeric domains; dictionary/text is acceptable for identifiers. Do not recode source files in place.
- `models`: entries with id, outcome, family, link, analysis_unit, predictors, reference_categories, random_intercept_groups, equation, original_syntax, original_settings, implementation_status, source_locator. Predictors use the actual analysis variable names; do not add unmeasured mediators. Reference categories use meaningful labels.
- `reliability`: input_type, preserve_independent_ratings, original_weights, settings_status and source_locator.
- `coverage`: an entry per analysis inventory ID with analysis_id, analysis_type, target, source_locator, status. Keep results not_run. V1 also needs `components` containing both `important_descriptive` and `core_advanced_model`; these are planned checks, not claims of completed verification.
- `human_review`: initial_explanation_received, foundational_readings_attested, specification_approved (booleans), source_record, and note. Synthetic test text is never actual human evidence.
- `deferred`: an array identifying unresolved assumptions and the explicit user-deferred advanced implementation/equivalence task for skill 2.

Model IDs: M1 is item ordered logit; M2 is actor-reference outrage; M3 is actor-reference recognition. Use target comparisons `majoritarian_vs_consensus`, `contested_vs_stable`, `website_vs_blog`, `newspaper_vs_blog` where relevant. Family names are `ordered_logistic` and `bernoulli`; the link is `logit`. Raw and analysis categories are different when the author script recodes them.

## Stable analysis IDs

Keep these IDs and machine-readable analysis_type values aligned in the inventory and JSON coverage. Multiple matrix rows may share an ID for distinct subtargets. Add other IDs when needed rather than replacing a required target.

| ID | analysis_type | Required scope |
|---|---|---|
| D1 | item_descriptive | Item tone distributions and sample summaries |
| D2 | reference_descriptive | Reference outrage/recognition proportions |
| R1 | tone_reliability | Independent-rater tone agreement |
| R2 | reference_reliability | Independent-rater reference agreement |
| M1 | ordered_logit | Main item ordinal model |
| M2 | outrage_multilevel_logit | Main reference outrage model |
| M3 | recognition_multilevel_logit | Main reference recognition model |
| C1 | proportional_odds_diagnostics | Both original parallel-lines diagnostics; keep their different predictor coding visible |
| C2 | original_alternative_links | Original logit/probit/cloglog comparison |
| C3 | null_multilevel_comparison | Original empty multilevel versus single-level comparison |
| P1 | ordinal_predictions | All ordinal probabilities and discrete contrasts |
| P2 | binary_predictions | Both binary outcome probabilities and discrete contrasts |
| A1 | supplement_inventory | Complete supplementary coverage/access inventory |
| V1 | independent_statistical_verification | Independent important descriptive AND core advanced-model numerical checks |
| N1 | statistical_negative_check | Assignment harmless statistical failure/detection/recovery check on copied or synthetic inputs |
| S1 | additional_sensitivity | One separately justified sensitivity analysis beyond the faithful reproduction |

Software-equivalence preparation is distinct from V1; use an additional ID if useful. Skill-validator corruption tests do not complete N1. Repeating the paper's alternative-link checks does not automatically complete S1. These are future planned targets during skill 1, with their exact design awaiting the appropriate task and student review.

## Review principles

An automatic structural/consistency check cannot verify whether prose correctly interprets a theoretical source or that a student has understood it. Retain a source-based substantive inspection and the student's eventual review. Do not certify a research checkpoint from skill tests. When a full-output test lacks a foundational full text, record the access gap and limit the theory claim; never use the target paper's quotation as if the foundation itself were inspected.
