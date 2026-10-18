# Use the two tested project skills

Open the **whole repository root** as your agent's working folder. Copying only a SKILL.md is insufficient: these are project skills that use the repository's documents, code, tests and inputs. No global skill installation or account credentials are required. The canonical packages are under `.agents/skills/`, as required by the assignment.

| Skill | Complete package and supporting project files | Evidence of actual use |
| --- | --- | --- |
| 1. Theory, variables and models (`specify-empirical-study`, 1.0.1) | [SKILL.md](../../.agents/skills/specify-empirical-study/SKILL.md), [output contract](../../.agents/skills/specify-empirical-study/references/output_contract.md), [validator](../../.agents/skills/specify-empirical-study/scripts/validate_specification.py), [test-input helper](../../tools/prepare_specification_test.py), [12 regression cases](../../tests/skill1_specification/test_validator_cases.py); canonical documents are indexed in [docs](../README.md) | [Forward-test report](../../records/skill_tests/specify-empirical-study/TEST_REPORT.md), [first real theory review](../../records/skill_invocations/2026-10-18_specify-empirical-study_theory-review/), [second real theory review](../../records/skill_invocations/2026-10-18_specify-empirical-study_theory-review_v2/) |
| 2. Data checks, reproduction and diagnosis (`reproduce-and-diagnose`, 1.1.0) | [SKILL.md](../../.agents/skills/reproduce-and-diagnose/SKILL.md), [execution contract](../../.agents/skills/reproduce-and-diagnose/references/execution_contract.md), [analysis modules](../../analysis/README.md), [numerical tests](../../tests/README.md), [execution specification](../execution_specification.md), [input instructions](../../sources/README.md) | [Execution/test report](../../records/skill_tests/reproduce-and-diagnose/TEST_REPORT.md), [native discovery](../../records/skill_tests/reproduce-and-diagnose/discovery.json), [real invocation and receipt](../../records/skill_invocations/2026-10-18_reproduce-and-diagnose/), [run logs](../../records/run_logs/skill2/) |

For Codex, explicitly select the skill or send one of these prompts from the repository root:

```text
Use $specify-empirical-study from .agents/skills/specify-empirical-study.
Review the supplied theory explanation against the registered sources.
Preserve the student input, save new feedback as a new version, and record the invocation.
Do not invent student approvals or completed readings.
```

```text
Use $reproduce-and-diagnose from .agents/skills/reproduce-and-diagnose.
Read docs/execution_specification.md, check the registered input hashes, and
reproduce the original Python analyses. Preserve the existing evidence in a copy
before a new run, save all results and diagnostics, and disclose unresolved
historical-software settings. Use analysis/run_replication.py as the entry point.
```

If another agent framework does not discover `.agents/skills`, explicitly ask it to read the appropriate SKILL.md and its linked contract, then follow those instructions in this repository. That is manual loading, not evidence of native discovery. The skill-1 validator example uses `rtk proxy`; an agent without RTK can run the identical validator with `python <skill-path>/scripts/validate_specification.py ...`.

Restore source inputs and set up Python using the [teacher quickstart](../guides/teacher_quickstart.md) before requesting a full reproduction. Each skill states its inputs, procedure, outputs, validation and stopping rules. Reading the package or passing static validation alone does not prove successful scientific use.

[Skill 3](../../.agents/skills/verify-and-package/SKILL.md) remains a scaffold for later verification and final packaging. It must not be presented as a third completed/tested skill. This folder is a reader guide; `.agents/skills/` is the only canonical skill installation in the repository.
