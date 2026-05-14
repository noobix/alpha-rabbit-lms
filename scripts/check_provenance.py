# 
# Author: Kelvin Kabute
# Last-updated: 2026-05-14
# Provenance-Evidence: comment-density:0.10, code-tokens:2, long-comment-block

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

EXTS = {".py", ".js", ".ts", ".md", ".yml", ".yaml"}


def files_to_check(root: Path):
    """Yield tracked repository files (via git ls-files) with recognised extensions."""
    result = subprocess.run(
        ["git", "ls-files"],
        capture_output=True, text=True, cwd=root,
    )
    if result.returncode != 0:
        print(
            f"Warning: 'git ls-files' failed (exit {result.returncode}): {result.stderr.strip()}",
            file=sys.stderr,
        )
        return
    for line in result.stdout.splitlines():
        p = root / line.strip()
        if p.suffix.lower() in EXTS and p.is_file():
            yield p


def check_file(p: Path):
    text = p.read_text(encoding='utf-8')
    # Allow optional comment prefix (#, //, *, or combinations thereof) before the key
    has_author = bool(re.search(r"^[#/*\s]*Author:\s*.+$", text, re.I | re.M))
    has_updated = bool(re.search(r"^[#/*\s]*Last-updated:\s*\d{4}-\d{2}-\d{2}$", text, re.I | re.M))
    return has_author, has_updated


def main():
    root = Path('.').resolve()
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


if __name__ == '__main__':
    sys.exit(main())
