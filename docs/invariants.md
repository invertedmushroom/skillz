# Repository Invariant & Load-Bearing Rationale Index
*Note for Review Agent: Match changed files against Scope globs. Verify relevant entries against current code before citing them as VERIFIED.*

Define cross-cutting constraints here when no contract owns them. For guarantees owned elsewhere, index their scope and enforcement with a link to the owning section. See [fact ownership](README.md#fact-ownership).

## System Invariants

- **Scope (`@MODULE`):** `.agents/skills/*/SKILL.md`, `.agents/skills/*/agents/*.yaml`, `scripts/validate_skills.py`
  - **Invariant (`!INVARIANT`):** [Skill static validity](contracts/agent-skills.md#static-validation).
  - **Enforcement Location:** `scripts/validate_skills.py::validate()`, `check_openai()`, `self_test()`
  - **Canonical Source:** [Agent skill contract](contracts/agent-skills.md).
- **Scope (`@MODULE`):** `.agents/skills/*/evals/**`
  - **Invariant (`!INVARIANT`):** [Behavioral Skill Evaluation & Iterative Optimization Invariant](contracts/agent-skills.md#behavioral-skill-evaluation--iterative-optimization-invariant).
  - **Enforcement Location:** Locked evaluator surface of each `.agents/skills/<name>/evals/` (`cases.json`, `checks/`, `fixtures/`, `run.py`); procedural review gate during `SKILL.md` optimization runs.
  - **Canonical Source:** [Agent skill contract](contracts/agent-skills.md).

<!--
Template entry (see .agents/skills/decision-pr-review/references/invariant-index-template.md):

- **Scope (`@MODULE`):** [Subsystem / Exact Path Glob, e.g., `src/domain/*`]
  - **Invariant (`!INVARIANT`):** [Constraint defined here, or a label linked to its owning contract section]
  - **Enforcement Location:** [`path/to/file.ext::symbolName()`]
  - **Causal Flow (`@FLOW`, Optional):** [`Trigger -> Guard -> StateMutation -> SideEffect`]
  - **Canonical Source:** [Owning contract section, or this entry when the constraint is defined here]
  - **Rationale / Evidence (Optional):** [ADR, PR, or regression test]
-->

## Load-Bearing Rationale (Rejected Simplifications)

<!--
Record non-obvious "scar tissue" here so future sessions or refactors do not re-introduce a broken simplification:

- **Condition:** [Operational/domain condition where code looks deceptively complex]
  - **Forbidden Change:** [Do not replace exact symbol X with simpler Y]
  - **Failure Consequence:** [Causal mechanism of why Y fails in practice and what breaks]
  - **Source:** [ADR, contract, PR, or regression test `tests/path/test_file.ext:line`]
-->

## Operational Symptom-Cause-Fix Matrix

<!--
Record non-obvious runtime, build, or integration traps discovered during `diagnosing-bugs` so future sessions resolve them in one lookup:

| Scope / Subsystem | Observable Symptom / Error | Root Cause | Mandatory Fix / Verification Command |
| :--- | :--- | :--- | :--- |
| *(e.g., `src/worker/*`)* | *(e.g., Deadlock on shutdown)* | *(e.g., Bounded channel `send` inside SDK callback)* | *(Use `try_send` + drain budget; run `rtk cargo test -p worker`)* |
-->