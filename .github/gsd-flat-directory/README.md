---
Author: Kelvin Kabute
Last-updated: 2026-05-05
---

# GSD Flat Directory — Copilot Planning Integration

This directory is the single entry point the Copilot planning module reads at the start of any planning session. It maps every GSD skill and agent in this repository to one of six lifecycle stages, explains when each resource should be spawned, and defines the protocol for handing off cleanly from planning to execution.

Do not modify this directory by hand unless you are adding a new GSD skill or agent and want to register it in the appropriate stage. Canonical skill instructions live in `.github/skills/gsd-*/SKILL.md`. Canonical agent instructions live in `.github/agents/*.agent.md`. This directory only indexes them — it does not duplicate their content.

---

## How Copilot uses this directory

At the start of any planning session, Copilot reads this README first. It then reads `copilot-integration.md` in this directory to understand the access rules — specifically which stages are open during planning and which are locked until after the HANDOFF protocol is satisfied. It navigates to the stage files only for stages it is permitted to access at that moment.

When a planning task requires spawning a GSD agent or running a GSD skill, Copilot identifies the correct resource by consulting the stage document for that stage. Each stage document describes every skill and agent that belongs to it, covering all commands, flags, modes, and edge cases in enough depth to make an informed dispatch decision without reading the full SKILL.md unless additional detail is needed.

When planning is complete and execution is ready to begin, Copilot reads `HANDOFF.md` in this directory, verifies all required artifacts exist, and produces a handoff package that the execution agent uses to begin the coding stage.

---

## The six stages

Every GSD skill and agent in this repository belongs to exactly one primary stage. The stages form an ordered lifecycle from discovery through delivery.

**Stage 01 — Research** covers everything that happens before a plan is written. You are trying to understand the codebase, the domain, prior decisions, or relevant technology. The skills and agents in this stage gather and synthesize information without making implementation commitments. Read `stages/01-research.md`.

**Stage 02 — Planning** is where decisions are locked and plans are written. Specifications are produced, gray areas are resolved through structured discussion, PLAN.md files are created and verified, and design contracts for UI and AI phases are generated. Read `stages/02-planning.md`.

**Stage 03 — Orchestration** is the control layer. It does not belong exclusively to planning or execution — it runs across the entire lifecycle to manage progress, route to the next action, control workstreams, handle pauses, import external artifacts, and configure GSD behavior. During a planning session Copilot can access this stage to manage its own workflow. Read `stages/03-orchestration.md`.

**Stage 04 — Coding** is locked during planning. It contains the skills and agents that write code. These resources are only accessible after a valid handoff package exists. Read `stages/04-coding.md` only when the coding stage has been entered.

**Stage 05 — Testing** is locked during planning. It contains verification, auditing, debugging, and security review resources that operate on implemented code. Read `stages/05-testing.md` only after code has been written.

**Stage 06 — Deployment** is locked during planning. It contains release, PR, documentation, and milestone archiving resources. Read `stages/06-deployment.md` only after testing passes.

---

## Access rules summary

Stages 01, 02, and 03 are accessible during any planning session. Stages 04, 05, and 06 are blocked at planning time. The detailed access rules, including the exact conditions under which each stage unlocks, are in `copilot-integration.md`.

---

## Handoff protocol

When planning is complete and Copilot is ready to hand off to an execution agent, it follows the protocol in `HANDOFF.md`. That document defines exactly which artifacts must exist, what the handoff package contains, and how the execution agent is invoked with that package.

---

## Directory layout

```text
.github/gsd-flat-directory/
  README.md              — this file, the entry point
  copilot-integration.md — access rules for the Copilot planning module
  HANDOFF.md             — transition protocol from planning to execution
  stages/
    01-research.md       — codebase exploration, domain research, doc ingestion
    02-planning.md       — spec, discuss, plan, UI/AI design contracts
    03-orchestration.md  — progress, routing, workstreams, config, lifecycle control
    04-coding.md         — execution, inline tasks, quick tasks (LOCKED during planning)
    05-testing.md        — verification, audit, debug, security (LOCKED during planning)
    06-deployment.md     — ship, PR, docs, milestone archiving (LOCKED during planning)
```
