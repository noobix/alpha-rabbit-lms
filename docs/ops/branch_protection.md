---
Author: Kelvin Kabute
Last-updated: 2026-05-03
---


# Branch protection setup

This document explains how to run the branch-protection workflow at `.github/workflows/enable-branch-protection.yml` and how the sole owner can merge PRs without a second reviewer.

## Solo-owner merge setup (no second reviewer required)

As the sole owner of this repository, you can merge your own PRs using the **Owner Merge PRs** workflow (`.github/workflows/owner-merge.yml`).

### How to merge PRs as the owner

1. Go to the **Actions** tab of the repository.
2. Select **Owner Merge PRs** in the left sidebar.
3. Click **Run workflow** (top-right dropdown).
4. Select any branch that contains this workflow file (e.g. `copilot/merge-prs-6-7-8` or `testing-main` after the first merge).
5. Enter the comma-separated PR numbers to merge in order (e.g. `6,7,8`).
6. Click **Run workflow**.

The workflow uses your `ADMIN_TOKEN` with the `--admin` flag to bypass all branch-protection requirements (required reviews, status checks, up-to-date branch) and merges the PRs sequentially.

---

## Enable Branch Protection workflow

This workflow applies standard branch-protection rules to `main` and `testing-main`. It is configured for solo-owner development:

- `enforce_admins: false` — repository admins/owners can bypass the protection rules and merge without a second reviewer.
- `required_approving_review_count: 0` — no mandatory review count; the owner can self-merge.
- `required_status_checks` with `strict: true` — PRs must be up-to-date with the base (admins can bypass with `--admin`).

### 1) Create an admin token

- Generate a personal access token (PAT) with `repo` and `admin:repo_hook` or repository administration permissions. Store it as a repository secret named `ADMIN_TOKEN`:

  - Repository -> Settings -> Secrets and variables -> Actions -> New repository secret
  - Name: `ADMIN_TOKEN`
  - Value: your PAT

### 2) Run the workflow (via GitHub UI)

- Open the Actions tab, select `Enable Branch Protection`, click `Run workflow`, adjust branches if needed, and run.

### 3) Run the workflow via curl (example)

Replace `OWNER/REPO` and `WORKFLOW_FILE` as needed and use your PAT in `ADMIN_TOKEN`:

```bash
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR_PAT>" \
  https://api.github.com/repos/OWNER/REPO/actions/workflows/enable-branch-protection.yml/dispatches \
  -d '{"ref":"main","inputs":{"branches":"main,testing-main"}}'
```

### 4) Notes

- The workflow requires admin rights to change branch protection. Use a PAT with appropriate scopes.
- The workflow sets `required_status_checks.contexts` to `CI` — ensure your CI workflow exposes that check name, or adjust the workflow to match your check name.
- After running this workflow, `enforce_admins` is set to `false`, so as the repo owner you can merge PRs without satisfying review or status-check requirements by using the **Owner Merge PRs** workflow.
