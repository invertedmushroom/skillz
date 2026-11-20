# Documentation Map

This directory separates durable technical documentation by purpose:

- **[`invariants.md`](invariants.md)** — High-entropy system invariants (`@MODULE -> !INVARIANT`) and load-bearing rationale (rejected simplifications).
- **[`architecture.md`](architecture.md)** — The system as currently implemented: module map, seams, data flow, and authority boundaries.
- **[`contracts/`](contracts/README.md)** — Behavioral and boundary contracts across subsystem seams.
- **[`adr/`](adr/README.md)** — Architectural Decision Records for consequential, hard-to-reverse trade-offs.
- **[`deferred.md`](deferred.md)** — Capabilities explicitly outside the current checkpoint.
- **[`plan/`](plan/README.md)** — Internal implementation plans and the living [`deviations.md`](plan/deviations.md) log.
- **Optional audience folders** — `guide/` (human onboarding, FAQ, testing walkthroughs), `operations/` (executable runbooks and drills), `security/` (threat model and evidence). Create a folder when its contents justify the maintenance. [`architecture.md`](architecture.md) stays the agent-facing map; human-facing exposition belongs in `guide/`, never in a parallel wiki that duplicates it.

## Fact Ownership

Each fact has one maintained definition. Navigation maps, indexes, and decision records link to that definition when they need to refer to it.

| Fact | Owner | When to update |
| :--- | :--- | :--- |
| Implementation and enforcement | Code, configuration, and tests | The implementation changes. Documentation links to evidence rather than cataloging implementation details. |
| Implemented modules, entrypoints, flows, and state ownership | [`architecture.md`](architecture.md) | A recorded responsibility, seam, flow, owner, or verification command changes. Link to contracts and invariants for their guarantees. |
| Guarantees and failure/recovery behavior at a subsystem seam | [`contracts/`](contracts/README.md) | A recorded guarantee or its enforcement changes. |
| Cross-cutting constraints and load-bearing rationale | [`invariants.md`](invariants.md) | A constraint or rationale changes. If a contract already owns the guarantee, index its scope and enforcement with a link to the owning section. |
| Decision context, alternatives, and trade-offs | [`adr/`](adr/README.md) | A decision meets the ADR creation criteria. Preserve past rationale and mark superseded decisions. Link to current guarantees in their owners. |
| Proposed work and intentionally deferred scope | [`plan/`](plan/README.md), [`deferred.md`](deferred.md) | A plan or recorded scope boundary changes. These documents do not define implemented behavior. |

Verify affected claims against code and tests. Surface disagreements between implementation and recorded guarantees. A documentation edit alone does not establish that a guarantee holds.

The scaffold shows where information belongs. A document's presence does not require filling it out. Create additional documents only when their contents justify the maintenance. Keep placeholders while this repository is a template. During adoption, replace or omit them according to the implemented system.

## Adoption Checklist

Use this checklist when copying the template into a project. Repeat the affected checks after changing harnesses, upgrading them, or editing skill configuration. Check only the harnesses and capabilities you actually use.

- [ ] **Adapt the project documentation.** Replace or omit architecture placeholders according to the implemented system. Use the [fact ownership table](#fact-ownership) to place consequential information in its owning document. Keep optional documents unpopulated until they have something to preserve.
- [ ] **Check the tool assumptions.** Review `AGENTS.md` against your environment. Confirm that the referenced tools, shell commands, and MCP servers are available, or adapt the instructions to your alternatives. The skill validator uses `uv` and declares its Python dependency. A tool named in an instruction is not automatically installed or connected.
- [ ] **Verify discovery in each harness.** In a fresh session, confirm that the harness receives the project's `AGENTS.md` instructions and discovers the intended `.agents/skills` entries. Record the harness version and date with the result. If discovery needs a native entry file or configuration, add a small adapter pointing to the shared instructions. Keep shared policy in one authoritative place.
- [ ] **Verify invocation and supporting paths.** Explicitly invoke a skill through the harness's supported mechanism. Confirm that it reads the intended instructions and resolves supporting files from the skill directory. Try a composite skill such as `grill-with-docs` and check that both sibling instructions load. Check automatic versus explicit-only invocation where those policies matter. Verify required tools or subagents separately from successful text loading.
- [ ] **Run static validation after customization.** From the repository root, run the command below. Resolve reported YAML, metadata, invocation-policy, and file-link errors. Passing this check establishes static validity within the [agent skill contract](contracts/agent-skills.md#static-validation). Live discovery and workflow behavior need the checks above.
- [ ] **Try representative requests.** Use a few ordinary tasks and nearby requests that should select a different skill. For example, compare a slide presentation, a [scrolling technical article](../.agents/skills/concept-article/SKILL.md), a standalone diagram, and a plain-text explanation. Confirm the intended workflow and useful output. Adjust skill descriptions or keep a workflow explicit-only when observed selection errors justify the change.
- [ ] **Check session cost and resumption where relevant.** Use the harness's own usage data when available. Separate always-loaded instructions and catalog metadata from activated skill bodies and retrieved evidence. Record unavailable measurements as unmeasured. For work spanning sessions, trial a short handoff containing the objective, constraints, completed work, open questions, verification evidence, and next action. Confirm that a fresh session can resume it.
- [ ] **Agree on concurrent editing.** When several harnesses or agents may write to the project at once, establish who owns each change and whether separate worktrees are needed. Verify that one session's edits and commits do not interfere with another session's work.

```powershell
rtk proxy uv run --script scripts/validate_skills.py --self-test
```

Record observed failures and adapt the smallest relevant instruction or adapter. Add routing, hooks, or shared runtime memory when a demonstrated need justifies them.
