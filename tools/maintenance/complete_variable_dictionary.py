"""Document archive fields and model-derived quantities without changing data."""
from pathlib import Path
from hashlib import sha256
import csv
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs"
META = json.loads((ROOT / "outputs/diagnostics/measurement/dataset_metadata.json").read_text())
BOOK1 = "sources/local/codebook_01_news_item.pdf"
BOOK2 = "sources/local/codebook_02_actor_identification.pdf"
BOOK5 = "sources/local/codebook_05_actor.pdf"
BOOK8 = "sources/local/codebook_08_actor_reference.pdf"
SPEC = "source-faithful-python-1.0.0"
SPECS = {}


def spec(var, concept, source, unit, kind, meaning, locator, role="Not used in M1/M2/M3", note="None identified", transform="Preserve original field unchanged"):
    SPECS[var] = dict(concept=concept, source_variable=source, unit=unit, measurement_type=kind,
                      values_meaning=meaning, source_locator=locator, model_use=role,
                      source_conflict_or_limit=note, transformation=transform)


def build_specs():
    spec("tone", "Overall intensity of item outrage", "TONE", "news item", "ordinal",
         "Archive 1,2,3,4,5 correspond after subtracting one to 0 no outrage, 1 slight, 2 moderate, 3 strong, 4 very strong outrage.",
         BOOK1 + " PDF pp.6-7, printed pp.4-5, section 1.11. Author analysis code tone recode. Article Table 3.",
         "M1 outcome in item file. Item metadata repeated in reference file, not an M2/M3 outcome.",
         "The codebook scale is 0-4, while the supplied archive stores 1-5. Do not subtract one twice.", "For M1, tone_analysis=tone_archive-1")
    for var, label, source, section, role in [
        ("actrefoutbin", "Explicit directed-reference outrage", "ACTREF_OUTRAGE_ACTOR", "8.8-8.9", "M2 outcome"),
        ("actrefrecbin", "Explicit directed-reference recognition", "ACTREF_RECOGNITION_ACTOR", "8.6-8.7", "M3 outcome")]:
        spec(var, label, source, "directed actor reference", "binary",
             "Author-prepared analytical value 0=absence, 1=explicit presence. This is communicative content or described gesture, not a measured audience emotion.",
             BOOK8 + f" PDF pp.7-9, printed pp.5-7, sections {section}. Author Analysis 4 and Article Table 4.", role,
             "Codebook lists 1=no and 2=yes but instructions/examples use 1=yes. Archive 0/1 is retained. One of 3770 references has both outcomes equal to 1 despite the codebook exclusion rule.")
    spec("polsys", "Political-system classification", "country-derived classification", "country context attached to item", "nominal",
         "Archive 1=consensus, 2=majoritarian, 3=mixed. Analysis 1=consensus, 2=mixed, 3=majoritarian.",
         "Article Table 1 and Political Systems section. Archive value labels. Author analysis recode polsys.",
         "Two fixed indicators in M1/M2/M3, reference consensus. No random country intercept.",
         transform="Archive 1/2/3 -> analysis 1/3/2. Create separate mixed and majoritarian 0/1 indicators.")
    spec("socdiv", "Socio-cultural division over secularism", "country-derived classification", "country context attached to item", "binary nominal",
         "Archive 1=contested secularism, 2=stable secularism. Analysis 1=stable, 2=contested.",
         "Article Table 1 and Socio-Cultural Division section. Archive value labels. Author analysis recode socdiv.",
         "One fixed contested indicator in M1/M2/M3, reference stable secularism.",
         transform="Archive 1/2 -> analysis 2/1. Create contested=I(socdiv_analysis=2).")
    spec("mediatype", "Author analytical media category", "MEDIATYPE / author-prepared Mediatype", "news item", "nominal",
         "Archive 1=blog, 2=newspaper, 3=website. Analysis 1=blog, 2=website, 3=newspaper.",
         BOOK1 + " PDF p.3, printed p.1, section 1.2. Archive value labels and author analysis recode mediatype.",
         "Two fixed indicators in M1/M2/M3, reference blogs.",
         "Use this author-selected field. Legacy medientyp has 52 disagreements among 1700 items after its expected category translation.",
         "Archive 1/2/3 -> analysis 1/3/2. Create website and newspaper 0/1 indicators.")
    spec("country", "Author analytical country", "COUNTRY / author-prepared Country", "news item / national context", "nominal",
         "1=Australia, 2=Germany, 3=Lebanon, 4=Switzerland, 5=Turkey, 6=USA.",
         "Archive value labels, Article Table 1, " + BOOK1 + " section 1.1.",
         "D1/D2 grouping and S1 sample deletion. Not an additional M1/M2/M3 covariate or random grouping level.")
    for var, concept, role, meaning in [
        ("text_idx", "Archive item index", "Cross-file item link and uniqueness checks", "String item identifier, unique among 1700 item rows and repeated on reference rows."),
        ("text_id", "Author item grouping ID", "M2/M3 item random-intercept grouping", "String news-item ID. 1700 in item file, 1183 represented in the reference file."),
        ("akteur_id", "Within-item originating actor/statement ID", "Part of the M2/M3 nested actor grouping", "String actor/statement sequence ID, reusable in other items. It is not a globally unique person identifier."),
        ("actref_idx", "Directed-reference index", "Reference uniqueness checks", "Unique string ID for each of the 3770 directed references."),
        ("resp_akteur_akteur_id", "Archive reference-originator ID", "Identifier cross-check, not substituted for the author model key", "Archive ID for the reference originator. Its 2453 distinct values map one-to-one to (text_id,akteur_id) model groups."),
        ("bezug_akteur_id", "Reference-object within-item actor ID", "Target metadata, not the model's originator grouping", "String target-list ID, local to the item. Do not use as the model's originating actor ID."),
        ("respobj_akteur", "Archive reference-object identifier", "Target metadata, not a random-effect grouping", "String reference-object identifier with 2362 distinct values. Keep separate from the originator identifier."),
    ]:
        spec(var, concept, "Archive " + var, "news item" if var in {"text_idx", "text_id"} else "directed reference / within-item actor", "identifier", meaning,
             BOOK2 + " PDF pp.3-5, printed pp.1-3. " + BOOK8 + " sections 8.1 and 8.3. Author egen act_id and Analysis 4.", role)
    spec("valenz_akteur", "Evaluation of the reference object", "ACTREF_VALENCE_ACTOR", "directed actor reference", "nominal",
         "Archive observed codes -99,0,1,2 with no embedded value labels. The codebook list is -99 unclear, 1 no evaluation, 2 positive, 3 negative, whereas its examples use 0 none and 2 negative. Archive 0 none/1 positive/2 negative is a plausible interpretation, not a fully verified archive label map.",
         BOOK8 + " PDF pp.6-7, printed pp.4-5, section 8.5.", "R2 reliability context only, not M1/M2/M3 predictor",
         "Source numbering conflict. Cross-tabs support the likely meaning but contain exceptions and cannot prove the full mapping. Keep exact numeric categories for faithful reliability calculations.")
    spec("genuinekonstruierte_resp_akteur", "Genuine versus journalist-constructed responsiveness", "ACTREF_GENUINE_CONSTRUCTED_RESP_ACTOR", "directed actor reference", "nominal",
         "Archive observed -99,1,2 without value labels. Codebook list is 0 genuine, 1 constructed, -99 unclear, but its example calls 1 genuine. The exact archive 1/2 semantic map is not confirmed by inspected sources.",
         BOOK8 + " PDF pp.5-6, printed pp.3-4, section 8.4.", "R2 reliability context only, not M1/M2/M3 predictor",
         "Documented source-numbering conflict. Do not silently impose the PDF list or infer code meanings from number order. Category equality is sufficient for identity-weighted agreement.")
    rolemap = "1 political, 2 military/police, 3 legal, 4 other national representatives, 5 business, 6 civil society, 7 journalists, 8 bloggers, 9 scientists/intellectuals/arts, 10 popular culture, 13 sports, 14 religious communities, 15 religious associations, 16 ordinary citizens, 17 organized protest, 18 violent-crime actors, 19 other, -99 not specified."
    actor_specs = [
        ("rolle_allgemein", "General actor role", "ACT_ROLE_GENERAL", "5.1", "PDF pp.3-5, printed pp.1-3", rolemap),
        ("rolle_pol_land", "Domestic or foreign actor status", "ACT_ROLE_POL_COUNTRY", "5.2", "PDF pp.5-6, printed pp.3-4", "11=domestic/national actor, 12=foreign actor, -99=not specified."),
        ("rolle_pol_level", "Political institutional level", "ACT_ROLE_POL_LEVEL", "5.3", "PDF p.6, printed p.4", "1=national, 2=subnational/supranational, -99=not specified. Applies to political actors."),
        ("rolle_pol_inland_national", "Domestic national political role", "ACT_ROLE_POL_DOMESTIC_NATIONAL", "5.4", "PDF pp.6-10, printed pp.4-8", "11110=executive as a whole, 11111=head of government, 11112=head of state, 11113=other executive, 11120=legislature as a whole, 11121=governing party, 11122=opposition, 11123=other legislature, -99=not specified."),
        ("rolle_pol_ausland_national", "Foreign national political role", "ACT_ROLE_POL_FOREIGN_NATIONAL", "5.5", "PDF p.10, printed p.8", "1211=foreign executive, 1212=foreign legislature, -99=not specified."),
        ("parteizugehoerigkeit", "Actor party affiliation", "ACT_PARTY_AFFILIATION", "5.6", "PDF pp.10-12, printed pp.8-10", "Country-specific party codes 1-7 Germany, 8-19 Switzerland, 20-22 USA, 23-27 Australia, 28-39 Lebanon, 40-44 Turkey, 45=no party affiliation, -99=not specified. Exact party-by-code list is in section 5.6 of the linked codebook."),
        ("parteizugehoerigkeit_other", "Other party affiliation text", "ACT_PARTY_AFFILIATION_OPEN", "5.7", "PDF p.12, printed p.10", "Open text for a country-specific other-party code. Empty text is not a party category."),
        ("herkunft", "Actor operational country of origin", "ACT_ORIGIN", "5.8", "PDF pp.12-13, printed pp.10-11", "Country-code string for current residence/work context, not ethnicity. Codebook's list of country codes is referenced but not contained in this step PDF. No numeric coercion of string codes."),
        ("herkunft_sonstige", "Other actor origin text", "ACT_ORIGIN_OPEN", "5.9", "PDF p.13, printed p.11", "Open text used when the origin category is Other."),
        ("geschlecht", "Historically coded actor gender", "ACT_GENDER", "5.10", "PDF pp.13-14, printed pp.11-12", "1=female, 2=male, 3=other, -99=not specified. These are the original study categories."),
        ("religionszugehoerigkeit", "Actor religious affiliation", "ACT_RELIGIOUS_AFFILIATION", "5.11", "PDF pp.14-15, printed pp.12-13", "1 Christian unspecified, 11 Roman Catholic, 12 Protestant, 121 Evangelical, 122 mainline Protestant, 123 other Protestant, 13 Maronite, 14 Orthodox, 15 Melkite Greek Catholic, 16 other Christian, 2 Islamic unspecified, 21 Sunni, 22 Shiite, 23 Alevi, 24 Alawite, 25 Druze, 26 Ismaili, 27 other Islamic, 3 Jewish, 4 Buddhist, 5 Hindu, 6 other, 7 no explicit affiliation, -99 not specified."),
        ("religion_offen", "Other religious affiliation text", "ACT_RELIGION_OPEN", "5.12", "PDF p.15, printed p.13", "Open text used for an Other religious affiliation category."),
    ]
    for var, concept, source, section, pages, meaning in actor_specs:
        spec(var, concept, source, "originating actor/statement, repeated across its references", "open text" if var.endswith(("_other", "_sonstige", "_offen")) else "nominal", meaning,
             f"{BOOK5}, {pages}, section {section}.", note="Auxiliary actor characteristics are not original model controls. Missing values may reflect conditional routing or absent coding, and are not automatically a substantive category.")
    for var, concept, source, kind, meaning, locator in [
        ("date_published", "Publication date", "DATE", "date stored as string", "Codebook requests YY-MM-DD. Archive stores publication-date strings. Timing is attached to the item, not a repeated-measures wave.", "PDF p.3, printed p.1, section 1.3"),
        ("mediaoutlet", "Author analytical outlet title", "MEDIA_OUTLET", "nominal string", "Outlet name in the author-prepared analytical archive. This is not identical by definition to numeric legacy medientitel.", "PDF p.3, printed p.1, section 1.4"),
        ("title", "Article title", "ARTICLE_TITLE", "open text", "Full article main title/subtitle text, not a modeled indicator.", "PDF p.4, printed p.2, section 1.5"),
        ("rubrik", "Article section/category", "SECTION", "nominal", "1 politics, 2 economy, 3 culture/society, 4 local/regional, 5 other, 6 no section/category.", "PDF p.4, printed p.2, section 1.6"),
        ("laenge", "Recorded article length", "LENGTH", "count concept, numeric archive", "Intended word count excluding titles, teasers, comments and subheadings. Archive contains at least one fractional positive value, so do not silently round or assume all stored values are valid integer word counts.", "PDF pp.4-5, printed pp.2-3, section 1.7"),
        ("darstellungsform", "Journalistic presentation genre", "FORM_OF_PRESENTATION", "nominal", "1 news report, 2 opinion/comment, 3 analysis, 4 report/reportage, 5 interview/discussion, 6 review, 7 reprint, 8 letter to editor, 9 other, -99 not specified.", "PDF pp.5-6, printed pp.3-4, section 1.8"),
        ("darstellungsform_other", "Other genre text", "FORM_OF_PRESENTATION_OPEN", "open text", "Other genre open field, applicable when genre is 9.", "PDF p.6, printed p.4, section 1.9"),
        ("anfangsseite", "Newspaper starting page", "STARTING_PAGE", "count-like page identifier", "Newspaper starting page only. Archive also contains zero and -99. Do not treat non-newspaper blanks or unclear codes as observed page counts.", "PDF p.6, printed p.4, section 1.10"),
    ]:
        spec(var, concept, source, "news item, repeated on reference rows where attached", kind, meaning, f"{BOOK1}, {locator}.")
    spec("land", "Legacy coded publication country", "COUNTRY / LAND", "news item", "nominal",
         "Observed mapping against analytical country is 1 Australia, 2 Switzerland, 3 Germany, 4 Lebanon, 5 Turkey, 6 USA. This differs from the analytical country numbering.",
         BOOK1 + " section 1.1 and aggregate cross-tab in semantic_checks.json.", note="Do not use land and country numeric codes interchangeably.")
    spec("medientyp", "Legacy coded media type", "MEDIATYPE / MEDIENTYP", "news item", "nominal",
         "Legacy expected coding is 1 newspaper, 2 website, 3 blog. This is not the author model variable mediatype.",
         BOOK1 + " section 1.2 and aggregate cross-tab in semantic_checks.json.",
         note="52/1700 items disagree with the analytical mediatype field under the expected translation. The original analysis explicitly selects mediatype, which is preserved.")
    for var, label, meaning in [
        ("techcon", "Technological media context", "Archive labels 1 new, 2 traditional."),
        ("profor", "Production-format grouping", "Archive labels 1 News, 2 Opinion. This is the source classification, not the nine-category journalistic genre."),
    ]:
        spec(var, label, "Author-derived " + var, "news item", "binary nominal", meaning,
             "Archive embedded value labels. Author Analysis 4 keep list, but not either melogit RHS.", note="Retained in author data but not an additional covariate in the original main models.")
    for var, label in [("anerkennung_text", "Recognition coding text"), ("hetze_text", "Outrage coding text"), ("resp_akteur_text", "Reference passage text"), ("resp_akteur_name", "Reference-object description"), ("resp_akteur_akteur", "Reference-originator description"), ("akteursname", "Originating actor name/description")]:
        spec(var, label, "Archive " + var, "directed reference / associated actor", "open text", "Stored descriptive text. Blank strings are retained separately from numeric missing. Not a binary event indicator.",
             BOOK8 + " sections 8.1-8.3, 8.7 and 8.9. " + BOOK2 + " actor-list creation.")


def main():
    build_specs()
    dictionary = []
    for dataset in META:
        for f in dataset["fields"]:
            name = f["variable"]
            default_unit = "news item" if dataset["dataset"] == "item" else "archive reference row or attached metadata, not an independent person"
            definition = SPECS.get(name, dict(concept="Archive technical or auxiliary field " + name,
                source_variable=f["label"] or name, unit=default_unit,
                measurement_type="string metadata" if f["storage"] == "string" else "numeric auxiliary field, no interval-scale inference",
                values_meaning="Retained archive field. Exact stored labels/domain and missing counts are documented. Its detailed upstream derivation is not specified in the inspected original model script, and it is not used in M1/M2/M3.",
                source_locator=f"{dataset['path']}, field {name}, label {f['label']}. outputs/diagnostics/measurement/dataset_metadata.json.",
                model_use="Not used in M1/M2/M3", source_conflict_or_limit="Upstream technical derivation not independently reconstructed. This does not affect the original main-model specification.", transformation="Preserve unchanged, do not add as a control"))
            counts = f.get("observed_numeric_counts", {})
            domain = "Numeric observed codes " + ",".join(counts) if counts else (
                f"Numeric nonmissing range {f.get('min')} to {f.get('max')}" if f["storage"] != "string" else
                f"String field, {f['unique_nonmissing_n']} distinct nonmissing values. Subject-level strings not exported in this dictionary.")
            missing = (f"System missing={f['system_missing_n']}, blank strings={f['blank_string_n']}, dataset rows={dataset['rows']}. "
                       f"Numeric -99 count={counts.get('-99', counts.get('-99.0', 'not present in enumerated domain'))}. "
                       "Preserve numeric sentinel codes and system missing separately. No auxiliary field is imputed or used to exclude main-model rows.")
            if name in {"tone", "polsys", "socdiv", "mediatype", "country", "actrefoutbin", "actrefrecbin", "text_id", "text_idx", "akteur_id", "actref_idx"}:
                missing += " Required original analysis fields have no missing values. Invalid model category or grouping key stops preparation."
            row = dict(row_id=f"{dataset['dataset'].upper()}_{name}", dataset=dataset["dataset"],
                       dataset_path=dataset["path"], dataset_sha256=dataset["sha256"],
                       **definition, actual_data_variable=name, raw_values_meaning=domain,
                       archive_value_labels=json.dumps(f["value_labels"], ensure_ascii=True, sort_keys=True),
                       reference_category="Consensus, stable secularism or blog as appropriate" if name in {"polsys", "socdiv", "mediatype"} else "0 absence" if name in {"actrefoutbin", "actrefrecbin"} else "Not applicable, identifier/ordinal thresholds/unused metadata",
                       missing_rule=missing, verification_status="Archive field/domain/missingness inspected. " + ("Source-linked semantic definition recorded." if name in SPECS else "Technical metadata only, no invented substantive meaning."),
                       observed_numeric_counts=json.dumps(counts, sort_keys=True),
                       source_storage_type=f["storage"], specification_version=SPEC,
                       measurement_evidence_path="outputs/diagnostics/measurement/dataset_metadata.json | outputs/diagnostics/measurement/semantic_checks.json")
            dictionary.append(row)
    for name, meaning, role in [
        ("act_id", "text_id + '_' + akteur_id, 2453 composite originating actor/statement groups in 1183 items", "M2/M3 nested actor grouping"),
        ("mixed_vs_consensus", "I(polsys_analysis=2)", "M1/M2/M3 fixed slope, additional comparison"),
        ("majoritarian_vs_consensus", "I(polsys_analysis=3)", "M1/M2/M3 fixed slope, H1a/H1b"),
        ("contested_vs_stable", "I(socdiv_analysis=2)", "M1/M2/M3 fixed slope, H2a/H2b"),
        ("website_vs_blog", "I(mediatype_analysis=2)", "M1/M2/M3 fixed slope, H3a/H3b"),
        ("newspaper_vs_blog", "I(mediatype_analysis=3)", "M1/M2/M3 fixed slope, H3a/H3b"),
    ]:
        r = {k: "Not applicable to a derived term" for k in dictionary[0]}
        r.update(row_id="DERIVED_" + name, dataset="derived", dataset_path="Derived in memory from item/reference inputs",
                 dataset_sha256="Parent input hashes recorded above", concept="Computational grouping or fixed-effect term",
                 source_variable="Derived from author-recoded source fields", unit="within-item actor/statement" if name == "act_id" else "item context",
                 measurement_type="identifier" if name == "act_id" else "binary indicator", values_meaning=meaning,
                 source_locator="analysis/prepare_replication.py, recode(), design() and load_data(). Author Analysis 4 egen act_id.",
                 model_use=role, source_conflict_or_limit="None identified, model terms are not additional measured constructs",
                 transformation=meaning, actual_data_variable=name, raw_values_meaning="See parent source fields",
                 reference_category="No global-person interpretation" if name == "act_id" else "0=reference or another nonfocal category, 1=focal category",
                 missing_rule="Fail on absent required parent values. No imputation or centering.",
                 verification_status="Verified against actual executing design/recode functions and source metadata.",
                 specification_version=SPEC, measurement_evidence_path="outputs/diagnostics/data_audit.json")
        dictionary.append(r)
    fields = list(dictionary[0])
    with (OUT / "variable_dictionary.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        w = csv.DictWriter(stream, fieldnames=fields)
        w.writeheader()
        w.writerows(dictionary)
    write_guide(dictionary)
    print(json.dumps({"observed_dataset_field_rows": sum(len(d["fields"]) for d in META), "derived_terms": 6, "total_dictionary_rows": len(dictionary)}))


def write_guide(dictionary):
    text = """# Variable dictionary reader guide

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
"""
    (OUT / "variable_dictionary.md").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
