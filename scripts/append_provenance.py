#!/usr/bin/env python3
# Author: Kelvin Kabute
# Last-updated: 2026-04-20

"""Append provenance metadata to staged files.

Intended for use from a pre-commit hook. Scans staged files and appends
an `Author:` and `Last-updated:` header when appropriate.
"""

import subprocess
import sys
import re
from datetime import date
from pathlib import Path

from scripts.detect_agent_provenance import detect_text


EXT_COMMENT_STYLES = {
    # ext: (start, line_prefix, end)
    ".py": ("# ", "# ", ""),
    ".md": ("---\n", "", "\n---\n"),
    ".js": ("/*\n", " * ", "\n */\n"),
    ".ts": ("/*\n", " * ", "\n */\n"),
    ".css": ("/*\n", " * ", "\n */\n"),
    ".json": ("/*\n", " * ", "\n */\n"),
}

# Treat YAML files as hash/comment style; default to hash for unknown extensions
EXT_COMMENT_STYLES.update({
    ".yml": ("# ", "# ", ""),
    ".yaml": ("# ", "# ", ""),
})


def get_staged_files():
    p = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"], capture_output=True, text=True)
    if p.returncode != 0:
        print("Failed to list staged files", file=sys.stderr)
        sys.exit(1)
    files = [s.strip() for s in p.stdout.splitlines() if s.strip()]
    return files


def read_file(path: Path):
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return None


def write_file(path: Path, text: str):
    path.write_text(text, encoding="utf-8")


def detect_agent_for_text(text: str):
    agent, confidence, evidence = detect_text(text)
    return agent, confidence, evidence
