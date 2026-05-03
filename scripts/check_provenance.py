#!/usr/bin/env python3
# Author: Kelvin Kabute
# Last-updated: 2026-04-20

"""
Simple CI checker: fails if tracked source files lack `Author:` or `Last-updated:` metadata.

Run in CI before merge: `python scripts/check_provenance.py`
"""
import subprocess
import sys
import re
from pathlib import Path

EXTS = {".py", ".js", ".ts", ".md"}

# Regex that matches Author/Last-updated regardless of comment prefix
# Handles: bare (YAML), # (Python/YAML/shell), * (JS/CSS block), // (JS inline)
_AUTHOR_RE = re.compile(r"^[#\s*/!-]*Author:\s*.+$", re.I | re.M)
_UPDATED_RE = re.compile(r"^[#\s*/!-]*Last-updated:\s*\d{4}-\d{2}-\d{2}$", re.I | re.M)


def files_to_check(root: Path):
    """Yield git-tracked source files with recognised extensions."""
    result = subprocess.run(
        ["git", "ls-files"],
        capture_output=True, text=True, cwd=root,
    )
    if result.returncode != 0:
        return
    for line in result.stdout.splitlines():
        p = root / line.strip()
        if p.suffix.lower() in EXTS and p.is_file():
            yield p


def check_file(p: Path):
    try:
        text = p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"  WARNING: could not read {p}: {exc}", file=sys.stderr)
        return False, False
    has_author = bool(_AUTHOR_RE.search(text))
    has_updated = bool(_UPDATED_RE.search(text))
    return has_author, has_updated


def main():
    root = Path(".").resolve()
    missing = []
    for p in files_to_check(root):
        a, u = check_file(p)
        if not (a and u):
            missing.append((p, a, u))

    if missing:
        print("Files missing provenance metadata:")
        for p, a, u in missing:
            print(f" - {p}: Author={'OK' if a else 'MISSING'}, Last-updated={'OK' if u else 'MISSING'}")
        return 2
    print("All checked files contain Author and Last-updated metadata.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
