---
Author: Kelvin Kabute
Last-updated: 2026-10-03
---

# Domain Pitfalls

**Domain:** African library operations and outreach services
**Researched:** 2026-10-03

## Critical Pitfalls

### Pitfall 1: Hard-coding national rules into the product

**What goes wrong:** The app works for one country but fails in another because IDs, curriculum, batch logic, and term dates are embedded in code.
**Why it happens:** Product teams often optimize for the first pilot site and do not separate policy from workflow logic.
**Consequences:** Rewrites, local forks, and painful cross-country rollout work.
**Prevention:** Keep regulations, language labels, and academic calendars in configurable metadata and regional policy layers.
**Detection:** Repeated code changes when moving from one country to another, or special-case logic in every form.

### Pitfall 2: Overwriting historical rotation state

**What goes wrong:** A book’s lifecycle is reset each time it rotates, making it impossible to trace degradation or missing-copy patterns.
**Why it happens:** The system models a current state but ignores the historical record that matters to audits and mobile-service tracking.
**Consequences:** Poor stewardship, loss of accountability, and unreliable stock reconciliation.
**Prevention:** Keep append-only cycle history, condition snapshots, and return outcomes.
**Detection:** Missing `rotationCycle` or `conditionAtReturn` data after a bulk issue or return event.

### Pitfall 3: Assuming internet is always available

**What goes wrong:** Transactions fail or become inconsistent during power cuts, poor network conditions, or remote service visits.
**Why it happens:** Field work often happens in rural or low-bandwidth locations.
**Consequences:** Delayed issue/return logs, inconsistent counts, and failed audits.
**Prevention:** Require local-first completion, deferred sync, and robust queue handling.
**Detection:** Transactions that are impossible to complete offline or rely on a live server for basic issue actions.

## Moderate Pitfalls

### Pitfall 1: Minimal learner profiles become too minimal

**What goes wrong:** Outreach records lose enough context to support later reporting or reconciliation.
**Prevention:** Keep only the required minimum identifiers, but still preserve route, school, and cycle metadata.

### Pitfall 2: Bulk allocation without missing-book control

**What goes wrong:** A batch of books is dispatched but no reconciliation process exists for returns, losses, or gaps.
**Prevention:** Pair each allocation with expected books, cycle status, and return verification.

## Minor Pitfalls

### Pitfall 1: Relying on single-language interfaces

**What goes wrong:** Staff and patrons in multilingual environments struggle with forms and notifications.
**Prevention:** Support local language labels and configurable UI strings.

## Phase-Specific Warnings

| Phase Topic         | Likely Pitfall                                  | Mitigation                                   |
| ------------------- | ----------------------------------------------- | -------------------------------------------- |
| Country config      | Hard-coded rules and metadata                   | Add policy engine and configuration objects  |
| Bulk outreach       | Missing-book reconciliation gaps                | Require expected book sets and return checks |
| Distribution        | Route ambiguity between depot and branch        | Explicit destination metadata                |
| Patron intelligence | Over-scoring or over-classifying low-data users | Default to minimal outreach profiles         |

## Sources

- African public and school library service patterns
- Mobile outreach and rural library logistics
- Cross-country operational design for low-connectivity institutions
