# Agent Skill Contract

- **Status:** Implemented
- **Owning Modules:** `.agents/skills/`, `scripts/validate_skills.py`

## Skill Authority

Each `.agents/skills/<name>/SKILL.md` is the shared entrypoint for the skill's name, trigger description, workflow, and supporting instructions. Supporting files own the instructions delegated to them. Resolve relative Markdown links from the containing file. When a native skill loader is unavailable, a composing skill reads the linked instructions directly. When a workflow requires an unavailable execution capability, report that limitation.

`agents/openai.yaml` owns host-specific UI metadata and invocation policy. Shared workflow and trigger descriptions remain in the skill entrypoint. Preserve existing invocation policies. When frontmatter explicitly sets `disable-model-invocation`, the OpenAI invocation policy must agree. When that flag is omitted, an existing host-specific policy can remain.

## Static Validation

[`scripts/validate_skills.py`](../../scripts/validate_skills.py) enforces these guarantees:

- Every direct skill directory has a `SKILL.md`. Empty skill discovery fails.
- Skill frontmatter and adapter YAML parse without duplicate keys. Skill names match their directories. Names and descriptions satisfy the validator's format and length checks.
- Inline relative Markdown file links resolve from the containing Markdown file throughout each skill directory. Links inside fenced code blocks are excluded.
- An explicit shared invocation flag agrees with the OpenAI invocation policy.
- OpenAI adapter checks cover supported top-level sections, string UI values, 25–64-character short descriptions, skill mentions in optional default prompts, and boolean invocation policy. Other adapters receive YAML checks only.

The validator resolves the repository from its own location unless `--root` selects an explicit root. Ordinary validation reads files without rewriting them. `--self-test` uses temporary fixtures outside the checkout.

## Verification Limits

These checks establish the template's local static validity. They do not establish full vendor-schema compatibility, live skill discovery, workflow execution, or model behavior.

The byte inventory separates root instructions, name/description metadata, and complete skill entrypoints. Inventory bytes do not establish which skills a host loaded or how many session tokens the host consumed.

## Verification Surface

`validate()` and `check_openai()` enforce static validity. `self_test()` checks a valid read-only fixture and rejected fixtures for invalid YAML, missing links, mismatched names, duplicate keys, policy conflicts, obsolete adapter fields, invalid policy types, empty discovery, and missing entrypoints.

```powershell
rtk proxy uv run --script scripts/validate_skills.py --self-test
```

Use the [adoption checklist](../README.md#adoption-checklist) for live harness verification. The [TypeScript browser evaluations](../../.agents/skills/typescript-browser-apps/evals/EVALUATION.md) own their procedure, results, and behavioral coverage limits.

## Behavioral Skill Evaluation & Iterative Optimization Invariant

When a skill directory includes a behavioral evaluation suite (`evals/EVALUATION.md`, `evals/cases.json`, `evals/checks/`, `evals/fixtures/`, `evals/run.py`), enforce strict separation between the evaluator and the mutable skill:
1. **Locked Evaluator Surface:** `evals/cases.json`, `evals/checks/`, `evals/fixtures/`, and `evals/run.py` are **read-only** during skill prompt optimization runs. An agent optimizing `SKILL.md` or `references/*.md` must never weaken or edit evaluation checks to make a failing case pass.
2. **Pareto Non-Regression:** A proposed edit to `SKILL.md` is accepted only if it improves target failure cases without regressing previously passing cases in `evals/cases.json`.
