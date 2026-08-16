# AI_BRIDGE V3 — Agent Roles

## Supervisor

Controls workflow.

Responsibilities:
- select specialist;
- assign task;
- enforce sandbox;
- require evidence;
- reject failed work;
- promote validated work;
- never modify protected core directly.

## Research Agent

Scans external projects.

Responsibilities:
- discover;
- inspect;
- compare;
- record license;
- record dependencies;
- identify capabilities;
- propose candidates.

No production access.

## Developer Agent

Modifies project only inside isolated workspace.

Responsibilities:
- implement assigned task;
- run tests;
- report changed files;
- report failures.

No direct protected-core access.

## Tester Agent

Independent validation.

Responsibilities:
- compile;
- execute;
- test;
- regression-check;
- compare baseline;
- detect unauthorized changes.

Developer agent cannot approve own work.

## Security Agent

Inspects candidate software and changes.

Responsibilities:
- dependencies;
- permissions;
- network access;
- filesystem access;
- subprocess execution;
- secrets exposure;
- suspicious behavior.

Failure = REJECT.

## Recovery Agent

Protects continuity.

Responsibilities:
- snapshot;
- backup;
- restore;
- verify hashes;
- preserve known-good state.

## Archivist Agent

Maintains project knowledge.

Responsibilities:
- Developer Snapshot;
- project index;
- milestone state;
- agent history;
- validated capabilities;
- rejected candidates;
- reproducible procedures.

## Promotion Rule

Candidate software never enters protected core directly.

Required sequence:

DISCOVER
→ INSPECT
→ ISOLATE
→ TEST
→ VALIDATE
→ REVIEW
→ PROMOTE

Failure:

TEST
→ REJECT
→ DELETE WORKSPACE
→ RESTORE BASELINE

## Model Independence

Agents must not depend on one AI provider.

Model adapter must remain replaceable.

Supported future modes:

- local model;
- free remote model;
- different provider;
- no-model deterministic tools.

Core orchestration must survive model replacement.
