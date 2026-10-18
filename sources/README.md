# Source materials and access instructions

## Materials already available locally

- Assignment: user-supplied `sources/local/COMD7290_assignment.pdf`.
- Selected article: user-supplied `sources/local/Lob_et_al_2024.pdf`; https://doi.org/10.1177/19401612221084206
- Online publication in 2022 and the 2024 journal volume refer to the same article.

Redistribution rights for PDFs and author materials remain under review. Git currently contains provenance and access instructions; original files under local/ are excluded. No project licence has been applied to third-party materials.

## Official author materials

- Codebooks: https://medcon-doc.github.io/documentation/content-analysis/codebook/
- Coded datasets: https://medcon-doc.github.io/documentation/content-analysis/data-sets/
- Independent ratings and reliability: https://medcon-doc.github.io/documentation/content-analysis/reliabilities/
- File index: https://medcon-doc.github.io/documentation/files/
- Substantive reproduction package: https://medcon-doc.github.io/documentation/files/Appendix%20-%20Content%20Analysis%20Repro%20Materials%20-%20STATA.zip

The downloaded package was checked for MedCon_Civility_item.dta, MedCon_Civility_actref.dta, MedCon_Civility_an.do, and readme.rtf. The Tone and Actor-reference independent-rating workbooks, their reliability script, and four relevant codebooks were also downloaded. Originals remain local and excluded by .gitignore; their URLs and checksums are registered. Author statistical programs have not been executed. Full supplementary coverage and permissions still require review.

The article uses coding steps 1, 2, 5, and 8 from the broader project. Other recorded project variables must not automatically be treated as controls in this article's models.

See ../records/source_manifest.csv for exact URLs, versions, retrieval dates, checksums, and current status.

## Restore exact-version inputs on another computer

[input_restore_manifest.json](input_restore_manifest.json) lists the required
original datasets, ZIP members, rating workbooks, codebooks, PDFs and archived
external method sources with SHA-256 values. Run `python tools/restore_inputs.py`
from the repository root for offline checking, or add `--download` to retrieve
registered direct sources. The tool never overwrites an existing file and never
changes the historical source manifest. Assignment/article copies need lawful
manual access; changed upstream versions are reported rather than accepted.
See [the teacher quickstart](../docs/guides/teacher_quickstart.md).

Original inputs and external method source files remain excluded from Git.
Subject-level prepared rating matrices, matching-row audits and conditional
influence arrays also remain local; rerun the reliability stage to recreate
them. Aggregate coefficient/benchmark tables, code, test summaries and provenance
are shared. Some historical GLMM documentation paths are under tmp; the
[method source manifest](../outputs/diagnostics/glmm/method_source_manifest.json)
records primary URLs/hashes. These PDFs are provenance, not runtime dependencies
of the saved Python likelihood engine.
