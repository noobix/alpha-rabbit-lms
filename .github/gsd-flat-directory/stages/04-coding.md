---
Author: Kelvin Kabute
Last-updated: 2026-05-05
---

# Stage 04 — Coding

Canonical skill files: `.github/skills/gsd-{name}/SKILL.md`
Canonical agent files: `.github/agents/gsd-{name}.agent.md`

---

## ACCESS RESTRICTION — PLANNING CONTEXT

This stage is blocked during the Copilot planning context. Skills and agents in this stage write production code and commit changes to the repository. They must not be invoked during a planning session.

A coding stage resource becomes accessible only after all of the following conditions are met: PLAN.md exists and has passed gsd-plan-checker verification, CONTEXT.md exists with recorded implementation decisions, and the HANDOFF.md transition protocol has been completed. See `.github/gsd-flat-directory/HANDOFF.md` for the transition protocol.

---

## When to use this stage

You are in the Coding stage when planning is complete and PLAN.md is verified. The execution agent reads the handoff package — PLAN.md, CONTEXT.md, RESEARCH.md, and any design contracts — and begins implementing according to the plan. All implementation is driven by PLAN.md task descriptions; the executor does not make design decisions that were not locked during planning.

---

## Skills in this stage

### gsd-execute-phase

`gsd-execute-phase` is the primary execution engine. It operates as a wave-based parallel orchestrator. The orchestrator uses approximately 15% of the available context budget to discover all plans in the phase, analyze their dependencies, group tasks into waves based on those dependencies, and spawn `gsd-executor` subagents. Each subagent gets a fresh 100% context window for its assigned plan, so complex implementation tasks do not compete with the orchestrator for context. The orchestrator waits for each wave to complete before spawning the next.

**Important flag behavior rule**: flags are active ONLY when their literal token appears in the arguments. None are implied or default-active. Running `gsd-execute-phase 3` with no flags always runs full standard execution.

```bash
/gsd-execute-phase 3
```

`--wave N` executes only wave N of the phase plan. Phase verification and completion only happen when no incomplete plans remain after the selected wave finishes. Use this for quota management (avoiding long-running sessions), for staged rollout (review Wave 1 database migrations before running Wave 2 application code), or when a previous wave was interrupted and needs to be re-run.

```bash
/gsd-execute-phase 3 --wave 1
/gsd-execute-phase 3 --wave 2
```

`--gaps-only` executes only plans that have `gap_closure: true` in their frontmatter. These are plans that `gsd-verify-work` created when it found implementation gaps after standard execution. Never use this flag for initial phase execution — it is exclusively for gap remediation.

```bash
/gsd-execute-phase 3 --gaps-only
```

`--interactive` executes plans sequentially in the main context with user checkpoints between each task. No subagents are spawned. This is pair-programming style execution: the developer can review and adjust each step before it is committed. Lower context efficiency but higher control. Best for small phases (under 5 tasks), bug fixes, and gap closures where you want to validate each fix before moving to the next.

```bash
/gsd-execute-phase 3 --interactive
```

Canonical path: `.github/skills/gsd-execute-phase/SKILL.md`

### gsd-fast

`gsd-fast` is the thin inline executor for trivial tasks — tasks that can be described in one sentence and completed in under two minutes. It does not spawn subagents, does not produce a PLAN.md, and does not create planning overhead. It is appropriate for typo fixes, configuration value changes, small refactors, forgotten commits, and simple one-file additions.

Do not use `gsd-fast` for anything that requires research, spans multiple files in a non-obvious way, or involves a decision that is not clearly implied by the existing codebase. For those tasks, use `gsd-quick` instead.

```bash
/gsd-fast rename `UserCard` to `MemberCard` across all files
/gsd-fast add `loading` prop to the `Button` component
/gsd-fast update the API base URL in `.env.example` to the new staging domain
```

Canonical path: `.github/skills/gsd-fast/SKILL.md`

### gsd-quick

`gsd-quick` handles ad-hoc tasks that need full GSD guarantees — atomic commits, STATE.md tracking, planning artifacts — but do not belong on the main ROADMAP.md. Quick tasks live in `.planning/quick/` and are not numbered phases. This makes `gsd-quick` appropriate for standalone bug fixes, small features requested mid-sprint, and technical debt items that are too small for a full phase.

The skill spawns `gsd-planner` in quick mode (a lighter version of the standard planner) and then `gsd-executor` agents. Unlike `gsd-fast`, it can handle multi-step work and research.

**Run modes:**

```bash
/gsd-quick fix the pagination bug on the course list
/gsd-quick --discuss add email verification to the signup flow
/gsd-quick --research implement Redis caching for the session store
/gsd-quick --validate add dark mode support to the dashboard
/gsd-quick --full implement the CSV export feature
```

`--discuss` runs a lightweight discussion before planning — surfaces assumptions, captures decisions in CONTEXT.md for this quick task. `--research` spawns a focused research agent before planning. `--validate` enables plan-checking (max 2 iterations) and post-execution verification. `--full` combines all of the above. Flags compose, so `--discuss --research --validate` is equivalent to `--full`.

**Management subcommands:**

```bash
/gsd-quick list
/gsd-quick status bug-pagination
/gsd-quick resume bug-pagination
```

`list` shows all quick tasks with their status (complete, incomplete, in-progress, or abandoned if older than 7 days with no summary). `status <slug>` shows the plan and summary for one task without spawning any agent. `resume <slug>` finds the task directory and delegates to the executor to continue where it left off.

Slug sanitization: only `[a-z0-9-]`, max 60 characters. Segments `..` and `/` are rejected.

Canonical path: `.github/skills/gsd-quick/SKILL.md`

### gsd-ultraplan-phase

`gsd-ultraplan-phase` is a BETA skill that offloads the plan-phase step to Claude Code's ultraplan cloud infrastructure. The plan is drafted in a remote cloud session while the local terminal stays free. You review and comment on the plan in the browser, and when satisfied, import it back into the local GSD project via `gsd-import --from`.

This skill is intended for situations where the plan is complex enough that you want to use Claude Code's ultraplan feature specifically — for example, when exploring deeply nested multi-service architectures or when you want a visually formatted, comment-annotated plan. It is not a replacement for `gsd-plan-phase` for standard work.

Requirements: Claude Code v2.1.91 or later, a claude.ai account, and a GitHub repository that the cloud session can read. This skill is marked BETA because the cloud session protocol is subject to change. Use `gsd-plan-phase` for all production planning.

```bash
/gsd-ultraplan-phase 3
```

Canonical path: `.github/skills/gsd-ultraplan-phase/SKILL.md`

---

## Agents in this stage

**gsd-executor** is spawned by `gsd-execute-phase` (one instance per plan, running in parallel waves) and by `gsd-quick`. Each executor instance receives a clean 100% context window and is responsible for implementing one plan file from end to end. It handles: reading its assigned PLAN.md tasks, executing them in order, writing atomic commits after each completed task, detecting deviations when implementation diverges from the plan, creating checkpoint files when a deviation requires user input, and writing a SUMMARY.md upon completion.

**gsd-code-fixer** is shared between the Coding stage and the Testing stage. In the Coding stage, it is spawned by `gsd-code-review --fix` (Stage 05) after a code review has been completed but the review results are then applied during what is technically still an execution phase. The fixer reads REVIEW.md findings, reads the relevant source files, applies intelligent fixes that respect the surrounding context, and commits each fix atomically with a message that references the original finding.
