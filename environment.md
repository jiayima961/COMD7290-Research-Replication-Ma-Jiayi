# Software and execution environment

## Initialization environment

- Operating system: Windows. Text files use UTF-8; CSV files use UTF-8 with a BOM for spreadsheet compatibility.
- Initialization checks: Python 3.12.14, standard library only. Git manages versions.
- `tools/check_repository.py` neither installs dependencies nor accesses the network or fits models.

## Statistical environment: verification pending

The inspected author script `MedCon_Civility_an.do`, dated 2021-04-24, specifies `version 16` and lists four Stata extensions: blindschemes, gologit2, omodel, and grc1leg2. Its multilevel models use `intpoints(7)`. The package readme is dated 2021-04-20. These are source-code requirements, not evidence that Stata or these extensions are installed or that integration and prediction settings have been verified locally.

The original reliability script, dated 2020-11-01, also specifies Stata 16 and requires `kappaetc`. Its imported filenames differ from the website download names. Preserve the originals and document path mappings in a project execution copy. No statistical extensions have been installed and neither author script has been run.

Before fitting, record engine and package versions, installation sources, commands, input and specification versions, estimator and integration settings, convergence criteria, interval type and level, runtime, seeds where applicable, and log locations. State how predictions handle random effects. Any alternative engine requires documented statistical equivalence and the student's review of the specification.

## Currently available check

```text
python tools/check_repository.py
```

This checks repository materials only. The complete statistical entry point and clean-rerun demonstration have not been implemented.
