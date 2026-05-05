---
Author: Kelvin Kabute
Last-updated: 2026-05-05
---

# Stage 01 — Research

Canonical skill files: `.github/skills/gsd-{name}/SKILL.md`
Canonical agent files: `.github/agents/gsd-{name}.agent.md`

---

## When to use this stage

You are in the Research stage when you need to understand something before committing to an approach. This includes understanding the shape of an existing codebase before adding to it, understanding the domain well enough to scope requirements correctly, understanding how a chosen library or framework actually works before writing a SPEC, or understanding what prior planning documents have already decided before adding new phases. Research does not produce PLAN.md files or CONTEXT.md files — it produces the raw material that planning skills consume.

If you catch yourself writing a plan based on assumptions about the codebase, stop and run a research skill first. Assumptions about file structure, existing patterns, and library APIs are the most common source of plan deviations during execution.

---

## Skills in this stage

### gsd-explore

`gsd-explore` is an open-ended Socratic ideation session. It is the right starting point when the problem is not yet well-defined — when you have a direction but not a scope, or when multiple approaches seem possible and you want to think them through before committing. The skill accepts an optional topic argument, so you can be specific or broad:

```bash
/gsd-explore
/gsd-explore authentication strategy
/gsd-explore how to handle offline sync without a service worker
```

The skill guides the developer through probing questions, optionally spawns research to ground the discussion in real data, and then routes the outputs to the appropriate planning artifact — which might be a note, a todo, a seed for a future phase, a set of research questions, a new requirement, or a new phase entry in ROADMAP.md. It does not commit to any of these automatically; the user chooses where the ideation lands.

Canonical path: `.github/skills/gsd-explore/SKILL.md`

### gsd-map-codebase

`gsd-map-codebase` analyzes the existing codebase using parallel mapper agents and produces a set of structured documents in `.planning/codebase/`. It should be run on any non-trivial brownfield codebase before initialization, and re-run any time the codebase has changed significantly since the last map.

The skill operates in three distinct modes depending on the flags passed.

The default mode (no flag) spawns four parallel `gsd-codebase-mapper` agents, one per focus area, each writing its documents directly to `.planning/codebase/`. The orchestrator receives only confirmations, keeping its context usage minimal. The output is seven documents: STACK.md and INTEGRATIONS.md (from the tech-focus agent), ARCHITECTURE.md and STRUCTURE.md (from the arch-focus agent), CONVENTIONS.md and TESTING.md (from the quality-focus agent), and CONCERNS.md (from the concerns-focus agent).

```bash
/gsd-map-codebase
/gsd-map-codebase src/auth
```

The `--fast` mode spawns a single mapper agent instead of four. It accepts an optional `--focus` qualifier to narrow the analysis: `tech`, `arch`, `quality`, `concerns`, or `tech+arch` (the default when no focus is specified). Use fast mode when context budget is tight, when you only need one angle on the codebase, or when speed matters more than completeness.

```bash
/gsd-map-codebase --fast
/gsd-map-codebase --fast --focus arch
/gsd-map-codebase --fast --focus quality
```

The `--query` mode is a read-only intelligence layer that requires `intel.enabled: true` in `.planning/config.json`. It provides four subcommands: `query <term>` searches the codebase intel for a specific term and returns matching references; `status` shows the freshness of the intel index; `diff` shows what has changed since the last index build; and `refresh` spawns a mapper agent to rebuild the intel index. The first three subcommands run inline without spawning any agent — only `refresh` spawns an agent.

```bash
/gsd-map-codebase --query status
/gsd-map-codebase --query auth token
/gsd-map-codebase --query diff
/gsd-map-codebase --query refresh
```

Canonical path: `.github/skills/gsd-map-codebase/SKILL.md`

### gsd-graphify

`gsd-graphify` builds and queries a project knowledge graph stored in `.planning/graphs/`. The graph captures relationships between code entities (files, functions, modules, dependencies) and planning entities (phases, requirements, decisions) that are too complex to express in flat documents.

Before this skill can run at all, `graphify.enabled` must be set to `true` in `.planning/config.json`. The skill begins with a config gate check — it reads the config file directly using the Read tool and stops with an activation message if graphify is disabled. It must not use `gsd-sdk config get-value` for this check because that command exits hard on missing keys.

The skill supports four operations:

`build` triggers the graphify-builder agent, which invokes the `graphify update .` command in the project root, validates the output JSON, copies the graph artifacts to `.planning/graphs/`, and writes a diff snapshot for future comparisons. This is the only operation that spawns an agent.

```bash
/gsd-graphify build
```

`query <term>` runs an inline CLI call and returns matched graph nodes grouped by type, with edge relationships and confidence tiers (EXTRACTED, INFERRED, AMBIGUOUS). No agent is spawned.

```bash
/gsd-graphify query authentication
/gsd-graphify query UserService
```

`status` shows the last build time, node count, edge count, and hyperedge count, plus a STALE or FRESH indicator. Inline, no agent.

```bash
/gsd-graphify status
```

`diff` shows node and edge changes since the last build snapshot. If no snapshot exists yet, the skill suggests running build twice to create a baseline. Inline, no agent.

```bash
/gsd-graphify diff
```

Canonical path: `.github/skills/gsd-graphify/SKILL.md`

### gsd-ingest-docs

`gsd-ingest-docs` bootstraps or merges a `.planning/` setup from pre-existing planning documents in the repository — ADRs, PRDs, SPECs, DOCs, and RFCs — in a single pass. This is the right skill when a project has existing documentation that predates GSD and you want that documentation to become the foundation of the GSD planning system rather than starting over.

The skill operates in two modes. When `.planning/` does not yet exist, it defaults to `--mode new` and produces the full initial setup: PROJECT.md, REQUIREMENTS.md, ROADMAP.md, and STATE.md derived from the synthesized document content. When `.planning/` already exists, it defaults to `--mode merge` and appends phases and requirements derived from the ingested docs, hard-blocking any contradiction with existing locked decisions.

Document discovery follows directory conventions automatically: `docs/adr/`, `docs/prd/`, `docs/specs/`, `docs/rfc/`, and root-level files matching `{ADR,PRD,SPEC,RFC}-*.md`. You can override discovery entirely with an explicit manifest file listing each document with its path, type, and optional precedence override.

```bash
/gsd-ingest-docs
/gsd-ingest-docs --mode new
/gsd-ingest-docs --mode merge
/gsd-ingest-docs --manifest docs/ingest-manifest.yaml
/gsd-ingest-docs --mode merge --manifest docs/custom-list.yaml
```

The conflict resolution precedence is fixed: ADR beats SPEC beats PRD beats DOC. When two documents make contradictory statements about the same decision, the higher-precedence document wins and the resolution is logged in `.planning/INGEST-CONFLICTS.md` under the "auto-resolved" bucket. Competing variants that have equal precedence land in the "competing-variants" bucket. True blockers — contradictions that cannot be resolved automatically — land in the "unresolved-blockers" bucket and trigger the BLOCKER gate, which prevents any destination file from being written until the user resolves them. The hard cap is 50 documents per invocation.

Canonical path: `.github/skills/gsd-ingest-docs/SKILL.md`

### gsd-new-project

`gsd-new-project` initializes the GSD planning system for a brand-new project. It runs a unified flow: questioning → optional domain research → requirements → roadmap. The output is the complete initial `.planning/` directory: PROJECT.md, config.json, an optional `research/` subfolder, REQUIREMENTS.md, ROADMAP.md, and STATE.md.

```bash
/gsd-new-project
/gsd-new-project --auto
```

Without `--auto`, the skill asks configuration questions interactively and gives the user opportunities to review and adjust at each stage. With `--auto`, it expects an idea document provided via an `@` reference in the prompt, answers configuration questions itself using reasonable defaults, and runs the full research → requirements → roadmap sequence without further interaction.

After this skill completes, the next step is always `/gsd-plan-phase 1`.

Canonical path: `.github/skills/gsd-new-project/SKILL.md`

### gsd-new-milestone

`gsd-new-milestone` is the brownfield equivalent of `gsd-new-project`. The project already exists, PROJECT.md already has history, and you are starting a new development cycle. The skill gathers "what's next", updates PROJECT.md with the new milestone goals, and runs the requirements → roadmap cycle continuing the phase numbering from where the previous milestone left off.

```bash
/gsd-new-milestone
/gsd-new-milestone v1.1 Notifications
```

The milestone name is optional — the skill will prompt if not provided. Domain research is optional and scoped to truly new features; existing architecture decisions are carried forward from PROJECT.md without re-researching them.

Canonical path: `.github/skills/gsd-new-milestone/SKILL.md`

---

## Agents in this stage

Agents in the Research stage are spawned by the skills above, not directly by Copilot. Copilot does not invoke agents directly — it invokes the skill that orchestrates the agent. The descriptions below explain what each agent does so Copilot can understand what it is waiting for when a skill spawns one.

**gsd-phase-researcher** is spawned by `gsd-plan-phase` (specifically by the `--research-phase <N>` mode or by the default research step). It investigates how to implement a specific phase — exploring library options, API patterns, pitfalls, and implementation approaches — and writes a RESEARCH.md file in the phase directory. This agent is the primary source of implementation-ready technical guidance that feeds the planner.

**gsd-project-researcher** is spawned by `gsd-new-project` during its optional research step. It researches the domain ecosystem — competitor approaches, common architectural patterns for this type of product, relevant libraries, and emerging standards — before the roadmap is written. Its output goes into `.planning/research/`.

**gsd-domain-researcher** is spawned by `gsd-ai-integration-phase` (Stage 02). It researches the business domain and real-world application context specifically for AI systems — what domain expert evaluation criteria look like, what industry-specific failure modes exist, and what regulatory context applies. Its findings feed the evaluation strategy in AI-SPEC.md.

**gsd-ai-researcher** is spawned by `gsd-ai-integration-phase` (Stage 02). It researches the chosen AI framework's official documentation and produces implementation-ready guidance — best practices, syntax, core patterns, and pitfalls distilled for the specific use case.

**gsd-advisor-researcher** is spawned by `gsd-discuss-phase` when advisor mode is active. It researches a single gray area decision — for example, whether to use optimistic UI updates or server-confirmed updates for a specific interaction — and returns a structured comparison with evidence and a recommended option.

**gsd-research-synthesizer** is spawned by `gsd-new-project` after parallel researcher agents have written their documents. It synthesizes the outputs from multiple researcher agents into a single coherent SUMMARY.md that the roadmapper can consume without reading every individual research file.

**gsd-pattern-mapper** is spawned by `gsd-plan-phase` before planning begins. It analyzes the codebase for existing patterns and produces a PATTERNS.md that maps new files the plan will create to their closest analogs in the existing codebase. This prevents the planner from inventing new patterns when existing ones already solve the problem.

**gsd-codebase-mapper** is spawned by `gsd-map-codebase` in groups of up to four parallel agents. Each instance is assigned a focus area (tech, arch, quality, or concerns) and writes its assigned documents directly to `.planning/codebase/` without returning large amounts of content to the orchestrator.

**gsd-doc-classifier** is spawned by `gsd-ingest-docs` in parallel groups for each discovered document. Each instance classifies a single document as ADR, PRD, SPEC, DOC, or UNKNOWN, extracts its title and scope summary, and identifies cross-references to other documents.

**gsd-doc-synthesizer** is spawned by `gsd-ingest-docs` after all classifiers have run. It synthesizes the classified documents into a single consolidated context, applies the precedence rules, detects cross-reference cycles, enforces the LOCKED-vs-LOCKED conflict constraint, and writes INGEST-CONFLICTS.md.

**gsd-doc-verifier** is spawned by `gsd-docs-update` (Stage 06) but is documented here because its input is research artifacts. It verifies factual claims in generated documentation against the live codebase — checking that referenced file paths exist, that described APIs match the actual implementation, and that version numbers are current.

**gsd-intel-updater** is spawned by `gsd-map-codebase --query refresh`. It analyzes the codebase and writes structured intel files to `.planning/intel/` that the `--query` subcommand reads.
