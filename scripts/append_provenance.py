#!/usr/bin/env python3
# Author: Kelvin Kabute
# Last-updated: 2026-05-12

# Author: Kelvin Kabute
# Last-updated: 2026-05-11

# Author: Kelvin Kabute
# Last-updated: 2026-05-10

# Author: Kelvin Kabute
# Last-updated: 2026-05-10

# Author: Kelvin Kabute
# Last-updated: 2026-05-10

# Author: Kelvin Kabute
# Last-updated: 2026-05-04

"""Append provenance metadata to staged files.

Intended for use from a pre-commit hook. Scans staged files and appends
an `Author:` and `Last-updated:` header when appropriate.
"""

import subprocess
import sys
from pathlib import Path
import re
from datetime import date
from typing import List

from scripts.detect_agent_provenance import detect_text


EXT_COMMENT_STYLES = {
    # ext: (start, line_prefix, end)
    # For Python we prefer inline `#` lines inserted after any shebang/encoding.
    ".py": ("", "# ", ""),
    ".md": ("---\n", "", "\n---\n"),
    ".js": ("/*\n", " * ", "\n */\n"),
    ".ts": ("/*\n", " * ", "\n */\n"),
    ".css": ("/*\n", " * ", "\n */\n"),
}

# Parsed / structured / config formats that must never receive a provenance
# header — injecting any comment-like text into these files breaks the parser
# or tool that consumes them.  Any extension NOT in EXT_COMMENT_STYLES above
# is also skipped implicitly by the SAFE_CODE_EXTS guard in main().
SKIP_EXTENSIONS = {
    # JSON variants — comments are invalid JSON/JSONC
    ".json", ".jsonc",
    # YAML — CI configs, Docker Compose, GH Actions; strict multi-doc parsers
    ".yaml", ".yml",
    # TOML — pyproject.toml, Cargo.toml, electron-builder configs
    ".toml",
    # XML / HTML / SVG — DOCTYPE or root element must be first byte
    ".xml", ".html", ".htm", ".svg",
    # Plain-text files consumed directly by tools (pip, dotenv, etc.)
    ".txt", ".env", ".ini", ".cfg", ".conf",
    # Lock / generated — auto-overwritten, never hand-edited
    ".lock",
    # Data formats — first line is a header record to parsers
    ".csv", ".tsv",
    # Named Dockerfile variants (bare Dockerfile has no ext — already skipped)
    ".dockerfile",
}

# Commentable source extensions the appender is allowed to touch
SAFE_CODE_EXTS = set(EXT_COMMENT_STYLES.keys())

# Specific filenames (case-insensitive basename) that must never receive a
# provenance header, regardless of extension.  Covers generated changelogs,
# canonical license/notice files, and other root-level files whose first
# line carries structural meaning consumed by tooling.
SKIP_FILENAMES = {
    "changelog.md",
    "about.md",
    "contributing.md",
    "license",
    "license.md",
    "license.txt",
    "notice",
    "notice.md",
    "authors",
    "authors.md",
}

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


def append_header(path: Path, author_line: str, updated_line: str):
    ext = path.suffix.lower()
    # Refuse to touch parsed/config formats even when called directly.
    if ext in SKIP_EXTENSIONS or ext not in SAFE_CODE_EXTS:
        return False
    content = read_file(path)
    if content is None:
        return False

    # find existing author/last-updated
    author_re = re.compile(r"^Author:\s*(.+)$", re.I | re.M)
    updated_re = re.compile(r"^Last-updated:\s*(\d{4}-\d{2}-\d{2})$", re.I | re.M)

    has_author = bool(author_re.search(content))
    updated_match = updated_re.search(content)
    today = date.today().isoformat()

    # If already today's update, do not overwrite; just ensure author exists
    if updated_match and updated_match.group(1) == today:
        if has_author:
            return False
        # append author near existing header block if possible

    # Compose header block according to file type
    start, line_prefix, end = EXT_COMMENT_STYLES.get(ext, ("/*\n", " * ", "\n */\n"))

    def make_comment_lines(prefix: str) -> List[str]:
        if prefix:
            return [f"{prefix}Author: {author_line}".rstrip(), f"{prefix}Last-updated: {updated_line}".rstrip()]
        return [f"Author: {author_line}", f"Last-updated: {updated_line}"]

    # Preserve shebang / encoding lines at top
    lines = content.splitlines(True)
    i = 0
    prefix_lines: List[str] = []
    while i < len(lines) and (
        lines[i].startswith("#!")
        or lines[i].lstrip().startswith("# -*-")
        or lines[i].lstrip().startswith("# coding")
        or not lines[i].strip()
    ):
        prefix_lines.append(lines[i])
        i += 1

    rest = "".join(lines[i:])
    # If Python and first non-prefix is a multi-line module docstring, inject metadata inside it
    if ext == ".py":
        # detect triple-quoted docstring
        stripped = rest.lstrip()
        if stripped.startswith('"""') or stripped.startswith("'''"):
            quote = '"""' if stripped.startswith('"""') else "'''"
            # find opening position, then closing position after that
            open_pos = rest.find(quote)
            close_pos = rest.find(quote, open_pos + len(quote))
            if open_pos != -1 and close_pos != -1:
                # determine if multi-line docstring by checking newline positions
                open_line = rest.count("\n", 0, open_pos)
                close_line = rest.count("\n", 0, close_pos)
                if close_line > open_line:
                    # multi-line docstring — insert metadata after opening quote line
                    rest_lines = rest.splitlines(True)
                    open_line_idx = None
                    for idx, ln in enumerate(rest_lines):
                        if quote in ln:
                            open_line_idx = idx
                            break
                    if open_line_idx is not None:
                        insert_at = open_line_idx + 1
                        comment_block = [f"Author: {author_line}\n", f"Last-updated: {updated_line}\n"]
                        # only insert if not already present in the first few lines
                        doc_slice = "".join(rest_lines[open_line_idx:open_line_idx+5])
                        if ("Author:" not in doc_slice) and ("Last-updated:" not in doc_slice):
                            for j, cb in enumerate(comment_block):
                                rest_lines.insert(insert_at + j, cb)
                            new_rest = "".join(rest_lines)
                            new_content = "".join(prefix_lines) + new_rest
                            write_file(path, new_content)
                            return True
        # fallback: insert simple # comment block after prefix_lines
        comment_lines = make_comment_lines(line_prefix)
        header_text = "\n".join(comment_lines) + "\n\n"
        new_content = "".join(prefix_lines) + header_text + rest
        write_file(path, new_content)
        return True

    # Markdown: update existing YAML frontmatter in-place; prepend a new block only when none exists.
    if ext == ".md":
        fm_re = re.compile(r'^---\r?\n(.*?\n)---[ \t]*\r?\n', re.DOTALL)
        fm_match = fm_re.match(content)
        if fm_match:
            fm_body = fm_match.group(1)
            # Update Last-updated in-place
            lu_re_inner = re.compile(r'^Last-updated:.*$', re.M | re.I)
            if lu_re_inner.search(fm_body):
                new_fm_body = lu_re_inner.sub(f'Last-updated: {updated_line}', fm_body)
            else:
                new_fm_body = fm_body.rstrip('\n') + f'\nLast-updated: {updated_line}\n'
            # Update Author in-place (or add it if missing)
            au_re_inner = re.compile(r'^Author:.*$', re.M | re.I)
            if au_re_inner.search(new_fm_body):
                new_fm_body = au_re_inner.sub(f'Author: {author_line}', new_fm_body)
            else:
                new_fm_body = f'Author: {author_line}\n' + new_fm_body
            new_content = f'---\n{new_fm_body}---\n' + content[fm_match.end():]
            if new_content == content:
                return False
            write_file(path, new_content)
            return True
        else:
            # No frontmatter block found — prepend a new one
            new_content = f'---\nAuthor: {author_line}\nLast-updated: {updated_line}\n---\n\n' + content
            write_file(path, new_content)
            return True

    # Generic comment insertion for other languages: preserve prefix_lines then insert comment block
    comment_lines = make_comment_lines(line_prefix)
    header_text = "\n".join(comment_lines) + "\n\n"
    new_content = "".join(prefix_lines) + header_text + rest
    write_file(path, new_content)
    return True


def git_add(path: str):
    subprocess.run(["git", "add", path])


def get_git_user():
    p = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True)
    if p.returncode != 0:
        return None
    return p.stdout.strip()


def main():
    files = get_staged_files()
    if not files:
        print("No staged files to process.")
        return 0

    today = date.today().isoformat()
    git_user = get_git_user() or "Unknown"
    modified = []

    for f in files:
        p = Path(f)
        if not p.exists():
            continue
        # Only modify recognized commentable source files.
        # SKIP_EXTENSIONS is an explicit deny-list for parsed/config formats.
        # SAFE_CODE_EXTS is the implicit allow-list derived from EXT_COMMENT_STYLES.
        ext = p.suffix.lower()
        if ext in SKIP_EXTENSIONS or ext not in SAFE_CODE_EXTS:
            continue
        if p.name.lower() in SKIP_FILENAMES:
            continue
        text = read_file(p)
        if text is None:
            continue

        # check for existing Last-updated
        updated_re = re.compile(r"^Last-updated:\s*(\d{4}-\d{2}-\d{2})$", re.I | re.M)
        updated_match = updated_re.search(text)

        # run detector
        agent, confidence, evidence = detect_agent_for_text(text)

        # decide author to append
        if updated_match and updated_match.group(1) == today:
            # assume agent already appended; if no author but agent detected, append agent
            author_to_append = agent if agent else git_user
        else:
            # not updated today: use git user
            author_to_append = git_user

        # Append author (append-only) and last-updated (today)
        changed = append_header(p, f"{author_to_append}", today)
        if changed:
            git_add(str(p))
            modified.append(str(p))

    if modified:
        print("Updated files:")
        for m in modified:
            print(" -", m)
    else:
        print("No files changed by provenance appender.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
