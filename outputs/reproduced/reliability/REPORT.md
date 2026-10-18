# Independent reliability forward test

Computed from original independent-rating workbooks and the original author script. All computations ran in Python; no Stata executable or new installation was used.

```text
coefficient                               brennan_prediger  cohen_conger_kappa  gwet_ac1  krippendorff_alpha  percent_agreement  scott_fleiss
outcome        selection                                                                                                                     
outrage        all_author_selected_slots          0.948599            0.714812  0.971701            0.751409           0.974300      0.720118
               two_slots                          0.950946            0.765871  0.972949            0.789259           0.975473      0.737110
recognition    all_author_selected_slots          0.944211            0.307723  0.969447            0.714855           0.972106      0.679463
               two_slots                          0.939734            0.691611  0.966988            0.713705           0.969867      0.654455
responsiveness all_author_selected_slots          0.922708            0.414202  0.943470            0.627300           0.948472      0.708841
               two_slots                          0.923373            0.679354  0.943945            0.636621           0.948915      0.711936
tone           all_author_selected_slots          0.924220            0.900801  0.935617            0.741737           0.939376      0.740396
               two_slots                          0.924220            0.741628  0.935617            0.740608           0.939376      0.740396
valence        all_author_selected_slots          0.785163            0.681458  0.795473            0.731581           0.838872      0.746882
               two_slots                          0.782294            0.744236  0.792709            0.745016           0.836720      0.743653
```

## Interpretation and limits

The original installed kappaetc build was not pinned. Basic methods follow recovered 2.1.0 source; its changelog identifies only benchmarking as the change from 2.0.0.

The script predates the 2022 truncated benchmark change. Both source-version benchmark methods are retained; exact historical installed build remains unknown.

Rater variables are positional slots containing different humans across subjects. Some actor rows repeat one human in multiple slots. The arithmetic faithfully reruns the supplied author matrix; independence and the original matching algorithm are not established by this rerun.

Numeric -99 is treated as a category because the original reliability script never declares it missing; interpreting -99 as missing would change the source specification.

Responsiveness uses only first five original long-header fields, independently resolved against Excel letters Q/AG/AW/BM/CC and the author comments; other actor outcomes use all 14 fields.

Conditional SEs follow the recovered source exactly. With singleton rows, its influence expression anchors the observed fraction with at least two ratings; it differs from differentiating an ordinary weighted point estimator that lets that fraction change. The numerical derivative check explicitly uses the source's anchored functional. Alpha SE uses the source's uncorrected-alpha influence, while its point coefficient includes epsilon correction.

No published target CSV or previous AI reliability conclusion was used for implementation or fitting. No exact cross-software equivalence claim is made.

## Outputs

- reliability_coefficients.csv: all six measures, conditional SEs, t tests, clipped and unclipped 95% intervals, expected/observed agreement, actual samples and source versions.
- probabilistic_benchmarks.csv: all Landis-Koch interval probabilities and selected categories for separately identified pre-2022 and current methods.
- sample_audit.json, column_audit.csv, matching_audit.json, matching_row_audit.csv and responsiveness_mapping.json: selection, missingness, numeric -99, exact headers, keys and named-coder audit.
- checks.json and independent_study_checks.json: closed-form known answers, independent installed implementations, numerical influence checks and harmless synthetic negative test/recovery.
- input_manifest.json, method_provenance.json, invocation_receipt.json, versions.json and stdout.log: exact input hashes, settings, source/code evidence and actual execution.
- Rating matrices and conditional influence NPY files retain the calculation inputs and subject-level variance contributions.

Run from the project root with `rtk proxy .venv/Scripts/python.exe -X utf8 analysis/reliability_reproduction.py --project-root .`. This reruns the statistical calculations and post-fit comparison offline from the archived primary page.


Artifact locations: results `E:\Statistics with AI\COMD7290-Research Replication-Ma Jiayi\outputs\reproduced\reliability`; diagnostics `E:\Statistics with AI\COMD7290-Research Replication-Ma Jiayi\outputs\diagnostics\reliability`; run logs `E:\Statistics with AI\COMD7290-Research Replication-Ma Jiayi\records\run_logs\skill2\reliability`; prepared rating matrices `E:\Statistics with AI\COMD7290-Research Replication-Ma Jiayi\data\prepared\reliability`; primary method evidence `E:\Statistics with AI\COMD7290-Research Replication-Ma Jiayi\sources\local\skill2_methods\reliability`.

All 30 first/second-slot coefficients and all five sample counts match the archived primary website at displayed precision. Primary targets are saved separately from computed estimates. The website does not supply SE/interval or all-slot targets.
