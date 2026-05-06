---
Author: Kelvin Kabute
Last-updated: 2026-05-06
---

# 🚀 Release Automation: Policy & Implementation

This document defines the automated release workflow for Alpha Rabbit LMS. It assumes the build/tag conventions in `docs/build.md` and `docs/semver_report.md` (lightweight build tags like `[261]` and semantic annotated tags `v<M.m.0`).

## 🎯 Goals

- Create an automatic, auditable release at the end of every sprint.
- Detect when a MINOR version is raised and produce a reproducible annotated release tag.
- Deploy production artifacts from signed, immutable tags.

## 📐 Principles

- Releases are authored as annotated tags (semantic version `vMAJOR.MINOR.PATCH`).
- Lightweight build tags (`[YY###]`) are internal traceability and are referenced inside annotated tag bodies.
- The CI system performs tagging and deployment. Deployments run from tags (not branch tip) for reproducibility.
- Tag creation requires maintainer permissions and GPG signing for production releases.

## 📌 Version baseline

- This project uses a `0` MAJOR baseline during initial development. The first minor release will therefore be `v0.1.0` (PATCH values increment per PR merges). Adjust `package.json` to start at `0.0.0` if not already set so the CI `minor-release` job produces `0.1.0` for the first sprint.

## 📦 Package.json starter (recommended)

Add or maintain a `package.json` at the repository root with a baseline version of `0.0.0`. The CI `minor-release` job will bump the MINOR component to produce `v0.1.0` for the first sprint.

```json
{
  "name": "alpha-rabbit-lms",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "build": "pnpm run build:app || echo 'replace with build command'",
    "release:patch": "node scripts/release-patch.js",
    "release:minor": "node scripts/release-minor.js"
  },
  "engines": {
    "node": ">=18"
  }
}
```

### Notes

- Keep `version` updated by CI on minor releases (optional) or let annotated tags be the authoritative release record.
- If you prefer the repo to be language-agnostic before build tooling is added, include only `name` and `version` fields.

## 🔄 Recommended Flow (high level)

1. During development, feature commits are tagged with a build tag (`[YY###]`) on the feature commit (see `build.md` Step 5).
2. When the sprint is complete, an operator marks the sprint complete by applying the `[minor-release]` label to the sprint completion PR or running a dispatch job.
3. The `minor-release` CI job runs against `testing-main`, aggregates the sprint's build numbers and PR `## Changes` entries, increments the MINOR version, and creates a single annotated tag `v<M.m.0>` with the aggregated body.
4. The annotated tag is pushed to `origin`. The `deploy-on-tag` CI workflow triggers on the pushed `v*.*.*` tag and builds/deploys production artifacts.
5. Optionally (policy decision): fast-forward `main` from `testing-main` or create a merge PR to update `main` so branch history and tags align. Deploys continue to be tag-driven.

## 🔍 Detection rule: how CI knows to create a MINOR annotated tag

- Primary trigger: a PR or manual workflow dispatch that signals sprint completion. Recommended signals:
  - Applying a `[minor-release]` label to the sprint completion PR (mergeable to `testing-main`), OR
  - Running `workflow_dispatch` on the `minor-release` workflow (manual trigger).
- The `minor-release` job runs on `testing-main` (post-merge event or manual dispatch) and:
  - Computes the next MINOR version by reading current version from `package.json` or git tags (prefers authoritative `package.json`) and bumping MINOR, resetting PATCH to 0.
  - Gathers all lightweight build tags included since the last minor release (via `git tag --list '\[2*' --sort=taggerdate` and filtering by taggerdate or taggername range), and builds the annotated tag body using PR `## Changes` sections.
  - Writes the annotated tag body to a temp file (e.g. `sprint-tag-body.txt`) and creates an annotated tag:

```
git tag -a v${NEW_MINOR_VERSION} -F sprint-tag-body.txt
git push origin v${NEW_MINOR_VERSION}
```

## 🌿 Trigger targets (branch policy)

- `testing-main`: used for integration and sprint aggregation. The `minor-release` job should run here (this is where sprint work is merged).
- `main`: production branch. Do not deploy directly from branch pushes; instead, deploy from tags created by the `minor-release` job. Optionally, reconcile `main` with `testing-main` via a controlled merge after release.

## ✅ Why this is standard

- Tag-driven releases are industry best practice: tags are immutable, reproducible, and serve as single-source-of-truth for deploys.
- Running the aggregation job on `testing-main` keeps sprint context localized to integration branch and avoids accidental production hotfix releases.

## 🔒 Security & permissions

- Tag creation and production deployment should require maintainer credentials or a CI service identity scoped to tag creation.
- Consider enabling GPG signing for production tags and restrict who can push signed tags.

## ⚙️ Example `minor-release` GitHub Actions job (concept)

```yaml
# File: .github/workflows/minor-release.yml
name: Minor Release
on:
  workflow_dispatch: {}
  pull_request:
    types: [closed]
    branches: [testing-main]

jobs:
  minor_release:
    if: github.event.pull_request.merged == true || github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Ensure we have tags
        run: git fetch --tags --prune

      - name: Read current version
        id: version
        run: |
          CURRENT=$(jq -r '.version' package.json)
          echo "current=$CURRENT" >> $GITHUB_OUTPUT

      - name: Bump minor version
        id: bump
        run: |
          CURRENT=${{ steps.version.outputs.current }}
          MAJOR=$(echo $CURRENT | cut -d. -f1)
          MINOR=$(echo $CURRENT | cut -d. -f2)
          NEW_MINOR=$((MINOR + 1))
          NEW_VERSION="$MAJOR.$NEW_MINOR.0"
          echo "new_version=$NEW_VERSION" >> $GITHUB_OUTPUT

      - name: Aggregate build tags and PR Changes
        run: |
          # Example: collect lightweight tags and PR bodies since last minor release
          # (Implementation detail: use git tag --list and gh CLI to collect PR bodies)
          echo "Build #[261]\nChanges:\n- Example change" > sprint-tag-body.txt

      - name: Create annotated tag
        env:
          NEW_VERSION: ${{ steps.bump.outputs.new_version }}
        run: |
          git config user.name "CI Bot"
          git config user.email "ci@alpharabbit.dev"
          git tag -a "v${NEW_VERSION}" -F sprint-tag-body.txt
          git push origin "v${NEW_VERSION}"

      - name: Update package.json version and commit (optional)
        run: |
          # Optional: update package.json to reflect new version and push
          npm version ${NEW_VERSION} --no-git-tag-version
          git add package.json
          git commit -m "chore(release): bump version to ${NEW_VERSION}" || echo "no changes"
          git push origin testing-main
```

## 🏷️ Example `deploy-on-tag` workflow (triggered by pushed tag)

```yaml
# File: .github/workflows/deploy-on-tag.yml
name: Deploy on Tag
on:
  push:
    tags:
      - "v*.*.*"

jobs:
  build_and_deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: 18

      - name: Install
        run: pnpm install --frozen-lockfile

      - name: Build
        run: pnpm run build

      - name: Deploy
        run: |
          # Production deployment steps (example)
          # Deploy from tag; this ensures reproducible artifacts
          echo "Deploying ${GITHUB_REF} to production"
```

## 🛠️ Operational notes

- Keep `.build_counter` tracked in repo root and ensure atomic increments (CI updates after tagging).
- Use `gh` CLI to fetch PR bodies and build the annotated tag body programmatically.
- Test the flows with `workflow_dispatch` before relying on event triggers.

## ⏭️ Next steps

- Add the two workflow files (`minor-release.yml`, `deploy-on-tag.yml`) to `.github/workflows/` and implement the aggregation script that builds `sprint-tag-body.txt` from PR `## Changes` sections.
- Add GPG signing and permissions notes for production maintainers.

## 🔐 Secrets: creation and storage

1. Create a Personal Access Token (PAT) for CI tag/commit pushes:

- Scopes: `repo` (full control of private repos), `workflow` (update GitHub Actions workflows), `write:packages` (if publishing packages).
- Save the token as repository secret `RELEASE_PAT` in GitHub Settings → Secrets → Actions.

2. (Optional) Create a GPG key for signing tags:

- Locally: `gpg --full-generate-key` then export `gpg --armor --export-secret-keys YOUR_KEY_ID > gpg-secret.asc`.
- Store the contents of `gpg-secret.asc` as `GPG_PRIVATE_KEY` and the passphrase as `GPG_PASSPHRASE` in repository secrets.

3. (Optional) Deployment tokens (Vercel/Netlify):

- Add `DEPLOY_TOKEN` or provider-specific secrets for automatic deployment.

## 🏠 Where to keep secrets for runtime use in the application

- CI-only secrets (above) must be stored in GitHub Secrets (do not commit to repo). The workflows will expose them to jobs via `${{ secrets.NAME }}`.
- Application runtime secrets (if your app needs API keys at runtime) should not be embedded in the build. For Electron apps, prefer:
  - Use a secure server-side store for secrets and fetch them at runtime over TLS after authenticating the app/user.
  - If short-lived tokens are required at runtime, mint them server-side and inject at app start; do not embed long-lived secrets in the packaged app.

## 📁 Adding the workflows and helper scripts

- I added `.github/workflows/minor-release.yml`, `.github/workflows/deploy-on-tag.yml`, and `scripts/release-aggregate.sh`.
- The `minor-release` workflow runs `scripts/release-aggregate.sh` to produce `sprint-tag-body.txt`, computes the next minor version (using `package.json` if present), tags `vMAJOR.MINOR.0`, pushes the annotated tag, increments `.build_counter`, and optionally updates `package.json` on `testing-main`.
- The `deploy-on-tag` workflow triggers on `v*.*.*` tags, builds the project (run `pnpm run build`) and creates a GitHub Release using `gh` CLI, uploading artifacts from `dist/` or `out/`.

### ✅ Secrets checklist

- `RELEASE_PAT` (required for CI tag/commit pushes)
- `GPG_PRIVATE_KEY` (optional, for tag signing)
- `GPG_PASSPHRASE` (optional)
- `DEPLOY_TOKEN` (optional, for external deploys)
