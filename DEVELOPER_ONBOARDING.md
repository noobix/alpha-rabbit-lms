---
Author: Kelvin Kabute
Last-updated: 2026-05-14
Provenance-Evidence: comment-density:0.08, long-comment-block
---

# Developer Onboarding

## Purpose

Short guide to branch discipline, documentation provenance checks, and PR flow for new contributors.

## Branching workflow

- **Feature branches**: All feature branches must be created before product launch and follow the naming convention: `feature/<short-description>` (e.g., `feature/ui-course-list`).
- **Pick the appropriate branch**: Always work on the feature branch that corresponds to the task you were assigned. Do not create unrelated changes on other branches.
- **Before you start coding**: Sync your feature branch with `develop` (or `testing-main` if your workflow uses that):
  - Fetch latest remote changes: `git fetch origin`
  - Switch to your feature branch: `git checkout feature/<name>`
  - Merge latest `develop` into your branch: `git merge origin/develop`
  - (Or rebase if your team prefers): `git rebase origin/develop`
- **At the end of work / before pushing**:
  - Commit locally with meaningful messages: `git add . && git commit -m "feat: short description"`
  - Push your feature branch: `git push origin feature/<name>`
  - Open a pull request targeting `develop` (see PR guidance below).

## Pull requests and reviews

- **PR target**: All PRs must target `develop`.
- **When to open a PR**: After finishing a logical change set and pushing your branch. One PR per feature/issue.
- **Checks before merge**:
  - Ensure CI passes (`CI` status check).
  - Ensure `scripts/check_provenance.py` passes locally (see below) or CI must run it.
- **Merging**: Use the repository's merge policy and follow required approvals.

## Documentation provenance & agent detection (documentation workflow)

- Project scripts:
  - `scripts/detect_agent_provenance.py` — heuristic detector that scans files or directories and outputs JSON-lines with `path`, `agent`, `confidence`, and `evidence`.
  - `scripts/check_provenance.py` — CI/local checker that fails if tracked source files are missing `Author:` or `Last-updated:` metadata.
- Recommended local setup (Windows / macOS / Linux):
  - Create and activate virtualenv:
    - Unix/macOS:
      ```bash
      python3 -m venv .venv
      source .venv/bin/activate
      ```
    - Windows (PowerShell):
      ```powershell
      python -m venv .venv
      .\.venv\Scripts\Activate.ps1
      ```
  - Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
- How to run detection:
  - Scan the docs folder and write a report:
    ```bash
    python scripts/detect_agent_provenance.py docs/ > provenance-report.jsonl
    ```
  - Scan the whole repo:
    ```bash
    python scripts/detect_agent_provenance.py .
    ```
  - Interpret output: each line is JSON with `path`, `agent`, `confidence`, `evidence`.
- How to run provenance checker:

  ```bash
  python scripts/check_provenance.py
  ```

  - Exit code `0` means all checked files contain `Author:` and `Last-updated:` metadata.
  - Non-zero exit code indicates missing metadata (CI should fail on this).

## Pre-commit / automated hooks

- The repository includes a pre-commit hook in `hooks/pre-commit` and installers:
  - Unix: `scripts/install_hook.sh`
  - Windows: `scripts/install_hook.bat`
- Install the hook locally (or run the installer) to auto-append/validate provenance on commit.

## Commit / PR etiquette

- Make focused commits with clear messages.
- After pushing your branch open a PR to `develop` and link the issue.
- Rebase or merge latest `develop` into your branch if requested by reviewers.
- Do not merge your PR without required approvals and passing CI.

## Troubleshooting

- If `scripts/detect_agent_provenance.py` reports false positives, inspect the `evidence` field and update front-matter or comments accordingly.
- If `scripts/check_provenance.py` fails, add or update the file header:
  ```
  ---
  Author: Your Name
  Last-updated: YYYY-MM-DD
  ---
  ```

---

_If you'd like, I can open a PR for this file and follow up to merge it._
