---
Author: Kelvin Kabute
Last-updated: 2026-05-05
---

# Stage 05 — Testing

Canonical skill files: `.github/skills/gsd-{name}/SKILL.md`
Canonical agent files: `.github/agents/gsd-{name}.agent.md`

---

## ACCESS RESTRICTION — PLANNING CONTEXT

This stage is blocked during the Copilot planning context. Skills and agents in this stage operate on implemented code. They must not be invoked during a planning session.

A testing stage resource becomes accessible only after the coding stage has produced committed implementation and the phase executor has written a SUMMARY.md for the phase.

---

## When to use this stage

You are in the Testing stage when code has been implemented and needs to be validated, verified, audited, debugged, or security-reviewed. Testing in GSD is not just automated test suites — it includes conversational UAT against real behavior, goal-backward verification that the implementation actually achieves the phase goal, multi-cycle debugging sessions with persistent state, and retroactive audits of security, accessibility, and evaluation coverage.

The recommended order within this stage for a newly completed phase is: code review first (catches mechanical issues before deeper review), then verify-work (UAT against the phase goal), then add-tests (generates test suites based on what was verified), then secure-phase (security threat verification), and finally validate-phase (Nyquist coverage audit). Not every phase requires all of these — a simple configuration change might need only verify-work. A phase building an AI feature should always run eval-review.

---

## Skills in this stage

### gsd-add-tests

`gsd-add-tests` generates unit and end-to-end test suites for a completed phase. It sources its specifications from SUMMARY.md, CONTEXT.md, and VERIFICATION.md — not from reading the implementation code directly — which means tests are written against the stated behavior rather than against the implementation details. This avoids tautological tests (tests that pass because they replicate the implementation rather than because they verify the behavior).

The skill classifies each implementation file into one of three categories: TDD (suitable for unit tests), E2E (suitable for browser-driven end-to-end tests), or Skip (infrastructure, configuration, or generated files that should not be directly tested). It presents this classification plus a test plan to the user for approval before generating any test code. RED-GREEN conventions are enforced: tests are written to be initially failing (RED) until the tested behavior is correctly implemented, then passing (GREEN). The commit message is standardized: `test(phase-{N}): add unit and E2E tests from add-tests command`.

```bash
/gsd-add-tests 3
```

Canonical path: `.github/skills/gsd-add-tests/SKILL.md`

### gsd-verify-work

`gsd-verify-work` is conversational UAT (User Acceptance Testing) against implemented features. It tests one scenario at a time in plain text, asking the developer to observe and report what they see in the running application. It does not run automated tests — it guides the developer through manual verification that the implemented behavior matches what the phase goal described.

When an issue is found during UAT, the skill automatically diagnoses it, creates a targeted gap-closure plan with `gap_closure: true` in the plan frontmatter, and marks the failed scenario in the UAT record. After all scenarios are tested, the executor re-runs with `gsd-execute-phase --gaps-only` to address the identified gaps. The UAT record is then re-verified for the fixed scenarios.

The phase number is optional — the skill defaults to the active phase or prompts if it cannot determine it automatically.

```bash
/gsd-verify-work
/gsd-verify-work 3
```

Output: `{phase_num}-UAT.md` in the phase directory.

Canonical path: `.github/skills/gsd-verify-work/SKILL.md`

### gsd-validate-phase

`gsd-validate-phase` performs a retroactive Nyquist validation audit for a completed phase. The Nyquist principle applied to software testing states that you need at least two test points per behavioral frequency — meaning that for every behavioral claim in the PLAN.md, there should be at least two independent verifiable test scenarios (ideally one positive-path and one negative-path or edge-case test). The audit finds gaps in this coverage and fills them.

The skill has three entry states based on what artifacts exist. If VALIDATION.md already exists for the phase, the skill audits it for coverage gaps and fills them. If VALIDATION.md does not exist but SUMMARY.md does, the skill reconstructs the phase's verification requirements from all available artifacts and then runs the audit. If the phase has not been executed yet, the skill exits with guidance — there is nothing to validate.

```bash
/gsd-validate-phase
/gsd-validate-phase 3
```

Canonical path: `.github/skills/gsd-validate-phase/SKILL.md`

### gsd-audit-uat

`gsd-audit-uat` performs a cross-phase audit of all outstanding UAT and verification items across the entire project — not just the current phase. It scans every `*-UAT.md` and `*-VERIFICATION.md` file under `.planning/phases/`, identifies items that were found-failing or deferred, and cross-references them against the current state of the codebase to detect stale documentation (items marked as failing that have since been fixed, or items marked as passing that may have regressed). The output is a prioritized human test plan that covers all outstanding work.

```bash
/gsd-audit-uat
```

Canonical path: `.github/skills/gsd-audit-uat/SKILL.md`

### gsd-code-review

`gsd-code-review` reviews source files changed during a phase for bugs, security issues, and code quality problems. It produces a REVIEW.md with findings classified by severity (Critical, Warning, Info). With the `--fix` flag it applies fixes automatically.

**Depth levels:**

`quick` runs pattern-matching only — no per-file analysis, approximately 2 minutes. Use when you want a fast sanity check before submitting for peer review.

`standard` runs per-file analysis with language-specific checks, approximately 5 to 15 minutes. This is the default when no depth is specified. It covers common bug patterns, security anti-patterns (OWASP Top 10 categories), missing error handling, and type safety issues.

`deep` runs cross-file analysis including import graphs and call chains, approximately 15 to 30 minutes. Use for critical paths, security-sensitive code, or phases where multiple files interact in complex ways.

```bash
/gsd-code-review 3
/gsd-code-review 3 quick
/gsd-code-review 3 deep
```

**File scoping:**

File scoping priority from highest to lowest: `--files file1,file2,...` (explicit override, skips SUMMARY.md and git diff entirely) > SUMMARY.md extraction > git diff fallback. If you know which files changed and want to scope the review tightly, use `--files`.

```bash
/gsd-code-review 3 --files src/auth/login.ts,src/auth/session.ts
```

**Fixing findings:**

`--fix` triggers `gsd-code-fixer` after the review completes (or immediately if REVIEW.md already exists). Default scope is Critical and Warning findings only. `--fix --all` extends the scope to include Info findings. `--fix --auto` enables an iteration loop: fix → re-review → fix → re-review, capped at 3 iterations.

```bash
/gsd-code-review 3 --fix
/gsd-code-review 3 --fix --all
/gsd-code-review 3 --fix --auto
```

Output: `{padded_phase}-REVIEW.md` in the phase directory.

Canonical path: `.github/skills/gsd-code-review/SKILL.md`

### gsd-audit-fix

`gsd-audit-fix` is an autonomous audit-to-fix pipeline that runs an audit, classifies findings, and applies fixes for auto-fixable items in a single operation. It is more automated than running `gsd-code-review --fix` manually because it handles the full pipeline including test verification after each fix.

`--source <audit-uat>` specifies which audit type to run. The only currently supported value is `audit-uat`. `--severity high|medium|all` sets the minimum severity threshold for findings to process. `--max N` caps the number of findings to fix per run, defaulting to 5. `--dry-run` classifies findings as auto-fixable vs manual-only without applying any fixes — use this to assess the scope of automated repair before committing to it.

```bash
/gsd-audit-fix --source audit-uat
/gsd-audit-fix --source audit-uat --severity high
/gsd-audit-fix --source audit-uat --max 10
/gsd-audit-fix --source audit-uat --dry-run
```

Canonical path: `.github/skills/gsd-audit-fix/SKILL.md`

### gsd-debug

`gsd-debug` is a systematic debugging skill with persistent state across context resets. It uses a checkpoint-based session model: each debug investigation is a named session stored in `.planning/debug/{slug}.md`. When a session is interrupted (by a context reset, a timeout, or a break), the next invocation can resume from the last checkpoint without losing the investigation state.

**Entry modes:**

`list` shows all active debug sessions with their current status, working hypothesis, and next action. This mode spawns nothing — it is purely read-only.

```bash
/gsd-debug list
```

`status <slug>` shows the full session state — frontmatter, Current Focus block, Evidence count, Eliminated hypotheses, and Resolution fields — without spawning any agent.

```bash
/gsd-debug status auth-redirect-loop
```

`continue <slug>` resumes a specific session, loading its checkpoint state and delegating directly to the session manager without re-gathering symptoms.

```bash
/gsd-debug continue auth-redirect-loop
```

Default (no subcommand) starts a new debug session or re-surfaces active sessions if any exist. A new session gathers five symptoms: expected behavior, actual behavior, error messages and stack traces, when it started and what changed around then, and reliable reproduction steps. It then generates a slug from the description, creates the session file, and delegates to `gsd-debug-session-manager`.

```bash
/gsd-debug the login form submits but users are redirected back to login instead of dashboard
```

`--diagnose` flag finds the root cause without applying any fix. It returns a structured Root Cause Report with the diagnosed cause, confidence level, and a `specialist_hint` field that the session manager uses to route to the appropriate domain skill for remediation.

```bash
/gsd-debug --diagnose the session token expires after 5 minutes despite 24h TTL config
```

Canonical path: `.github/skills/gsd-debug/SKILL.md`

### gsd-secure-phase

`gsd-secure-phase` retroactively verifies that the threat mitigations defined in PLAN.md's threat model section were actually implemented in the code. Every GSD PLAN.md includes a threat model section (added by the planner) — `gsd-secure-phase` closes the loop by verifying those threats were addressed.

The skill has three entry states. If SECURITY.md already exists for the phase, the skill audits it and verifies that each mitigation was implemented. If no SECURITY.md exists but PLAN.md has a threat model, the skill runs the security audit from scratch using PLAN.md as the specification. If the phase has not been executed, the skill exits with guidance.

```bash
/gsd-secure-phase
/gsd-secure-phase 3
```

Canonical path: `.github/skills/gsd-secure-phase/SKILL.md`

### gsd-forensics

`gsd-forensics` is a post-mortem investigation skill for failed or stuck GSD workflows. It is strictly read-only — it never modifies any project source file. Use it when something went wrong during execution that you need to understand before deciding how to proceed.

The skill checks at least four anomaly types: stuck loops (the same operation has been retried many times without progress), missing artifacts (STATE.md says a phase is complete but expected output files are absent), abandoned work (commits were made but the phase was never closed), and crash or interruption indicators (git log shows an unusual pattern consistent with a mid-operation termination). Every anomaly it reports must be backed by specific evidence — a commit hash, a file path, a STATE.md value — not speculation.

Findings are written to `.planning/forensics/report-{timestamp}.md`. The report redacts absolute file paths, API keys, and tokens automatically.

```bash
/gsd-forensics
```

Canonical path: `.github/skills/gsd-forensics/SKILL.md`

### gsd-ui-review

`gsd-ui-review` audits implemented frontend code against the same six quality pillars used by `gsd-ui-phase` to produce the UI-SPEC.md. This retroactive audit catches gaps between what the design contract specified and what was actually implemented. It produces `{phase_num}-UI-REVIEW.md` with a grade of 1 through 4 per pillar and specific findings with line references.

The phase number is optional and defaults to the last completed phase. The skill works on any project — it does not require that a UI-SPEC.md was produced during planning.

```bash
/gsd-ui-review
/gsd-ui-review 3
```

Canonical path: `.github/skills/gsd-ui-review/SKILL.md`

### gsd-eval-review

`gsd-eval-review` audits a completed AI phase to determine whether the evaluation strategy defined in AI-SPEC.md was actually implemented in code. It checks each evaluation dimension from the AI-SPEC.md evaluation plan and scores it as COVERED, PARTIAL, or MISSING based on what exists in the implementation. The output is EVAL-REVIEW.md with an overall score, a verdict, a list of gaps with evidence, and a remediation plan for the gaps.

```bash
/gsd-eval-review
/gsd-eval-review 3
```

Canonical path: `.github/skills/gsd-eval-review/SKILL.md`

### gsd-audit-milestone

`gsd-audit-milestone` audits full milestone completion against the original milestone intent before archiving. It reads all phase VERIFICATION.md files (already verified during execute-phase), aggregates tech debt and deferred gap items, and spawns `gsd-integration-checker` to verify that phases connect properly and that user-facing end-to-end workflows actually work. The version argument is optional and defaults to the current milestone version.

```bash
/gsd-audit-milestone
/gsd-audit-milestone v1.0
```

Canonical path: `.github/skills/gsd-audit-milestone/SKILL.md`

---

## Agents in this stage

**gsd-verifier** performs goal-backward verification for a phase. Starting from the phase goal statement in ROADMAP.md, it works backward through PLAN.md tasks and then forward through the codebase to confirm that the implementation actually achieves what the phase promised — not just that the tasks were completed. It creates VERIFICATION.md with a PASS or FAIL verdict and a list of verified and unverified items.

**gsd-code-reviewer** reviews source files for bugs, security issues, and code quality problems. Produces a REVIEW.md with severity-classified findings. Spawned by `gsd-code-review`. Works across all languages by selecting appropriate language-specific checks at runtime.

**gsd-code-fixer** applies fixes to findings in REVIEW.md. Spawned by `gsd-code-review --fix` and by `gsd-audit-fix`. Reads each finding, reads the relevant source file, applies a context-aware fix, and commits atomically. Shared with Stage 04.

**gsd-security-auditor** verifies that threat mitigations from PLAN.md's threat model exist in the implemented code. Spawned by `gsd-secure-phase`. Produces SECURITY.md with per-threat verification results. Covers OWASP Top 10 categories and any project-specific threats documented in the plan.

**gsd-nyquist-auditor** fills Nyquist validation coverage gaps for a phase. Spawned by `gsd-validate-phase`. Generates test files for behavioral claims that lack sufficient test coverage, validates the generated tests, and commits them.

**gsd-ui-auditor** performs the retroactive 6-pillar visual audit. Spawned by `gsd-ui-review`. Produces the scored UI-REVIEW.md.

**gsd-ui-checker** validates UI-SPEC.md design contracts. Shared with Stage 02 (Planning) where it runs during UI-SPEC creation. In the Testing stage, it can be invoked independently to re-validate a UI-SPEC against an updated design system.

**gsd-eval-auditor** audits implemented AI phase code for evaluation coverage. Spawned by `gsd-eval-review`. Checks implementation against AI-SPEC.md evaluation plan and scores each eval dimension.

**gsd-debugger** investigates bugs using the scientific method — forms hypotheses, designs experiments, gathers evidence, eliminates hypotheses, and converges on a root cause. Spawned by `gsd-debug-session-manager` in a fresh context window for each investigation cycle.

**gsd-debug-session-manager** manages the multi-cycle debug checkpoint and continuation loop. Spawned by `gsd-debug` for new and resumed sessions. It orchestrates `gsd-debugger` instances, handles checkpoint creation and loading, and when the debugger returns ROOT CAUSE FOUND, it extracts the `specialist_hint` field and routes to the matching domain skill (for example, routing a database query optimization finding to the query optimization specialist skill).

**gsd-integration-checker** verifies cross-phase integration and E2E flows at milestone completion. Spawned by `gsd-audit-milestone`. Checks that APIs defined in one phase are correctly consumed in dependent phases, that data flows through the system end-to-end, and that user-facing workflows complete successfully.
