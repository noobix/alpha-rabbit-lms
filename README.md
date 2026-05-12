---
Author: Kelvin Kabute
Last-updated: 2026-05-12
---

# 🐇 Alpha Rabbit LMS

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](./LICENSE)

Alpha Rabbit LMS is an open-source, offline-first Library Management System built for Ghanaian libraries. It ships in two editions:

- **Manager** — single-library, offline desktop app (Electron + PouchDB + SQLite).
- **Enterprise** — multi-department, multi-site edition with CouchDB server sync.

---

## License

Released under the GNU General Public License v3.0 (GPL-3.0). See the `LICENSE` file for full details.

## Attribution

This project was initiated by `noobix` (2026). Please keep the `LICENSE` and `ABOUT.md` files intact in derivative works to preserve attribution.

---

## 🏛️ Project Departments

Alpha Rabbit LMS is organised into six departments. Each has a dedicated spec under `docs/research_dmp/`. Tickets in `docs/jira/compression.md` carry a department prefix so you can find the owning module quickly.

| Department             | Synopsis                                                                                                                                                                                                                                                                                              | Spec                                          |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| **Acquisitions**       | Bibliographic data entry, Ghana Curriculum Tag assignment, vendor management, and offline-first book intake for both Manager and Enterprise versions.                                                                                                                                                 | `docs/research_dmp/aquisisions_module.md`     |
| **Processing**         | Physical inspection, condition scoring, PDF417 barcode generation, Extension Services routing flag, and Ghana climate durability thresholds.                                                                                                                                                          | `docs/research_dmp/processing_module.md`      |
| **Distribution**       | Section routing, batch-aware packing slips, rural delivery mode for the Tamale-Bolgatanga corridor, and Extension Services depot delivery with rotation-cycle metadata.                                                                                                                               | `docs/research_dmp/distribution_module.md`    |
| **Library Operations** | Day-to-day circulation across Children's, Adult, Reference, and Lending sections; patron degradation engine; Adinkra badge awards; GES batch promotion.                                                                                                                                               | `docs/research_dmp/library_sections_pi_sg.md` |
| **Extension Services** | Mobile library van and designated-room service for underserved schools. Operates as a top-level peer department — borrows books from the Lending section via bulk allocation, tracks learners with QR smart tags only (no Ghana Card ID, no condition scoring), and syncs via an offline Android app. | `docs/research_dmp/extension_module.md`       |
| **Deployment**         | Field validation, installer packaging, Ghana Library Authority compliance, Enterprise CouchDB pilot setup, and UAT checklist.                                                                                                                                                                         | `docs/research_dmp/deploy_doc.md`             |

> **Critical boundary:** Extension Services is NOT a library section. It is a full department peer to Acquisitions, Processing, and Distribution. Extension learners carry `extension_service: true` and are never given degradation scores.

---

## 💻 Environment Setup

### Prerequisites

- Python 3.10 or 3.11
- Git
- Node.js 18+ and pnpm (for the Electron app build)
- `gh` CLI (for release workflows)

### Python virtualenv

**Unix / macOS / Git Bash:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Windows (cmd.exe):**

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

### Node / pnpm (Electron app)

```bash
corepack enable
corepack prepare pnpm@latest --activate
pnpm install
```

---

## 🪝 Pre-commit Hook

The repository ships a pre-commit hook at `hooks/pre-commit`. Install it once and every future commit is checked automatically.

| Platform                | Installer                      |
| ----------------------- | ------------------------------ |
| Unix / macOS / Git Bash | `bash scripts/install_hook.sh` |
| Windows (cmd.exe)       | `scripts\install_hook.bat`     |

### What the hook does

1. **Appends / updates provenance metadata** (`scripts/append_provenance.py`) — runs on every staged file whose extension is in the allowed set (`.py`, `.md`, `.js`, `.ts`, `.css`).
   - **Markdown files** — finds the existing YAML front-matter block (`--- … ---`) and updates `Author:` and `Last-updated:` in place. If no front-matter exists, one is prepended.
   - **Python / JS / TS / CSS files** — inserts or updates `# Author:` / `# Last-updated:` comment lines near the top of the file.
   - Certain filenames are always skipped: `CHANGELOG.md`, `ABOUT.md`, `CONTRIBUTING.md`, `LICENSE`, `NOTICE`, `AUTHORS`, and their variants.
2. **Validates provenance** (`scripts/check_provenance.py`) — fails the commit if any tracked source file is missing `Author:` or `Last-updated:` after the append step.

### Files the hook skips

Extensions in the deny-list are never touched: `.json`, `.yaml`, `.yml`, `.toml`, `.xml`, `.html`, `.svg`, `.txt`, `.env`, `.lock`, `.csv`.

---

## 🔍 Coding-Agent Tracking

The project records which AI coding assistant (if any) contributed to each file. This is enforced at the metadata level and checked in CI.

### How it works

`scripts/detect_agent_provenance.py` is a heuristic scanner. It reads each file and looks for:

- Regex patterns matching known agent signatures: `GitHub Copilot`, `OpenAI / GPT-*`, `Claude / Anthropic`, `LLM-assisted`.
- Front-matter / comment keys: `Author:`, `generated-by:`.

Output is one JSON line per file:

```json
{
  "path": "scripts/foo.py",
  "agent": "github-copilot",
  "confidence": 0.85,
  "evidence": ["..."]
}
```

### Running the detector

```bash
# Scan the docs folder
python scripts/detect_agent_provenance.py docs/ > provenance-report.jsonl

# Scan the whole repository
python scripts/detect_agent_provenance.py .
```

### What the `Author:` field means

The pre-commit hook sets `Author:` to the committing developer's `git config user.name` by default. When the detector recognises an AI agent signature in the file with sufficient confidence, it sets `Author:` to the agent identifier (e.g. `github-copilot`) instead. This creates an auditable record of AI involvement at the file level.

### Running the CI checker locally

```bash
python scripts/check_provenance.py
```

- Exit `0` — every tracked source file has `Author:` and `Last-updated:`. ✅
- Non-zero — one or more files are missing metadata; CI will fail the same way. ❌

---

## 🌿 Branching & Commit Workflow

All work follows a branch-per-ticket model. Tickets live in `docs/jira/compression.md`.

### Branch naming

```text
LMS-[XXX]/[title-or-description]
```

Examples: `LMS-101/implement-sha256-hashing-ghana-card-id`, `LMS-502/extension-qr-smart-tag-generation`

### Day-to-day steps

```bash
# 1. Sync with integration branch
git fetch origin
git checkout LMS-[XXX]/[title-or-description]
git merge origin/testing-main

# 2. Work, then commit
git add .
git commit -m "LMS-[XXX]: feat: short vivid description"
# Hook runs automatically: appends metadata, validates provenance

# 3. Push and open PR
git push origin LMS-[XXX]/[title-or-description]
```

### Commit message format

```text
LMS-[XXX]: <type>: <vivid summary>

<Paragraph: what was built, how it works, why this approach.>
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`.

---

## 📬 Pull Requests

- **Target branch** — always `testing-main`.
- **One PR per ticket** — do not bundle unrelated changes.
- **PR body** must follow the template in `docs/build.md` Section 5 Step 6: `## Ticket`, `## Changes`, `## Acceptance Criteria`, `## Completion Gate Checklist`.
- **Merging rules**:
  - Developers require at least 1 approval from the repository owner before merging.
  - The repository owner can merge their own PRs directly using the **Owner Merge PRs** workflow (see CI section below).
  - CI (`CI` status check) must be green.

---

## ⚙️ CI Workflows

All workflows live in `.github/workflows/`. Here is what each one does.

### `ci.yml` — CI (primary gate)

**Triggers:** push or PR to `main` or `testing-main`.

| Step                 | What it does                                                   |
| -------------------- | -------------------------------------------------------------- |
| Checkout             | Full clone                                                     |
| Cache pip            | Speeds up dependency installs                                  |
| Set up Python        | Runs the matrix for Python 3.10 and 3.11                       |
| Install dependencies | `pip install -r requirements.txt`                              |
| Run flake8           | Lints all Python files (max line length 120, excludes `.venv`) |
| Run tests            | `pytest -q` across the full test suite                         |

This is the check that must be green before any PR can merge.

---

### `minor-release.yml` — Minor Release

**Triggers:** merged PR to `testing-main` **or** manual `workflow_dispatch`.

| Step                    | What it does                                                                   |
| ----------------------- | ------------------------------------------------------------------------------ |
| Checkout                | Full clone with all tags                                                       |
| Setup Node + pnpm       | Node 18, latest pnpm via corepack                                              |
| Authenticate gh CLI     | Uses `RELEASE_PAT` (falls back to `GITHUB_TOKEN`)                              |
| Check GPG secret        | Tests whether `GPG_PRIVATE_KEY` secret is set                                  |
| Import GPG key          | Imports key and configures `user.signingkey` (only when GPG secret is present) |
| Read build counter      | Reads next build number from `.build_counter`                                  |
| Aggregate sprint builds | Runs `scripts/release-aggregate.sh` → writes `sprint-tag-body.txt`             |
| Bump minor version      | Reads `package.json`, increments MINOR, resets PATCH to 0                      |
| Create annotated tag    | `git tag -a vX.Y.0 -F sprint-tag-body.txt` then pushes                         |
| Increment build counter | Writes `BUILD + 1` back to `.build_counter`, commits to `testing-main`         |

**Secrets required:** `RELEASE_PAT` (required), `GPG_PRIVATE_KEY` + `GPG_PASSPHRASE` (optional, for signed tags).

---

### `deploy-on-tag.yml` — Deploy on Tag

**Triggers:** any `v*.*.*` tag pushed to the repository.

| Step                  | What it does                                                                                                                 |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Checkout              | Full clone with all history                                                                                                  |
| Setup Node + pnpm     | Node 18, latest pnpm via corepack                                                                                            |
| Install dependencies  | `pnpm install --frozen-lockfile`                                                                                             |
| Build                 | `pnpm run build`                                                                                                             |
| Generate CHANGELOG.md | Runs `scripts/generate-changelog.sh` — reads annotated tag body, prepends entry to `CHANGELOG.md`, writes `release-entry.md` |
| Commit changelog      | Checks out `testing-main`, commits `CHANGELOG.md` update, pushes via `RELEASE_PAT`                                           |
| Create GitHub Release | `gh release create` using `release-entry.md` as release notes; uploads `dist/` / `out/` artifacts                            |

**Secrets required:** `RELEASE_PAT`.

---

### `enable-branch-protection.yml` — Enable Branch Protection

**Triggers:** manual `workflow_dispatch`.

Applies branch protection rules to the comma-separated list of branches provided as input (default: `main,testing-main`).

Rules applied:

- Required status check: `CI` (strict mode)
- Required approving review count: 1
- Stale review dismissal: enabled
- `enforce_admins: false` — the repository owner is exempt and can merge their own PRs

**Secrets required:** `ADMIN_TOKEN` (PAT with `repo` + `admin:repo_hook` scopes).

See `docs/ops/branch_protection.md` for setup steps.

---

### `owner-merge.yml` — Owner Merge PRs

**Triggers:** manual `workflow_dispatch` only.

Allows the repository owner to merge one or more PRs by number, bypassing branch-protection review requirements via `--admin`. Enter a comma-separated list of PR numbers in the workflow input.

**Secrets required:** `ADMIN_TOKEN`.

---

## 📚 Documentation Map

### `docs/`

| File / Folder                   | Contents                                                                                                                                               |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `docs/build.md`                 | Full development workflow — branch naming, commit format, build tags, PR template (Step 6), sprint annotated tag format (Step 7). **Read this first.** |
| `docs/release.md`               | Release automation policy — minor-release trigger, annotated tag structure, changelog generation, secrets setup, `.build_counter` management.          |
| `docs/semver_report.md`         | Semantic versioning specification — build number format `[YY###]`, MINOR/PATCH increment rules, CI pipeline requirements.                              |
| `docs/database.md`              | PouchDB + CouchDB data model decisions, sync strategy, offline-first architecture.                                                                     |
| `docs/provenance.md`            | Provenance hook deep-dive — how `append_provenance.py` works, front-matter format, SKIP rules, manual override.                                        |
| `docs/prompt_main.md`           | AI prompt context and guidelines for contributors using coding assistants.                                                                             |
| `docs/ops/branch_protection.md` | Step-by-step guide to running the branch-protection workflow and configuring `ADMIN_TOKEN`.                                                            |
| `docs/jira/compression.md`      | Compressed Jira-style ticket list — the authoritative source for ticket IDs, acceptance criteria, and department assignments.                          |
| `docs/jira/jira_doc.md`         | Extended Jira ticket documentation with Ghana context and offline-resilience notes.                                                                    |

### `docs/research_dmp/` — Implementation Specs

| File                        | Contents                                                                                                  |
| --------------------------- | --------------------------------------------------------------------------------------------------------- |
| `aquisisions_module.md`     | Week 1 — book intake, bibliographic model, Ghana Curriculum Tag, vendor management.                       |
| `processing_module.md`      | Week 2 — condition scoring, barcode generation, Extension Services routing flag.                          |
| `distribution_module.md`    | Week 3 — section routing, packing slips, depot delivery, rural mode.                                      |
| `library_sections_pi_sg.md` | Week 4 — circulation, patron intelligence, staff governance, Enterprise prep.                             |
| `extension_module.md`       | Extension Services department — mobile library van, QR smart tags, Android app, bulk allocation boundary. |
| `deploy_doc.md`             | Week 5 — field validation, installer packaging, compliance, UAT.                                          |

### `docs/ressources/` — Architecture & Product References

| File                              | Contents                                                                                                                         |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `system_specs.md`                 | Manager vs Enterprise comparison — hardware, software, environment variables, data storage layout.                               |
| `product_specs.md`                | Unified tech stack — Electron, React, Tailwind, PouchDB/CouchDB, build tooling, Ghana adaptations.                               |
| `functionality_specs.md`          | Core feature list and module breakdown.                                                                                          |
| `functionality_specs_expanded.md` | Enhanced features — patron lifecycle, badge system, book degradation engine, programs module, staff governance, batch promotion. |
| `module_functionality_specs.md`   | Per-module feature matrix.                                                                                                       |

---

## ✍️ Commit / PR Etiquette

- One branch per ticket. Never bundle unrelated changes.
- Write commit messages that describe what was built and why — not just what changed.
- Link the ticket number (`LMS-XXX`) in every commit and PR title.
- Do not merge without required approvals and a green CI check.
- Do not force-push to `testing-main` or `main`.

---

## 🛠️ Troubleshooting

**Pre-commit hook not running?**
Re-run the installer: `bash scripts/install_hook.sh` (Unix) or `scripts\install_hook.bat` (Windows).

**Duplicate front-matter appearing in a markdown file?**
Add a `--- … ---` block manually and re-commit — the hook will update it in place from that point on.

**`check_provenance.py` failing in CI?**
Add or update the file header:

```yaml
---
Author: Your Name
Last-updated: YYYY-MM-DD
---
```

For Python/JS/TS files use comment style:

```python
# Author: Your Name
# Last-updated: YYYY-MM-DD
```

**False positives from `detect_agent_provenance.py`?**
Inspect the `evidence` field in the JSON output. Update the `Author:` field in the file's header to your name to override the agent attribution.

**CI flake8 failing?**
Run locally: `python -m flake8 --max-line-length=120 --exclude=.venv` and fix the reported lines before pushing.

**Need to merge a PR as the owner without a reviewer?**
Use the **Owner Merge PRs** workflow in the Actions tab — enter the PR number(s) and run.
