# Non-destructive reorganization — 2026-10-19

The user requested two reusable/tested skills, a clearer project layout with no deleted files, and synchronization to the private GitHub repository after local checks.

The assignment's `docs / data / analysis / tests / outputs / records` structure and `.agents/skills` discovery paths are retained. Auxiliary guides moved to docs/guides; one-time writers moved to tools/maintenance. Stable scientific document, code, numerical-result, student-input and historical-receipt paths were preserved. Canonical statistical formulas and existing numerical results were not altered. Logging/notebook/launcher transport now supports ordinary Python when RTK is absent.

- [moves.json](moves.json): every old/new path and excluded untouched runtime directories.
- [before_sha256.json](before_sha256.json): pre-change file fingerprints.
- [previous_versions](previous_versions/): originals of replaced navigation/wrappers and moved helpers. These are historical copies, not current instructions.
- verification.json and validation logs (created after edits): preservation, references, package completeness and portable execution checks.

No original file was deleted. Where an authored file was revised, its prior bytes remain in previous_versions; moves retain the file under its new path. Original data/PDF/method inputs and subject-level derived arrays remain local under existing access restrictions; the GitHub payload supplies access and exact-version restoration instructions. Runtime directories were left in place and were not repackaged.

The existing completed skill invocations and saved model results remain the evidence of research execution. The cleanup checks only establish that layout and transport changes preserve use; they do not constitute a new full independent refit or final course completion. Remote synchronization evidence is recorded separately after the upload.
