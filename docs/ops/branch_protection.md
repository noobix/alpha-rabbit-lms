---
Author: Kelvin Kabute
Last-updated: 2026-05-12
---

# Branch protection setup

This document explains how to run the branch-protection workflow added at `.github/workflows/enable-branch-protection.yml`.

## Solo-owner policy

`noobix` is the sole developer and repository owner. The protection rules reflect this:

- **Required approving reviews: 0** — the owner merges their own PRs directly; no second reviewer exists or is required.
- **enforce_admins: false** — the owner is exempt from protection rules and can merge without restriction.
- **Required status checks: CI (strict)** — all PRs must pass CI before merging.
- **PRs required** — all changes to `testing-main` must go through a pull request; direct push is blocked.

Do **not** raise `required_approving_review_count` above `0` unless additional developers with write access join the project.

1. Create an admin token
   - Generate a personal access token (PAT) with `repo` and `admin:repo_hook` or repository administration permissions. Store it as a repository secret named `ADMIN_TOKEN`:
     - Repository -> Settings -> Secrets and variables -> Actions -> New repository secret
     - Name: `ADMIN_TOKEN`
     - Value: your PAT

2. Run the workflow (via GitHub UI)
   - Open the Actions tab, select `Enable Branch Protection`, click `Run workflow`, adjust branches if needed, and run.

3. Run the workflow via curl (example)

   Replace `OWNER/REPO` and `WORKFLOW_FILE` as needed and use your PAT in `ADMIN_TOKEN`:

   ```bash
   curl -X POST \
     -H "Accept: application/vnd.github+json" \
     -H "Authorization: Bearer <YOUR_PAT>" \
     https://api.github.com/repos/OWNER/REPO/actions/workflows/enable-branch-protection.yml/dispatches \
     -d '{"ref":"main","inputs":{"branches":"main,testing-main"}}'
   ```

4. Notes
   - The workflow requires admin rights to change branch protection. Use a PAT with appropriate scopes.
   - The workflow sets `required_status_checks.contexts` to `CI` — ensure your CI workflow exposes that check name, or adjust the workflow to match your check name.
