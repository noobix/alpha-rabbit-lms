---
Author: Kelvin Kabute
Last-updated: 2026-10-06
---

# Development Guardrails

This document defines the mandatory guardrails that ensure consistency when building across sprints in Alpha Rabbit LMS. Every agent and contributor must follow these guardrails before, during, and after implementing any ticket.

## File Context

**Purpose:** This is the single source of truth for the development workflow — from branch creation to PR merge. It consolidates scattered conventions from `build.md`, `provenance.md`, `release.md`, and the GSD planning system into one enforceable document.

**Why this matters:** Without guardrails, sprint work drifts — branch names become inconsistent, commit messages lose traceability, provenance metadata goes missing, and PRs target the wrong branch. This document prevents that drift.

**How agents use it:** Before starting any ticket, the agent reads this document and follows each section in sequence. The guardrails are not suggestions — they are the workflow.

---

## 1. Initial Git Operations (via MCP)

> **All git operations must go through GitHub MCP Server tools.** No direct `git` CLI commands for remote operations.

### 1.1 Sync with the Development Base Branch

Before creating any feature branch, ensure `develop` is up to date by fetching the latest state via MCP:

```yaml
Tool: github-mcp-server-list_branches
  owner: noobix
  repo: alpha-rabbit-lms
```

> **Note:** The development base branch is `develop`. This is where all feature work integrates during a sprint. The `testing-main` branch is only targeted after a full sprint is complete and verified (see Section 5.4).

### 1.2 Generate Branch Name Per Convention

Branch names must follow the exact pattern:

```text
LMS-[XXX]/[title-or-description]
```

- `[XXX]` = the numeric ticket ID from `docs/jira/compression.md` (e.g., `101`, `302`, `801`)
- `[title-or-description]` = kebab-case summary of the ticket title

**Examples:**

| Ticket     | Branch Name                                         |
| ---------- | --------------------------------------------------- |
| LMS-101    | `LMS-101/implement-sha256-hashing-ghana-card-id`    |
| LMS-302    | `LMS-302/build-budget-tracking-ges-alignment`       |
| LMS-801    | `LMS-801/create-bulk-book-requests-rotation-cycles` |
| LMS-NA-001 | `LMS-NA-001/power-outage-resilience-validation`     |

**Create the branch via MCP:**

```yaml
Tool: mcp_io_github_git_create_branch
  owner: noobix
  repo: alpha-rabbit-lms
  branch: LMS-[XXX]/[title-or-description]
  from_branch: develop
```

---

## 2. Subagent and Skills Involvement During Planning

### 2.1 GSD Planning Entry Point

When planning a feature, phase, or milestone, the agent must first read the GSD planning system:

1. Read `.github/gsd-flat-directory/README.md` — the single entry point for all GSD skills and agents, organized into six lifecycle stages.
2. Read `.github/gsd-flat-directory/copilot-integration.md` — access rules governing which stage documents may be used at any point in the session.
3. When ready to hand off to an execution agent, follow `.github/gsd-flat-directory/HANDOFF.md`.

> **Rule:** Do not invoke any GSD execution skill (`gsd-execute-phase`, `gsd-fast`, `gsd-quick`) or any testing or deployment skill during a planning session. All skill and agent dispatch during planning is mediated through the stage documents in `.github/gsd-flat-directory/stages/`.

### 2.2 Available Subagents

The repository provides specialized subagents in `.github/agents/` that can be harnessed during planning and execution:

| Agent                      | Purpose                                                                    |
| -------------------------- | -------------------------------------------------------------------------- |
| `gsd-planner`              | Creates executable phase plans with task breakdown and dependency analysis |
| `gsd-executor`             | Executes phase plans with wave-based parallelization                       |
| `gsd-code-reviewer`        | Reviews source files for bugs, security issues, and code quality           |
| `gsd-verifier`             | Validates built features through conversational UAT                        |
| `gsd-debugger`             | Systematic debugging with persistent state                                 |
| `gsd-security-auditor`     | Retroactively verifies threat mitigations                                  |
| `gsd-ui-auditor`           | Retroactive 6-pillar visual audit of frontend code                         |
| `gsd-research-synthesizer` | Synthesizes research findings                                              |
| `gsd-doc-writer`           | Generates documentation verified against the codebase                      |

### 2.3 Available Skills

Skills are domain-specific capabilities that improve output quality. The agent should be aware that these skills exist and can be invoked when the task falls within their domain. For detailed trigger phrases and usage, see `.copilot/copilot-instructions.md`.

**Skill categories registered for this project:**

- **UI & Frontend Design:** `frontend-design`, `impeccable`, `uncodixfy`, `animate`, `adapt`, `layout`
- **Platform / Runtime:** `electron`, `native-feel-cross-platform-desktop`
- **GitHub / PR Workflows:** `summarize-github-issue-pr-notification`, `address-pr-comments`, `create-pull-request`
- **Code Quality:** `agent-provenance-detector`
- **GSD Orchestration:** `gsd-plan-phase`, `gsd-execute-phase`, `gsd-fast`, `gsd-quick`, `gsd-discuss-phase`, `gsd-research-phase`

> **Note:** Skills are not detailed in plans. The plan should reference that a skill exists for a domain and let the executor invoke it when appropriate.

---

## 3. Source Code Documentation & Agent Recognition

### 3.1 Per-File Header Template

Every source file must carry a structured JSDoc-style header at the top using the appropriate comment style for the language. The header must include: `@scope`, `@description`, `@access`, `@depends`, `@author`, and `@updated`.

**TypeScript / JavaScript / TSX:**

```typescript
/**
 * GhanaCardHasher
 *
 * @scope       LMS-CORE-SECURITY (LMS-101)
 * @description Validates Ghana Card IDs against the GHA-000000000-0 format, then salts and hashes them with SHA-256 in the Electron main process. Plaintext IDs never reach the renderer — all UI surfaces display the masked format GHA-123***89-0. Log sanitization strips any accidental plaintext leakage from backups and debug output.
 * @access      Called by StaffProfileForm, VendorRegistrationForm, and any component that captures or displays national ID values.
 * @depends     crypto (Node.js native), zod (validation), electron-store (config)
 * @author      Claude Opus 4.6 (Copilot Agent), Kelvin Kabute
 * @updated     2026-04-05
 */
```

**Python:**

```python
"""
GhanaCardHasher

@scope       LMS-CORE-SECURITY (LMS-101)
@description Validates Ghana Card IDs against the GHA-000000000-0 format, then salts and hashes them with SHA-256 in the Electron main process. Plaintext IDs never reach the renderer — all UI surfaces display the masked format GHA-123***89-0. Log sanitization strips any accidental plaintext leakage from backups and debug output.
@access      Called by StaffProfileForm, VendorRegistrationForm, and any component that captures or displays national ID values.
@depends     hashlib (Python native), re (regex), zod (validation)
@author      Claude Opus 4.6 (Copilot Agent), Kelvin Kabute
@updated     2026-04-05
"""
```

**Markdown (YAML front-matter):**

```markdown
---
scope: LMS-CORE-SECURITY (LMS-101)
description: Canonical schema reference for LMS-assisted database design. Consolidates entities from acquisitions, processing, distribution, extension services, patron intelligence, governance, and cross-country African library workflows. Every persistent document must follow the BaseDocument contract (_id, _rev, type, createdAt, updatedAt, _syncStatus, _schemaVersion).
access: Source of truth before implementing forms, APIs, sync rules, or validation logic. Read by gsd-planner and gsd-executor agents during phase planning.
depends: PouchDB, CouchDB, Zod
author: Claude Opus 4.6 (Copilot Agent), Kelvin Kabute
updated: 2026-04-05
---
```

### 3.2 Header Field Definitions

| Field          | Required | Description                                                                                                                                        |
| -------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `@scope`       | Yes      | The module or ticket scope this file belongs to (e.g., `LMS-CORE-SECURITY (LMS-102)`). Use the ticket epic and ID from `docs/jira/compression.md`. |
| `@description` | Yes      | A concise description of what the file does — its purpose, key behavior, and any important constraints.                                            |
| `@access`      | Yes      | How this file is consumed — which components, screens, or services call it.                                                                        |
| `@depends`     | Yes      | External dependencies — libraries, APIs, environment variables, or other modules this file relies on.                                              |
| `@author`      | Yes      | The human author and/or agent that created or contributed to the file. Format: `Agent Name (Agent Identifier), Human Name`.                        |
| `@updated`     | Yes      | The date the file was last modified in `YYYY-MM-DD` format.                                                                                        |

### 3.3 Provenance Detection & Append Rules

The repository enforces provenance metadata through automated tools:

- **Detection:** The `agent-provenance-detector` skill determines whether an LLM or coding agent likely contributed to a file.
- **Pre-commit hook:** Runs `scripts/append_provenance.py` which appends `Author:` and `Last-updated:` lines as needed.
- **Author entries are append-only:** The hook never removes existing `Author` lines; it appends another when new contributors or agents are detected.
- **Last-updated behavior:** If `Last-updated` already equals today's date, the hook assumes an agent already appended the author; otherwise it appends the git user name.

### 3.4 Skipped Extensions

The following extensions are **never touched** by the appender. Injecting comment-like text into these files breaks the parser or tool that consumes them.

| Group                    | Extensions                              | Reason                                                    |
| ------------------------ | --------------------------------------- | --------------------------------------------------------- |
| JSON / JSONC             | `.json`, `.jsonc`                       | Comments are invalid JSON                                 |
| YAML                     | `.yaml`, `.yml`                         | CI configs, Docker Compose, GH Actions                    |
| TOML                     | `.toml`                                 | `pyproject.toml`, Cargo.toml, Electron builder configs    |
| XML / HTML / SVG         | `.xml`, `.html`, `.htm`, `.svg`         | Strict parsers; DOCTYPE or root element must appear first |
| Plain text / tool config | `.txt`, `.env`, `.ini`, `.cfg`, `.conf` | Consumed verbatim by pip, dotenv, configparser            |
| Lock / generated         | `.lock`                                 | Auto-generated and always overwritten                     |
| Data                     | `.csv`, `.tsv`                          | First line is a header record                             |
| Docker                   | `.dockerfile`                           | Named `*.dockerfile` variants                             |

Any extension **not** in `EXT_COMMENT_STYLES` inside `scripts/append_provenance.py` is also skipped implicitly.

### 3.5 When a File Is Edited

When an agent or contributor edits a file:

1. Update the `@updated` field to today's date in `YYYY-MM-DD` format.
2. If the edit is made by an agent, ensure the `@author` field includes the agent identifier (e.g., `Claude Opus 4.6 (Copilot Agent)`).
3. If the file's scope, description, access pattern, or dependencies change, update the corresponding fields.
4. The pre-commit hook will handle appending if the agent forgets — but do not rely on the hook. Update the header explicitly.

---

## 4. Code Quality & UI Design Skills

### 4.1 Skills for Code Quality

The following skills are available to improve code quality. Invoke them when the task matches their domain:

- **`agent-provenance-detector`** — Detects whether code was authored or assisted by a coding agent. Use when checking authorship or before commits.
- **`gsd-code-review`** — Reviews source files changed during a phase for bugs, security issues, and code quality problems. Use after implementation is complete.
- **`gsd-audit-fix`** — Autonomous audit-to-fix pipeline. Use when systematic quality improvement is needed.
- **`suggest-fix-issue`** — Proposes fixes for described bugs or issues.

### 4.2 Skills for UI Design

The following skills are available for frontend and UI work:

- **`frontend-design`** — Creates production-grade UI components and page layouts. Use when building web components, pages, or applications.
- **`impeccable`** — Generates refined, product-quality UI code that avoids generic AI aesthetics. Use when aesthetics matter.
- **`uncodixfy`** — Sanitizes generic AI-generated UI code into crisp, human-quality patterns. Use after an initial component is produced and needs polishing.
- **`animate`** — Adds purposeful animations, transitions, and micro-interactions. Use when motion design is requested.
- **`adapt`** — Makes layouts responsive across screen sizes and devices. Use when building for multiple viewports.
- **`layout`** — Improves layout, spacing, and visual rhythm. Use when spacing or alignment feels off.
- **`electron`** — Electron-specific patterns for desktop apps. Use when working with main/renderer processes, IPC, or native integrations.

### 4.3 When to Invoke Skills

- If the task involves creating or modifying UI components → invoke `frontend-design` or `impeccable`.
- If the task involves responsive design or mobile layouts → invoke `adapt` or `layout`.
- If the task involves animations or transitions → invoke `animate`.
- If the task involves Electron-specific patterns → invoke `electron`.
- If the task involves reviewing code quality → invoke `gsd-code-review`.
- If the task involves checking authorship → invoke `agent-provenance-detector`.

---

## 5. Git Operations (Continued — via MCP)

> **All git operations must go through GitHub MCP Server tools.** No direct `git` CLI commands for remote operations.

### 5.1 Commit Implementation Per Convention

Every commit message must paint a clear picture of what was built and why. Use the acceptance criteria from `docs/jira/compression.md` as context — don't copy them verbatim, describe the work you actually did.

**Commit message format:**

```text
LMS-[XXX]: <type>: <vivid summary of what was accomplished>

<Paragraph explaining what was built, how it works, and why it was
done this way. Reference the real behavior and constraints from the
ticket naturally — not as a checklist.>
```

Where `<type>` is one of: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`.

**Example (LMS-101):**

```text
LMS-101: feat: implement SHA-256 hashing pipeline for Ghana Card ID storage

Built the hashing service in the Electron main process to ensure plaintext
Ghana Card IDs never reach the renderer. IDs are validated against the
GHA-000000000-0 format at the form boundary, salted and hashed with SHA-256
before persistence, and displayed as masked values (GHA-123***89-0) across
all UI surfaces. Log sanitization strips any accidental plaintext leakage
from backups and debug output. The masked format function is shared with
the vendor Ghana Card display for reuse in LMS-301.
```

**Commit and push via MCP:**

```yaml
Tool: mcp_io_github_git_push_files
  owner: noobix
  repo: alpha-rabbit-lms
  branch: LMS-[XXX]/[title-or-description]
  files:
    - path: "<relative/path/to/file>"
      content: "<full file content>"
  message: |
    LMS-[XXX]: <type>: <vivid summary>

    <Paragraph describing what was built, how it works,
    and why it was done this way.>
```

### 5.2 Tag the Commit with a Build Number (Lightweight Tag)

Before opening the PR, tag the current commit on the feature branch with a lightweight build number tag. Each commit receives exactly one build number. Build numbers are the primary traceability unit linking a commit to its delivered work.

**Build number format:**

```text
[YY###]
```

- `YY` = two-digit year (2026 → `26`)
- `###` = sequential counter starting at `1` for the year, incrementing by one per merged PR
- 2026 range: `[261]` through `[26999]`
- Build numbers are year-scoped, never reset mid-year, and never appear in the semantic version string

**Reading the next build number from `.build_counter`:**

The repo tracks the next build number to use in a plain text file at the root. Read this file before tagging via MCP:

```yaml
Tool: mcp_io_github_git_get_file_contents
  owner: noobix
  repo: alpha-rabbit-lms
  path: ".build_counter"
  ref: "refs/heads/LMS-[XXX]/[title-or-description]"
```

**Tagging and incrementing via MCP:**

1. Read `.build_counter` → the value it contains is the number you apply to your commit
2. Create the lightweight tag `[YY###]` on the current commit via MCP
3. Push the tag to origin via MCP
4. Increment the counter and commit it back to `develop` via `mcp_io_github_git_push_files`

```yaml
# Step 4: Increment and commit the counter
Tool: mcp_io_github_git_push_files
  owner: noobix
  repo: alpha-rabbit-lms
  branch: develop
  files:
    - path: ".build_counter"
      content: "<incremented value>"
  message: "chore: increment build counter to <new value>"
```

> **Race condition note:** If two PRs are being tagged concurrently, both may read the same counter value. Serialise this step manually (one tag operation at a time) or rely on CI automation in `docs/release.md` which handles this atomically.

### 5.5 Create Sprint Annotated Tag (Semantic Version Tag)

> **Important:** The annotated tag is created when the sprint is merged into `testing-main`, NOT `develop`. The `develop` branch is just a branch to accumulate tickets until a sprint is achieved. After manual testing on `develop` confirms no issues, a PR is made to `testing-main` where the CI `minor-release` job creates the annotated tag.

When the sprint completion PR from `develop` to `testing-main` is merged, the CI `minor-release` job runs on `testing-main` and creates a single annotated tag covering the entire sprint. The annotated tag is the durable, human-readable record of everything delivered in the sprint; its body feeds release notes and audit records. The semantic version increments the MINOR component at sprint completion.

**Annotated tag body format:**

```text
Build #[261]
Changes:
- <Paraphrased description of what was delivered — drawn from the PR ## Changes section, not copied verbatim>
- <Additional delivered behavior expressed as what the system now does as a result of this build>

Build #[262]
Changes:
- <Paraphrased description of what was delivered>
- <Additional delivered behavior>

Contributors:
@github-handle (Display Name)
@github-handle-2 (Display Name)

---

Appendix: Full PR descriptions
[Full PR description for each build, appended in chronological order]
```

**Rules:**

- Open each build entry with `Build #[YY###]`.
- `Changes:` items are paraphrased from the PR `## Changes` section. Describe what the system now does as a result of the build — implementation behavior, not requirements. Do not copy from the acceptance criteria list or lift wording from the commit message verbatim.
- Order entries chronologically by merge date.
- After all build entries, include a `Contributors:` section listing every GitHub handle (and display name where available) that authored a PR or commit merged in this sprint. Format each line as `@handle (Display Name)` — or `@handle` alone when no display name is set. Deduplicate and sort alphabetically. This section is generated automatically by `scripts/release-aggregate.sh`.
- After the contributors section, append a `---` separator followed by `Appendix: Full PR descriptions`, then the full PR description body for each build in chronological order. This appendix is the reference used by `docs/release.md` and for audit purposes.
- The tag body must be entirely self-contained — readable without accessing GitHub.

**Example (Sprint 1, v1.1.0):**

```text
Build #[261]
Changes:
- Ghana Card IDs submitted at any form boundary are validated against the GHA-000000000-0 format, then hashed and salted exclusively in the Electron main process before reaching the database — plaintext values never appear in storage, logs, or the renderer.
- All UI surfaces render the masked format GHA-123***89-0; the masking function is shared with the vendor identity form.

Build #[262]
Changes:
- The backup scheduler fires daily at 8 PM, produces an incremental snapshot capped at 5% of database size, and resumes automatically from the last checkpoint after a power interruption.
- A WhatsApp export path compresses the output below 10 MB; a retention job prunes backups older than 30 days on schedule.

Build #[263]
Changes:
- Active transaction drafts are persisted to a local snapshot every 30 seconds and stamped with a checksum; on restart after an outage the app locates the last clean snapshot, verifies its integrity, and displays the exact timestamp of the recovered state to the user.

Contributors:
@noobix (Kelvin Kabute)

---

Appendix: Full PR descriptions
[Full PR description for Build #[261] — LMS-101]
[Full PR description for Build #[262] — LMS-102]
[Full PR description for Build #[263] — LMS-103]
```

**Create the annotated tag via MCP:**

Use the GitHub MCP `create_commit` or direct tag creation via the MCP server. Write the tag body to a temporary file to handle multi-line content reliably; remove the file after tagging. Automation details live in `docs/release.md`.

### 5.3 Create Pull Request to `develop`

> **CRITICAL DEVIATION FROM `build.md`:** During a sprint, all PRs target `develop` — NOT `testing-main`. The `build.md` document says to target `testing-main`, but this is overridden by the project owner's directive. After a full sprint is implemented and verified with no issues, a single PR is made from `develop` to `testing-main` (see Section 5.4).

**PR title format:**

```text
LMS-[XXX]: <ticket title>
```

**PR body template:**

```markdown
## Ticket

**LMS-[XXX]**: <ticket title>

## Changes

- Write this section as a paraphrase of the ticket's acceptance criteria, phrased as completed implementation behavior rather than a checklist.
- Describe what the code now does, how it behaves, and why it satisfies the ticket, without copying the acceptance criteria verbatim.
- You may reference the commit message for context, but do not lift its wording directly.
- This section will be reused in annotated tags, so keep it clear, factual, and implementation-focused.

## Acceptance Criteria (from compression.md)

- [ ] <AC 1>
- [ ] <AC 2>
- [ ] <AC 3>

## Completion Gate Checklist

- [ ] All acceptance criteria satisfied
- [ ] Offline behavior demonstrated
- [ ] Security/privacy checks pass
- [ ] Audit artifacts exist where required
- [ ] Manager/Enterprise impact recorded
```

**Create the PR via MCP:**

```yaml
Tool: mcp_io_github_git_create_pull_request
  owner: noobix
  repo: alpha-rabbit-lms
  title: "LMS-[XXX]: <ticket title>"
  head: LMS-[XXX]/[title-or-description]
  base: develop
  body: |
    ## Ticket
    **LMS-[XXX]**: <ticket title>

    ## Changes
    - <Paraphrased implementation behavior>

    ## Acceptance Criteria (from compression.md)
    - [ ] <AC 1>
    - [ ] <AC 2>
    - [ ] <AC 3>

    ## Completion Gate Checklist
    - [ ] All acceptance criteria satisfied
    - [ ] Offline behavior demonstrated
    - [ ] Security/privacy checks pass
    - [ ] Audit artifacts exist where required
    - [ ] Manager/Enterprise impact recorded
```

### 5.4 Sprint Completion: PR to `testing-main`

When every ticket in a sprint is merged into `develop` and the sprint is fully implemented with no issues, create a single PR from `develop` to `testing-main` via MCP:

```yaml
Tool: mcp_io_github_git_create_pull_request
  owner: noobix
  repo: alpha-rabbit-lms
  title: "Sprint [N]: <sprint title> — Complete"
  head: develop
  base: testing-main
  body: |
    Sprint [N] complete. All tickets merged to develop. Ready for testing integration.
```

**After the PR to `testing-main` is merged:**

1. The CI `minor-release` job automatically creates the sprint annotated tag (see below for format).
2. The semantic version increments the MINOR component at sprint completion.
3. Update `.build_counter` if needed for the next sprint.

---

## 6. Quick Reference: Full Workflow Sequence (All via MCP)

```text
1. github-mcp-server-list_branches → Verify develop exists and is current
2. mcp_io_github_git_create_branch → Create LMS-[XXX]/[title-or-description] from develop
3. Implement the feature (update file headers with @author + @updated)
4. mcp_io_github_git_push_files → Commit and push all changes with LMS-[XXX]: <type>: <summary>
5. Read .build_counter via mcp_io_github_git_get_file_contents → tag commit [YY###] → increment counter via mcp_io_github_git_push_files
6. mcp_io_github_git_create_pull_request → Open PR to develop
7. After PR merge → next ticket (repeat steps 1-6)
8. After all sprint tickets merged to develop → manual testing on develop
9. mcp_io_github_git_create_pull_request (develop → testing-main)
10. After PR merge to testing-main → CI minor-release job creates sprint annotated tag (vMAJOR.MINOR.0)
```

---

## 7. Testing Gates & Quality Enforcement

This section documents every testing gate that runs on `testing-main` and `main`, what each gate expects to pass, how to locate failures, and how to solve problems. It is the single source of truth for understanding CI/CD enforcement.

### 7.1 Gate Hierarchy

```text
┌─────────────────────────────────────────────────────────────────┐
│                    CONTINUATION GATE                            │
│         (aggregates CI + Security + PR Gate)                    │
│         Blocks merge if any upstream workflow fails             │
├─────────────────────────────────────────────────────────────────┤
│                         CI GATE                                 │
│    ┌─────────────┬──────────────┬──────────────┬─────────────┐  │
│    │   Policy     │  Workflow    │    Lint      │    Test     │  │
│    │   (pnpm,     │  Lint        │  (flake8,    │  (pytest,   │  │
│    │   SHA pins,  │  (actionlint)│   shellcheck)│   node)     │  │
│    │   no env)    │              │              │             │  │
│    └─────────────┴──────────────┴──────────────┴─────────────┘  │
│    ┌──────────────────────────────────────────────────────────┐  │
│    │              Coverage Ratchet (main only)                │  │
│    │     Ensures coverage does not regress vs last main      │  │
│    └──────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                      SECURITY GATE                              │
│    ┌─────────────┬──────────────┬──────────────┬─────────────┐  │
│    │   CodeQL    │  Python      │  Node        │  Secrets    │  │
│    │   (JS/TS,   │  Security    │  Dependency  │  (gitleaks) │  │
│    │   Python,   │  (bandit,    │  Audit       │             │  │
│    │   Actions)  │  pip-audit)  │  (pnpm audit)│             │  │
│    └─────────────┴──────────────┴──────────────┴─────────────┘  │
│    ┌──────────────────────────────────────────────────────────┐  │
│    │              CodeQL Alert Gate                           │  │
│    │     Blocks on open high/critical CodeQL alerts          │  │
│    └──────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                        PR GATE (main only)                      │
│    ┌─────────────┬──────────────┬──────────────┬─────────────┐  │
│    │  Head repo  │  Head ref    │  PR body     │  Coverage   │  │
│    │  (no forks) │  (testing-   │  (5 required │  declaration│  │
│    │             │   main only) │   headings)  │  (main only)│  │
│    └─────────────┴──────────────┴──────────────┴─────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 CI Gate

**File:** `.github/workflows/ci.yml`
**Runs on:** Push to `main`, `testing-main`; PRs to `main`, `testing-main`

**What it checks:**

| Job | What it validates | Required? |
| --- | ----------------- | --------- |
| `policy` | Only pnpm lockfile, no committed `.env` files, all actions pinned to SHA | Yes |
| `workflow-lint` | GitHub Actions workflow YAML syntax via `actionlint` | Yes |
| `lint` | Python `flake8` (max line 120, complexity 22), `shellcheck` for scripts | Yes |
| `test` | `pytest` with branch coverage (floor: 10% on `testing-main`, 80% on `main`) | Yes |
| `node` | `pnpm run lint`, `typecheck`, `test`, `build` (only if `package.json` exists) | Skipped if no Node |
| `coverage-ratchet` | Coverage does not regress vs last successful `main` run | Yes (main only) |

**How to locate failures:**

1. Go to **GitHub → Actions → CI → failed run**
2. Click the failed job (e.g., `test (ubuntu-latest, py3.12)`)
3. Expand the failed step to see the error output

**How to solve common problems:**

| Failure | Cause | Solution |
| --- | --- | --- |
| `::error::Forbidden files (pnpm only, no committed env files)` | `package-lock.json`, `yarn.lock`, or `.env` committed | Delete the file, add to `.gitignore`, commit the removal |
| `::error::package.json must set packageManager to pnpm@<version>` | Missing `packageManager` field | Add `"packageManager": "pnpm@latest"` to `package.json` |
| `::error::Actions must be pinned to a full commit SHA` | Action uses `@v4` instead of SHA | Pin to SHA: `uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4` |
| `pytest ... --cov-fail-under=XX` | Coverage below floor | Add tests or raise coverage; floor is 10% on `testing-main`, 80% on `main` |
| `flake8` errors | Line too long, complexity too high | Refactor: shorten lines, reduce nesting |
| `shellcheck` errors | Shell script issues | Fix quoting, use `set -euo pipefail`, check with `shellcheck scripts/*.sh` |
| `pnpm run lint` / `typecheck` / `build` | Node project issues | Run locally: `pnpm run lint && pnpm run typecheck && pnpm run build` |
| `Coverage regressed from X to Y` | Coverage dropped vs last `main` | Add tests to restore coverage to at least the previous level |

### 7.3 Security Gate

**File:** `.github/workflows/security.yml`
**Runs on:** Push to `main`, `testing-main`; PRs to `main`, `testing-main`

**What it checks:**

| Job | What it validates | Required? |
| --- | ----------------- | --------- |
| `codeql` | Static analysis for Python and GitHub Actions code | Yes |
| `codeql-node` | Static analysis for JavaScript/TypeScript (only if `package.json` exists) | Skipped if no Node |
| `python-security` | `bandit` (medium+ severity) on `scripts/`, `pip-audit` on `requirements.txt` | Yes |
| `node-security` | `pnpm audit --prod --audit-level=high` | Skipped if no Node |
| `secrets` | `gitleaks` scan for committed secrets | Yes |
| `dependency-review` | Checks for high-severity dependency vulnerabilities (PR only) | Skipped on push |
| `codeql-gate` | Blocks if open high/critical CodeQL alerts exist | Yes |

**How to locate failures:**

1. Go to **GitHub → Actions → Security → failed run**
2. Click the failed job
3. For CodeQL: **GitHub → Security → Code scanning alerts**

**How to solve common problems:**

| Failure | Cause | Solution |
| --- | --- | --- |
| `bandit` high/medium severity | Security issue in Python code (e.g., `subprocess`, `eval`, hardcoded password) | Refactor to use safe alternatives; see [bandit docs](https://bandit.readthedocs.io/) |
| `pip-audit` known vulnerabilities | Dependency with CVE | Update the dependency: `pip install --upgrade <package>` |
| `pnpm audit --audit-level=high` | High-severity vulnerability in Node deps | Run `pnpm audit --fix` or update the affected package |
| `gitleaks` detected secret | API key, token, or password in code | Remove the secret, rotate it if exposed, use environment variables |
| CodeQL high/critical alert | SQL injection, XSS, path traversal, etc. | Fix the code pattern; see the alert details for the exact fix |
| `dependency-review` failure | New dependency has high-severity vulnerability | Choose an alternative dependency or wait for a patched version |

### 7.4 PR Gate

**File:** `.github/workflows/pr-gate.yml`
**Runs on:** PRs to `main` only

**What it checks:**

| Check | Requirement |
| --- | ----------- |
| Head repo | PR must come from the same repo (no forks) |
| Head ref | PR must be from `testing-main` (no direct PRs from feature branches) |
| Draft status | Draft PRs cannot target `main` |
| PR body headings | Must contain: `Tickets`, `Summary`, `Acceptance criteria`, `Known gaps`, `Verification` |
| Coverage declaration | Must include `Coverage: XX%` (e.g., `Coverage: 85%`) |

**How to locate failures:**

1. Go to the PR page
2. Check the `PR Gate` check status — it will show `failed` with the error message
3. Click "Details" to see the specific validation that failed

**How to solve common problems:**

| Failure | Cause | Solution |
| --- | --- | --- |
| `PRs from forks are not accepted into main` | PR from a fork | Push to a branch in the main repo instead |
| `main only accepts promotions from testing-main` | PR from `develop` or feature branch | PR must be from `testing-main` to `main` |
| `Draft PRs cannot target main` | PR is still a draft | Mark as ready for review |
| `PR body needs a '## <Section>' heading` | Missing required section | Add all 5 headings to the PR body |
| `PRs into main must declare test coverage` | Missing `Coverage: XX%` line | Add `Coverage: 85%` (replace with actual coverage) to the PR body |

### 7.5 Continuation Gate

**File:** `.github/continuation-gate.yml`
**Runs on:** After CI, Security, and PR Gate complete on `main` or `testing-main`

**What it checks:**

| Check | Requirement |
| --- | ----------- |
| CI conclusion | Must be `success` or `skipped` |
| Security conclusion | Must be `success` or `skipped` |
| PR Gate conclusion | Must be `success` or `skipped` |

**How to locate failures:**

1. Go to **GitHub → Actions → Continuation Gate → failed run**
2. The output shows the conclusion of each upstream workflow:

```text
CI:          success
Security:    failure
PR Gate:      skipped
```

**How to solve:**

The Continuation Gate itself never fails independently — it reflects upstream failures. Fix the underlying CI, Security, or PR Gate failure first, then re-run.

### 7.6 Coverage Ratchet

**File:** `.github/workflows/ci.yml` (job: `coverage-ratchet`)
**Runs on:** `main` only

**What it checks:**

| Check | Requirement |
| --- | ----------- |
| Current coverage | Must be ≥ last successful `main` coverage |
| Coverage floor | Must be ≥ 80% (`MAIN_COVERAGE_FLOOR`) |

**How to locate failures:**

1. Go to **GitHub → Actions → CI → failed run → coverage-ratchet**
2. The error shows: `Coverage regressed from 0.85 to 0.82`

**How to solve:**

| Failure | Cause | Solution |
| --- | --- | --- |
| `Coverage regressed from X to Y` | New code added without tests | Add tests for the new code to restore coverage |
| Coverage below 80% | Insufficient test coverage | Add more unit tests; aim for 80%+ on `main` |

### 7.7 CodeQL Alert Gate

**File:** `.github/workflows/security.yml` (job: `codeql-gate`)
**Runs on:** Push to `main`, `testing-main`; PRs to `main`, `testing-main`

**What it checks:**

| Check | Requirement |
| --- | ----------- |
| Open high/critical alerts | Must be 0 |

**How to locate failures:**

1. Go to **GitHub → Security → Code scanning alerts**
2. Filter by severity: `high` or `critical`
3. Filter by state: `open`

**How to solve:**

1. Click the alert to see the exact code path
2. Follow the recommendation in the alert description
3. Fix the code pattern (e.g., use parameterized queries for SQL injection)
4. The alert will auto-close on the next push

### 7.8 Branch Protection

**File:** `.github/workflows/enable-branch-protection.yml`
**Policy:** `docs/ops/branch_protection.md`

**What it enforces:**

| Rule | `main` | `testing-main` |
| ---- | ------ | -------------- |
| PR required | Yes | Yes |
| Required approving reviews | 1 (dismissed on new pushes) | 0 |
| Required checks (strict) | `Continuation Gate`, `CI Gate`, `Security Gate`, `PR Gate` | `CI Gate`, `Security Gate` |
| Conversation resolution | Yes | Yes |
| Force pushes / deletions | Blocked | Blocked |
| `enforce_admins` | False (owner bypass) | False (owner bypass) |

**How to locate failures:**

1. Go to the PR page
2. Check the "Checks" tab — failed checks show in red
3. The merge button is blocked until all required checks pass

**How to solve:**

| Failure | Cause | Solution |
| --- | --- | --- |
| `Required check: CI Gate` failed | CI workflow failed | Fix the underlying CI failure (see Section 7.2) |
| `Required check: Security Gate` failed | Security workflow failed | Fix the underlying Security failure (see Section 7.3) |
| `Required check: PR Gate` failed | PR body missing sections | Add required headings to PR body (see Section 7.4) |
| `Required check: Continuation Gate` failed | Upstream workflow failed | Fix CI/Security/PR Gate first |
| `Review required` | No approvals | Owner can use **Owner Merge PRs** workflow to bypass |

**Owner Bypass:**

The owner (`noobix`) can merge without reviews using the `Owner Merge PRs` workflow:

1. Go to **GitHub → Actions → Owner Merge PRs → Run workflow**
2. Enter comma-separated PR numbers (e.g., `6,7,8`)
3. Click **Run workflow**

This uses `--admin` flag to bypass branch protection requirements.

### 7.9 Pre-commit Hook

**File:** `hooks/pre-commit` + `scripts/append_provenance.py`
**Runs on:** Every `git commit`

**What it checks:**

| Check | Requirement |
| --- | ----------- |
| Provenance metadata | Appends `Author:` and `Last-updated:` to staged files |
| Skip extensions | Never touches `.json`, `.yml`, `.yaml`, `.toml`, `.xml`, `.html`, `.txt`, `.env`, `.lock`, `.csv`, `.dockerfile` |

**How to locate failures:**

1. The commit aborts with an error message in the terminal
2. Common error: `Python was not found` — the hook needs Python on PATH

**How to solve:**

| Failure | Cause | Solution |
| --- | --- | --- |
| `Python was not found` | No Python on PATH | Install Python 3.10+ and ensure it's on PATH |
| `ModuleNotFoundError: No module named 'scripts'` | Hook run from wrong directory | The hook now uses `runpy` — update to latest version |
| Commit succeeds but no `Author:` line | Hook skipped the file | File extension is in `SKIP_EXTENSIONS` — this is expected behavior |

**To install the hook:**

```bash
# Windows
scripts\install_hook.bat

# macOS / Linux
bash scripts/install_hook.sh
```

### 7.10 Troubleshooting Guide

**Common failure patterns and solutions:**

| Symptom | Likely Cause | Solution |
| --- | --- | --- |
| PR to `develop` fails CI | Flake8, pytest, or policy failure | Run locally: `flake8 --max-line-length=120` and `pytest --cov=scripts --cov-fail-under=10` |
| PR to `testing-main` fails CI | Same as above + coverage floor | Ensure coverage ≥ 10% on `testing-main` |
| PR to `main` fails PR Gate | Missing PR body headings | Add `## Tickets`, `## Summary`, `## Acceptance criteria`, `## Known gaps`, `## Verification` |
| PR to `main` fails with `Coverage regressed` | Coverage dropped vs last `main` | Add tests to restore coverage |
| Security gate fails on `bandit` | Unsafe Python pattern | Refactor: avoid `subprocess`, `eval`, hardcoded secrets |
| Security gate fails on `gitleaks` | Secret in code | Remove secret, rotate if exposed, use env vars |
| CodeQL alert on SQL injection | String concatenation in query | Use parameterized queries or an ORM |
| `pnpm audit` fails | Vulnerable dependency | Run `pnpm audit --fix` or update the package |
| Merge button grayed out | Required checks failing | Check the "Checks" tab for which gate failed |
| `continuation-gate` red | Upstream CI/Security failed | Fix the upstream failure first |

**Local validation commands (run before pushing):**

```bash
# Python lint
flake8 --max-line-length=120 --max-complexity=22 --exclude=.venv,.git

# Python tests with coverage
pytest --cov=scripts --cov-branch --cov-report=term --cov-fail-under=10

# Shell scripts
shellcheck scripts/*.sh hooks/pre-commit

# Node (if applicable)
pnpm install --frozen-lockfile
pnpm run lint
pnpm run typecheck
pnpm run test
pnpm run build
pnpm audit --prod --audit-level=high

# Provenance
python scripts/append_provenance.py
python scripts/check_provenance.py
```
