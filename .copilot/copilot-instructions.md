# Copilot Agent Skill Usage Guide

Purpose
-------
This file gives Copilot and contributors a clear, human-readable mapping of the project's agent skills to the situations where they should be invoked. The goal is to help the assistant pick the correct skill automatically by matching context, intent, and common trigger phrases. Place this file at `.copilot/copilot-instructions.md` so the Copilot assistant can find it alongside project configuration.

How to read this file
---------------------
- Each section groups skills by domain (Best Practices, UI, GitHub, Search, etc.).
- For each skill we list: a short description, when to call it, trigger phrases or cues, and example prompts.
- Keep SKILL.md files under `.agents/skills/<skill>/SKILL.md` up-to-date; Copilot can inspect those files for technical details.

Usage patterns and guidance
--------------------------

**Best Practices**
- Purpose: Skills in this group should be used when the user asks for high-level engineering guidance, design patterns, or process-level recommendations.
- Typical triggers: "best practice", "guidance", "how should we", "recommended", "guidelines for".

- `adapt` — Use when asked to make layouts responsive, provide breakpoints, or adapt components for multiple devices.
  - When to call: Requests about responsive design, mobile-first adjustments, or viewport-dependent layouts.
  - Example: "Make this component work on small screens and suggest breakpoints."

- `layout` — Use when layout, spacing, or visual rhythm needs improvement across screens.
  - When to call: Visual spacing issues, inconsistent grids, or alignment problems.
  - Example: "Fix the spacing and alignment on the course list view." 

**UI & Frontend Design**
- Purpose: Use these skills for UI composition, component design, and aesthetic decisions.
- Typical triggers: "design", "UI", "component", "visual", "style", "token", "theme".

- `frontend-design` — Use for high-level UI implementations, component libraries, or page-level design.
  - When to call: Requests to create production-grade UI, accessible components, or design tokens.
  - Example: "Create a course card component with accessible labels and a compact layout."

- `impeccable` — Use when the user expects refined, product-quality UI code and design patterns.
  - When to call: When aesthetics matter and AI-typical UI patterns must be avoided.
  - Example: "Generate a polished dashboard layout following our design language."

- `uncodixfy` — Use to sanitize generic AI-generated UI code into crisp, human-quality patterns.
  - When to call: After an initial component is produced and needs stylistic polishing.
  - Example: "Refactor this modal's markup/styles to follow our product style." 

**Animation & Interactions**
- Purpose: Add purposeful motion or micro-interactions.
- Typical triggers: "animate", "transition", "micro-interaction", "motion".

- `animate` — Use when the user requests transitions, motion design, or micro-interactions.
  - When to call: Requests for hover states, enter/exit transitions, or subtle motion guidance.
  - Example: "Add a tasteful hover animation to the primary button." 

**Platform / Runtime**
- Purpose: Use these skills when the target is a specific runtime or platform.

- `electron` — Use when building or debugging desktop apps using Electron, or when packaging native features.
  - When to call: Questions about main/renderer process, IPC, native modules, or distribution/build specifics for desktop.
  - Example: "How should we open a native file dialog and send the path to the renderer?"

**GitHub / PR / Issue Workflows**
- Purpose: Use for PR summaries, addressing review comments, and automating common GitHub tasks.
- Typical triggers: "PR", "pull request", "review", "address comments", "issue summary".

- `summarize-github-issue-pr-notification` — Use to summarize issues or PRs.
  - When to call: When the user asks for a concise summary of a PR or issue body and discussion.
  - Example: "Summarize this PR and highlight the TODOs for reviewers."

- `address-pr-comments` — Use to generate or implement responses to review feedback and to prepare a patch.
  - When to call: After review comments exist and the user asks to address or implement them.
  - Example: "Fix the comment about the missing prop validation and respond to the reviewer."

- `create-pull-request` — Use when the user requests to create a PR from current changes or branch.
  - When to call: "open a PR", "create a PR", "draft PR" and include branch and brief description.
  - Example: "Open a pull request for branch feature/skill-mapping into testing-phase." 

**Search & Discovery**
- Purpose: These skills help form search queries, find code, and present results.

- `form-github-search-query` — Use when the user needs a precise GitHub search query.
  - When to call: Requests to find issues/PRs/code by semantic criteria.
  - Example: "Find issues mentioning 'course import' labeled 'bug' in this org."

- `show-github-search-result` — Use to summarize search results into a readable table.
  - When to call: After a search query returns results and the user wants a concise display.
  - Example: "Show the top 10 matching PRs and their statuses." 

- `find-skills` — Use when the user asks whether a relevant skill exists or to discover available skills.
  - When to call: "Is there a skill for X?" or "Find a skill that can do Y." 

**Code-Fix & Suggestion**
- Purpose: Suggest or apply fixes for code, or propose quick patches.

- `suggest-fix-issue` — Use to propose a fix for a described bug or issue.
  - When to call: When an issue description is provided and the user asks for a fix suggestion.
  - Example: "Suggest a fix for unit test failing in course import." 

**When to call skills vs. when to reply directly**
- Use a skill when the user's request is explicitly in the skill's domain or when the skill offers structured, tested behavior (e.g., PR creation, query formation, summarization).
- Prefer a direct assistant reply when the user asks a small, self-contained question (single-line clarifications, quick definitions) that doesn't need the specialized skill output.

Trigger heuristics (examples)
----------------------------
- If the user mentions "PR", "pull request", "review comments", or provides a diff: prioritize GitHub / PR skills.
- If the user mentions "responsive", "mobile", "breakpoint", or a viewport width: prioritize `adapt` and `layout`.
- If the user provides a UI component or asks to "make it prettier", or mentions "design language": prioritize `impeccable` or `uncodixfy` after an initial draft.
- If the user asks to "animate", "transition", or "motion": call `animate`.

Technical integration tips
-------------------------
- Keep each skill's SKILL.md (in `.agents/skills/<skill>/SKILL.md`) up-to-date with its intent, examples, and interface. Copilot can inspect those files to determine whether the skill applies.
- Provide short, clear examples in the skill's SKILL.md. Concrete examples improve automatic matching.
- Use consistent trigger phrases in both this instruction file and each SKILL.md to help the assistant map natural language to a skill.

Examples of combined flows
-------------------------
- Flow: Improve a broken component for mobile
  1. User: "This course card breaks on mobile; fix it." — assistant detects "mobile" and `layout`/`adapt` triggers.
 2. Assistant: call `layout` to propose spacing changes and `adapt` to propose breakpoints and CSS.

- Flow: Address PR review and submit
  1. User: "Address reviewer comments and open a PR." — assistant should call `address-pr-comments` to prepare fixes, then `create-pull-request` to open the PR.

Maintaining this file
---------------------
- Update this document whenever a new skill is added or an existing skill's scope changes.
- Add one-line trigger summaries at the top of new SKILL.md files to improve auto-detection.

Appendix: Skill quick index
--------------------------
- adapt — responsive design, breakpoints, multi-device UI.
- animate — transitions and micro-interactions.
- electron — desktop app packaging, IPC, native integrations.
- frontend-design — production-ready UI components and page layout.
- impeccable — high-quality UI polishing and product-grade aesthetics.
- layout — spacing, grids, visual rhythm.
- uncodixfy — refactor AI-generated UI into human-quality patterns.
- find-skills — discover available agent skills.
- summarize-github-issue-pr-notification — summarize PRs and issues.
- suggest-fix-issue — propose fixes for described issues.
- form-github-search-query — build precise GitHub search queries.
- show-github-search-result — present search results in a human-friendly table.
- address-pr-comments — take or suggest actions to resolve PR comments.
- create-pull-request — open pull requests from branches or changes.

If you want, I can also generate a short checklist for SKILL.md contributors to make skill detection more reliable.
