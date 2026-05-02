#!/usr/bin/env python3
# Author: Kelvin Kabute
# Last-updated: 2026-04-20

"""
Simple CI checker: fails if tracked source files lack `Author:` or `Last-updated:` metadata.

Run in CI before merge: `python scripts/check_provenance.py`
"""
import sys
import re
import subprocess
from pathlib import Path

EXTS = [".py", ".js", ".ts", ".md"]


def files_to_check(root: Path):
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        excluded_dirs = {".git", ".venv", "venv", "node_modules", "vendor", "dist"}
        for ext in EXTS:
            for p in root.rglob(f"*{ext}"):
                if p.is_file() and not any(part in excluded_dirs for part in p.parts):
                    yield p
        return

    for rel_path in result.stdout.splitlines():
        p = root / rel_path
        if p.is_file() and p.suffix in EXTS:
            yield p


def check_file(p: Path):
    text = p.read_text(encoding='utf-8')
    has_author = bool(re.search(r"^\s*(?:(?:#|//|\*)\s*)*Author:\s*.+$", text, re.I | re.M))
    has_updated = bool(re.search(r"^\s*(?:(?:#|//|\*)\s*)*Last-updated:\s*\d{4}-\d{2}-\d{2}$", text, re.I | re.M))
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
