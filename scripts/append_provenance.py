# 
# Author: Kelvin Kabute
# Last-updated: 2026-04-20
# Provenance-Evidence: low-lexical-uniqueness:0.30, comment-density:0.13, code-tokens:2, long-comment-block

# 
# Author: Kelvin Kabute
# Last-updated: 2026-04-20

# 
# Author: Kelvin Kabute
# Last-updated: 2026-04-20

#!/usr/bin/env python3
"""
Append provenance metadata to staged files. Intended for use from a pre-commit hook.

Behavior:
- Scans staged files (`git diff --cached --name-only --diff-filter=ACM`).
- For each file, runs the detector to see if an agent likely authored it.
- Appends an `Author:` line (append-only) and a `Last-updated:` line.
- If `Last-updated` already equals today's date, assumes agent already appended author; otherwise appends git user name.

This script modifies files and re-adds them to the index when changed.
"""
import subprocess
import sys
import re
from datetime import date
from pathlib import Path

try:
    from scripts.detect_agent_provenance import detect_text
except Exception:
    detect_text = None


EXT_COMMENT_STYLES = {
    # ext: (start, line_prefix, end)
    ".py": ("# ", "# ", ""),
    ".md": ("---\n", "", "\n---\n"),
    ".js": ("/*\n", " * ", "\n */\n"),
    ".ts": ("/*\n", " * ", "\n */\n"),
    ".css": ("/*\n", " * ", "\n */\n"),
    ".json": ("/*\n", " * ", "\n */\n"),
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
    # If the detector isn't importable (hook context), gracefully fall back.
    if detect_text is None:
        return None, 0.0, []
    try:
        return detect_text(text)
    except Exception:
        return None, 0.0, []


def append_header(path: Path, author_line: str, updated_line: str,
                  provenance_agent: str = None, provenance_confidence: float = 0.0,
                  provenance_evidence: list | None = None):
    ext = path.suffix.lower()
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

    header_lines = []
    if start:
        header_lines.append(start.rstrip('\n'))
    if line_prefix:
        header_lines.append(f"{line_prefix}Author: {author_line}".rstrip())
        header_lines.append(f"{line_prefix}Last-updated: {updated_line}".rstrip())
        if provenance_agent:
            header_lines.append(f"{line_prefix}Provenance-Agent: {provenance_agent}".rstrip())
            header_lines.append(f"{line_prefix}Provenance-Confidence: {provenance_confidence:.2f}".rstrip())
        if provenance_evidence:
            ev = ", ".join(str(e) for e in provenance_evidence)
            header_lines.append(f"{line_prefix}Provenance-Evidence: {ev}".rstrip())
    else:
        # YAML front-matter or markdown
        header_lines.append(f"Author: {author_line}")
        header_lines.append(f"Last-updated: {updated_line}")
        if provenance_agent:
            header_lines.append(f"Provenance-Agent: {provenance_agent}")
            header_lines.append(f"Provenance-Confidence: {provenance_confidence:.2f}")
        if provenance_evidence:
            ev = ", ".join(str(e) for e in provenance_evidence)
            header_lines.append(f"Provenance-Evidence: {ev}")

    if end:
        header_lines.append(end.lstrip('\n'))

    header_text = "\n".join([line for line in header_lines if line is not None and line != ""]) + "\n\n"

    # Insert header at top if not present
    if ext == ".md":
        # prepend YAML front matter
        new_content = header_text + content
    else:
        new_content = header_text + content

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
        text = read_file(p)
        if text is None:
            continue

        # check for existing Last-updated
        updated_re = re.compile(r"^Last-updated:\s*(\d{4}-\d{2}-\d{2})$", re.I | re.M)
        updated_match = updated_re.search(text)

        # run detector
        agent, confidence, evidence = detect_agent_for_text(text)

        # choose author: prefer detected agent when confidence >= 0.5
        if agent and confidence >= 0.5:
            author_choice = agent
        else:
            author_choice = git_user

        # If file already updated today, only add missing author; still include provenance
        changed = append_header(p, f"{author_choice}", today,
                                provenance_agent=agent,
                                provenance_confidence=confidence,
                                provenance_evidence=evidence)
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
