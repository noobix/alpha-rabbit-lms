---
Author: Kelvin Kabute
Last-updated: 2026-05-05
---

# Copilot Integration Rules

This document defines the exact rules that govern how the Copilot planning module accesses GSD resources during a planning session. Copilot reads this file immediately after reading `README.md` and applies these rules for the duration of the session.

---

## Session lifecycle

A planning session begins when Copilot is asked to plan a feature, phase, milestone, or any multi-step implementation task. It ends either when Copilot produces a valid handoff package (transitioning to execution) or when the user explicitly closes the planning context.

During a planning session Copilot operates as an orchestrator that can discover and spawn GSD skills and agents, but it does not execute code itself. Its role is to gather enough information and produce enough structured decisions that an execution agent can begin the coding stage without ambiguity.

---

## Stage access during planning

Copilot may read and use resources from stages 01, 02, and 03 freely during a planning session.

Stage 01 (Research) is always accessible. If the codebase has not been mapped, or if a domain needs investigation before committing to an approach, Copilot should use the appropriate research skill or agent. Research is never wasted — it informs the plan and reduces deviation during execution.

Stage 02 (Planning) is the primary working stage. Copilot should progress through the planning workflow in roughly the order the skills are designed to be used: spec before discuss, discuss before plan, plan before any design contracts. That said, the workflow is not strictly linear — if a spec already exists or discuss was already run in a prior session, Copilot should detect the existing artifacts and skip or update rather than re-run from scratch.

Stage 03 (Orchestration) is accessible throughout. Copilot uses orchestration skills to check progress, route to the next logical step, manage workstreams when parallel tracks exist, import external plans from other AI sessions, and configure GSD behavior when a feature gate needs to be set before a planning skill can run.

Stages 04, 05, and 06 are locked during planning. Copilot must not invoke any skill or agent from these stages during a planning session. The stage documents for coding, testing, and deployment are present in this directory so the execution agent can read them after handoff — Copilot should not pre-load or reference them during planning.

---

## How to discover and spawn a resource

When Copilot needs to invoke a GSD skill or agent during planning, it follows this process.

First, identify which stage the task belongs to (01, 02, or 03). If the task is about gathering information or understanding the system, it is Stage 01. If the task is about producing a spec, a discussion record, or a plan, it is Stage 02. If the task is about controlling the workflow, checking progress, managing state, or importing artifacts, it is Stage 03.

Second, read the stage document for that stage. Each stage document names every skill and agent available in that stage and describes how they work, what commands they accept, and what edge cases apply.

Third, match the task to the appropriate skill or agent. Skills are invoked as commands (for example `/gsd-plan-phase 3 --mvp`). Agents are spawned as subagents inside skill workflows — Copilot does not spawn agents directly; it invokes the skill that orchestrates the agent.

Fourth, load the canonical SKILL.md or agent file only if the stage document does not have enough detail for a specific flag or edge case. Canonical paths follow the pattern `.github/skills/gsd-{name}/SKILL.md` for skills and `.github/agents/gsd-{name}.agent.md` for agents.

---

## Progression through the planning workflow

For a typical new feature or phase, the planning workflow proceeds as follows.

Copilot first checks whether a codebase map exists in `.planning/codebase/`. If not and the codebase is non-trivial, it considers running `gsd-map-codebase` from Stage 01 before anything else. This prevents the planner from making assumptions about the codebase that turn out to be wrong.

Copilot then checks whether `SPEC.md` exists for the phase. If not, it runs `gsd-spec-phase` from Stage 02 to lock WHAT the phase delivers before any HOW discussion begins. `gsd-spec-phase` uses an ambiguity scoring gate — it does not exit until the ambiguity score is at or below 0.20 across four dimensions.

Next, if `CONTEXT.md` does not exist for the phase, Copilot runs `gsd-discuss-phase` from Stage 02. This produces the implementation decisions that the planner needs. It loads prior context automatically so already-decided questions are never re-asked.

Once CONTEXT.md exists, Copilot runs `gsd-plan-phase` from Stage 02. This skill orchestrates research (if needed), spawns the gsd-planner agent, and runs a verification loop with gsd-plan-checker. The output is one or more PLAN.md files.

If the phase involves a frontend component, Copilot additionally runs `gsd-ui-phase` from Stage 02 to produce a UI-SPEC.md design contract. If the phase involves an AI system, it runs `gsd-ai-integration-phase` to produce an AI-SPEC.md with an embedded evaluation strategy.

When PLAN.md is ready and verified, Copilot reads `HANDOFF.md` and executes the handoff protocol.

---

## Feature gates

Some GSD skills require a feature gate to be set before they can run. Copilot is responsible for detecting these requirements and setting them using `gsd-config` or `gsd-settings` from Stage 03 before attempting to invoke the gated skill. The most common gate requirement is `workflow.plan_review_convergence=true`, which must be set before running `gsd-plan-review-convergence`.

---

## What Copilot must not do during planning

Copilot must not invoke `gsd-execute-phase`, `gsd-fast`, `gsd-quick`, or any other Stage 04 skill. These skills write code and commit changes. A planning session does not write production code.

Copilot must not invoke any Stage 05 skill (testing, verification, audit, debug). These operate on implemented code that does not yet exist at planning time.

Copilot must not invoke any Stage 06 skill (ship, PR, docs, milestone archive). These operate on completed, merged work.

Copilot must not skip the handoff protocol and tell the execution agent to "just start". The handoff package is a structured brief. Execution without it will produce deviations that are expensive to diagnose.

---

## When planning is done

Planning is done when all of the following are true: PLAN.md exists and has passed gsd-plan-checker verification, CONTEXT.md exists with implementation decisions recorded, RESEARCH.md exists if the plan required a research phase, and any required design contracts (UI-SPEC.md, AI-SPEC.md) exist. When all of these conditions are met, Copilot reads `HANDOFF.md` and follows the transition protocol.
