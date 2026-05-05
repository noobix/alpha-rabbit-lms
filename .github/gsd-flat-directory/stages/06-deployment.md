---
Author: Kelvin Kabute
Last-updated: 2026-05-05
---

# Stage 06 — Deployment

Canonical skill files: `.github/skills/gsd-{name}/SKILL.md`
Canonical agent files: `.github/agents/gsd-{name}.agent.md`

---

## ACCESS RESTRICTION — PLANNING CONTEXT

This stage is blocked during the Copilot planning context. Skills and agents in this stage manage release operations, pull requests, documentation, and milestone archiving. They must not be invoked during a planning session.

A deployment stage resource becomes accessible only after testing has passed and the phase is ready to ship. For most phases, the prerequisite is a passing `gsd-verify-work` session (producing a UAT.md with no unresolved failures) or a passing `gsd-audit-milestone` run (for milestone-level operations).

---

## When to use this stage

You are in the Deployment stage when code has passed verification and is ready to be shipped — committed, pushed, reviewed via PR, documented, and archived. This stage also handles cleanup after milestone completion, extraction of learnings for future milestones, and lifecycle management of GitHub issues and PRs.

---

## Skills in this stage

### gsd-ship

`gsd-ship` closes the plan → execute → verify → ship loop. After `gsd-verify-work` produces a passing UAT record, `gsd-ship` pushes the branch, creates a PR with an auto-generated body drawn from the phase SUMMARY.md and CONTEXT.md, optionally triggers `gsd-review` for PR-level review, and then tracks the merge. The PR body includes: what changed (from SUMMARY.md), why it changed (from the phase goal in ROADMAP.md), how to test it (from UAT.md), and any known deferred items or tech debt.

```bash
/gsd-ship 3
/gsd-ship v1.0
```

Canonical path: `.github/skills/gsd-ship/SKILL.md`

### gsd-pr-branch

`gsd-pr-branch` creates a clean PR branch by filtering out all `.planning/` commits from the current branch. GSD commits planning artifacts (PLAN.md, CONTEXT.md, SUMMARY.md, STATE.md updates) as part of its normal workflow — these commits are valuable for project history but should not appear in PR diffs where code reviewers are trying to understand what changed in the codebase. `gsd-pr-branch` produces a new branch that contains only the code commits, which is then what gets pushed and reviewed.

```bash
/gsd-pr-branch
/gsd-pr-branch main
/gsd-pr-branch staging
```

The target branch argument defaults to `main` if omitted.

Canonical path: `.github/skills/gsd-pr-branch/SKILL.md`

### gsd-complete-milestone

`gsd-complete-milestone` archives a completed milestone. It reads the current milestone's ROADMAP.md and REQUIREMENTS.md, archives them to `milestones/{version}/`, evolves PROJECT.md to reflect that this milestone is complete and note what was delivered, and creates a git tag for the milestone version. The version argument is required.

```bash
/gsd-complete-milestone v1.0
/gsd-complete-milestone v1.1-notifications
```

The typical workflow is: `gsd-audit-milestone` → `gsd-complete-milestone` → `gsd-cleanup` → `gsd-new-milestone` for the next version.

Canonical path: `.github/skills/gsd-complete-milestone/SKILL.md`

### gsd-cleanup

`gsd-cleanup` archives the accumulated phase directories from completed milestones. Phase directories in `.planning/phases/` can accumulate over the course of a milestone and become noise once the milestone is archived. This skill moves them to `milestones/{version}/phases/` so the `.planning/phases/` directory only contains work in progress.

The skill always confirms before deleting or moving anything. It will not touch phase directories that appear to contain in-progress work.

```bash
/gsd-cleanup
```

Canonical path: `.github/skills/gsd-cleanup/SKILL.md`

### gsd-milestone-summary

`gsd-milestone-summary` generates a comprehensive project summary from all milestone artifacts — SUMMARY.md files, VERIFICATION.md files, CONTEXT.md files, and REQUIREMENTS.md — synthesized into a single document suitable for team onboarding or stakeholder review. The summary covers: what was built, why each phase was prioritized, what decisions were made and why, what was deferred, and what the project's current architecture looks like.

```bash
/gsd-milestone-summary
/gsd-milestone-summary v1.0
```

Canonical path: `.github/skills/gsd-milestone-summary/SKILL.md`

### gsd-docs-update

`gsd-docs-update` generates or updates up to nine documentation files for the project. Each documentation file is written by a `gsd-doc-writer` subagent that explores the codebase directly before writing — it reads the actual source files, checks actual file paths, and verifies actual API signatures rather than relying on planning artifacts that may be stale. This prevents the common documentation failure mode of phantom endpoints, wrong function signatures, and stale version numbers.

The supported documentation types include: README, API reference, architecture overview, development setup guide, deployment guide, contribution guide, changelog, and component library reference. You specify which documents to generate and whether to create them fresh or update existing ones.

```bash
/gsd-docs-update
/gsd-docs-update --type readme
/gsd-docs-update --type api,architecture
/gsd-docs-update --mode update --type changelog
```

Canonical path: `.github/skills/gsd-docs-update/SKILL.md`

### gsd-extract-learnings

`gsd-extract-learnings` extracts decisions, lessons, patterns, and surprises from completed phase artifacts and writes a structured learnings document. Learnings from one milestone inform better planning for the next — they capture things like "the Phase 3 approach to pagination worked well and should be reused", "the Redis caching layer added significant complexity for minimal performance gain and should be reconsidered before v2", or "the UI-SPEC.md for Phase 5 was too vague about animation timing and required a mid-execution revision".

The learnings document is stored in `.planning/learnings/` and is referenced automatically by future `gsd-new-milestone` runs.

```bash
/gsd-extract-learnings
/gsd-extract-learnings 3
/gsd-extract-learnings v1.0
```

Canonical path: `.github/skills/gsd-extract-learnings/SKILL.md`

### gsd-undo

`gsd-undo` safely rolls back phase or plan commits using the phase manifest. It knows which commits belong to which phase plan (because GSD's executor commits atomically with structured messages), so it can undo a specific plan's commits without disturbing commits from other plans or phases. It always prompts before performing any operation that modifies git history.

```bash
/gsd-undo 3
/gsd-undo 3 plan-2
```

Canonical path: `.github/skills/gsd-undo/SKILL.md`

### gsd-inbox

`gsd-inbox` triages open GitHub issues and PRs against the project's templates and contribution guidelines. It reads issue and PR bodies and discussion threads, suggests appropriate labels, identifies issues that are duplicates or out of scope, and prepares suggested responses. It can write comments to GitHub on items that need a response. Use this skill during regular project maintenance to keep the issue tracker clean and responsive.

```bash
/gsd-inbox
```

Canonical path: `.github/skills/gsd-inbox/SKILL.md`

---

## Agents in this stage

**gsd-doc-writer** writes and updates project documentation files. Spawned by `gsd-docs-update` with a `doc_assignment` block specifying the documentation type, the mode (create, update, or supplement), and the project context from planning artifacts. The agent explores the codebase directly using Read and Search tools — it does not rely solely on SUMMARY.md or CONTEXT.md. This exploration-first approach produces documentation that accurately reflects the current state of the code rather than the state described in planning artifacts (which may be months old).

**gsd-doc-verifier** is spawned by `gsd-docs-update` after each doc-writer agent completes. It verifies factual claims in the generated documentation against the live codebase — checking that file paths in the documentation actually exist, that API endpoints described match the actual router definitions, and that configuration values and environment variable names are current. Returns a structured JSON report per document.

**gsd-doc-classifier** and **gsd-doc-synthesizer** are primarily Research stage agents spawned by `gsd-ingest-docs`, but they are also relevant at the Deployment stage when importing external documentation into the planning system after a milestone completes.
