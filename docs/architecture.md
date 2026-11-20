# Architecture Reference

This document describes the technical architecture of the repository **as implemented today**. Keep proposals and unbuilt scope in [`docs/plan/`](plan/README.md) or [`docs/deferred.md`](deferred.md).

This map owns implemented structure and state ownership. Link to the owning contract or invariant for behavioral guarantees, following the [fact ownership rules](README.md#fact-ownership).

This file stays the map. When a subsystem section outgrows a screenful, move the detail to its owning contract or a subsystem page and keep a one-line pointer here. Code and configuration already declare schemas, tables, and endpoint lists; link to that source instead of restating it.

**Writing style.** Keep exact identifiers (paths, types, functions, tables, CLI flags, env vars) verbatim, and strip filler prose, transitions, and explanations of standard framework patterns.

## 1. System Overview & Data Flow

```text
[Caller / Client] ──▶ [Boundary / Seam] ──▶ [Deep Domain Module] ──▶ [Persistence / Output]
```

## 2. Execution Flows

Represent key behaviors as causal chains (`Trigger -> Guard -> StateMutation -> SideEffect`), not file lists. Keep each step short and use these operators:

- `->` synchronous call or step transition
- `=>` async emission, event, or return projection
- `::` state read/write or ownership binding
- `|` branch or fallback path
- `&` parallel execution

```text
@FLOW [SubmitOrder]: api::submit(req) -> validate(req) -> Orders.insert :: orders => Emit(OrderCreated) | Reject(reason)
```

List the flows an agent must not misread: state transitions crossing module seams, concurrency-sensitive orderings, and failure/fallback paths. Hard constraints on these flows live in [`docs/invariants.md`](invariants.md) (`@MODULE -> !INVARIANT`); link, don't restate.

## 3. Module & Seam Map

| Module / Path | Responsibility | Interface (External Seam) | Dependencies / Adapters |
| :--- | :--- | :--- | :--- |
| *(e.g. `crates/core` or `packages/core`)* | *(Core domain logic)* | *(Small public entry points)* | *(In-process / Port adapters)* |

## 4. Authority & State Boundaries

- **Single Writer / Ownership:** Document which module or transaction boundary owns mutations to each state store or table.
- **Trust & Validation Boundary:** Where untrusted inputs are parsed into typed domain values.

## 5. Verification Commands

```bash
# Fast checks (types, lint)
# Task checks (unit/integration tests)
# Full CI gates

# Template skill validation and deliberately invalid fixtures
rtk proxy uv run --script scripts/validate_skills.py --self-test

# Markdown link check (all tracked .md files)
node scripts/check-markdown-links.mjs
```

## 6. Agent Skill Infrastructure

| Path | Responsibility |
| :--- | :--- |
| `.agents/skills/<name>/SKILL.md` and supporting files | Shared skill entrypoint and workflow. |
| `.agents/skills/<name>/agents/openai.yaml` | Host-specific UI metadata and invocation policy. |
| [Concept article shell](../.agents/skills/concept-article/assets/article.html) | Offline-readable, naturally scrolling technical explanations with scientific figures, mathematics, and progressively enhanced interactions. |
| [`scripts/validate_skills.py`](../scripts/validate_skills.py) | Static validation, temporary self-test fixtures, and byte inventory. |
| [`scripts/check-markdown-links.mjs`](../scripts/check-markdown-links.mjs) | Repo-wide markdown link, path, and heading-anchor verification. |
| [TypeScript browser evaluation suite](../.agents/skills/typescript-browser-apps/evals/EVALUATION.md) | Behavioral fixtures, grading procedure, recorded results, and evaluation limits. |

The [agent skill contract](contracts/agent-skills.md) owns skill authority rules, validation guarantees, and verification limits. Use the [adoption checklist](README.md#adoption-checklist) for live harness checks.
