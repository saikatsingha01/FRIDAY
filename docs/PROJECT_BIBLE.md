# PROJECT FRIDAY
## Canonical Architecture Bible
Version: 2.0
Status: ACTIVE

---

# Vision

FRIDAY is not a chatbot.

FRIDAY is an AI Operating System.

The goal is to build a trustworthy AI companion capable of understanding, reasoning, planning, remembering, executing, learning and evolving while always remaining under the user's authority.

Architecture comes before features.

Long-term maintainability is valued over short-term speed.

---

# Core Principles

1. User Authority First

The user is always in control.

FRIDAY never performs sensitive actions without permission.

---

2. Security Before Intelligence

Security is never sacrificed for convenience.

Every powerful capability must be permission-controlled.

---

3. Architecture Before Features

Features may change.

Architecture should not.

Every feature must fit the architecture instead of modifying it.

---

4. Modular Design

Every module owns exactly one responsibility.

Modules communicate through contracts.

No module should perform another module's job.

---

5. Technology Independence

FRIDAY must never depend on one AI model.

Every external dependency should be replaceable.

Examples

- Ollama
- OpenAI
- Claude
- Gemini
- DeepSeek
- AirLLM

must all be interchangeable.

---

6. Long-Term Evolution

FRIDAY should continue improving for years.

The architecture should support future capabilities without major rewrites.

---

# Architecture Philosophy

Everything inside FRIDAY follows this pipeline:

User

↓

Input

↓

Understanding

↓

Reasoning

↓

Execution

↓

Prompt Construction

↓

LLM

↓

Response

↓

Reflection (future)

↓

Memory Update

No layer may skip another layer.

---

# Folder Responsibilities

## input/

Receives user input.

Responsibilities

- Keyboard
- Voice
- Camera

Does NOT

- Understand language
- Execute commands

---

## speech/

Speech recognition and speech synthesis.

Responsibilities

- STT
- TTS
- Voice Activity Detection

---

## understanding/

Purpose

Understand language.

Responsibilities

- Semantic understanding
- Conversation analysis
- Emotion analysis
- Context analysis
- Memory analysis

Never

- Retrieve memory
- Execute commands
- Perform reasoning
- Talk to tools

Output

LanguageUnderstanding

---

## contracts/

Purpose

Shared data models.

Responsibilities

- LanguageUnderstanding
- ExecutionResult
- PlannerContract
- ReflectionContract

Never

- Execute logic

---

## reasoning/

(Currently located in core)

Purpose

Convert understanding into execution decisions.

Responsibilities

- Decide which systems participate
- Build execution plan

Never

- Parse English
- Retrieve memory
- Call tools

Output

ReasoningResult

---

## execution/

Purpose

Coordinate every execution subsystem.

Responsibilities

- Memory
- Context
- Tools
- Web
- Vision
- Planning

Never

- Understand language

Output

ExecutionResult

---

## memory/

Purpose

Store and retrieve knowledge.

Responsibilities

- Long-term memory
- Episodic memory
- Consolidation
- Validation

Never

- Understand English
- Generate responses

---

## ai/

Purpose

Interact with language models.

Responsibilities

- Prompt construction
- Model routing
- Provider abstraction

Never

- Make decisions

---

## skills/

Purpose

Tool implementations.

Examples

- Calculator
- File Manager
- Browser
- Music

Never

- Decide when to execute

---

## core/

Temporary orchestration layer.

Contains

- Brain
- Conversation Manager
- Response Generator

Future

Most orchestration will gradually move into dedicated architecture layers.

---

# Engineering Rules

Rule 1

Every module owns one responsibility.

---

Rule 2

Never create a new file unless an existing file has become too large or gained multiple responsibilities.

---

Rule 3

No premature abstraction.

Architecture grows only when necessary.

---

Rule 4

Brain orchestrates.

Brain does not think.

---

Rule 5

Understanding never executes.

---

Rule 6

Execution never understands language.

---

Rule 7

Memory never decides.

---

Rule 8

Reasoning never parses English.

---

Rule 9

LLMs are replaceable.

The system must never depend on one provider.

---

Rule 10

Architecture changes require updating this document.

---

# Development Philosophy

Whenever adding a feature, ask:

1. Which layer owns this responsibility?

2. Does an existing module already own it?

3. Can this be added without creating a new file?

4. Does this violate any architecture rule?

If any answer is uncertain:

Stop.

Review the architecture.

---

# Roadmap

Phase 1

✓ Voice Foundation

✓ Memory Foundation

✓ Understanding Engine

✓ Contracts

✓ Reasoning Engine

✓ Execution Layer Foundation

---

Phase 2

Execution Layer Expansion

- Context Execution

- Tool Execution

- Web Execution

- Vision Execution

- Planner Integration

---

Phase 3

Planning System

- Planner

- Task Graph

- Scheduler

- Executor

---

Phase 4

Reflection Engine

- Response Evaluation

- Failure Analysis

- Self Improvement

---

Phase 5

Dynamic Model Routing

- Local Models

- Cloud Models

- Automatic Model Selection

---

Phase 6

Autonomous Workflows

- Multi-agent execution

- Background tasks

- Long-running plans

---

Phase 7

Learning and Evolution

- User adaptation

- Skill acquisition

- Workflow optimization

---

# Permanent Rule

This document is the source of truth.

When architecture changes,

update this document first.

Then update the code.

Never the other way around.