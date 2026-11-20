---
name: codebase-map
description: Map an existing codebase, trace a user action to its effects, or explain which callers, outputs, and tests a change could affect.
---

# Codebase Map

Start with the reader's question. For someone new to the app, name the action they recognize and its visible outcome. Use the code's exact names alongside that explanation so a maintainer can follow it back to source.

| Reader's question | What to map |
| --- | --- |
| How does this app fit together? | Identify the entry points, the few subsystems that do the work, where state lives, and the systems outside the checkout. Connect them with one representative user action. |
| What happens when I do this? | Follow that action from its screen, command, event, or endpoint to the resulting read, write, or response. Expand the handoff the reader cares about. Include a failure branch when it changes what the user sees or what gets saved. |
| What did this change affect? | Identify the compared revisions or working-tree diff. Trace the changed behavior back to callers and forward to affected outputs or stored data. Point to a test that exercises the path and say whether it ran. |

## Ground each connection

Use the architecture overview for names and the local graph for candidate callers, callees, and tests. Check its revision and scope. Follow a consequential edge to the call site, route binding, event subscription, query, or configuration that wires it. If the index is unavailable or stale, use targeted source searches and reads. For a cross-repository handoff, name the interface and how far each available checkout lets you follow it.

Distinguish what the evidence establishes:

- **Confirmed in source** means the binding is visible. Name the operation precisely, such as “enqueues a receipt” or “commits the order.” An import alone establishes a dependency.
- **Observed** means a test or trace exercised the path. Identify the check and any substituted external service. A test with a fake mailer can demonstrate dispatch to the mailer interface.
- **Inferred or unknown** means a link depends on missing wiring, deployment settings, or an external system. Mark the uncertain hop where it occurs and name the evidence that would settle it.

## Deliver the view at the requested scale

For a single question, a short chain of verbs and links to files or symbols is often enough. For a broad map, group by responsibility and let the reader follow one feature down to its files and handlers. In a requested interactive view, selecting a subsystem or edge should reveal its explanation, source, and any uncertainty. When a spec and the running implementation differ, identify the intended behavior and the evidence for the implemented path.

When updating an existing map, identify its baseline, revisit the edges touched by the diff and their neighbors, and remove stale links. If the baseline is unknown, verify the requested slice against the current checkout. Save or update a map artifact when the request calls for one.

For a choice of external mapping tools or visual formats, use the [map approaches guide](references/approaches.md). The workflow also works entirely with the repository and its local tools.
