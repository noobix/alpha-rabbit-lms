---
name: get shit done
aliases: [gsd, get-shit-done, get_it_done, gsd-autonomous]
short_description: High-level orchestration and autonomous execution skill for multi-step engineering tasks (plan → implement → test → verify → document).
---

Purpose
-------

`get shit done` (primary human-facing name preserved intentionally) is an orchestration skill that converts multi-step engineering intents into concrete, verifiable outputs. It is designed to be the canonical entry point for requests that require planning, sequencing, and optional autonomous execution across the repository (examples: implement a small feature end-to-end, address a set of review comments and open a PR, run an audit-and-fix wave).

When to call
------------

- Use when the user asks for multi-step work that spans planning, code changes, tests, documentation, or PR workflows.
- Example triggers (explicit): "get shit done", "gsd", "gsd-autonomous", "/gsd-apply", "run the phase", "execute the plan"
- Example structural cues (implicit): the user's request contains an ordered list of steps, mentions branch/PR/workflow actions, references `PLAN.md` or ROADMAP, or asks for both code and verification tasks.

When NOT to call
-----------------

- Avoid when the user asks for one-off, single-line clarifications, or design advice only.
- Avoid for privileged, destructive, or security-sensitive operations without explicit approvals (see Safety & Permissions).

Precedence and matching rules
-----------------------------

- Priority: GSD should have high matching priority for multi-step, sequenced-intent requests and for explicit alias mentions. It should outrank general-purpose planning skills for these cases but remain below highly-restricted, security-only skills.
- Matching heuristic (recommended): if message contains an explicit alias (`gsd`, `get shit done`) → strong match. Otherwise, compute a multi-step intent score: two or more sequenced actions OR explicit mention of branches/PRs/tests/documentation → match if score ≥ threshold.

Modes & Autonomy Levels
-----------------------

1. assist-only (default): produce a clear implementation plan, patch/diff suggestions, and commands to run locally. Do not perform remote repo operations.
2. semi-autonomous: create branches and PRs locally and push them to a draft PR, but do NOT merge. Requires explicit user approval before merging.
3. autonomous: allowed to create branches, push, create/merge PRs, and run permitted tooling. This mode MUST be gated by repo policy and explicit owner opt-in.

Default: `assist-only`. Use sanitized aliases for programmatic matching while keeping the literal name in human-facing docs.

Safety & Permissions
--------------------

- Never attempt destructive operations (force-push to protected branches, delete branches on remote, bypass CI) without explicit confirmation.
- Never exfiltrate secrets, credentials, or private tokens. If a requested operation requires secrets, surface the requirement to the user and stop.
- Require a documented opt-in from repository admins for `semi-autonomous` or `autonomous` runs; log all autonomous actions and create traceable artifacts (branches/PRs with prefixed metadata in titles).
- Always present a readable plan and ask for confirmation before performing remote actions. When in `assist-only` mode, include copy-paste-safe commands for the user to run.

Subskills and decomposition
---------------------------

GSD acts as an orchestrator that may invoke focused subskills. Existing subskill modules (examples in this repo) should be referenced when appropriate:

- `gsd-audit-fix` — audit and patch-fix flows
- `gsd-code-review` — apply review fixes
- `gsd-execute-phase` — run plan execution waves
- `gsd-new-project`, `gsd-plan-phase` — planning and research phases
- `gsd-ui-phase`, `gsd-ui-review` — UI-spec and visual audits
- `gsd-add-tests` — generate and add tests for a change

Each subskill remains authoritative for its domain; GSD composes them into higher-order flows.

Examples (prompts)
------------------

1. "gsd: implement feature X — create API, add tests, and open a draft PR against testing-main"
2. "Get shit done: address review comments in PR #42 and run unit tests" (assist-only by default)
3. "Run GSD autonomous audit-and-fix wave for the `auth` module" (requires explicit opt-in)

Suggested outputs
-----------------

- A concise plan with numbered steps
- A minimal patch/diff (or multiple patches) with file paths changed
- A list of exact shell commands to run locally (or that the agent will run in semi-autonomous/autonomous modes)
- A verification checklist (lint, tests, CI status)

Templates
---------

Prompt template (assist-only):

"gsd: assist-only — implement <short-description>. Provide a step-by-step plan, a patch/diff, tests to add, and commands to run locally."

Prompt template (semi-autonomous):

"gsd: semi-autonomous — implement <short-description>. Create a branch, push a draft PR titled '<prefix>: <short-description>', and include the patch and verification steps. Do not merge without my approval."

Verification & Discovery
------------------------

- Include a short discovery test in the repo to ensure `.agents/skills/gsd/SKILL.md` is discoverable. The detection logic should look for aliases and the multi-step heuristic described above.

Maintenance
-----------

- Keep this SKILL.md in sync with concrete subskill files under `.github/skills/gsd-*` and with `.github/copilot-instructions.md` precedence notes.

References
----------

- `.github/skills/gsd-audit-fix/SKILL.md` (and peers) — reuse examples and templates where appropriate.

Config & Opt-in
---------------

This repository supports a configurable opt-in model for MCP-driven branch/PR operations. Place a `.github/gsd-config.yaml` file in the repository root to declare allowed modes and administrative opt-ins. Example keys:

- `enable` (boolean): master switch to allow MCP-driven operations.
- `allowed_modes` (list): which modes are permitted (`assist-only`, `semi-autonomous`, `autonomous`).
- `branch_prefix`: prefix used for branches created by GSD.
- `require_admin_opt_in` (boolean): whether an explicit admin approval is required.

GSD agents should always check `.github/gsd-config.yaml` before attempting remote actions. If `require_admin_opt_in` is true, require a signed approval file or confirmation from an admin listed under `admin_approvals`.
