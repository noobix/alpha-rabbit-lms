#!/usr/bin/env python3
"""Append simple provenance header to staged text files.

This script is intentionally conservative: it only adds a small YAML-like
header to files that do not already contain a `Last-updated:` marker.

It is safe to run multiple times.
"""
from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path


def get_staged_files() -> list[Path]:
    cmd = ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"]
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0:
        return []
    files = [Path(p) for p in out.stdout.splitlines() if p]
    return files


def is_text_file(path: Path) -> bool:
    try:
        data = path.read_bytes()
    except Exception:
        return False
    # heuristic: if null byte present, consider binary
    return b"\x00" not in data


def ensure_header(path: Path, author: str, today: str) -> bool:
    """Return True if file was modified."""
    if not path.exists() or not is_text_file(path):
        return False

    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return False

    if "Last-updated:" in text:
        return False

    header = f"---\nAuthor: {author}\nLast-updated: {today}\n---\n\n"
    path.write_text(header + text, encoding="utf-8")
    return True


def git_user_name() -> str:
    out = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True)
    name = out.stdout.strip() if out.returncode == 0 else "unknown"
    if not name:
        name = "unknown"
    return name


def main() -> int:
    files = get_staged_files()
    if not files:
        return 0

    today = date.today().isoformat()
    author = git_user_name()
    changed = False

    for p in files:
        # skip virtualenv, git internals, and node_modules
        if any(part.startswith(".venv") or part in (".git", "node_modules") for part in p.parts):
            continue
        if ensure_header(p, author, today):
            changed = True
            # add updated file to index
            subprocess.run(["git", "add", str(p)])

    return 1 if changed else 0


if __name__ == "__main__":
    sys.exit(main())
