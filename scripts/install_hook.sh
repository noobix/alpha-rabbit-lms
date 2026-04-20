/*
 * Author: Kelvin Kabute
 * Last-updated: 2026-04-19
 */


#!/usr/bin/env bash
set -e
if [ ! -d ".git" ]; then
  echo "Not a git repository. Run from repo root." >&2
  exit 1
fi
PYTHON_CMD=""
# Prefer python3, fall back to python
if command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON_CMD=python
fi

if [ -z "$PYTHON_CMD" ]; then
  echo "Warning: no python executable found (python3/python). Skipping venv creation." >&2
else
  if [ ! -x ".venv/bin/python" ] && [ ! -x ".venv/Scripts/python.exe" ]; then
    echo "Creating virtualenv .venv..."
    "$PYTHON_CMD" -m venv .venv
    echo "Created .venv"
  else
    echo ".venv already exists; skipping venv creation"
  fi
fi

# Copy and make hook executable
if cp hooks/pre-commit .git/hooks/pre-commit; then
  chmod +x .git/hooks/pre-commit || true
  echo "Hook installed to .git/hooks/pre-commit"
else
  echo "Failed to copy hook; ensure you're running from the repository root." >&2
  exit 1
fi
echo "Activate venv: source .venv/bin/activate (or .venv\Scripts\activate on Windows)"
