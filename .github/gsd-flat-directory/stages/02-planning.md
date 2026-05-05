---
Author: Kelvin Kabute
Last-updated: 2026-05-05
---

# Stage 02 — Planning

Canonical skill files: `.github/skills/gsd-{name}/SKILL.md`
Canonical agent files: `.github/agents/gsd-{name}.agent.md`

---

## When to use this stage

You are in the Planning stage when you have enough research to start locking decisions and producing executable plans. Planning is not about generating ideas — that is Stage 01. Planning is about converting ambiguity into structure. When you leave this stage you should have a PLAN.md that a coding agent can execute without coming back to ask questions.

The ordering within this stage matters. The designed sequence is: spec-phase to lock WHAT is being built, discuss-phase to resolve HOW it will be built, plan-phase to produce the executable PLAN.md, and then optional design contracts (UI-SPEC or AI-SPEC) if the phase requires them. You do not have to run every skill for every phase — if a phase is simple and unambiguous, you might go straight to plan-phase. But you should never skip spec-phase and discuss-phase for phases where the scope is genuinely unclear, because the planner will make assumptions that cause deviations during execution.

---

## Skills in this stage

### gsd-spec-phase

`gsd-spec-phase` clarifies WHAT a phase delivers before any discussion of HOW. It uses a structured Socratic interview loop, running up to six rounds of questions that rotate through different analytical perspectives. After each round it scores ambiguity across four weighted dimensions. The skill does not exit until the ambiguity score is at or below 0.20 across all four dimensions and all dimensional minimums are met. The output is a SPEC.md file that `gsd-discuss-phase` picks up automatically on its next run.

The SPEC.md locks the "what and why" — the deliverables, the acceptance criteria, the scope boundaries, and what is explicitly out of scope. It does not contain implementation decisions. Those come from discuss-phase.

```bash
/gsd-spec-phase 3
/gsd-spec-phase 3 --auto
/gsd-spec-phase 3 --text
```

`--auto` instructs the agent to select recommended defaults for all questions without waiting for user input. This is useful when the phase description in ROADMAP.md is detailed enough that the spec questions have obvious answers, or when you want to generate a draft spec quickly and then edit it manually. `--text` switches from TUI-style interactive menus to plain numbered lists, which is required when running the skill through remote sessions or terminals that do not support interactive TUI elements.

Canonical path: `.github/skills/gsd-spec-phase/SKILL.md`

### gsd-discuss-phase

`gsd-discuss-phase` extracts the implementation decisions that the planner and executor need to work without ambiguity. It does not re-ask questions that prior phases or prior sessions have already answered — it loads PROJECT.md, REQUIREMENTS.md, STATE.md, and any prior CONTEXT.md files first, scouts the codebase for reusable assets and existing patterns, and then identifies only the remaining gray areas. The user selects which gray areas to discuss, and the skill deep-dives each selected area. The output is a CONTEXT.md file containing the decisions that guide downstream agents.

The skill operates in two workflow modes controlled by the `workflow.discuss_mode` configuration value. The default mode is `"discuss"`, which runs an interactive multi-round conversation to resolve gray areas. When set to `"assumptions"`, the skill runs a codebase analysis mode that surfaces hidden assumptions in the plan rather than conducting a discussion — this is useful when you want to validate that you have not missed important considerations before writing the plan.

```bash
/gsd-discuss-phase 3
/gsd-discuss-phase 3 --auto
/gsd-discuss-phase 3 --chain
/gsd-discuss-phase 3 --batch
/gsd-discuss-phase 3 --analyze
/gsd-discuss-phase 3 --text
/gsd-discuss-phase 3 --power
```

`--auto` answers all questions with the agent's recommended defaults, useful for phases where the correct decisions are already implied by the project context. `--chain` connects discuss-phase output directly to plan-phase in a single session without a manual handoff step. `--batch` processes multiple phases in sequence. `--analyze` triggers the assumptions analyzer mode, surfacing hidden assumptions in the codebase relevant to this phase. `--text` switches to plain-text output for remote sessions. `--power` activates extended questioning depth — more perspectives, more follow-up rounds — for phases where the implementation decisions are particularly consequential.

Canonical path: `.github/skills/gsd-discuss-phase/SKILL.md`

### gsd-plan-phase

`gsd-plan-phase` is the central skill of the Planning stage. It orchestrates a research → plan → verify loop and produces one or more PLAN.md files that the execution agent uses to implement the phase.

The default flow is: check whether RESEARCH.md exists (prompt to update, view, or skip if it does), spawn `gsd-phase-researcher` if research is needed, spawn `gsd-planner` to produce PLAN.md, run `gsd-plan-checker` in an iteration loop to verify the plan achieves its goal, and present the verified plan to the user. The skill iterates the plan→verify loop until gsd-plan-checker passes or max iterations are reached.

**Research controls:**

`--research-phase <N>` runs only the research step for phase N and exits before the planner runs. This is useful for preparing research in advance, for reviewing research before committing to planning, or for updating research without replanning.

`--research` forces research to re-run even if RESEARCH.md already exists, without prompting.

`--view` prints the existing RESEARCH.md to stdout without spawning any agent. This is the cheapest way to check what research already says before deciding whether to update it.

`--skip-research` skips the research step entirely and goes directly to planning. Use when you are confident the plan can be written from CONTEXT.md alone.

**Plan controls:**

`--gaps` activates gap closure mode. Instead of producing a new plan, the skill reads an existing VERIFICATION.md (produced when a prior execution attempt partially failed) and creates targeted gap-closure plans for the specific items that failed. This is never used for initial planning.

`--skip-verify` skips the gsd-plan-checker verification loop. Useful when you have very high confidence in the plan and want to save the verification iteration cost.

`--prd <file>` uses a PRD or acceptance criteria file as the source of truth instead of running discuss-phase. The skill parses the PRD into CONTEXT.md automatically and then proceeds to planning. This is useful when requirements are provided externally in a document format.

`--reviews` replans incorporating cross-AI review feedback from a REVIEWS.md file produced by `gsd-review`. The planner reads the HIGH-severity concerns from all reviewers and adjusts the plan to address them.

`--text` switches to plain-text menus for remote sessions.

`--mvp` activates vertical MVP mode. The planner organizes tasks as feature slices (UI → API → DB) rather than horizontal layers (all DB migrations, then all API, then all UI). On Phase 1 of a new project, MVP mode also emits a SKELETON.md Walking Skeleton document. MVP mode can be persisted on a phase by adding `**Mode:** mvp` to the phase entry in ROADMAP.md.

```bash
/gsd-plan-phase 3
/gsd-plan-phase 3 --research
/gsd-plan-phase 3 --research-phase 3
/gsd-plan-phase 3 --view
/gsd-plan-phase 3 --skip-research
/gsd-plan-phase 3 --mvp
/gsd-plan-phase 3 --prd docs/phase3-requirements.md
/gsd-plan-phase 3 --reviews
/gsd-plan-phase 3 --skip-research --skip-verify
/gsd-plan-phase 3 --text
```

Canonical path: `.github/skills/gsd-plan-phase/SKILL.md`

### gsd-ui-phase

`gsd-ui-phase` generates a UI-SPEC.md design contract for frontend phases. A UI-SPEC.md is the equivalent of a CONTEXT.md for visual and interaction decisions — it captures component structure, design tokens, interaction patterns, accessibility requirements, responsive behavior, and motion/animation intent in enough detail that an executor can produce consistent UI without making visual judgment calls during implementation.

The skill spawns `gsd-ui-researcher` to produce the initial design contract, then validates it using `gsd-ui-checker` against six quality dimensions. If the checker returns a BLOCK verdict the contract is revised before being accepted. A FLAG verdict is presented to the user for a judgment call. Only a PASS verdict results in a committed UI-SPEC.md.

```bash
/gsd-ui-phase 3
```

Canonical path: `.github/skills/gsd-ui-phase/SKILL.md`

### gsd-ai-integration-phase

`gsd-ai-integration-phase` generates an AI-SPEC.md design contract for phases that involve building AI systems — LLM integrations, RAG pipelines, classification models, evaluation harnesses, or any component where AI model behavior is a first-class concern. The AI-SPEC.md goes beyond what a regular CONTEXT.md captures: it includes framework selection rationale, implementation guidance from official documentation, an evaluation strategy with measurable rubrics, guardrails for production behavior, and production monitoring guidance.

The skill orchestrates several research agents: `gsd-domain-researcher` researches the business domain and real-world application context, `gsd-framework-selector` runs a decision matrix to select the appropriate AI/LLM framework, `gsd-ai-researcher` researches the chosen framework's documentation, and `gsd-eval-planner` designs the evaluation strategy.

```bash
/gsd-ai-integration-phase 3
```

Canonical path: `.github/skills/gsd-ai-integration-phase/SKILL.md`

### gsd-sketch

`gsd-sketch` creates throwaway HTML mockups for UI and design ideas. It is the right tool when you want to visualize a layout, interaction, or component before locking it in a UI-SPEC.md. Sketches are intentionally disposable — the goal is speed of iteration, not production quality.

The skill accepts a description of what to sketch and optionally uses WebSearch and WebFetch to pull in reference examples or design inspiration from the web. `--auto` skips interactive questions and generates a sketch directly from the description.

```bash
/gsd-sketch the course card component with progress bar
/gsd-sketch --auto the admin dashboard sidebar navigation
```

Canonical path: `.github/skills/gsd-sketch/SKILL.md`

### gsd-spike

`gsd-spike` is experiential exploration of a technical idea. Where `gsd-explore` is Socratic (question-driven), a spike is experimental (try-it-and-see). Use it when you want to actually attempt a small implementation or integration to validate an approach before committing to it in a plan. The spike output — findings, code fragments, pitfalls discovered — is routed back to the appropriate GSD artifact (usually a RESEARCH.md or a CONTEXT.md decision).

Like gsd-sketch, it supports WebSearch and WebFetch for pulling in documentation and examples during the spike.

```bash
/gsd-spike how to stream LLM responses into a React component
/gsd-spike rate limiting with Redis sliding window
```

Canonical path: `.github/skills/gsd-spike/SKILL.md`

### gsd-capture

`gsd-capture` captures ideas, tasks, notes, and seeds to their destination without requiring a full planning session. When a thought occurs during a conversation that does not fit the current phase or session, `gsd-capture` routes it to the right place — a backlog item, a thread, a todo, a seed for a future phase, or a requirement — without interrupting the current work.

```bash
/gsd-capture we should add rate limiting to the auth endpoints before v1
/gsd-capture idea: use a virtual list for the course table to handle 10k+ rows
```

Canonical path: `.github/skills/gsd-capture/SKILL.md`

---

## Agents in this stage

**gsd-planner** is spawned by `gsd-plan-phase`. It creates the executable PLAN.md with a task breakdown, dependency graph, threat model, and wave structure. When spawned by `gsd-quick` it operates in quick mode, producing a lighter plan appropriate for ad-hoc tasks.

**gsd-plan-checker** is spawned by `gsd-plan-phase` after the planner writes PLAN.md. It performs a goal-backward analysis — starting from the phase goal and working backward to verify that the plan's tasks will actually achieve it. It returns a pass/fail verdict with specific concerns, and the plan-phase skill iterates the plan until all blocking concerns are resolved or max iterations are reached.

**gsd-roadmapper** is spawned by `gsd-new-project` and `gsd-new-milestone`. It creates the project ROADMAP.md with phase breakdown, requirement-to-phase mapping, success criteria derivation, and coverage validation ensuring that every requirement is addressed by at least one phase.

**gsd-assumptions-analyzer** is spawned by `gsd-discuss-phase` in assumptions mode. It deeply analyzes the codebase for a specific phase and returns structured hidden assumptions with evidence — for example, "Phase 3 assumes that `User.preferences` is always a non-null object, but 47 records in the fixture data have null preferences." Each assumption is classified by risk level and comes with a suggested mitigation.

**gsd-ui-researcher** is spawned by `gsd-ui-phase`. It reads the project's existing design system (if any), the phase requirements, and the CONTEXT.md, then produces the initial UI-SPEC.md design contract structured across six quality pillars: layout and hierarchy, typography and spacing, color and contrast, interaction and motion, accessibility, and responsive behavior.

**gsd-ui-checker** is spawned by `gsd-ui-phase` immediately after `gsd-ui-researcher` completes. It validates the UI-SPEC.md against the same six pillars and returns a BLOCK, FLAG, or PASS verdict per pillar. BLOCK means the contract has a quality issue that will produce unacceptable UI — the contract must be revised before proceeding. FLAG means there is a concern the user should review. PASS means the pillar is acceptable.

**gsd-framework-selector** is spawned by `gsd-ai-integration-phase`. It presents an interactive decision matrix that surfaces the right AI/LLM framework for the user's specific use case — comparing options on dimensions like latency, cost, ecosystem maturity, evaluation tooling, and fit with the existing stack — and returns a scored recommendation with rationale.

**gsd-eval-planner** is spawned by `gsd-ai-integration-phase`. It designs a structured evaluation strategy for an AI phase: identifying critical failure modes, selecting evaluation dimensions with measurable rubrics, recommending evaluation tooling, and specifying a reference dataset for evaluation runs.
