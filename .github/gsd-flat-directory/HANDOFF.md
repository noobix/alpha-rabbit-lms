---
Author: Kelvin Kabute
Last-updated: 2026-05-05
---

# Handoff Protocol — Planning to Execution

This document defines the transition from a completed planning session to the execution agent. Copilot reads this document after the planning workflow is complete. The execution agent reads it before beginning the coding stage. It is designed to be self-contained: an execution agent that reads only this document and the artifacts referenced in the handoff package should have everything it needs to begin without asking the user questions that planning already answered.

---

## Required artifacts

Before a handoff is valid, all of the following artifacts must exist. Copilot verifies each one before generating the handoff package. If any is missing, planning is not complete and the missing item must be produced first.

**PLAN.md** — the executable phase plan produced by `gsd-plan-phase`. It must have passed at least one iteration of gsd-plan-checker verification with no blocking findings. The file lives at `.planning/phases/{phase_dir}/{padded_phase}-PLAN.md` or within plan subdirectories for phases with multiple plans. If multiple PLAN.md files exist for a phase (wave-based execution), all of them must be present.

**CONTEXT.md** — the implementation decisions document produced by `gsd-discuss-phase`. It lives at `.planning/phases/{phase_dir}/{padded_phase}-CONTEXT.md`. This document answers the gray areas that the planner and executor need to make consistent choices — technology selections, API design decisions, data model choices, and anything else that could have gone multiple ways.

**RESEARCH.md** — required only if `gsd-plan-phase` ran a research phase (i.e., `gsd-phase-researcher` was spawned). When present it lives at `.planning/phases/{phase_dir}/RESEARCH.md`. If gsd-plan-phase was run with `--skip-research` and no RESEARCH.md exists, this artifact is waived.

**UI-SPEC.md** — required only if the phase involves frontend work and `gsd-ui-phase` was run. Lives at `.planning/phases/{phase_dir}/{padded_phase}-UI-SPEC.md`. Contains the 6-pillar design contract that the executor uses to produce consistent UI. If the phase has no frontend component, this artifact is waived.

**AI-SPEC.md** — required only if the phase involves an AI system and `gsd-ai-integration-phase` was run. Lives at `.planning/phases/{phase_dir}/{padded_phase}-AI-SPEC.md`. Contains framework guidance, evaluation strategy, and guardrails. If the phase has no AI component, this artifact is waived.

---

## Handoff checklist

Copilot works through this checklist in order. Each item must be confirmed before the handoff package is produced.

Confirm that PLAN.md exists and contains a `## Tasks` or equivalent section with discrete, executable steps. If the plan is structured as a wave plan with multiple files, confirm that wave boundaries and dependencies are clearly stated.

Confirm that CONTEXT.md contains at least one recorded decision in each significant decision area that the plan references. A CONTEXT.md that only says "use the existing stack" with no specifics is not sufficient. If CONTEXT.md is thin, re-run `gsd-discuss-phase` targeting the remaining gray areas before proceeding.

Confirm that RESEARCH.md (if required) contains implementation-ready guidance — not just a summary of what was researched, but actual API patterns, library version notes, and pitfall warnings that the executor will encounter.

Confirm that STATE.md has been updated to reflect the current phase as the active phase. This ensures the execution agent picks up the correct context when it loads project state.

Confirm that `.planning/ROADMAP.md` shows the current phase as the next phase in sequence. If phases are out of order, the executor may pick up the wrong phase.

If a UI-SPEC.md is required, confirm it passed gsd-ui-checker validation (verdict: PASS, not BLOCK or FLAG). A BLOCK verdict means the design contract has unresolved quality issues that will produce poor UI output.

If an AI-SPEC.md is required, confirm it contains an Evaluation Strategy section with at least one measurable rubric. Execution without measurable eval criteria makes it impossible to verify AI behavior post-implementation.

---

## The handoff package

The handoff package is not a separate file. It is the set of confirmed artifacts listed above, passed as context to the execution agent. When invoking `gsd-execute-phase`, the execution agent loads these artifacts through the workflow's `init.execute-phase` step. Copilot does not need to assemble them manually — it only needs to confirm they exist and are valid.

The command that transitions from planning to execution is:

```bash
/gsd-execute-phase {phase_number}
```

Optional flags that may be appropriate depending on the situation:

```bash
/gsd-execute-phase {phase_number} --wave 1
```

Use `--wave 1` when the phase has multiple waves and you want to execute only the first wave to review output before committing to the full phase. This is useful for large phases or phases with risky Wave 1 database migrations.

```bash
/gsd-execute-phase {phase_number} --interactive
```

Use `--interactive` for small phases, bug fixes, or when you want to pair-program rather than run parallel subagents. This executes plans sequentially in the main context with user checkpoints between tasks.

```bash
/gsd-execute-phase {phase_number} --gaps-only
```

Use `--gaps-only` only when returning to a phase after `gsd-verify-work` has identified gaps and produced gap-closure plans. This is not for initial execution.

---

## Rollback path

If execution fails — meaning the executor encounters a blocker it cannot resolve, produces output that fails verification, or makes changes that need to be undone — the path back is through the orchestration stage.

To undo committed phase work safely, use `gsd-undo` from Stage 06 (Deployment). This rolls back phase or plan commits using the phase manifest with dependency checks. It prompts before performing any destructive operation.

To diagnose what went wrong without undoing anything, use `gsd-forensics` from Stage 05 (Testing). This is a read-only investigation that analyzes git history, planning artifacts, and STATE.md to identify anomalies and generate a structured diagnostic report.

To re-enter the planning stage after a failed execution, re-open the CONTEXT.md for the phase and use `gsd-discuss-phase` to resolve whatever decision caused the deviation. Then re-run `gsd-plan-phase --gaps` (gap closure mode) rather than replanning from scratch. Gap closure mode reads the VERIFICATION.md produced by failed verification and creates targeted fix plans rather than replacing the entire plan.

---

## Parallel workstream handoff

When the project has multiple active workstreams managed by `gsd-workstreams`, each workstream produces its own independent handoff. The execution agent for each workstream reads the PLAN.md for that workstream's active phase. Workstreams do not share CONTEXT.md — each maintains its own phase directory. Before handing off a workstream, confirm that `GSD_WORKSTREAM` is set correctly so the execution agent picks up the right workstream context.
