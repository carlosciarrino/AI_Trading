# AI_BRIDGE V3 — AGENT WORKFORCE ARCHITECTURE

## Decision

Selected architecture: **HYBRID**

### Execution substrate
**OpenHands Software Agent SDK**

Provides agent reasoning/action loop, context, tools, security analysis, workspaces, agent-server and automation-compatible runtime.

### Governance/control plane
**Liza-inspired governance pattern**

AI_BRIDGE owns:
- immutable task contracts
- explicit state machine
- deterministic gates
- independent reviewer
- audit trail
- circuit breaker
- bounded retries
- HUMAN_REQUIRED escalation

### Dispatch/orchestration pattern
**Looper-inspired autonomous loop**

AI_BRIDGE supervisor owns:
`DISCOVER → ASSIGN → EXECUTE → VERIFY → REVIEW → MERGE/REJECT → NEXT`

### Reference components

**mini-swe-agent**
- simplicity
- small agent loop
- interchangeable model/environment interfaces
- sandbox execution patterns

**Aider**
- repository mapping
- automatic lint/test cycle
- Git integration

Neither becomes AI_BRIDGE foundation.

## Architectural rule

Do not fork or recreate existing agent runtime capabilities when OpenHands already provides them.

AI_BRIDGE remains owner of:
- business/workforce policy
- task contracts
- persistent state
- role assignment
- verification gates
- recovery
- escalation
- project memory
- MT4/trading integration

External projects provide execution primitives, not project authority.

## Target topology

Human
  ↓
AI_BRIDGE Control Plane
  ↓
Supervisor
  ↓
Task Queue / Persistent State
  ↓
Role Worker
  ↓
OpenHands Agent Runtime
  ↓
Sandbox / Workspace
  ↓
Deterministic Verification
  ↓
Independent Review
  ↓
Commit / Reject
  ↓
Next Task

## Binding constraints

1. Repository remains source of truth.
2. Approved decisions persist immediately.
3. One aggregated terminal command preferred.
4. Human interaction only on HUMAN_REQUIRED or strategic approval.
5. Bounded retries mandatory.
6. False positives require second inspection.
7. Every completed task produces evidence.
8. No autonomous merge without deterministic gates.
9. Unknown failure stops system; never infinite-loop.
10. Architecture may improve only through explicit evidence-backed revision.

## Status

ARCHITECTURE_SELECTION: APPROVED
NEXT: ARCHITECTURE_IMPLEMENTATION
