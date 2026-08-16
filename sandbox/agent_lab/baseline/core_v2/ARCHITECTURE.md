# AI_BRIDGE V2 Architecture

## Purpose

AI_BRIDGE V2 is designed as a modular, deterministic and extensible trading operating system.

The project is intentionally divided into independent components, each responsible for a single domain of responsibility.

Every module must be:

- deterministic
- independently testable
- fully typed
- documented
- based exclusively on the Python Standard Library

---

# Architectural Principles

The architecture follows these principles:

- Single Responsibility Principle
- Explicit dependencies
- Immutable public interfaces
- Separation between infrastructure and business logic
- Fail-fast error handling
- Deterministic behaviour
- Progressive extensibility

---

# Architecture Layers

The system is divided into logical layers.

Layer 1

Infrastructure

- exceptions.py
- utils.py
- telemetry.py
- constants.py
- config.py
- bootstrap.py

Layer 2

Runtime

- runtime_controller.py
- orchestrator.py

Layer 3

Business Engines

- market_engine.py
- decision_engine.py
- risk_engine.py
- execution_engine.py
- monitoring_engine.py
- recovery_engine.py
- memory_engine.py
- learning_engine.py
- event_engine.py

---

# Dependency Rules

A module may only depend on modules located in the same layer or in a lower layer.

Forbidden:

Infrastructure importing Engines

Execution importing Decision

Decision importing Monitoring

Recovery importing Learning

No circular dependency is allowed.

---

# Engine Design Rules

Every Engine exposes one public class.

Example

MarketEngine

DecisionEngine

RiskEngine

ExecutionEngine

MonitoringEngine

RecoveryEngine

MemoryEngine

LearningEngine

EventEngine

Each Engine owns its internal state.

No Engine may modify another Engine directly.

Communication always happens through explicit public methods.

---

# Public API

Public methods should remain stable.

Internal implementation may evolve without breaking the public API.

---

# Configuration

Configuration is loaded exclusively through

core_v2.config

No module reads YAML files directly.

---

# Logging

Every module uses the shared logger initialized by telemetry.py.

No module creates independent loggers.

---

# Exceptions

Infrastructure exceptions belong to

core_v2.exceptions

Runtime modules may define domain-specific exceptions when appropriate.

---

# Typing

All public APIs must be fully type annotated.

Use dataclasses whenever appropriate.

Use Protocol for abstraction boundaries.

---

# Standard Library

External dependencies are not allowed.

Only Python Standard Library modules may be imported.

---

# Testing Policy

Every module must successfully pass

python3 -m py_compile

before integration.

Every integration must preserve bootstrap execution.

---

# Git Policy

Each module is committed independently.

Every commit must leave the repository in a working state.

---

# Future Evolution

The architecture is intentionally designed to support future extensions without breaking compatibility.

New Engines must respect all rules defined in this document.
