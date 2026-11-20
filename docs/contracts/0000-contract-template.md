# [Subsystem / Seam] Contract

- **Status:** Draft | Implemented | Superseded
- **Owning Modules:** `path/to/module`

## 1. Scope & Authority Boundary

Define which module owns truth for this seam, what inputs cross the interface, and what outputs or side effects are guaranteed.

## 2. Behavioral Invariants

1. **[Invariant 1]:** Exact condition that must hold across all callers, retries, and failure modes.
2. **[Invariant 2]:** Ordering, idempotency, or isolation guarantee.

## 3. Failure & Recovery Semantics

How invalid inputs, partial failures, timeouts, or restarts are handled across this seam.

## 4. Verification Surface

List the integration/unit test files or probes that prove this contract holds.
