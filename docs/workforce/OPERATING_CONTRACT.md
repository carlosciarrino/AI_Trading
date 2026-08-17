# AI_BRIDGE V3 — OPERATING CONTRACT

## Binding

1. APPROVED decision = binding immediately.
2. Binding decisions must be persisted in repository.
3. Repository = source of truth.
4. Chat = coordination surface only.
5. Never re-open resolved decisions unless concrete technical evidence requires change.
6. Known failure classes must use existing recovery procedure.
7. Human copy/paste must be minimized.
8. Prefer one aggregated terminal command.
9. Every operational command must self-check.
10. Every operation must verify postconditions.
11. Recoverable failures must be retried automatically with bounded retries.
12. False positives require SECOND_INSPECTION before escalation.
13. State and evidence must be persisted.
14. Pipeline must advance automatically after PASS.
15. No infinite loops.
16. HUMAN_REQUIRED only for genuinely unresolved conditions.
17. Future improvements may replace this procedure only when demonstrably better.
18. Replaced procedures must remain documented.
19. Resolved problems must not return as unresolved workflow decisions.
20. Operator is not a courier.

## Execution contract

GOAL
→ PRECHECK
→ ACTION
→ INSPECT
→ RECOVER
→ VERIFY
→ PERSIST
→ NEXT ACTION

Failure classes:

KNOWN_RECOVERABLE
→ automatic recovery
→ bounded retry
→ verification

FALSE_POSITIVE
→ SECOND_INSPECTION
→ verification

UNKNOWN
→ bounded diagnostic attempt
→ HUMAN_REQUIRED

HUMAN_REQUIRED must contain:
- reason
- failed stage
- evidence
- attempts
- last output

## Human role

HUMAN = strategic decision maker / escalation authority.

HUMAN != terminal worker.

## One-command rule

Operational procedures must be executable through one aggregated command whenever technically possible.

A command is incomplete if normal expected recovery requires another manual command.

## Permanence

Once failure class is solved and encoded, same class must be handled automatically forever unless a better verified strategy replaces it.

1. Minimize human copy/paste
