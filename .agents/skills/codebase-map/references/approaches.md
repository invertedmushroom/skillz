# Choosing a codebase map

Choose by the decision the reader needs to make. A local source trace is usually the shortest answer to a single feature question. A persistent, navigable map earns its upkeep when people return to it to explore other features or compare revisions.

| Reader's goal | Approach and examples | What to check |
| --- | --- | --- |
| Understand an unfamiliar app | Walk a non-expert through the subsystems in plain language. A whole-app explorer can make details available on demand. [Floorplan](https://github.com/haydenschmitty/floorplan) | Can the reader follow a familiar action to the component that owns its result? |
| Explore code relationships | Start from a symbol and follow callers or dependencies in the local code graph or an explorable knowledge graph. [Understand Anything](https://github.com/egonex-ai/understand-anything) | Does the chosen edge mean imports, calls, or subscribes? Point to the binding for a behavioral claim. |
| Assess change impact | Trace reverse dependencies from a changed symbol to entry points, then inspect which consumers use the changed behavior. [Cartograph](https://github.com/adrianhajdin/cartograph) and [Codeflow](https://github.com/braedonsaunders/codeflow) | A dependency identifies a candidate. Show which caller or test actually reaches the changed branch. |
| Communicate structure visually | Select an overview, sequence, or state diagram to suit the question. [GitDiagram](https://github.com/ahmedkhaleel2004/gitdiagram), [Archify](https://github.com/tt-a1i/archify), and [Oh My Mermaid](https://github.com/oh-my-mermaid/oh-my-mermaid) | Label a blueprint drawn from a spec as proposed. For an implementation diagram, link important arrows to source. |
| Reconcile code with contracts, schemas, or deployment configuration | Connect artifacts with identifiers such as a route, table, or event name. [Graphify](https://github.com/graphify-labs/graphify) | Identify which artifact records intent, which defines a binding, and which provides evidence of execution. |

These are optional tools. Use the project's available tooling by default. Check project-sharing permissions before sending repository content to an external service.
