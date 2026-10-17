# Data access, separation, and sharing

Official data documentation: https://medcon-doc.github.io/documentation/content-analysis/data-sets/

1. Substantive-analysis package: https://medcon-doc.github.io/documentation/files/Appendix%20-%20Content%20Analysis%20Repro%20Materials%20-%20STATA.zip
2. Original independent ratings and reliability materials: https://medcon-doc.github.io/documentation/content-analysis/reliabilities/

Save unchanged extracted data in original/ and original author scripts in sources/author_code/. Save programmatically derived analytical data in prepared/. Keep original independent ratings separate from adjudicated or consensus codes.

Redistribution rights have not been established for every input, so .gitignore excludes actual data by default. Verify terms and record permissions before deciding which inputs can be tracked. Readers should obtain excluded files lawfully through the documented sources. Record versions and SHA-256 checksums rather than identifying versions by filenames alone.

The availability of coded data does not establish access to the underlying news corpus. Computational reproduction can use the coded inputs, but it must not be described as independently recoding the original texts. AI recoding would be a separate, explicitly labelled optional extension.
