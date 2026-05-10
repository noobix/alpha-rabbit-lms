#!/usr/bin/env bash
set -euo pipefail

# generate-changelog.sh
# Reads the annotated tag body from git, formats a changelog entry, and
# prepends it to CHANGELOG.md at the repo root.
#
# Usage (CI): TAG is set via GITHUB_REF_NAME; script requires no arguments.
# Usage (local): ./scripts/generate-changelog.sh v0.1.0
#
# Requirements: git (with full tag history), bash >= 3.2

TAG="${GITHUB_REF_NAME:-${1:-}}"
if [ -z "$TAG" ]; then
  echo "Error: no tag supplied. Set GITHUB_REF_NAME or pass the tag as \$1." >&2
  exit 1
fi

echo "Generating changelog entry for $TAG"

# ── Detect release type ────────────────────────────────────────────────────
# Strip leading 'v' and split into components
VERSION="${TAG#v}"
MAJOR=$(echo "$VERSION" | cut -d. -f1)
MINOR=$(echo "$VERSION" | cut -d. -f2)
PATCH=$(echo "$VERSION" | cut -d. -f3)

IS_MAJOR=false
if [ "$MINOR" = "0" ] && [ "$PATCH" = "0" ]; then
  IS_MAJOR=true
  echo "Major release detected — Breaking Changes section will be included"
fi

# ── Read tag body from git ─────────────────────────────────────────────────
TAG_BODY=$(git for-each-ref "refs/tags/$TAG" --format='%(contents)' 2>/dev/null || true)
if [ -z "$TAG_BODY" ]; then
  echo "Warning: no tag body found for $TAG; creating minimal changelog entry"
  TAG_BODY="(no sprint builds recorded)"
fi

# ── Split tag body into sections ───────────────────────────────────────────
# The tag body produced by release-aggregate.sh has this structure:
#   Build #[…]\nChanges:\n…\n\nContributors:\n@…\n\n---\n\nAppendix: Full PR descriptions\n…

# Extract sprint builds block (everything before "Contributors:" line)
BUILDS_BLOCK=$(echo "$TAG_BODY" | awk '/^Contributors:/{exit} {print}' | sed '/^[[:space:]]*$/d; $a\\')

# Extract contributors block (lines between "Contributors:" and "---")
CONTRIBUTORS_BLOCK=$(echo "$TAG_BODY" | awk '/^Contributors:/{found=1; next} found && /^---/{exit} found{print}' | sed '/^[[:space:]]*$/d')

# Extract appendix (everything after "Appendix: Full PR descriptions")
APPENDIX_BLOCK=$(echo "$TAG_BODY" | awk '/^Appendix: Full PR descriptions/{found=1; next} found{print}')

# ── Extract Breaking Changes for major releases ────────────────────────────
BREAKING_CHANGES=""
if [ "$IS_MAJOR" = "true" ]; then
  # Scan appendix for any "## Breaking Changes" section
  BREAKING_CHANGES=$(echo "$APPENDIX_BLOCK" | awk '/^## Breaking Changes/{found=1; next} found && /^## /{exit} found{print}' | sed '/^[[:space:]]*$/d')
  if [ -z "$BREAKING_CHANGES" ]; then
    BREAKING_CHANGES="_No breaking changes were documented in PR bodies. Update this section before publishing the release notes._"
  fi
fi

# ── Format date ───────────────────────────────────────────────────────────
RELEASE_DATE=$(date -u +%Y-%m-%d)

# ── Build the changelog entry ─────────────────────────────────────────────
{
  echo "## [$TAG] — $RELEASE_DATE"
  echo ""
  echo "### Sprint Builds"
  echo ""
  if [ -n "$BUILDS_BLOCK" ]; then
    echo "$BUILDS_BLOCK"
  else
    echo "_No builds recorded._"
  fi
  echo ""
  echo "### Contributors"
  echo ""
  if [ -n "$CONTRIBUTORS_BLOCK" ]; then
    echo "$CONTRIBUTORS_BLOCK"
  else
    echo "_No contributors recorded._"
  fi
  if [ "$IS_MAJOR" = "true" ]; then
    echo ""
    echo "### ⚠️ Breaking Changes"
    echo ""
    echo "$BREAKING_CHANGES"
  fi
  echo ""
  echo "---"
  echo ""
} > changelog_entry.tmp

# ── Prepend to CHANGELOG.md ───────────────────────────────────────────────
CHANGELOG="CHANGELOG.md"
HEADER='# Changelog

All notable changes to Alpha Rabbit LMS are documented here.
Each entry maps to a semantic version tag and includes the build numbers
delivered in that sprint, the contributors acknowledged in the annotated
tag, and (for major releases) any breaking changes requiring migration steps.

---

'

if [ ! -f "$CHANGELOG" ]; then
  echo "Creating $CHANGELOG"
  printf '%s' "$HEADER" > "$CHANGELOG"
fi

# Detect whether the file already has the standard header (first line starts with "# Changelog")
FIRST_LINE=$(head -n1 "$CHANGELOG")
if echo "$FIRST_LINE" | grep -q '^# Changelog'; then
  # File has header — find insertion point (the first blank line after the last "---" separator in header)
  # Strategy: read header lines until first "## [" entry or end-of-header marker, then insert before it
  TMPFILE=$(mktemp)
  awk -v entry_file="changelog_entry.tmp" '
    !inserted && /^## \[/ {
      while ((getline line < entry_file) > 0) print line
      close(entry_file)
      inserted=1
    }
    { print }
    END {
      if (!inserted) {
        while ((getline line < entry_file) > 0) print line
        close(entry_file)
      }
    }
  ' "$CHANGELOG" > "$TMPFILE"
  mv "$TMPFILE" "$CHANGELOG"
else
  # File exists but has no standard header — prepend header + entry
  TMPFILE=$(mktemp)
  { printf '%s' "$HEADER"; cat changelog_entry.tmp; cat "$CHANGELOG"; } > "$TMPFILE"
  mv "$TMPFILE" "$CHANGELOG"
fi

rm -f changelog_entry.tmp

echo "CHANGELOG.md updated for $TAG"
