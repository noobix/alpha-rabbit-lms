---
Author: Kelvin Kabute
Last-updated: 2026-05-10
---

Per-file Provenance & Implementation Notes
=========================================

This document describes the per-file header template and how the repository detects and appends author/provenance metadata.

Template (recommended): place a short header at the top of each source file. Use the appropriate comment style for the language.

Example (Python):

```python
# Purpose: Brief intent of the module
# Author: github-copilot
# Last-updated: 2026-04-19
```

Example (Markdown YAML front-matter):

---

Purpose: Brief intent of the document
Author: github-copilot
Last-updated: 2026-04-19

---

Rules enforced by the repository tools

- A skill (`agent-provenance-detector`) determines whether an LLM or coding agent likely contributed to a file.
- The pre-commit hook runs `scripts/append_provenance.py` which appends `Author:` and `Last-updated:` lines as needed.
- `Author` entries are append-only: the hook will never remove existing `Author` lines; it will append another `Author` line when new contributors or agents are detected.
- If `Last-updated` already equals today's date, the hook assumes an agent already appended the author; otherwise it appends the git user name.

Skipped extensions
------------------

The following extensions are **never touched** by the appender. Injecting any comment-like text into these files breaks the parser or tool that consumes them.

| Group | Extensions | Reason |
|---|---|---|
| JSON / JSONC | `.json`, `.jsonc` | Comments are invalid JSON; breaks markdownlint, eslint, tsconfig, package.json parsers |
| YAML | `.yaml`, `.yml` | CI configs, Docker Compose, GH Actions — some parsers reject unexpected leading lines |
| TOML | `.toml` | `pyproject.toml`, `Cargo.toml`, Electron builder configs |
| XML / HTML / SVG | `.xml`, `.html`, `.htm`, `.svg` | Strict parsers; DOCTYPE or root element must appear first |
| Plain text / tool config | `.txt`, `.env`, `.ini`, `.cfg`, `.conf` | Consumed verbatim by pip, dotenv, configparser, nginx |
| Lock / generated | `.lock` | Auto-generated and always overwritten; headers would be lost anyway |
| Data | `.csv`, `.tsv` | First line is a header record to data parsers |
| Docker | `.dockerfile` | Named `*.dockerfile`; bare `Dockerfile` has no extension and is already skipped |

Any extension **not** in `EXT_COMMENT_STYLES` inside `scripts/append_provenance.py` is also skipped implicitly, so files with no extension (`Dockerfile`, `Makefile`, `.gitignore`, `hooks/pre-commit`) are safe without needing an explicit entry.

> **Regression guard:** `tests/test_append_provenance.py` asserts that `SKIP_EXTENSIONS` and `SAFE_CODE_EXTS` have zero overlap and that `.json`/`.yml`/`.yaml` are never added to the commentable-file allow-list by mistake.

How to run locally

```bash
python scripts/detect_agent_provenance.py path/to/file
python scripts/append_provenance.py   # runs against staged files
python scripts/check_provenance.py    # CI checker
```

Installer / rollout

- To install the pre-commit hook and create a local virtualenv, run the appropriate installer from the repository root:
  - On Windows (cmd.exe):

    scripts\install_hook.bat

  - On macOS / Linux / Git Bash:

    bash scripts/install_hook.sh

- The installers prefer an existing system `python3` or `python` executable. If no Python is available on PATH the installers will skip venv creation but will still install the hook when possible.

Troubleshooting

- If commits abort with "Python was not found" inside the hook, ensure either:
  - You have a `python` or `python3` executable on your PATH, or
  - You created the repo `.venv` (the hook prefers `.venv/Scripts/python.exe` or `.venv/bin/python`).

- If the hook fails with `ModuleNotFoundError: No module named 'scripts'`, the hook is executed from a different working directory; the hook now runs the appender via `runpy` so this should be resolved. If you still see this error, ensure the hook file at `.git/hooks/pre-commit` matches `hooks/pre-commit` in the repo.

- To manually install the hook without running installers:
  - Copy `hooks/pre-commit` into `.git/hooks/pre-commit` and make it executable.

    On Unix-like systems:

    ```bash
    cp hooks/pre-commit .git/hooks/pre-commit
    chmod +x .git/hooks/pre-commit
    ```

  - On Windows (PowerShell / cmd): copy the file and ensure it is present at `.git\hooks\pre-commit`.

Testing the hook (demo)

- Create and stage a test file, then run `git commit`. The hook will attempt to append `Author:` and `Last-updated:` to staged files and re-add them before the commit completes.

Privacy note

The detection script only reports minimal evidence strings and confidence scores; it does not store raw prompts or sensitive data.
