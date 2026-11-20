# Contracts

This directory contains stability and behavioral contracts for subsystem seams where boundaries must remain explicit as the implementation grows.

## Current Contracts

- [`agent-skills.md`](agent-skills.md) — Skill authority, static validation, and verification limits.
- [`0000-contract-template.md`](0000-contract-template.md) — Template for new subsystem contracts.

## How To Use

- Treat these as behavior contracts across module seams, not line-by-line implementation notes.
- Update the contract first (or in the same change) when changing semantics.
- Define each seam guarantee here once. Link architecture summaries and [`docs/invariants.md`](../invariants.md) entries to the owning section. Reference separately owned cross-cutting constraints by link.
- Link guarantees to the tests or probes that establish their enforcement.
- Keep current implemented behavior, required invariants, and future proposals distinct.
