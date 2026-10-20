# Variable dictionary reader guide

Updated on 20 October 2026. The [complete CSV](variable_dictionary.csv) is the
canonical dictionary. Its 144 entries cover all 46 item-file fields, all 92
reference-file fields and six computational terms. Identically named fields are
documented separately for each file so their observation units and missingness
are explicit. Auxiliary metadata is not automatically an original model control.

## Main variables and coding

| Variable | Meaning and measurement | Exact faithful-analysis treatment |
|---|---|---|
| tone | Item outrage intensity, ordinal | Archive 1-5 minus one gives 0 no outrage through 4 very strong outrage. M1 uses the 1700 item rows. |
| actrefoutbin | Explicit reference outrage, binary | Preserve author 0 absent/1 present. M2 uses 3770 directed references. |
| actrefrecbin | Explicit reference recognition, binary | Preserve author 0 absent/1 present. M3 is fitted separately from M2. |
| polsys | Political system, nominal | Raw 1 consensus/2 majoritarian/3 mixed becomes analysis 1 consensus/2 mixed/3 majoritarian. Two dummy slopes, consensus base. |
| socdiv | Division over secularism, binary nominal | Raw 1 contested/2 stable becomes analysis 1 stable/2 contested. Stable base. |
| mediatype | Author analytical medium, nominal | Raw 1 blog/2 newspaper/3 website becomes analysis 1 blog/2 website/3 newspaper. Blog base. |
| text_id | Item identifier | Item random-intercept group in M2/M3. It is not a country identifier. |
| akteur_id and act_id | Originating actor/statement identifiers | Actor ID is local to an item. act_id concatenates text_id and akteur_id. 2453 groups in 1183 items. |
| country | Analytical country classification | Australia, Germany, Lebanon, Switzerland, Turkey and USA. Descriptive grouping and country deletion, not an extra main-model random level. |

The [model diagrams](model_diagram.md) show how these variables enter M1-M3.
The [hypothesis matrix](hypothesis_matrix.md) identifies the tested contrasts.

## The previously unfinished mappings

The target actor is represented by `bezug_akteur_id` and the archive object
identifier `respobj_akteur`. These must be distinguished from the originating
actor and the model's random-effect group. The archive originator identifier
`resp_akteur_akteur_id` maps one-to-one to the model's composite actor groups.

Evaluation maps to `valenz_akteur`. Genuine versus constructed responsiveness
maps to `genuinekonstruierte_resp_akteur`. Both fields have inconsistent numeric
descriptions across the codebook lists, examples and archive. The dictionary
records their actual stored domains and the exact source conflict. It does not
invent a fully verified semantic map. Neither field is an original M1-M3
predictor. Identity-weighted reliability retains the author's numeric categories.

The actor-characteristic entry has been split into general role, domestic or
foreign role, political level, domestic and foreign national role, party,
operational origin, gender, religious affiliation and their open-text fields.
Each now has its actual German archive name, codebook locator and observed
missingness. These are metadata repeated across references, not extra controls
or independently sampled people.

Article metadata is split into publication date, analytical outlet, title,
section, word length, journalistic genre, other genre and starting page. The
legacy outlet and administrative fields are also inventoried. The dictionary
distinguishes these from the author-prepared analytical classifications.

## Source differences to retain

`land` and `country` use different numeric country orders. Legacy `medientyp`
also differs from `mediatype`, with 52/1700 item disagreements under the expected
legacy category translation. The original script selects `mediatype`, so the
replication preserves it. These fields must not be swapped just because their
names appear similar.

The codebook says outrage and recognition cannot both be present in one
reference. One of 3770 author-prepared reference rows has both coded 1. The two
outcomes are modeled separately and the faithful reproduction retains that row.
This is a documented coding-rule exception, not an instruction to alter a value.
Valence cross-tabs also contain a few exceptions to the codebook's logical rules.

Some numerical auxiliary fields are loaded as object columns because they
contain missing values. Their Stata storage types, observed numeric domains,
system missing and numeric -99 codes are recorded separately. Integer storage
does not prove interval measurement. The recorded article-length field contains
a fractional positive value, so it is described as an intended word count with
an archive anomaly rather than silently rounded.

## How to inspect an entry

Use `dataset` and `actual_data_variable` to find the field. `raw_values_meaning`
describes the archive domain, while `values_meaning` and `transformation`
describe its interpretation and analytical treatment. `model_use` makes clear
whether it is a predictor, outcome, identifier or unused auxiliary variable.
`missing_rule` gives actual per-file counts and the faithful handling.

Each row has source and evidence locations. For unmodeled technical fields whose
upstream derivation was not documented by the supplied analysis code, the scope
is stated explicitly. A populated inventory is not a claim of complete recovery
of every upstream data-production operation. The main-model measures, coding,
references and grouping are fully specified for the executed reproduction.

Independent-coder ratings remain separate from these consensus analytical
files. Their exact column selections, code domains and missing rules are in
[the reliability column audit](../outputs/diagnostics/reliability/column_audit.csv)
and [sample audit](../outputs/diagnostics/reliability/sample_audit.json).
Never calculate independent-coder agreement from the consensus model outcomes.

The source-description evidence is saved in
[dataset_metadata.json](../outputs/diagnostics/measurement/dataset_metadata.json),
[field_inventory.csv](../outputs/diagnostics/measurement/field_inventory.csv) and
[semantic_checks.json](../outputs/diagnostics/measurement/semantic_checks.json).
These contain metadata and aggregate checks, not exported actor quotations or
subject-level records. Original inputs, fitted estimates and the final report
were not modified. Student review of the documentation remains separate.
