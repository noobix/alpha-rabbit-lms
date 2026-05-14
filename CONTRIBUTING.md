---
Author: Kelvin Kabute
Last-updated: 2026-05-14
Provenance-Evidence: explanatory phrases: 1, comment-density:0.05, long-comment-block
---


# Contributing

This project uses the Developer Certificate of Origin (DCO) to record
contributors' agreement to the project's contribution terms.

Please sign your commits with the DCO sign-off line. You can do this
automatically by adding `-s` when committing, or add the Signed-off-by
line manually.

Examples:

- Automatic (recommended):

```bash
git commit -s -m "fix: description of change"
```

- Manual (if needed): Add the following line to the end of your commit message:

```text
Signed-off-by: Your Name <your.email@example.com>
```

Why DCO?

- Simple, developer-friendly: the DCO sign-off is a single line that
  declares you have the right to contribute the work and that you agree
  to the project's license.
- Easy to automate: CI can check for the presence of the Signed-off-by line.

Optional: Use a CLA if you need legal assignment/licensing control over
contributions — we can add a CLA later.

DCO enforcement (recommended CI step)

- Add a simple CI check that fails the build if commits are missing the
  Signed-off-by line. See <https://github.com/probot/dco> for an example
  GitHub App integration.
