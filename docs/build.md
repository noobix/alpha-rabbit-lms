---
Author: Kelvin Kabute
Last-updated: 2026-10-03
---

# Alpha Rabbit LMS Build Document

## File Context

**Purpose:** This file is the implementation blueprint for agents and contributors. It explains the authoritative source documents, project guardrails, sprint structure, and verification gates that should guide build work.

**Why this matters:** A library system in Africa is operationally different from a single-branch desktop product. This document keeps the project adaptable across national policies, rural delivery realities, school calendars, and multi-department workflows without breaking the existing lifecycle model.

**How agents use it:** Agents should use this file to understand the sequence of work, the project constraints, and the country-configurable rules that must remain in place before a feature is considered complete.

## 1. Source Assets & Defaults

### Source Assets

| Asset                                             | Purpose                                                  | Required Use                                            |
| ------------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------- |
| `docs/jira/compression.md`                        | Canonical ticket scope and acceptance criteria           | Source of truth for every ticket                        |
| `docs/jira/jira_doc.md`                           | Detailed ticket specification with sprint planning       | Sprint sequencing, labeling, quality gates              |
| `docs/prompt_main.md`                             | Architecture constraints and project structure           | Codebase layout, mode split, non-functional constraints |
| `docs/database.md`                                | Canonical schema contracts                               | Doc types, retention, sync state, audit fields          |
| `docs/ressources/product_specs.md`                | Stack and deployment decisions                           | Offline-first stack, packaging, Ghana hardware          |
| `docs/ressources/system_specs.md`                 | Manager vs Enterprise setup                              | Environment-specific behavior                           |
| `docs/ressources/functionality_specs.md`          | End-to-end module behavior                               | Acquisitions → Processing → Distribution → Sections     |
| `docs/ressources/module_functionality_specs.md`   | User-centric module acceptance                           | User stories, offline behavior, Extension workflows     |
| `docs/ressources/functionality_specs_expanded.md` | Patron intelligence, governance extensions               | Degradation engine, badges, patron signals              |
| `docs/research_dmp/aquisisions_module.md`         | Deep implementation notes for acquisitions               | Forms, metadata shape, offline patterns                 |
| `docs/research_dmp/processing_module.md`          | Deep implementation notes for processing                 | Condition model, mold risk, barcode behavior            |
| `docs/research_dmp/distribution_module.md`        | Deep implementation notes for distribution               | Packing slips, rural mode, delivery confirmation        |
| `docs/research_dmp/extension_module.md`           | Deep implementation notes for Extension Services         | Android app, QR learner tracking, bulk allocation       |
| `docs/research_dmp/library_sections_pi_sg.md`     | Deep implementation notes for sections + PI + governance | Degradation enforcement, section workflows              |
| `docs/research_dmp/deploy_doc.md`                 | Pilot/deployment/validation package                      | Pilot validation, packaging constraints                 |

### Global Non-Negotiables

- **One codebase, two modes**: Manager (offline standalone) and Enterprise (local-first with sync)
- **No plaintext national ID values** in storage, logs, backups, exports, or UI state dumps; local identity rules must be configurable by country and institution
- **Identity hashing** must execute in the Electron main process only; the UI should never hold plaintext identity data
- **Core data envelope**: `_id`, `_rev`, `type`, `createdAt`, `updatedAt`, `_syncStatus`, `_schemaVersion`
- **One database per logical domain**: books, patrons, loans, extensionLoans, departments, auditLog, config, and related domain stores must be initialized independently and indexed by query path rather than stored in a single giant collection
- **Schema discipline**: every document must extend the same `BaseDocument` contract; no field drift without a schema version bump and migration note; data must be validated at the application boundary (Zod) and, for Enterprise, by CouchDB validation logic where relevant
- **Query-first indexing**: required indexes must exist for typical access patterns such as `type + status`, `type + department`, `type + barcode`, `type + cycleCode`, `type + schoolId`, `type + patronId + status`, and `type + dueDate` so that offline performance does not degrade as data grows
- **Conflict-safe sync**: PouchDB/CouchDB conflicts must be treated as first-class events; no silent overwrite of concurrent edits; every conflict must be resolved with an explicit audit trail and human-visible review when needed
- **Package manager**: `pnpm` only — no `npm`, `yarn`, or `bun`
- **Device baseline**: Windows 10, 4GB RAM, unstable power/internet expected
- **Offline-first**: Every critical workflow completes locally; sync is deferred
- **Country policy configuration**: school calendar, language labels, curriculum rules, compliance checks, and academic terms must be data-driven rather than hard-coded to a single nation. Each selected country or custom institution profile must be saved and reused for batch promotions, expiry checks, and curriculum tagging.
- **Extension Services is a top-level DEPARTMENT** (peer to Acquisitions, Processing, Distribution, Library Operations, System Admin) — NOT a library section
- **Books remain owned by Lending Section**; Extension Services borrows temporarily via bulk allocation: `Extension Request → Lending Fulfillment → Distribution Delivery → Extension Rotation → Return to Lending`
- **Community handoff remains under Extension Services**: books sent to community leaders and rural outreach points retain their extension workflow, not a separate one-off library section.
- **Outreach learners and mobile-library patrons have minimal profiles** (QR or local token ID only, no condition scoring, no degradation tracking unless the country policy explicitly requires it)
- **Android app is an external tool** for Extension Services field operations only — NOT part of the Electron desktop application
- **Operational reality**: many African libraries combine public-library, school-library, outreach-library, and community-reading functions. The system must support those mixed workflows without forcing a single branch model

### Database Modeling Requirements (must be planned before build work)

- **Domain separation**: maintain distinct domain databases or collections for `books`, `patrons`, `loans`, `extensionLoans`, `departments`, `auditLog`, and `config` rather than building one large flat document store.
- **Shared document contract**: every record must include the shared `BaseDocument` fields (`_id`, `_rev`, `type`, `createdAt`, `updatedAt`, `_syncStatus`, `_schemaVersion`) and any domain-specific fields must be added through a versioned schema definition.
- **Validation layer**: implement runtime validation with Zod at the application boundary, and enforce critical business rules at the server or replication layer (Enterprise) when the data crosses trust boundaries.
- **Migration readiness**: schema changes must be traceable and reversible; document versioning and migration notes are part of the delivery requirements, not a later cleanup task.
- **Conflict handling**: record writes from multiple rural devices must be treated as concurrent edits. The system must preserve both histories and expose conflicts rather than silently overwriting.
- **Department-level security**: a single application cannot assume all users share the same access pattern; Enterprise security objects and per-role data access must be part of the data model design, not a post-implementation fix.

---

### Sprint 1: Core Infrastructure + Acquisitions

**Results to achieve:**

- PouchDB offline storage with SQLite adapter operational
- Database model contract defined and enforced for shared records
- Zod validation and required indexes wired for core domains
- Ghana Card ID hashing and masking verified by DPC liaison
- 247 GES curriculum tags available offline
- Vendor management with Ghana Card compliance
- Budget tracking with GES alignment and quarterly limits

**Build Focus:**

- SQLite database creation at `C:/GhanaLibraryData/`
- Indexed collections for books, patrons, staff, extension records, audits, and config
- `BaseDocument` contract enforced for all saved records
- Zod validation for domain records before write to PouchDB
- Query-specific indexes for `books`, `loans`, `extensionLoans`, `patrons`, and `auditLog`
- Explicit conflict handling policy for offline edits and sync replays
- Ghana Card ID format validation (`GHA-000000000-0`) at form boundary
- Hashing service in Electron main process only
- Masked display: `GHA-123***89-0`
- Offline curriculum tag dropdown with 247 tags grouped by level (Basic/JHS/SHS)
- Auto-suggest Dewey Decimal based on curriculum tag
- Budget code format enforcement (`CHILDREN-2024-Q1`)
- Real-time remaining balance with amber warning at <20%

**Verification Gate:**

- SQLite inspection confirms indexed collections
- Database schema validation rejects malformed documents before persistence
- Indexes exist for the critical access paths across books, loans, extension loans, and patrons
- Hashing audit: plaintext ID never in storage/logs/backups
- Curriculum tags match MoE 2024/25 validation certificate
- Vendor form rejects invalid Ghana Card format
- Budget blocks orders exceeding remaining balance

---

### Database Model Architecture Requirements (must be satisfied before release gate)

- **Schema contract**: Domain entities must abide by the canonical `BaseDocument` shape and domain-specific typing.
- **Database split**: local data must be separated by logical domain to keep index size manageable and access patterns predictable.
- **Validation**: all writes must pass Zod validation; critical security objects and document update checks must also run in CouchDB for Enterprise.
- **Auditability**: writes that modify identity, financial values, route assignment, extension allocation, or promotion rules must emit an `audit_log` entry.
- **Conflict traceability**: all document conflicts must be visible in the data layer and reviewable by staff or administrators.
- **Versioning**: new fields require a schema version bump and migration path; no undocumented schema drift is allowed.

---

## 2. Sprint Plan Overview

| Sprint | Weeks | Theme                                           | Tickets                                                                                                                          | Goal                                                                                                                    |
| ------ | ----- | ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **1**  | 1-2   | Core Infrastructure + Acquisitions              | LMS-CORE-01, LMS-CORE-02, LMS-CORE-07, LMS-CORE-08, LMS-ACQ-10, LMS-ACQ-01, LMS-ACQ-02                                           | Offline-capable acquisitions with hashed identity rules, a validated data model, and a country-aware curriculum profile |
| **2**  | 3-4   | Processing + Climate + Extension Routing        | LMS-CORE-04, LMS-PROC-10, LMS-PROC-11, LMS-PROC-12, LMS-PROC-01, LMS-PROC-02, LMS-PROC-03, LMS-PROC-04                           | Processing workflow with climate-aware condition scoring and Extension Services routing                                 |
| **3**  | 5-6   | Distribution + Rural Delivery + Extension Depot | LMS-CORE-03, LMS-DIST-10, LMS-DIST-11, LMS-DIST-12, LMS-DIST-01, LMS-DIST-02, LMS-DIST-03, LMS-DIST-04                           | Batch-aware distribution with rural delivery mode and extension depot routing                                           |
| **4**  | 7-8   | Section Policy + Degradation Engine             | LMS-CHILD-10, LMS-CHILD-11, LMS-CHILD-01, LMS-CHILD-02, LMS-CHILD-03                                                             | Section management with country-driven batch promotion and degradation enforcement                                      |
| **5**  | 9-10  | Staff Governance + Lending + Compliance         | LMS-STAFF-10, LMS-STAFF-01, LMS-STAFF-02, LMS-STAFF-03, LMS-LEND-10, LMS-LEND-01, LMS-LEND-02, LMS-GH-10, LMS-GH-01              | Staff governance with extension roles, lending bulk allocation, and country-compliant messaging                         |
| **6**  | 11-12 | Extension Services Department + Android App     | LMS-CORE-06, LMS-EXT-10, LMS-EXT-11, LMS-EXT-12, LMS-EXT-13, LMS-EXT-01, LMS-EXT-02, LMS-EXT-03                                  | Extension Services department with bulk requests, rotation cycles, and Android offline app                              |
| **7**  | 13-14 | Extension Android + Pilot Prep                  | LMS-EXT-04, LMS-EXT-05, LMS-GH-11, LMS-GH-12, LMS-GH-02, LMS-LEND-03, LMS-CORE-05                                                | Complete extension Android app, local language support, and pilot readiness                                             |
| **8**  | 15-16 | Data Operations & Disaster Recovery             | LMS-DATA-01, LMS-DATA-02, LMS-DATA-03, LMS-DATA-04, LMS-DATA-05, LMS-DATA-06, LMS-DATA-07                                        | Import, export, seeding, retention, migration, and disaster recovery                                                    |
| **9**  | 17-18 | Sync Infrastructure & Conflict Resolution       | LMS-SYNC-01, LMS-SYNC-02, LMS-SYNC-03, LMS-SYNC-04, LMS-SYNC-05, LMS-SYNC-06                                                     | Conflict UX, partitions, server validation, Android sync, and sync testing                                              |
| **10** | 19-20 | Data Quality & Integrity                        | LMS-QUAL-01, LMS-QUAL-02, LMS-QUAL-03, LMS-QUAL-04, LMS-QUAL-05, LMS-QUAL-06, LMS-QUAL-07, LMS-QUAL-08, LMS-QUAL-09, LMS-QUAL-10 | Duplicate detection, collision handling, monitoring, error handling, and performance targets                            |

---

## 3. Detailed Sprint Breakdown

### Sprint 1: Core Infrastructure + Acquisitions

**Results to achieve:**

- PouchDB offline storage with SQLite adapter operational
- Ghana Card ID hashing and masking verified by DPC liaison
- 247 GES curriculum tags available offline
- Vendor management with Ghana Card compliance
- Budget tracking with GES alignment and quarterly limits

**Tickets in scope:**

| Ticket      | Type    | Title                                                         | Effort | Dependencies |
| ----------- | ------- | ------------------------------------------------------------- | ------ | ------------ |
| LMS-CORE-01 | System  | Set up PouchDB with SQLite adapter                            | 5      | None         |
| LMS-CORE-02 | System  | Implement SHA-256 hashing for Ghana Card ID                   | 3      | LMS-CORE-01  |
| LMS-CORE-07 | System  | Define shared database contract and domain indexes            | 5      | LMS-CORE-01  |
| LMS-CORE-08 | System  | Enforce Zod validation and migration gates for schema changes | 4      | LMS-CORE-07  |
| LMS-ACQ-10  | System  | Pre-load GES curriculum tags database                         | 3      | LMS-CORE-01  |
| LMS-ACQ-01  | Feature | Vendor management with Ghana Card ID validation               | 3      | LMS-ACQ-10   |
| LMS-ACQ-02  | Feature | GES curriculum tag selection during order creation            | 5      | LMS-ACQ-10   |

**Build Focus:**

- SQLite database creation at `C:/GhanaLibraryData/`
- Indexed collections for books, patrons, staff, extension records
- Ghana Card ID format validation (`GHA-000000000-0`) at form boundary
- Hashing service in Electron main process only
- Masked display: `GHA-123***89-0`
- Offline curriculum tag dropdown with 247 tags grouped by level (Basic/JHS/SHS)
- Auto-suggest Dewey Decimal based on curriculum tag
- Budget code format enforcement (`CHILDREN-2024-Q1`)
- Real-time remaining balance with amber warning at <20%

**Verification Gate:**

- SQLite inspection confirms indexed collections
- Hashing audit: plaintext ID never in storage/logs/backups
- Curriculum tags match MoE 2024/25 validation certificate
- Vendor form rejects invalid Ghana Card format
- Budget blocks orders exceeding remaining balance

---

### Sprint 2: Processing + Climate + Extension Routing

**Results to achieve:**

- Condition scoring sliders with climate-aware weighting
- Automatic mold risk assessment based on Ghana seasonal calendar
- PDF417 barcodes with Ghana Library Authority format
- Extension Services routing with durability scoring and corridor safety
- 30-second auto-save for power outage resilience

**Tickets in scope:**

| Ticket      | Type    | Title                                               | Effort | Dependencies |
| ----------- | ------- | --------------------------------------------------- | ------ | ------------ |
| LMS-CORE-04 | System  | 30-second auto-save for power outage resilience     | 5      | LMS-CORE-01  |
| LMS-PROC-10 | System  | PDF417 barcode generator (GLA format)               | 5      | LMS-CORE-01  |
| LMS-PROC-11 | System  | Ghana seasonal calendar service                     | 3      | LMS-CORE-01  |
| LMS-PROC-12 | System  | Barcode rotation cycle indicator for Extension      | 3      | LMS-PROC-10  |
| LMS-PROC-01 | Feature | Condition scoring sliders (spine/cover/pages/edges) | 5      | LMS-PROC-10  |
| LMS-PROC-02 | Feature | Automatic mold risk assessment                      | 3      | LMS-PROC-11  |
| LMS-PROC-03 | Feature | Batch assignment (GRADE-4A)                         | 3      | LMS-PROC-01  |
| LMS-PROC-04 | Feature | Extension Services routing with durability scoring  | 5      | LMS-PROC-12  |

**Build Focus:**

- Four 1-5 sliders: Spine (40%), Cover (25%), Pages (25%), Edges (10%)
- Climate-aware tooltips: "Critical in humid climate – check for separation"
- Auto-save every 30 seconds with checksum validation
- Recovery snapshot with timestamp display
- Barcode format: `[SUBJECT]-[GRADE][AUTHOR_INITIAL]-[SEQUENTIAL]`
- Extension suffix: `-C[1-4]` for rotation cycles
- Seasonal calendar: Dec-Feb (dry), Mar-May/Sept-Nov (rainy), Jun-Aug (major rainy)
- Extension routing conditional fields: Rotation Cycle, Mobile Handling Durability, Destination Region
- Durability ≥3 required for Tamale-Bolgatanga corridor
- Corridor safety protocols auto-trigger for Northern Region

**Verification Gate:**

- Condition scoring works offline
- Mold risk assessment matches manual review (≥90%)
- Barcode format `SCI-6M-042-C2` generated correctly
- Extension routing shows conditional fields, hides batch assignment
- Auto-save recovers 99% of transactions >30s old after 4h outage

---

### Sprint 3: Distribution + Rural Delivery + Extension Depot

**Results to achieve:**

- Batch-aware packing slips with GRADE-4A vs GRADE-4B separation
- Rural delivery mode for Tamale-Bolgatanga corridor
- Rainy season alerts on packing slips
- Extension Services depot delivery with rotation cycle metadata
- Incremental backup scheduler with WhatsApp compression

**Tickets in scope:**

| Ticket      | Type    | Title                                                  | Effort | Dependencies |
| ----------- | ------- | ------------------------------------------------------ | ------ | ------------ |
| LMS-CORE-03 | System  | Incremental backup scheduler with WhatsApp compression | 8      | LMS-CORE-01  |
| LMS-DIST-10 | System  | Offline PDF generation for packing slips               | 5      | LMS-CORE-01  |
| LMS-DIST-11 | System  | Tamale-Bolgatanga corridor detection service           | 3      | LMS-CORE-01  |
| LMS-DIST-12 | System  | Extension Services depot routing with Dagbani SMS      | 5      | LMS-DIST-10  |
| LMS-DIST-01 | Feature | Batch-aware packing slips                              | 5      | LMS-DIST-10  |
| LMS-DIST-02 | Feature | Rural delivery mode for Tamale-Bolgatanga              | 3      | LMS-DIST-11  |
| LMS-DIST-03 | Feature | Rainy season alerts on packing slips                   | 2      | LMS-PROC-11  |
| LMS-DIST-04 | Feature | Extension depot delivery with rotation metadata        | 5      | LMS-DIST-12  |

**Build Focus:**

- Packing slip groups books by batch with learner counts
- Repeat batch warning: "Repeat learners – 20% extra books required"
- Rural mode toggle disables GPS, requires community leader contact
- Rainy season banner: "RAINY SEASON ALERT: Use waterproof covers + silica gel"
- Glossy page books (Science/Math) flagged for extra protection
- Depot routing: rotation cycle indicator, depot location, community leader signature
- READ-ONLY rotation cycle metadata (assigned during Lending fulfillment)
- Dagbani SMS: "Zuli libri ka ti kpɛ. Cycle 2 books arriving today."
- Backup: daily 8 PM incremental, ≤5% DB size, WhatsApp compression <10MB
- 30-day retention with auto-deletion

**Verification Gate:**

- Packing slips generate offline <10s
- Rural mode disables GPS without errors
- Extension depot packing slips include rotation metadata
- Backup resumes after power outage
- Dagbani SMS queues offline, sends on reconnect

---

### Sprint 4: Children's Section + Degradation Engine

**Results to achieve:**

- GES-aligned batch promotion on August 15
- Degradation threshold enforcement blocking poor-care patrons
- "Teleporter" detection with oral tradition context
- GES academic calendar with August 31 expiry enforcement

**Tickets in scope:**

| Ticket       | Type    | Title                                              | Effort | Dependencies |
| ------------ | ------- | -------------------------------------------------- | ------ | ------------ |
| LMS-CHILD-10 | System  | Degradation engine with climate-aware weighting    | 8      | LMS-CORE-01  |
| LMS-CHILD-11 | System  | GES academic calendar service                      | 3      | LMS-CORE-01  |
| LMS-CHILD-01 | Feature | Automatic batch promotion on August 15             | 5      | LMS-CHILD-11 |
| LMS-CHILD-02 | Feature | Degradation threshold enforcement                  | 5      | LMS-CHILD-10 |
| LMS-CHILD-03 | Feature | "Teleporter" detection with oral tradition context | 3      | LMS-CHILD-10 |

**Build Focus:**

- Degradation formula: `(spine_loss*0.4 + cover_loss*0.25 + pages_loss*0.25 + edges_loss*0.1)`
- Zone logic: Green (≤0.15), Yellow (0.16-0.29), Red (0.30-0.44), Critical (≥0.45)
- Red zone: block issuance + require staff override with 10-char reason
- Critical zone: block + auto-schedule coaching workshop
- Auto-promotion: >80% attendance → promote, <70% → repeat batch
- SMS notifications in Twi/English to parents
- Teleporter detection: 3+ pristine returns after >7 days
- Context-aware: does NOT flag if staff notes contain "read aloud" or "sibling"
- GES calendar: August 31 expiry, August 15 promotion, June 15 pre-promotion report

**Verification Gate:**

- Batch promotion accurate (100% learner assignment)
- Degradation engine ≥90% accuracy vs manual review
- Teleporter flags show "Watch" not "Teleporter" (non-punitive)
- Calendar auto-expires batches on September 1

---

### Sprint 5: Staff Governance + Lending + Jurisdiction Compliance

**Results to achieve:**

- Staff profiles with hashed national ID or equivalent identity metadata
- Department role switching (including Extension Services)
- Extension staff route certification and bulk request authority
- Lending Section bulk allocation fulfillment
- Rotation tracking and return workflow
- Local-language SMS templates driven by the active country profile

**Tickets in scope:**

| Ticket       | Type    | Title                                           | Effort | Dependencies |
| ------------ | ------- | ----------------------------------------------- | ------ | ------------ |
| LMS-STAFF-10 | System  | Role-based UI filtering for Manager version     | 5      | LMS-CORE-01  |
| LMS-STAFF-01 | Feature | Staff profiles with Ghana Card ID hashing       | 3      | LMS-CORE-02  |
| LMS-STAFF-02 | Feature | Department role switching                       | 5      | LMS-STAFF-10 |
| LMS-STAFF-03 | Feature | Extension staff route certification             | 3      | LMS-STAFF-10 |
| LMS-LEND-10  | System  | Cross-department book status tracking           | 5      | LMS-CORE-01  |
| LMS-LEND-01  | Feature | Fulfill bulk allocation requests from Extension | 5      | LMS-LEND-10  |
| LMS-LEND-02  | Feature | Rotation tracking and return workflow           | 3      | LMS-LEND-10  |
| LMS-GH-10    | System  | Offline SMS queue with Ghana network support    | 5      | LMS-CORE-01  |
| LMS-GH-01    | Feature | Twi/Dagbani SMS templates for rural patrons     | 3      | LMS-GH-10    |

**Build Focus:**

- Staff form: document ID validation, hashing, and masked display according to the selected country policy
- Duplicate ID prevention across staff records
- Role switcher dropdown: System Admin, Acquisitions, Processing, Distribution, Library Operations, Extension Services
- Extension role shows ONLY Extension workflows
- Lending role shows "Bulk Requests" tab alongside regular lending
- Extension staff: department field = "extension_services" (NOT section code)
- Route certification: regional or rural corridor requirements derived from the active policy
- Bulk request fulfillment: select books from available collection
- Status change: "On Loan to Extension Services" with cycle metadata
- Books marked unavailable for regular circulation
- Return workflow: condition reassessment, status revert to "Available"
- Track: cycle history, rotation count, cumulative condition changes
- Overdue returns beyond the active academic policy trigger escalation
- SMS queue: local storage, send when connectivity returns
- Local-language templates with English fallback

**Verification Gate:**

- Staff roles switch without data loss
- Extension staff CANNOT access library section data
- Lending bulk allocation fulfills requests correctly
- Local-language SMS delivers ≥95% success rate when connectivity allows
- Cross-department sync prevents double-allocation

---

### Sprint 6: Extension Services Department + Android App

**Results to achieve:**

- Department security objects for 6 departments
- Bulk book requests for school rotation cycles
- Rotation cycle management aligned with GES calendar
- School delivery tracking via mobile library van
- Android offline transaction app
- QR-based learner identification with smart tag design
- Extension-Lending cross-department book status sync
- Schedule management with corridor safety

**Tickets in scope:**

| Ticket      | Type    | Title                                               | Effort | Dependencies |
| ----------- | ------- | --------------------------------------------------- | ------ | ------------ |
| LMS-CORE-06 | System  | Department security objects for 6 departments       | 5      | LMS-CORE-01  |
| LMS-EXT-10  | System  | Android offline transaction app                     | 13     | LMS-EXT-12   |
| LMS-EXT-11  | System  | QR-based learner identification with smart tag      | 5      | LMS-EXT-10   |
| LMS-EXT-12  | System  | Extension-Lending cross-department book status sync | 8      | LMS-LEND-10  |
| LMS-EXT-13  | System  | Extension schedule management with corridor safety  | 3      | LMS-CORE-01  |
| LMS-EXT-01  | Feature | Bulk book requests for school rotation cycles       | 5      | LMS-EXT-12   |
| LMS-EXT-02  | Feature | Rotation cycle management with GES calendar         | 5      | LMS-EXT-13   |
| LMS-EXT-03  | Feature | School delivery tracking via mobile van             | 3      | LMS-EXT-13   |

**Build Focus:**

- 6 departments: Acquisitions, Processing, Distribution, Library Operations, Extension Services, System Admin
- Extension staff CANNOT access library section data
- Lending staff see ONLY "Bulk Requests" tab for Extension
- Bulk request form: school, cycle, quantity, subject areas, destination region
- Request status: Pending → Approved → Fulfilling → Ready for Delivery
- 4-cycle rotation: CYCLE-1 (Sept-Dec), CYCLE-2 (Jan-Mar), CYCLE-3 (Apr-Jun), CYCLE-4 (Jul-Aug)
- Auto-flag sets for collection 14 days before cycle end
- August 31 hard stop: ALL sets return to depot
- Cycle 2 prioritizes WASSCE/BECE materials
- Cycle 3 includes rainy season mold prevention kits
- Schedule dashboard: scheduled/in-progress/completed/missed
- Community leader contacts pre-loaded per school
- Rainy season road alerts for affected routes
- Android app: ZXing QR scanning, low-light capable
- Local SQLite encrypted at rest (Android Keystore)
- Battery optimization: 30s screen timeout, low-power mode
- Post-service sync on depot Wi-Fi
- QR smart tag: 85.6x54mm, 250-micron laminate, rounded corners
- QR contains ONLY `qrCodeId` — NO personal data
- Lost tag reuses same `qrCodeId` to preserve history
- Cross-department sync: status "On Loan to Extension Services"
- Real-time sync prevents double-allocation
- Return triggers condition reassessment in Lending

**Verification Gate:**

- Department boundary enforced (Extension cannot access library sections)
- Bulk allocation workflow: request → fulfillment → delivery → return
- Zero books stranded; 100% requests fulfilled within 48 hours
- Android app processes 100 transactions offline without data loss
- QR scanning works in low-light rural conditions
- Cross-department sync prevents double-allocation

---

### Sprint 7: Extension Android + Pilot Prep

**Results to achieve:**

- QR-based learner checkout/return on Android app
- Dagbani SMS templates for Northern Region schools
- Ghana seasonal calendar with automatic mold risk updates
- Dagbani language support for Extension Services
- Community leader notification workflow
- Collection health monitoring for Extension-loaned books
- CouchDB server deployment for Raspberry Pi 4 (Enterprise)

**Tickets in scope:**

| Ticket      | Type    | Title                                                   | Effort | Dependencies           |
| ----------- | ------- | ------------------------------------------------------- | ------ | ---------------------- |
| LMS-EXT-04  | Feature | QR-based learner checkout/return on Android             | 8      | LMS-EXT-10, LMS-EXT-11 |
| LMS-EXT-05  | Feature | Dagbani SMS templates for Northern Region               | 3      | LMS-GH-10              |
| LMS-GH-11   | System  | Ghana seasonal calendar with auto mold risk updates     | 3      | LMS-CORE-01            |
| LMS-GH-12   | System  | Dagbani language support for Extension Services         | 5      | LMS-GH-10              |
| LMS-GH-02   | Feature | Community leader notification workflow                  | 3      | LMS-GH-10              |
| LMS-LEND-03 | Feature | Collection health monitoring for Extension-loaned books | 3      | LMS-LEND-10            |
| LMS-CORE-05 | System  | CouchDB server deployment for Raspberry Pi 4            | 8      | None                   |

**Build Focus:**

- Android checkout: scan QR → display learner → scan book barcode → max 2 books
- NO condition scoring, NO interaction scores, NO degradation tracking
- Transaction saves to local encrypted SQLite
- Dagbani template: "Zuli libri ka ti kpɛ. Yɛlsim cycle 2 books."
- Seasonal calendar: auto-detect season from device date
- Mold risk defaults: high during rainy seasons
- Dagbani translations validated by UDS linguist
- Language toggle: English/Twi/Dagbani
- Community leader notification: require name + phone for rural deliveries
- Twi/Dagbani templates based on destination region
- Collection health: rotation history, cycles served, destinations, condition at each return
- Cumulative Extension degradation tracked separately
- Withdrawal recommendation when condition drops below threshold
- CouchDB 3.3 on Raspberry Pi 4, port 5984
- Data persists in `/home/pi/couchdb/data`
- ≤15% CPU during idle

**Verification Gate:**

- Android field test at Bolgatanga school: 100 transactions offline
- QR smart tag scanning works in low-light conditions
- Full offline resilience: 24h simulated outage, zero data loss
- Dagbani SMS delivers ≥95% success rate
- DPC submission package complete
- Pilot-ready: all acceptance criteria pass on Ghana-spec hardware

---

## 4. Git Workflow & PR Guidelines

### Branching Rules

- `testing-main` is the development base branch
- Create one branch per ticket only
- Never combine multiple tickets into one branch or PR
- Branch naming: `LMS-[XXX]/[kebab-case-title]`
- Create from latest `testing-main`
- Sync with `testing-main` before starting work

### Commit Format

```
LMS-[XXX]: <type>: <vivid summary>

<Paragraph explaining what was built, how it works, and why>
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

### Pull Request Requirements

Every PR to `testing-main` must include:

- Ticket ID and title
- Short implementation summary
- Acceptance criteria covered
- Known gaps
- Evidence of verification performed

### Build Tags

- Lightweight tag per commit: `[YY###]` (e.g., `[261]`)
- Annotated sprint tag on sprint completion: `v<M.m.0>`
- Tag body includes: build entries, contributors, full PR descriptions

### MCP Tool Sequence

```
1. Create feature branch from testing-main
2. Sync feature branch with testing-main
3. Read existing files before editing
4. Commit and push all changes
5. Tag commit with build number [YY###]
6. Open PR to testing-main
7. Create annotated sprint tag on sprint completion
```

### Fork-to-Upstream Contribution Workflow

This repository requires using GitHub MCP for any pull request targeting the upstream organizational repository.

Steps:

1. Add upstream remote (once):

   ```bash
   git remote add upstream https://github.com/noobix/alpha-rabbit-lms.git
   git fetch upstream
   ```

2. Create feature branch from latest upstream `testing-main`:

   ```bash
   git fetch upstream
   git checkout -b LMS-[XXX]/[title] upstream/testing-main
   git push origin LMS-[XXX]/[title]
   ```

3. Work on only that ticket. Commit with ticket ID and concise acceptance summary.

4. Keep branch current with upstream `testing-main` before PR review:

   ```bash
   git fetch upstream
   git checkout testing-main
   git pull upstream testing-main
   git checkout <feature-branch>
   git merge testing-main
   git push origin <feature-branch>
   ```

5. Open fork PR targeting `origin/testing-main` and require:
   - CI passing on fork PR
   - Explicit QA sign-off from QA reviewer in fork PR

6. After CI and QA sign-off, open upstream MCP PR. Link fork PR, note QA sign-off, include verification steps.

7. Post-merge housekeeping:
   ```bash
   git checkout testing-main
   git pull upstream testing-main
   git push origin testing-main
   git branch -d <feature-branch>
   git push origin --delete <feature-branch>
   ```

### Sprint Branch Mapping

| Sprint   | Tickets                                                                                                             | Branch Names                                                                                                                                                                                                                                                                                                                                                           |
| -------- | ------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sprint 1 | LMS-CORE-01, LMS-CORE-02, LMS-ACQ-10, LMS-ACQ-01, LMS-ACQ-02                                                        | `LMS-CORE-01/setup-pouchdb-sqlite`, `LMS-CORE-02/implement-sha256-hashing`, `LMS-ACQ-10/preload-ges-curriculum-tags`, `LMS-ACQ-01/vendor-management-ghana-card`, `LMS-ACQ-02/curriculum-tag-selection`                                                                                                                                                                 |
| Sprint 2 | LMS-CORE-04, LMS-PROC-10, LMS-PROC-11, LMS-PROC-12, LMS-PROC-01, LMS-PROC-02, LMS-PROC-03, LMS-PROC-04              | `LMS-CORE-04/30-second-auto-save`, `LMS-PROC-10/pdf417-barcode-generator`, `LMS-PROC-11/ghana-seasonal-calendar`, `LMS-PROC-12/barcode-rotation-cycle`, `LMS-PROC-01/condition-scoring-sliders`, `LMS-PROC-02/mold-risk-assessment`, `LMS-PROC-03/batch-assignment`, `LMS-PROC-04/extension-services-routing`                                                          |
| Sprint 3 | LMS-CORE-03, LMS-DIST-10, LMS-DIST-11, LMS-DIST-12, LMS-DIST-01, LMS-DIST-02, LMS-DIST-03, LMS-DIST-04              | `LMS-CORE-03/incremental-backup-scheduler`, `LMS-DIST-10/offline-pdf-generation`, `LMS-DIST-11/tamale-bolgatanga-corridor`, `LMS-DIST-12/extension-depot-routing`, `LMS-DIST-01/batch-aware-packing-slips`, `LMS-DIST-02/rural-delivery-mode`, `LMS-DIST-03/rainy-season-alerts`, `LMS-DIST-04/extension-depot-delivery`                                               |
| Sprint 4 | LMS-CHILD-10, LMS-CHILD-11, LMS-CHILD-01, LMS-CHILD-02, LMS-CHILD-03                                                | `LMS-CHILD-10/degradation-engine`, `LMS-CHILD-11/ges-academic-calendar`, `LMS-CHILD-01/batch-promotion`, `LMS-CHILD-02/degradation-threshold-enforcement`, `LMS-CHILD-03/teleporter-detection`                                                                                                                                                                         |
| Sprint 5 | LMS-STAFF-10, LMS-STAFF-01, LMS-STAFF-02, LMS-STAFF-03, LMS-LEND-10, LMS-LEND-01, LMS-LEND-02, LMS-GH-10, LMS-GH-01 | `LMS-STAFF-10/role-based-ui-filtering`, `LMS-STAFF-01/staff-profiles-hashing`, `LMS-STAFF-02/department-role-switching`, `LMS-STAFF-03/extension-staff-certification`, `LMS-LEND-10/cross-department-book-status`, `LMS-LEND-01/fulfill-bulk-allocation`, `LMS-LEND-02/rotation-tracking-return`, `LMS-GH-10/offline-sms-queue`, `LMS-GH-01/twi-dagbani-sms-templates` |
| Sprint 6 | LMS-CORE-06, LMS-EXT-10, LMS-EXT-11, LMS-EXT-12, LMS-EXT-13, LMS-EXT-01, LMS-EXT-02, LMS-EXT-03                     | `LMS-CORE-06/department-security-objects`, `LMS-EXT-10/android-offline-transaction-app`, `LMS-EXT-11/qr-learner-identification`, `LMS-EXT-12/extension-lending-sync`, `LMS-EXT-13/extension-schedule-safety`, `LMS-EXT-01/bulk-book-requests`, `LMS-EXT-02/rotation-cycle-management`, `LMS-EXT-03/school-delivery-tracking`                                           |
| Sprint 7 | LMS-EXT-04, LMS-EXT-05, LMS-GH-11, LMS-GH-12, LMS-GH-02, LMS-LEND-03, LMS-CORE-05                                   | `LMS-EXT-04/qr-checkout-return-android`, `LMS-EXT-05/dagbani-sms-templates`, `LMS-GH-11/ghana-seasonal-calendar-mold`, `LMS-GH-12/dagbani-language-support`, `LMS-GH-02/community-leader-notification`, `LMS-LEND-03/collection-health-monitoring`, `LMS-CORE-05/couchdb-raspberry-pi`                                                                                 |

---

## 5. Cross-Cutting Constraints

### Architecture Boundaries

| Boundary              | Rule                                                      |
| --------------------- | --------------------------------------------------------- |
| System vs Application | System tasks enable features; features deliver user value |
| Manager vs Enterprise | Manager first, Enterprise builds on top                   |
| Department Isolation  | Extension ↔ Lending data access blocked                   |
| Desktop vs Android    | Android is external tool, not part of Electron app        |

### Department Security

- Extension Services staff CANNOT access library section data
- Lending staff see ONLY "Bulk Requests" tab for Extension requests
- Cross-department writes blocked by security objects

### Jurisdiction Compliance

- Country-specific privacy rules: auto-anonymization, purge, and audit trails
- Curriculum tags stored from the selected national or institutional profile, available offline as needed
- Academic calendar rules derived from the active country policy: promotion windows, expiry dates, and rollover logic
- Local-language support for rural or mobile operations
- Rural corridor safety protocols based on active delivery policy and community leadership requirements

### Offline-First Requirements

- All critical workflows complete locally
- Sync deferred to reconnect
- 30-second auto-save for power resilience
- 24-hour outage tolerance with zero data loss

---

## 6. Ticket Completion Gate

A ticket is complete only when:

- [ ] All acceptance criteria from `jira_doc.md` satisfied
- [ ] Offline behavior demonstrated
- [ ] Security/privacy checks pass for sensitive fields
- [ ] Audit artifacts exist where required
- [ ] Manager/Enterprise impact recorded
- [ ] Extension Services department boundary verified (where applicable)
- [ ] Bulk allocation workflow integrity confirmed (where applicable)

---

## 7. Quick Reference

| Question             | Answer                       |
| -------------------- | ---------------------------- |
| Base branch?         | `testing-main`               |
| Issues per branch?   | Exactly one                  |
| PR target?           | `testing-main`               |
| Package manager?     | `pnpm` only                  |
| Device baseline?     | Windows 10, 4GB RAM          |
| Department boundary? | Extension ↔ Lending isolated |
| Offline requirement? | All critical workflows       |
| Country policy?      | Configurable by jurisdiction |

---

_Document Version: 2.0 • Prepared for multi-country African library operations • October 2026_
