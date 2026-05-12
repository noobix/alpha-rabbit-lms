---
Author: Kelvin Kabute
Last-updated: 2026-05-12
---

# 🐇 Developer Onboarding

## 🎯 Purpose

Short guide to branch discipline, documentation provenance checks, and PR flow for new contributors.

---

## 🌿 Branching Workflow

- 🏷️ **Feature branches** — Follow the naming convention:
  `LMS-[XXX]/[title-or-description]`
  (e.g., `LMS-101/implement-sha256-hashing-ghana-card-id`)
  where `[XXX]` is the numeric ticket ID from `docs/jira/compression.md`.

- 🎯 **Pick the right branch** — Always work on the feature branch that matches your assigned ticket. Do not make unrelated changes on other branches.

- 🔄 **Before you start coding** — Sync your feature branch with `testing-main`:

  ```bash
  git fetch origin
  git checkout LMS-[XXX]/[title-or-description]
  git merge origin/testing-main
  # Or rebase if your team prefers:
  git rebase origin/testing-main
  ```

- 🚀 **Before pushing** — Commit and push your work:

  ```bash
  git add .
  git commit -m "LMS-[XXX]: feat: short description"
  git push origin LMS-[XXX]/[title-or-description]
  ```

  Then open a pull request targeting `testing-main` (see [Pull Requests](#-pull-requests-and-reviews) below).

---

## 📬 Pull Requests and Reviews

- 🎯 **PR target** — All PRs must target `testing-main`.
- ⏰ **When to open a PR** — After finishing a logical change set and pushing your branch. One PR per feature/issue.
- ✅ **Checks before merge**:
  - CI must pass (`CI` status check).
  - `scripts/check_provenance.py` must pass locally or via CI.
- 🔀 **Merging** — Follow the repository merge policy and required approvals.

---

## 🔍 Documentation Provenance & Agent Detection

### 📜 Project Scripts

| Script                               | Purpose                                                                                                                 |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| `scripts/detect_agent_provenance.py` | Heuristic detector — scans files/directories and outputs JSON-lines with `path`, `agent`, `confidence`, and `evidence`. |
| `scripts/check_provenance.py`        | CI/local checker — fails if tracked source files are missing `Author:` or `Last-updated:` metadata.                     |

### 💻 Local Setup

**Unix / macOS:**

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

### 🕵️ Running Detection

```bash
# Scan docs folder and write a report
python scripts/detect_agent_provenance.py docs/ > provenance-report.jsonl

# Scan the whole repo
python scripts/detect_agent_provenance.py .
```

Each output line is JSON with `path`, `agent`, `confidence`, `evidence`.

### ✅ Running the Provenance Checker

```bash
python scripts/check_provenance.py
```

- Exit code `0` — all checked files contain `Author:` and `Last-updated:` metadata. ✅
- Non-zero exit code — missing metadata; CI will fail. ❌

---

## 🪝 Pre-commit / Automated Hooks

The repository ships a pre-commit hook in `hooks/pre-commit` with platform installers:

| Platform                | Installer                      |
| ----------------------- | ------------------------------ |
| Unix / macOS / Git Bash | `bash scripts/install_hook.sh` |
| Windows (cmd.exe)       | `scripts\install_hook.bat`     |

Run the installer once — the hook will auto-append and validate provenance on every commit.

---

## ✍️ Commit / PR Etiquette

- 🎯 Make focused commits with clear, descriptive messages.
- 🔗 After pushing, open a PR to `testing-main` and link the issue.
- 🔄 Rebase or merge latest `testing-main` if requested by reviewers.
- 🚫 Do not merge your PR without required approvals and passing CI.

---

## 🛠️ Troubleshooting

**False positives from `detect_agent_provenance.py`?**
Inspect the `evidence` field and update front-matter or comments accordingly.

**`check_provenance.py` failing?**
Add or update the file header:

```yaml
---
Author: Your Name
Last-updated: YYYY-MM-DD
---
```
