---
Author: Kelvin Kabute
Last-updated: 2026-10-04
---

# Feature Landscape

**Domain:** African public, school, and mobile library services
**Researched:** 2026-10-03

## Table Stakes

| Feature                                | Why Expected                                                                   | Complexity | Notes                                                            |
| -------------------------------------- | ------------------------------------------------------------------------------ | ---------- | ---------------------------------------------------------------- |
| Offline issue and return workflow      | Libraries still operate in uncertain power and connectivity conditions         | High       | Must complete locally without a live network                     |
| Batch or school grouping               | Most African school libraries and rural services work by class or term batches | Medium     | Necessary for classroom circulation and allocation               |
| Bulk allocation and rotation tracking  | Books move between lending, extension, and outreach cycles                     | High       | The core of mobile outreach management                           |
| Patron and learner minimal IDs         | Privacy and speed matter in high-volume service environments                   | Medium     | Minimal identifiers are common in outreach and school operations |
| Backup and restore workflow            | Power cuts are common and recovery must be straightforward                     | High       | Recovery is a critical operational requirement                   |
| Acquisitions and vendor management     | New titles still require budget tracking and supplier management               | Medium     | Local procurement rules vary by country                          |
| Distribution and delivery confirmation | Books must move from depot to branch to school to outreach route               | Medium     | Key to public library logistics                                  |

## Differentiators

| Feature                                    | Value Proposition                                                           | Complexity | Notes                                               |
| ------------------------------------------ | --------------------------------------------------------------------------- | ---------- | --------------------------------------------------- |
| Mobile outreach rotation engine            | Makes outreach service predictable and auditable                            | High       | Reduces loss and understaffing during remote visits |
| Missing-book reconciliation at cycle level | Helps recover from bulk loan losses and field service gaps                  | High       | Very valuable in school and extension services      |
| Country policy profile                     | Allows the same app to work across different school calendars and languages | Medium     | Enables regional rollout without a rewrite          |
| Community leader routing                   | Supports rural and school-based service with trusted contact channels       | Medium     | Important in mobile library operations              |
| Patron risk and degradation intelligence   | Helps identify overuse, damage patterns, and repeat issues                  | Medium     | Useful for public and school libraries              |

## Anti-Features

| Anti-Feature                                | Why Avoid                                                    | What to Do Instead                                                           |
| ------------------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| Single national hard-code                   | Breaks when used across jurisdictions                        | Use policy config and metadata                                               |
| Overly complex analytics before core ops    | Causes adoption failure                                      | Prioritize issue/return, stock, and missing-book flows                       |
| Full patron identity collection by default  | Slows down outreach and raises privacy concerns              | Use minimal ID for outreach and optional full profile for core library users |
| Assuming a permanent fixed library building | Many African services are mobile, temporary, or school-based | Support delivery depots and outreach routes                                  |

## Feature Dependencies

```text
Country policy config → school calendar + curriculum rules
Acquisitions → cataloging → processing → routing
Routing → distribution → delivery confirmation
Issue workflow → return workflow → degradation checks
Bulk outreach request → allocation → rotation → missing-book reconciliation
```

## MVP Recommendation

Prioritize:

1. Offline issue/return and local backup
2. Bulk allocation and rotation tracking
3. Depots, delivery confirmation, and missing-book reconciliation

Defer:

- Highly specialized regional reporting dashboards
- Broad, nation-specific language packs until the country configuration layer is in place
- Advanced analytics that depend on a stable, audited transaction model
