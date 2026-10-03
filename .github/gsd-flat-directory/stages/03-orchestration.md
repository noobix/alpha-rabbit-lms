---
Author: Kelvin Kabute
Last-updated: 2026-05-05
---

# Stage 03 — Orchestration

Canonical skill files: `.github/skills/gsd-{name}/SKILL.md`
Canonical agent files: `.github/agents/gsd-{name}.agent.md`

---

## When to use this stage

The Orchestration stage does not belong to any single moment in the lifecycle — it runs throughout. It is the control layer that keeps the project moving forward, surfaces what has been done and what comes next, manages parallel tracks, handles interruptions and context switches, and provides the configuration and health-check tools that other GSD skills depend on.

During a planning session specifically, Copilot uses orchestration skills to check project state before beginning, route between planning steps, configure feature gates that are required before a planning skill can run, import external artifacts, and manage workstreams when multiple phases are planned in parallel. Orchestration skills never write production code.

---

## Skills in this stage

### gsd-progress

`gsd-progress` is the first skill to run at the start of any GSD session. It reads STATE.md, ROADMAP.md, and phase directories, then presents a concise summary of where the project is — which phase is active, which plans are in progress, which have completed, and what blocking issues are known. It then presents Routes A through F (route names are stable across projects) for the next logical action.

The skill has four modes:

Default mode (no flag) produces the progress report and route list. The user chooses a route and the skill hands off to the selected next action.

```bash
/gsd-progress
```

`--next` automatically advances to the next logical step without presenting routes for user selection. It scans all prior phases for incomplete work before routing, so it will catch overlooked gaps rather than blindly proceeding to the next phase number. The `--force` modifier bypasses safety gates when you know it is safe to skip ahead.

```bash
/gsd-progress --next
/gsd-progress --next --force
```

`--do "task description"` is a smart dispatcher. It matches freeform natural language to the best available GSD command using routing rules, confirms the match with the user, and hands off. It never does the work itself — it only routes. This is useful when you know what you want to do but are not sure which GSD command to invoke.

```bash
/gsd-progress --do "I want to check whether my plan covers all the requirements"
/gsd-progress --do "start phase 4 planning"
```

`--forensic` appends a six-check integrity audit to the standard progress report. It looks for: stuck loops (the same phase has been in-progress for an unusually long time), missing artifacts (phases with completed status but no SUMMARY.md), abandoned work (plans committed but never verified), and crash/interruption indicators in git history.

```bash
/gsd-progress --forensic
```

Canonical path: `.github/skills/gsd-progress/SKILL.md`

### gsd-phase

`gsd-phase` is the CRUD interface for phases in ROADMAP.md. It handles structural changes to the milestone plan — adding new phases, inserting urgent work between existing phases, removing phases that are no longer needed, and editing the metadata of any existing phase.

Adding a new phase appends it at the end of the current milestone's phase list with an integer phase number. This is the default mode.

```bash
/gsd-phase add "Implement notification system" --goal "Users receive real-time notifications for course events"
```

`--insert` creates a decimal phase (e.g. 4.1) between two existing phases. Use this when urgent work needs to be done before the next planned phase but you do not want to renumber the entire roadmap.

```bash
/gsd-phase --insert 4.1 "Hotfix authentication regression"
```

`--remove` removes a future phase that is no longer needed and renumbers subsequent phases to close the gap.

```bash
/gsd-phase --remove 7
```

`--edit` edits any field of an existing phase in place — goal, description, mode, dependencies, or success criteria.

```bash
/gsd-phase --edit 4 --goal "Updated goal statement"
```

Canonical path: `.github/skills/gsd-phase/SKILL.md`

### gsd-review

`gsd-review` invokes external AI CLIs to independently peer-review phase plans. It produces a REVIEWS.md file containing the findings from each reviewer, which `gsd-plan-phase --reviews` then incorporates into a revised plan. This is the GSD mechanism for cross-AI plan review — using a different model's perspective to catch blind spots in the planner's output.

The skill requires a phase number and at least one reviewer flag. Reviewers are invoked as separate subprocess sessions to ensure they see only the plan, not the GSD session context.

```bash
/gsd-review 3 --gemini
/gsd-review 3 --claude
/gsd-review 3 --codex
/gsd-review 3 --opencode
/gsd-review 3 --qwen
/gsd-review 3 --cursor
/gsd-review 3 --all
```

Canonical path: `.github/skills/gsd-review/SKILL.md`

### gsd-plan-review-convergence

`gsd-plan-review-convergence` wraps `gsd-review` and `gsd-plan-phase` in an outer convergence loop. It reviews the plan, checks for HIGH-severity concerns, replans to address them, re-reviews, and repeats until no HIGH concerns remain or the maximum cycle count is reached. This gives a stronger plan quality guarantee than running `gsd-review` and `gsd-plan-phase --reviews` manually — the loop enforces that all HIGH concerns are actually resolved, not just acknowledged.

This skill requires the feature gate `workflow.plan_review_convergence=true` to be set before running. Enable it with:

```bash
/gsd-config set workflow.plan_review_convergence true
```

Then invoke it:

```bash
/gsd-plan-review-convergence 3
/gsd-plan-review-convergence 3 --codex
/gsd-plan-review-convergence 3 --gemini
/gsd-plan-review-convergence 3 --all
/gsd-plan-review-convergence 3 --ollama
/gsd-plan-review-convergence 3 --lm-studio
/gsd-plan-review-convergence 3 --llama-cpp
/gsd-plan-review-convergence 3 --max-cycles 5
```

The default reviewer is `--codex` when no reviewer is specified. Local model flags require a locally running server — `--ollama` defaults to `http://localhost:11434`, `--lm-studio` to `http://localhost:1234`, `--llama-cpp` to `http://localhost:8080`. The `--max-cycles` flag defaults to 3.

Canonical path: `.github/skills/gsd-plan-review-convergence/SKILL.md`

### gsd-review-backlog

`gsd-review-backlog` lists all backlog phases (phases numbered in the 999.x range) with their accumulated context — CONTEXT.md, RESEARCH.md if run, creation date, and description. For each item the user can choose to Promote (move to the active milestone), Keep (leave in backlog), or Remove (delete). Promoted items are renumbered to the next available active phase number and their ROADMAP.md entry is moved from the Backlog section to the active phases list with a Depends-on field.

```bash
/gsd-review-backlog
```

Canonical path: `.github/skills/gsd-review-backlog/SKILL.md`

### gsd-workstreams

`gsd-workstreams` manages parallel workstreams for concurrent milestone work. Each workstream is an independent planning and execution track with its own set of phases. Use this skill when multiple parallel features need to be planned and developed simultaneously without interfering with each other's STATE.md and phase numbering.

The default subcommand when none is given is `list`.

```bash
/gsd-workstreams list
/gsd-workstreams create notifications
/gsd-workstreams status notifications
/gsd-workstreams switch auth-redesign
/gsd-workstreams progress
/gsd-workstreams complete notifications
/gsd-workstreams resume auth-redesign
```

`create <name>` creates a new workstream and suggests the next command to run, which is `/gsd-new-milestone --ws <name>` to initialize the workstream's planning directory. `switch <name>` sets the active workstream for the current session and sets `GSD_WORKSTREAM` so subsequent commands operate in that workstream's context. `complete <name>` archives the workstream to `milestones/`.

Canonical path: `.github/skills/gsd-workstreams/SKILL.md`

### gsd-manager

`gsd-manager` is a single-terminal dashboard for running all phases of a milestone from one session. Discuss commands run inline in the main context. Plan and execute commands are dispatched as background Task agents. This allows you to discuss one phase while another is being planned or executed in the background. The manager reads STATE.md and ROADMAP.md and presents an interactive interface for selecting which phase to work on and which step to advance.

```bash
/gsd-manager
```

Canonical path: `.github/skills/gsd-manager/SKILL.md`

### gsd-autonomous

`gsd-autonomous` runs all remaining milestone phases end-to-end without user intervention between phases. For each phase it runs discuss → plan → execute in sequence, then proceeds to the next phase automatically. It pauses only when a user decision is genuinely required: a gray area that cannot be resolved from existing context, a verification failure that needs human judgment, or a blocker that cannot be recovered programmatically. After all phases complete, it runs the milestone audit, completes the milestone, and runs cleanup.

```bash
/gsd-autonomous
/gsd-autonomous --from 3
/gsd-autonomous --to 5
/gsd-autonomous --only 4
/gsd-autonomous --interactive
```

`--from N` starts from phase N instead of the first incomplete phase. `--to N` stops after phase N rather than running all phases. `--only N` runs only phase N. `--interactive` changes the execution style: discuss runs inline with real user input rather than auto-resolving, and plan and execute dispatch as background agents. This keeps the main conversation context lean while still allowing the developer to participate in key decisions.

Canonical path: `.github/skills/gsd-autonomous/SKILL.md`

### gsd-import

`gsd-import` brings an external plan file — produced by Claude Code's ultraplan feature, another GSD instance, or any structured planning document — into the current GSD project. The skill runs a conflict detection pass against PROJECT.md decisions before writing anything. If the imported plan contradicts existing locked decisions, those conflicts are surfaced and the user resolves them before the plan is written as a GSD PLAN.md and validated by gsd-plan-checker.

```bash
/gsd-import --from exported-plan.md
/gsd-import --from .planning/phases/3-auth/ultraplan-output.md
```

Canonical path: `.github/skills/gsd-import/SKILL.md`

### gsd-thread

`gsd-thread` creates and manages persistent context threads for cross-session work that spans multiple conversations but does not belong to any specific phase. A thread is a named document in `.planning/threads/{slug}.md` that records a goal, in-progress state, decisions, and next steps. Use threads for ongoing explorations, recurring review cycles, or investigations that stay open across many sessions.

```bash
/gsd-thread create investigate websocket vs sse for live updates
/gsd-thread list
/gsd-thread list --open
/gsd-thread list --resolved
/gsd-thread resume investigate-websocket-vs-sse
/gsd-thread status investigate-websocket-vs-sse
/gsd-thread close investigate-websocket-vs-sse
```

Slug sanitization: only `[a-z0-9-]`, max 60 characters. Segments `..` and `/` are rejected.

Canonical path: `.github/skills/gsd-thread/SKILL.md`

### gsd-pause-work

`gsd-pause-work` creates a context handoff document when you need to stop mid-phase and resume later (in a different session, on a different machine, or after a long break). It records the current state — what was just completed, what is in progress, what was about to start, and any open decisions — in a PAUSE.md file that the next session loads via `gsd-resume-work`.

```bash
/gsd-pause-work
```

Canonical path: `.github/skills/gsd-pause-work/SKILL.md`

### gsd-workspace

`gsd-workspace` manages GSD workspaces — isolated planning environments within the same repository. Each workspace has its own `.planning/` directory scoped to a different product area, team, or experiment. This is different from workstreams (parallel tracks within a single milestone) — workspaces are fully isolated planning contexts.

```bash
/gsd-workspace list
/gsd-workspace create backend-team
/gsd-workspace remove experiment-2024
```

Canonical path: `.github/skills/gsd-workspace/SKILL.md`

### gsd-health

`gsd-health` diagnoses the `.planning/` directory for structural problems that would cause other GSD commands to fail or behave incorrectly. It checks: config.json validity, STATE.md consistency with ROADMAP.md phase numbers, the presence of expected artifacts for phases that are in a given status, and orphaned directories that no longer correspond to ROADMAP.md entries.

```bash
/gsd-health
/gsd-health --repair
```

The `--repair` flag automatically fixes safe issues (updating STATE.md fields that are stale, removing orphaned lock files). It prompts before performing any repair that could change planning state.

Canonical path: `.github/skills/gsd-health/SKILL.md`

### gsd-config

`gsd-config` is the full configuration interface for GSD. It reads and writes `.planning/config.json` and surfaces all available settings with descriptions. Use it when you need to enable a feature gate, adjust a workflow toggle, change the model profile, or configure an integration.

```bash
/gsd-config
/gsd-config set workflow.plan_review_convergence true
/gsd-config set graphify.enabled true
/gsd-config set intel.enabled true
/gsd-config get workflow.discuss_mode
```

Canonical path: `.github/skills/gsd-config/SKILL.md`

### gsd-settings

`gsd-settings` is a lighter-weight alias of `gsd-config` for the most commonly adjusted settings — workflow toggles and model profile. Use it for everyday configuration changes. Use `gsd-config` for deep configuration or when you need to see all available options.

```bash
/gsd-settings
```

Canonical path: `.github/skills/gsd-settings/SKILL.md`

### gsd-stats

`gsd-stats` displays read-only project statistics: phase count, plan count, requirement coverage, git activity metrics, and milestone timeline. It does not change any state. Use it for progress reporting or to get a quick sense of project health before a planning session.

```bash
/gsd-stats
```

Canonical path: `.github/skills/gsd-stats/SKILL.md`

### gsd-update

`gsd-update` updates GSD to the latest version. It fetches the changelog, presents the differences, and prompts before making any changes. Use it when a skill is behaving unexpectedly and you suspect it may be running on a stale version of the workflow.

```bash
/gsd-update
```

Canonical path: `.github/skills/gsd-update/SKILL.md`

### gsd-help

`gsd-help` displays all available GSD commands and a compact usage guide. It is the quickest way to discover what commands exist when you are not sure which skill to use. Read-only, no state changes.

```bash
/gsd-help
```

Canonical path: `.github/skills/gsd-help/SKILL.md`

---

## Agents in this stage

The Orchestration stage does not spawn research or planning agents — it delegates to skills and inline operations. The orchestration skills that spawn any agent do so only as part of a specific flow that is documented within the skill (for example, `gsd-autonomous` spawns discuss, plan, and execute skills which in turn spawn their own agents). There are no standalone orchestration agents that Copilot would interact with directly.
