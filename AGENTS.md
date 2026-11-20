# Repository Agent Instructions

## 1. Canonical Sources of Truth (Tier 3 Cold Memory)

Read the smallest authoritative source that resolves the uncertainty: code for implementation questions, contracts and invariants for behavior, the architecture map for structure, ADRs for past decisions.

- [`docs/architecture.md`](docs/architecture.md) — Current implemented architecture: module & seam map, state authority boundaries, and verification commands. Kept technical, dense, and current. Start structural work here.
- [`docs/invariants.md`](docs/invariants.md) — System invariants (`@MODULE -> !INVARIANT`), load-bearing rationale (rejected simplifications), and operational symptom-cause-fix matrices.
- [`docs/contracts/`](docs/contracts/README.md) — Stability and behavioral contracts across subsystem seams.
- [`docs/adr/`](docs/adr/README.md) — Architectural Decision Records for hard-to-reverse choices.
- [`docs/plan/deviations.md`](docs/plan/deviations.md) — Living log of deliberate departures from initial plans and applied review hardening.

Do not rely on chat history alone when a contract, invariant, or test can establish the fact. Update the corresponding contract or invariant entry in the same change that alters behavior.

---

## 2. Structural Tool Routing & Context Retrieval

Select retrieval tools by the question being answered, and retrieve the smallest evidence set capable of resolving consequential uncertainty:

- **Code relationships, impact radius, or affected tests → `code-review-graph`:**
  - On Windows, always pass the absolute `repo_root` parameter to MCP tool calls.
  - **Fast structural refresh (routine edits):** `rtk proxy uvx code-review-graph update --repo "<ABSOLUTE_REPO_ROOT>" --skip-flows`
  - **Full flow & community refresh:** When a consequential decision depends on multi-hop execution flows or community boundaries and the derived data is stale, omit `--skip-flows` (`rtk proxy uvx code-review-graph update --repo "<ABSOLUTE_REPO_ROOT>"`) to recompute that data.
  - Check both symbol freshness and flow freshness before trusting flow queries; an unindexed symbol or skipped flow pass is not proof that no caller or execution path exists.
- **Structure of large or unfamiliar files → `ast-grep outline` (`sg outline`):**
  - Before first use, check `ast-grep outline --help`. If `outline` is unavailable, use `rg`, LSP document symbols, or focused file reads.
  - For small files, read the source directly when cheaper than outlining.
  - Use `ast-grep outline <file>` (defaults to `--items structure --view digest`) to inspect a candidate file's items, members, and line numbers before reading it in full.
  - Use `ast-grep outline <dir> --items exports` to scan a subtree's public surface, or `--match <Symbol> --view expanded` to zoom into a specific type/class.
- **Syntax shapes, boundary checks, or codemods across files → `ast-grep run` / `scan` (`sg`):**
  - Match AST patterns across implementations where text search (`rg`) is too noisy.
- **Ambiguous symbol/trait resolution → Compiler / LSP (`rtk cargo check`, `tsc`, etc.):**
  - Neither `code-review-graph` nor `ast-grep outline` resolves types or trait dispatch; use compiler diagnostics or LSP when static structure is ambiguous.
- **Noisy CLI output → `rtk` (Rust Token Killer):**
  - Prefix CLI commands with `rtk` (`rtk git status`, `rtk cargo test`). Use `rtk proxy <cmd>` when raw machine-readable output is required.

Treat extracted structure as navigation evidence, not proof of runtime behavior.

---

## 3. Orchestration Trigger Table (Tier 1 -> Tier 2/3 Routing)

When a task or modified file matches a signal below, load the mapped skill and owning reference BEFORE editing or finalizing:

| Phase | Observable Signal / Path Glob | Required Skill (Tier 2) | Owning Reference / Contract (Tier 3) |
| :--- | :--- | :--- | :--- |
| **Exploration** | Map the existing system, trace a feature, or explain a change’s impact | [`codebase-map`](.agents/skills/codebase-map/SKILL.md) | [`docs/architecture.md`](docs/architecture.md) |
| **Pre-Change** | Designing/restructuring modules, interfaces, or seams | [`codebase-design`](.agents/skills/codebase-design/SKILL.md) | [`docs/architecture.md`](docs/architecture.md), [`docs/contracts/`](docs/contracts/README.md) |
| **Pre-Change** | Ambiguous domain rules, ownership, or state transitions | [`domain-modeling`](.agents/skills/domain-modeling/SKILL.md) | [`docs/invariants.md`](docs/invariants.md), [`docs/adr/`](docs/adr/README.md) |
| **Pre-Change** | Hard-to-reverse auth, migration, concurrency, or unverified claim | [`doubt-driven-development`](.agents/skills/doubt-driven-development/SKILL.md) | [`docs/invariants.md`](docs/invariants.md), [`docs/contracts/`](docs/contracts/README.md) |
| **Pre-Change** | TypeScript browser input, storage, resource lifetimes, or PWA | [`typescript-browser-apps`](.agents/skills/typescript-browser-apps/SKILL.md) | [`.agents/skills/typescript-browser-apps/references/`](.agents/skills/typescript-browser-apps/references/browser-runtime.md) |
| **Pre-Change** | Rust crate trait dispatch, feature flags, or callback bounds | [`advanced-rust-integration`](.agents/skills/advanced-rust-integration/SKILL.md) | Resolved crate `manifest_path` via `cargo metadata` |
| **In-Flight** | Bug report, flaky test, or performance regression | [`diagnosing-bugs`](.agents/skills/diagnosing-bugs/SKILL.md) | [`docs/invariants.md`](docs/invariants.md), [`docs/contracts/`](docs/contracts/README.md) |
| **In-Flight** | Throwaway state-machine demo or UI variant exploration | [`prototype`](.agents/skills/prototype/SKILL.md) | [`.agents/skills/prototype/LOGIC.md`](.agents/skills/prototype/LOGIC.md) / [`UI.md`](.agents/skills/prototype/UI.md) |
| **Post-Change** | Refactoring working code for clarity without behavior change | [`code-simplification`](.agents/skills/code-simplification/SKILL.md) | [`docs/invariants.md`](docs/invariants.md) (Chesterton's Fence check) |
| **Post-Change** | Auditing a PR, branch diff, or invariant compliance | [`decision-pr-review`](.agents/skills/decision-pr-review/SKILL.md) | [`docs/invariants.md`](docs/invariants.md), [`docs/plan/deviations.md`](docs/plan/deviations.md) |
| **Post-Change** | Editing `.agents/skills/*`, `AGENTS.md`, or `docs/*.md` | [`writing-for-agents`](.agents/skills/writing-for-agents/SKILL.md) | [`docs/contracts/agent-skills.md`](docs/contracts/agent-skills.md) |

---

## 4. Core Execution & Isolation Guardrails

- **Deep Modules & Deletion Test (`codebase-design`):** Design deep modules (significant domain behavior behind a small, simple interface at a real seam). If deleting a layer removes complexity rather than duplicating it across callers, inline it.
- **No Relocated Complexity (`code-simplification`):** Refactors must reduce the number of concepts a reader holds in mind, not merely move branches across more files.
- **Tight Feedback Loop First (`diagnosing-bugs`):** Build a tight, red-capable, deterministic feedback loop before forming any bug hypothesis.
- **Prototype Scope (`prototype`):** Keep transient prototype state in memory. For disposable local development data, prefer one current schema and a development reset over intermediate migrations. Require explicit approval before resetting existing data.
- **Subagent Isolation:** When dispatching subagents for exploration, `DESIGN-IT-TWICE`, or `doubt-driven-development`, start them with a clean, isolated context window — pass only the explicit brief, artifact, and contract. Never fork the parent session's history: an inherited context anchors the subagent on prior reasoning and defeats adversarial review and independent design.