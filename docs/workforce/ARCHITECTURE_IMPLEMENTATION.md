# AI_BRIDGE V3 — WORKFORCE ARCHITECTURE IMPLEMENTATION

## WF-003

Hybrid architecture implemented as local control plane:

- Runtime/agent base: OpenHands SDK compatible boundary.
- Governance: deterministic supervisor/state machine.
- Dispatch: worker registry + dispatcher.
- Workflow inspiration: Looper-style bounded autonomous loops.
- Governance inspiration: Liza-style code-enforced gates, evidence, review boundaries.
- `mini-swe-agent` and `aider`: reference workers/adapters, not control plane.
- Repository remains source of truth.
- Chat remains coordination surface.
- Human intervention only on `HUMAN_REQUIRED` or explicit strategic approval.
- Unknown failure stops; no infinite retry.
- Evidence required at stage checkpoint.
- State persisted after every transition.
- No production dependency forced into control plane.
