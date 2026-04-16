---
name: skill-name
description: Short one-line summary of what the skill does.
---

# Skill SKILL.md Template / Contributor Checklist

## Purpose

This document is a short, practical checklist and template contributors should copy into `.agents/skills/<skill>/SKILL.md` when adding or updating a skill. The goal is to make skills easy to discover by automated tooling and by other contributors.

## Required sections

- `name` (YAML front-matter): short unique identifier (use kebab-case).
- `description` (YAML front-matter): one-line summary that appears in search results.
- **When to Use This Skill**: 2–6 short bullets describing user intents that should trigger the skill.
- **Trigger Phrases / Examples**: 3–6 short example user prompts or phrases that map to this skill.
- **Install / Run**: concise install and usage commands (e.g., `npx skills add owner/repo@skill`).

## Recommended metadata

- `categories`: comma-separated keywords (e.g., `testing, react, ci-cd`).
- `keywords`: alternate search terms / synonyms.
- `homepage` or `docs`: link to longer documentation or README.

## Quality checklist (make sure each item is present)

- [ ] Skill `name` is unique and descriptive.
- [ ] `description` front-matter is concise (<= 140 characters).
- [ ] Provide 3 short example prompts that a user might say to trigger this skill.
- [ ] Include the minimal `npx skills add` install command and a one-line usage example.
- [ ] List common categories and 3–6 keywords to aid search.
- [ ] Add a short "When to Use" section describing intent and edge cases.
- [ ] Provide a fallback: what the assistant should do if the skill can't help (e.g., perform the task directly).
- [ ] If the skill runs shell commands or side effects, document required permissions and flags (e.g., `-g`, `-y`).

## Short example (copy & edit)

---

name: vercel-react-best-practices
description: React and Next.js performance guidance and optimizations.

---

## When to Use This Skill

- Ask when you need performance guidance for React/Next.js apps.

## Trigger Phrases / Examples

- "How do I make my React app faster?"
- "Suggest Next.js performance best practices for a course listing page."

## Install / Run

- `npx skills add vercel-labs/agent-skills@vercel-react-best-practices`

## Fallback

- If the skill cannot be installed or doesn't match exactly, the assistant should still provide best-effort guidance and offer to scaffold tests or commands.

## Contributor notes

- Keep examples concise and concrete.
- Favor specific keywords over very generic terms (e.g., `nextjs` instead of `web`).
- Update `keywords` when you add significant sub-features so searches improve.

## Maintenance

- Update the `description` and `trigger phrases` when the skill's scope changes.
- Add compatibility notes if the skill depends on particular runtimes or CLIs.

## Why this matters

Search and automatic skill matching rely on short, accurate signals: name, description, example prompts, and keywords. A well-formed `SKILL.md` significantly improves discoverability and reduces false positives.

If you want, I can:

- Expand this template into a repository-level CONTRIBUTING doc.
- Copy this checklist into each existing skill folder.
