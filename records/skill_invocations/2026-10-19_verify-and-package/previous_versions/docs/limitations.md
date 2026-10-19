# Limitations and unresolved issues

## Observed source inconsistencies

| Issue | Evidence | Current handling | Possible impact |
|---|---|---|---|
| Inconsistent numeric coding examples | Codebook step 8 recognition/outrage lists versus examples | Verify data labels and author syntax; do not guess binary mappings | Incorrect coding could alter estimates |
| Anomalous published percentages | Table 2 Australia/news-website row prints 97, 2, 11, 0, 0, with total 100 | Preserve the discrepancy; do not silently replace 11 with 1 | Requires data checking; at least a reporting issue |
| Inconsistent pseudo-R-squared label | Results text names Nagelkerke; Table 3 names McFadden | Check code; do not interpret as 9% of ordinary variance explained | Reporting and fit-measure comparison |
| Different reliability and model counts | Official reference-rating reliability N = 3,863; Table 4 N = 3,770 | Trace matching and exclusions without inventing an explanation | Potential sample-construction issue |

## Interpretation boundaries of the original design

The six-country design has one country per comparison cell. Unobserved national differences may account for associations. The topic, 2015–2016 period, and three media types limit generalization. The study observes associations rather than directly measuring audience emotion or establishing editorial norms as a causal mechanism. More recognition does not by itself establish reconciliation across opposing groups.

## Questions requiring actual reproduction

Missingness, undocumented cleaning, convergence, integration stability, prediction differences, and environment dependencies have not yet been empirically checked in this project. Record demonstrated findings separately from speculation, with evidence paths, numerical results, and whether each issue affects conclusions, estimates, or reporting transparency.
