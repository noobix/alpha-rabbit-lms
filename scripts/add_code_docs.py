# Author: Kelvin Kabute
# Last-updated: 2026-05-03

# Author: Kelvin Kabute
# Last-updated: 2026-05-03

#!/usr/bin/env python3
"""
Add simple module/file doc headers to code files only.

Usage:
  python scripts/add_code_docs.py --dry-run <path>
  python scripts/add_code_docs.py --apply <path>

The script will:
 - Walk the given path (file or directory)
 - Operate only on recognized code file extensions (py, js, ts, java, go, rs, c, cpp, h, cs, php, rb)
 - For Python files: insert a module-level triple-quoted docstring if missing
 - For other code files: insert a top-of-file comment header using the language's line comment style
 - Skip non-code files (markdown, json, txt, etc.)

This is conservative by design: it only inserts top-of-file headers and does not
attempt to modify function/class bodies to avoid risky edits.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List, Tuple

CODE_EXTS = {
    ".py",
    ".js",
    ".ts",
    ".java",
    ".go",
    ".rs",
    ".c",
    ".cpp",
    ".cc",
    ".h",
    ".hpp",
    ".cs",
    ".php",
    ".rb",
}

LINE_COMMENT = {
    ".py": "#",
    ".rb": "#",
    ".sh": "#",
    ".js": "//",
    ".ts": "//",
    ".java": "//",
    ".go": "//",
    ".rs": "//",
    ".c": "//",
    ".cpp": "//",
    ".cc": "//",
    ".h": "//",
    ".hpp": "//",
    ".cs": "//",
    ".php": "//",
}


def iter_targets(paths: Iterable[Path]) -> Iterable[Path]:
    IGNORE_DIRS = {".venv", "venv", "env", "node_modules", "build", "dist", ".git", "__pycache__"}
    for p in paths:
        if p.is_dir():
            for f in p.rglob("*"):
                if not f.is_file():
                    continue
                # skip files in vendor/virtualenv/build directories
                if any(part in IGNORE_DIRS for part in f.parts):
                    continue
                if f.suffix.lower() in CODE_EXTS:
                    yield f
        else:
            if p.is_file() and p.suffix.lower() in CODE_EXTS:
                if not any(part in {".venv", "venv", "env"} for part in p.parts):
                    yield p


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf8")


def has_python_module_doc(text: str) -> bool:
    # Skip shebang or encoding lines, then check if the first non-blank is a triple-quoted string
    lines = text.splitlines()
    i = 0
    # skip shebang and encoding comments
    while i < len(lines) and (lines[i].startswith("#!") or lines[i].lstrip().startswith("#")):
        i += 1
    # skip blank lines
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i >= len(lines):
        return False
    first = lines[i].lstrip()
    return first.startswith('"""') or first.startswith("'''")


def insert_python_module_doc(path: Path, text: str, apply: bool) -> Tuple[bool, str]:
    if has_python_module_doc(text):
        return False, text
    # preserve shebang/encoding/comments at top
    lines = text.splitlines(True)
    i = 0
    header = """Module summary.

TODO: add module description.
"""

    # keep initial shebang and encoding comments
    prefix: List[str] = []
    while i < len(lines) and (lines[i].startswith("#!") or lines[i].lstrip().startswith("#")):
        prefix.append(lines[i])
        i += 1

    new_text = "".join(prefix) + '"""' + "\n" + header + '"""' + "\n\n" + "".join(lines[i:])
    if apply:
        path.write_text(new_text, encoding="utf8")
    return True, new_text


def insert_generic_header(path: Path, text: str, apply: bool) -> Tuple[bool, str]:
    suffix = path.suffix.lower()
    comment = LINE_COMMENT.get(suffix, "//")
    # Check first non-blank line; if it already starts with the comment
    # and contains 'Module' or 'SUMMARY', assume present
    for ln in text.splitlines():
        if not ln.strip():
            continue
        if (
            ln.lstrip().startswith(comment)
            and (
                "module" in ln.lower()
                or "summary" in ln.lower()
                or "todo" in ln.lower()
            )
        ):
            return False, text
        break

    header_lines = [
        f"{comment} Module: {path.name} - TODO: add description",
        f"{comment}\n",
    ]
    new_text = "\n".join(header_lines) + "\n" + text
    if apply:
        path.write_text(new_text, encoding="utf8")
    return True, new_text


def process_file(path: Path, apply: bool) -> Tuple[Path, bool, str]:
    text = read_text(path)
    if path.suffix.lower() == ".py":
        changed, new_text = insert_python_module_doc(path, text, apply)
        return path, changed, new_text
    else:
        changed, new_text = insert_generic_header(path, text, apply)
        return path, changed, new_text


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Add conservative top-of-file doc headers to code files only.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true", help="Show proposed changes without writing files")
    g.add_argument("--apply", action="store_true", help="Apply changes to files")
    ap.add_argument("paths", nargs="+", help="Files or directories to scan")
    args = ap.parse_args(argv)

    paths = [Path(p) for p in args.paths]
    targets = list(iter_targets(paths))
    if not targets:
        print("No code files found in the provided paths.")
        return 0

    any_changed = False
    for f in targets:
        try:
            p, changed, _ = process_file(f, apply=args.apply)
            if changed:
                any_changed = True
                if args.dry_run:
                    print(f"[DRY] Would add header to: {p}")
                else:
                    print(f"Updated: {p}")
        except Exception as exc:  # conservative: report and continue
            print(f"Error processing {f}: {exc}")

    if not any_changed:
        print("No missing headers detected.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
