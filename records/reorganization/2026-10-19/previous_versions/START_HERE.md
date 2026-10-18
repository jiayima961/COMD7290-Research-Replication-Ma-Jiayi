# Start here: project documents and review history

Updated: 2026-10-18. Project: **COMD7290-Research Replication-Ma Jiayi**.

**Current work: skill-2 Python replication. Open the [results and evidence index](docs/replication_results.md) for calculated results, diagnostics and rerun instructions.** Latest student theory explanation: v2; latest AI feedback: round 2. Foundational reading notes and the student's theory diagram remain pending. The user explicitly authorized source-bound analysis execution; this is distinct from final scientific/submission approval.

## 1. Read the current theory work

| Read in order | Document | Purpose |
|---|---|---|
| 1 | [Student theory explanation v2](records/student_inputs/2026-10-18_revised_theory_explanation_v2.txt) | Latest version supplied by the student; wording preserved |
| 2 | [AI feedback on v2](docs/theory_feedback_v2.md) | Remaining refinements and exact source locators |
| 3 | [Student review and revision progress](docs/student_review.md) | Changes observed between v1/v2 and remaining student-owned entries |
| 4 | [Project status](STATUS.md) | Completed work and next tasks |

## 2. Follow the theory review in chronological order

All four steps occurred on 2026-10-18. The sequence below, not the shared date alone, identifies their order.

| Step | Document | Supporting record |
|---|---|---|
| 01. Student initial explanation | [v1](records/student_inputs/2026-10-18_initial_theory_explanation_v1.txt) | Included in round 1 below |
| 02. First AI critique | [Feedback round 1](docs/theory_feedback_v1.md) | [Round-1 request, sources, checks and handoff](records/skill_invocations/2026-10-18_specify-empirical-study_theory-review/README.md) |
| 03. Student revised explanation | [v2](records/student_inputs/2026-10-18_revised_theory_explanation_v2.txt) | Included in round 2 below |
| 04. Second AI critique | [Feedback round 2](docs/theory_feedback_v2.md) | [Round-2 request, sources, checks and handoff](records/skill_invocations/2026-10-18_specify-empirical-study_theory-review_v2/README.md) |

Student versions are stored in `records/student_inputs/`; AI feedback is stored in `docs/`; detailed invocation evidence is stored in `records/skill_invocations/`. Use this index to navigate. Each version has one preserved copy at its registered path.

## 3. Find the study specification and analysis evidence

| Question | Main document | Current status |
|---|---|---|
| What is the argument? | [Theory overview and current-version links](docs/theory.md) | Student v2 reviewed; source-bound execution specification recorded |
| How does each hypothesis connect to analysis? | [Hypothesis-to-evidence matrix](docs/hypothesis_matrix.csv) | 12 executed directional targets plus non-hypothesis analyses; linked outputs |
| What do the variables mean? | [Variable dictionary](docs/variable_dictionary.csv) | Focal variables verified against actual data/code; unused metadata remains labelled |
| What are the design and models? | [Design and models](docs/design_and_models.md), [diagram source](docs/model_diagram.mmd) | Executed model mapping; historical numerical limits documented |
| Which analyses must be covered? | [Analysis inventory](docs/analysis_inventory.csv) | Actual execution coverage and explicit unresolved items |
| Where are the source/access records? | [Source manifest](records/source_manifest.csv), [source access instructions](sources/README.md), [data instructions](data/README.md) | Original inputs held locally where redistribution is unresolved |
| Where will code and new results be? | [Analysis plan](analysis/README.md), [reproduced-results folder](outputs/reproduced/), [comparison table](outputs/comparison.csv) | Actual fits, coefficients, uncertainty, predictions and comparisons saved |
| Which values came from the publication? | [Published model targets](outputs/published/model_targets.csv) | Published comparison values, not locally reproduced findings |

H1a uses M1/M2; H1b uses M3; H2a uses M1/M2; H2b uses M3; H3a uses M1/M2 with separate website/newspaper comparisons; H3b uses M3 with those separate comparisons. The matrix is the route from these claims to executed scripts, outputs and conclusions. See analysis/run_replication.py and docs/replication_results.md for rerun commands.

## 4. Inspect workflow and technical records

| Material | Location |
|---|---|
| Actual theory-review records | Round-1 and round-2 links in section 2 |
| First skill instructions and use | [Skill](.agents/skills/specify-empirical-study/SKILL.md), [usage guide](docs/skill1_usage.md) |
| Earlier synthetic skill test | [Test report](records/skill_tests/specify-empirical-study/TEST_REPORT.md); synthetic examples are separate from student drafts |
| AI work, decisions and handoffs | [Agent record](records/agent_records.md), [decisions](records/decisions.md), [handoffs](records/handoffs.md) |
| Environment and software feasibility | [Environment](environment.md), [Python route assessment](docs/python_route_assessment.md), [setup record](records/run_logs/python_environment_setup.md) |
| Course requirements and checkpoints | [Assignment checklist](docs/assignment_checklist.md), [checkpoints](records/checkpoints.md) |
| Final report preparation | [Report guide](report/README.md), [submission checklist](report/submission_checklist.md) |
| Full folder/workflow explanation | [Repository workflow guide](docs/github_structure_and_workflow.txt) |

For a new student version, use the next version number and add the corresponding feedback/receipt to section 2. Keep existing student inputs, feedback and completed-run evidence unchanged; update this index and the current status. Working context records may evolve and should identify the current version. New local records are not automatically synchronized to GitHub.
