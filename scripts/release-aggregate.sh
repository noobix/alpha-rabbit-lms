#!/usr/bin/env bash
set -euo pipefail

# release-aggregate.sh
# Collect merged PRs since last minor release and assemble sprint-tag-body.txt

REPO="${GITHUB_REPOSITORY:-$(git config --get remote.origin.url | sed -E 's#.*/([^/]+/[^/]+)(\.git)?$#\1#')}"

echo "Repository: $REPO"

# Find last annotated semantic tag (vMAJOR.MINOR.PATCH)
LAST_TAG=$(git tag --list "v*.*.*" --sort=-v:refname | head -n1 || true)
echo "Last tag: ${LAST_TAG:-<none>}"

if [ -n "$LAST_TAG" ]; then
  SINCE_DATE=$(git log -1 --format=%aI "$LAST_TAG")
else
  SINCE_DATE="1970-01-01T00:00:00Z"
fi

echo "Collecting PRs merged after $SINCE_DATE"

# Requires gh CLI and jq
PR_JSON=$(gh pr list --state merged --base testing-main --json number,mergeCommit,headRefOid,mergedAt --limit 1000)

echo "[]" > pr_pluck.json
echo "$PR_JSON" | jq --arg since "$SINCE_DATE" '[.[] | select(.mergedAt > $since) ]' > pr_pluck.json

COUNT=$(jq 'length' pr_pluck.json)
echo "Found $COUNT merged PR(s) since last tag"

> sprint-tag-body.txt

for i in $(jq -r '.[].number' pr_pluck.json); do
  echo "Processing PR #$i"
  PR_BODY=$(gh pr view $i --json body,title,mergeCommit,headRefOid --jq '.body')
  PR_TITLE=$(gh pr view $i --json body,title --jq '.title')
  MERGE_SHA=$(gh pr view $i --json mergeCommit --jq '.mergeCommit.oid')
  HEAD_SHA=$(gh pr view $i --json headRefOid --jq '.headRefOid')

  # Try to find a lightweight build tag that points at merge commit or head commit
  BUILD_TAG=""
  if [ -n "$MERGE_SHA" ] && [ "$MERGE_SHA" != "null" ]; then
    BUILD_TAG=$(git tag --points-at "$MERGE_SHA" | grep '^\[' | head -n1 || true)
  fi
  if [ -z "$BUILD_TAG" ] && [ -n "$HEAD_SHA" ] && [ "$HEAD_SHA" != "null" ]; then
    BUILD_TAG=$(git tag --points-at "$HEAD_SHA" | grep '^\[' | head -n1 || true)
  fi

  if [ -z "$BUILD_TAG" ]; then
    BUILD_TAG="[unassigned]"
  fi

  echo "Build #${BUILD_TAG}" >> sprint-tag-body.txt
  echo "Changes:" >> sprint-tag-body.txt
  # Extract a concise paraphrase: use first paragraph of PR body
  PARAPHRASE=$(echo "$PR_BODY" | awk 'BEGIN{RS="\n\n"} NR==1{print; exit}')
  if [ -z "$PARAPHRASE" ]; then
    PARAPHRASE="- ${PR_TITLE}"
  else
    # prefix lines with - for bullet
    PARAPHRASE=$(echo "$PARAPHRASE" | sed -E 's/^/- /')
  fi
  echo "$PARAPHRASE" >> sprint-tag-body.txt
  echo "" >> sprint-tag-body.txt
done

# Append full PR descriptions as appendix
echo "\n---\n\nAppendix: Full PR descriptions" >> sprint-tag-body.txt
for i in $(jq -r '.[].number' pr_pluck.json); do
  PR_BODY=$(gh pr view $i --json body,title --jq '.body')
  echo "[Full PR description for Build #[${i}] — PR#$i]" >> sprint-tag-body.txt
  echo "$PR_BODY" >> sprint-tag-body.txt
  echo "" >> sprint-tag-body.txt
done

echo "Wrote sprint-tag-body.txt"
