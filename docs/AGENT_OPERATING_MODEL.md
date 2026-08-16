# AI_BRIDGE V3 — AGENT OPERATING MODEL

## 1. Principle

AI_BRIDGE V3 uses a dynamic agent workforce.

The repository is the source of truth.

Chat is a meeting room, not project memory.

Agents perform work.

Supervisor coordinates work.

Owner approves strategic decisions.

## 2. Roles

### OWNER

Responsibilities:
- strategic decisions;
- milestone approval;
- scope approval;
- final acceptance.

Owner does not perform repository inspection manually.

### SUPERVISOR

Responsibilities:
- decompose tasks;
- create task graph;
- select agents;
- assign contracts;
- enforce gates;
- collect evidence;
- compare results;
- reject incomplete work;
- approve promotion candidates;
- maintain project state.

Supervisor must never assume an agent completed a check merely because agent reports PASS.

### SPECIALIST AGENTS

Agents are temporary specialists.

Examples:
- security;
- license;
- architecture;
- capability;
- testing;
- benchmark;
- integration;
- documentation;
- repository audit.

Agent count is dynamic.

No fixed workforce size.

## 3. Agent Contract

Every agent must receive:

- ROLE
- MISSION
- INPUTS
- CHECKLIST
- FORBIDDEN ACTIONS
- REQUIRED EVIDENCE
- PASS CONDITIONS
- FAIL CONDITIONS
- ESCALATION CONDITIONS
- OUTPUT SCHEMA

Agent cannot redefine own mission.

Agent cannot skip mandatory checklist items.

Agent cannot mark unchecked items PASS.

## 4. Checklist Rule

Every inspection uses explicit checklist.

Each item must produce:

- STATUS
- EVIDENCE
- RISK
- NOTES

Allowed STATUS values:

- PASS
- FAIL
- WARNING
- NOT_APPLICABLE
- BLOCKED

Missing evidence means item is not PASS.

## 5. Evidence Rule

Evidence must be machine-readable whenever possible.

Examples:

- file path;
- line range;
- hash;
- command;
- exit code;
- test result;
- dependency;
- configuration value;
- benchmark result.

Chat output is not authoritative evidence.

Repository artifacts are authoritative evidence.

## 6. Security Gate

Candidate repository cannot enter sandbox until security gate passes.

Security inspection must cover:

- hidden files;
- symlinks;
- executable files;
- network access;
- subprocess execution;
- shell execution;
- privilege escalation;
- dynamic execution;
- encoded payloads;
- credential access;
- filesystem destruction;
- persistence;
- CI workflows;
- Dockerfiles;
- installation scripts;
- Git hooks;
- dependencies;
- external binaries;
- external URLs.

Pattern matches are not automatically malicious.

Every finding requires contextual classification.

Security verdict:

- ALLOW_SANDBOX
- HOLD
- REJECT

## 7. Repository Qualification Gate

Candidate must be evaluated for:

- provenance;
- license;
- maintenance;
- compatibility;
- architecture;
- dependencies;
- APIs;
- tests;
- documentation;
- sandbox compatibility;
- Docker compatibility;
- Git compatibility;
- resource requirements;
- integration complexity;
- usefulness;
- rollback capability.

## 8. Sandbox Rule

No external agent may modify:

- core_v2;
- production files;
- protected configuration;
- authoritative project history.

Agents work inside disposable sandbox.

Sandbox must support:

- baseline;
- modification;
- validation;
- recovery;
- rollback.

## 9. Promotion Gate

Candidate can be promoted only when:

1. security PASS;
2. repository qualification PASS;
3. sandbox PASS;
4. modification test PASS;
5. recovery test PASS;
6. benchmark PASS;
7. required evidence exists;
8. supervisor validates checklist completeness.

Promotion is controlled.

No automatic production integration.

## 10. Dynamic Workforce

Supervisor creates agents according to task graph.

Examples:

- small task: 1 specialist;
- medium task: multiple specialists;
- large task: parallel specialist pool.

Agent count is workload-dependent.

Agents may be:

- recruited;
- tested;
- assigned;
- suspended;
- rejected;
- promoted;
- retired.

No permanent dependency on one external agent.

## 11. Failure Handling

FAIL does not automatically mean code change.

Supervisor classifies failure:

- agent defect;
- repository defect;
- environment defect;
- false positive;
- missing evidence;
- genuine security risk;
- compatibility problem;
- architectural mismatch.

Only classified failures trigger corrective action.

## 12. Owner Interface

Owner receives compact decision packets.

Format:

TASK:
STATUS:
RECOMMENDATION:
BLOCKERS:
RISKS:
EVIDENCE:
DECISION REQUIRED:

Owner should not receive raw repository dumps.

## 13. Chat Rule

Chat must remain lightweight.

Do not paste:

- full repository trees;
- large source files;
- large logs;
- repeated diagnostics;
- raw agent output.

Chat receives only:

- decision packets;
- blockers;
- relevant evidence;
- milestone results.

## 14. Project Memory

Project state must live in repository artifacts.

Primary state:

- docs/SESSION_STATE.md
- docs/DEVELOPER_SNAPSHOT.md
- docs/AGENT_OPERATING_MODEL.md
- docs/research/AGENT_REGISTRY.json
- sandbox/agent_lab/

Chat is temporary interface.

## 15. Core Protection

External agents are RESEARCH_ONLY until promotion.

core_v2 remains protected.

Experiments remain sandboxed.

Validation is mandatory.

Rollback is mandatory.

Promotion is controlled.

Paid services are forbidden.

## 16. Final Principle

Owner decides WHAT.

Supervisor decides HOW.

Specialists execute PARTS.

Gates decide WHETHER.

Evidence decides TRUST.

Repository stores MEMORY.

Chat coordinates DECISIONS.
