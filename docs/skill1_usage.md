# Using the theory, measurement and model specification skill

The project skill is `.agents/skills/specify-empirical-study/SKILL.md`. It helps reconstruct and review the study's argument from primary evidence. Its preparation/test records are in `records/skill_tests/specify-empirical-study/`. Test examples are not the student's theory map or a final study specification.

Real-use update (2026-10-18): student written v1 has now been received and reviewed. See [the preserved input](../records/student_inputs/2026-10-18_initial_theory_explanation_v1.txt), [feedback](theory_feedback_v1.md), [student decision worksheet](student_review.md) and [invocation receipt](../records/skill_invocations/2026-10-18_specify-empirical-study_theory-review/README.md). The instructions below remain reusable; the current next step is the student's revision/reading notes, not another request for the same initial explanation.

Second-round update: the student's [v2](../records/student_inputs/2026-10-18_revised_theory_explanation_v2.txt) and [round-2 feedback](theory_feedback_v2.md) are now recorded. Use [START_HERE.md](../START_HERE.md) for the current version and complete chronological trail. The student has supplied a revision; reading notes, a separate diagram and complete-specification acceptance are still pending.

## Working directory and discovery

Actual runtime discovery passed when Codex was given the repository root, `E:/Statistics with AI/COMD7290-Research Replication-Ma Jiayi`. The current chat's outer workspace, `E:/Statistics with AI`, did not discover the nested repository skills. This was tested separately; see `discovery.json` and `discovery_parent_folder.json` in the skill-test records.

For normal automatic skill selection, open or launch Codex with the actual repository as its working root. In a conversation opened on the outer workspace, explicitly identify the full skill path below and have the agent load it. This explicit-path use is distinct from claiming that the outer workspace's automatic skill selector discovered it.

## What the student supplies next

Write a preliminary explanation in your own words and, where possible, an initial diagram: the phenomenon and gap, why each predictor might relate to outrage and recognition, the six predictions, what would be measured, the relevant observation units, and how a model would address each prediction. Mark uncertainty rather than guessing. List the foundational sources and sections actually read, with brief notes; at least two cited theoretical or methodological works are required by the assignment.

Prior AI exposure and timing should be disclosed. The current project already contains AI drafts and discussed published results, so a later student reconstruction must not be described as a pristine pre-AI or preregistered prediction. Preserve its actual date and provenance.

## Example real invocation after the preliminary explanation is supplied

```text
Use $specify-empirical-study at E:/Statistics with AI/COMD7290-Research Replication-Ma Jiayi/.agents/skills/specify-empirical-study/SKILL.md. Read my initial explanation and theory map from the supplied project files, preserve their original versions, check them against the selected article, codebooks, author syntax and cited foundational sources, and give source-linked criticism. Keep author claims, my reconstruction and methodological criticism separate. Update the theory, dictionary, hypothesis matrix, design/models and original diagram in the canonical docs/ locations, retain unresolved issues and a handoff, and leave my approval pending until I respond. Do not fit models or validate the Python three-level engine in this task.
```

The skill should return concrete suggestions and a traceable specification draft. The student decides whether to accept or revise the suggestions and supplies their own reading attestations. Source conflicts or missing settings stay visible. Completing the first skill does not complete statistical execution, independent verification or final submission.
