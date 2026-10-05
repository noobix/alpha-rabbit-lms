---
Author: Kelvin Kabute
Last-updated: 2026-10-05
---

# Branch protection setup

This document explains how to run the branch-protection workflow at `.github/workflows/enable-branch-protection.yml` and how the sole owner can merge PRs without a second reviewer.

## Policy

`noobix` is the sole developer and repository owner. Two profiles are applied by the workflow:

| Rule                                                | `main`                                                  | `testing-main`             |
| --------------------------------------------------- | ------------------------------------------------------- | -------------------------- |
| Pull request required                               | yes                                                     | yes                        |
| Required approving reviews                          | 1 (dismissed on new pushes, last pusher cannot approve) | 0                          |
| Required checks (strict, branch must be up to date) | `CI Gate`, `Security Gate`, `PR Gate`                   | `CI Gate`, `Security Gate` |
| Conversation resolution required                    | yes                                                     | yes                        |
| Force pushes / deletions                            | blocked                                                 | blocked                    |
| `enforce_admins`                                    | false                                                   | false                      |

- **PR sources into `main`**: only `testing-main`, enforced by `PR Gate`, which also requires the PR body headings Tickets, Summary, Acceptance criteria, Known gaps and Verification.
- **Owner bypass**: because `enforce_admins` is false and GitHub does not let an author approve their own PR, the owner merges unreviewed PRs with the `Owner Merge PRs` workflow. Set `enforce_admins` to true in the workflow to remove this bypass.
- **Only the gate jobs are required**: `CI Gate` and `Security Gate` aggregate every other job and always run, so skipped or renamed jobs can never leave a required check pending.
- The workflow verifies the applied protection after writing it and fails if it differs from the policy above.

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
     -d '{"ref":"main","inputs":{"branches":"main"}}'
   ```

4. Notes
   - The workflow requires admin rights to change branch protection. Use a PAT with appropriate scopes.
   - Run it only after the `CI`, `Security` and `PR Gate` workflows exist on the branch the workflow runs from, so the required check names match real checks.
