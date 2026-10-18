# Project utilities

| Utility | Purpose |
| --- | --- |
| restore_inputs.py | Offline hash check; optional verified download/extraction without overwriting existing files |
| check_repository.py | Material structure, CSV schemas and registered source hashes; no fitting |
| run_logged.py | Real command/stdout/stderr/runtime capture; RTK optional |
| prepare_specification_test.py | Restore ignored source copies for the archived skill-1 forward case |
| probe_skill_discovery.py | Read-only local Codex app-server discovery probe; requires an installed Codex runtime |
| check_python_environment.py | Synthetic environment checks |
| fetch_sources.py | Original acquisition helper retained for historical reproducibility; prefer restore_inputs.py for another computer because it does not revise the historical manifest |
| reorganize_project.py | One-time 2026-10-19 non-destructive migration; refuses a repeat |
| maintenance/ | Historical document/checkpoint writers and notebook builder |

Run current analysis through [analysis/run_replication.py](../analysis/run_replication.py). The maintenance writers contain historical content and can overwrite current narrative files; inspect them before explicitly using one. They are retained because the user requested no file deletion. Their project-root calculation was updated after relocation.
