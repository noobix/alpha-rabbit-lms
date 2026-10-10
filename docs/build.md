---
Author: Kelvin Kabute
Last-updated: 2026-10-10
---

# 🏗️ Alpha Rabbit LMS Build Document

## 📋 File Context

**Purpose:** This file is the implementation blueprint for agents and contributors. It explains the authoritative source documents, project guardrails, sprint structure, and verification gates that should guide build work.

**Why this matters:** A library system in Africa is operationally different from a single-branch desktop product. This document keeps the project adaptable across national policies, rural delivery realities, school calendars, and multi-department workflows without breaking the existing lifecycle model.

**How agents use it:** Agents should use this file to understand the sequence of work, the project constraints, and the country-configurable rules that must remain in place before a feature is considered complete.

## 1. 📦 Source Assets & Defaults

### 📚 Source Assets

| Asset | Purpose | Required Use |
|-------|---------|--------------|
| `docs/jira/compression.md` | Canonical ticket scope and acceptance criteria | Source of truth for every ticket |
| `docs/jira/jira_doc.md` | Detailed ticket specification with sprint planning | Sprint sequencing, labeling, quality gates |
| `docs/prompt_main.md` | Architecture constraints and project structure | Codebase layout, mode split, non-functional constraints |
| `docs/database.md` | Canonical schema contracts | Doc types, retention, sync state, audit fields |
| `docs/ressources/product_specs.md` | Stack and deployment decisions | Offline-first stack, packaging, Ghana hardware |
| `docs/ressources/system_specs.md` | Manager vs Enterprise setup | Environment-specific behavior |
| `docs/ressources/functionality_specs.md` | End-to-end module behavior | Acquisitions → Processing → Distribution → Sections |
| `docs/ressources/module_functionality_specs.md` | User-centric module acceptance | User stories, offline behavior, Extension workflows |
| `docs/ressources/functionality_specs_expanded.md` | Patron intelligence, governance extensions | Degradation engine, badges, patron signals |
| `docs/ressources/db_engineering.md` | Database architecture and patterns | PouchDB setup, sync, conflict resolution, repository pattern |
| `docs/research_dmp/aquisisions_module.md` | Deep implementation notes for acquisitions | Forms, metadata shape, offline patterns |
| `docs/research_dmp/processing_module.md` | Deep implementation notes for processing | Condition model, mold risk, barcode behavior |
| `docs/research_dmp/distribution_module.md` | Deep implementation notes for distribution | Packing slips, rural mode, delivery confirmation |
| `docs/research_dmp/extension_module.md` | Deep implementation notes for Extension Services | Android app, QR learner tracking, bulk allocation |
| `docs/research_dmp/library_sections_pi_sg.md` | Deep implementation notes for sections + PI + governance | Degradation enforcement, section workflows |
| `docs/research_dmp/deploy_doc.md` | Pilot/deployment/validation package | Pilot validation, packaging constraints |

### 🛡️ Global Non-Negotiables

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

### 🗄️ Database Modeling Requirements (must be planned before build work)

- **Domain separation**: maintain distinct domain databases or collections for `books`, `patrons`, `loans`, `extensionLoans`, `departments`, `auditLog`, and `config` rather than building one large flat document store.
- **Shared document contract**: every record must include the shared `BaseDocument` fields (`_id`, `_rev`, `type`, `createdAt`, `updatedAt`, `_syncStatus`, `_schemaVersion`) and any domain-specific fields must be added through a versioned schema definition.
- **Validation layer**: implement runtime validation with Zod at the application boundary, and enforce critical business rules at the server or replication layer (Enterprise) when the data crosses trust boundaries.
- **Migration readiness**: schema changes must be traceable and reversible; document versioning and migration notes are part of the delivery requirements, not a later cleanup task.
- **Conflict handling**: record writes from multiple rural devices must be treated as first-class events; no silent overwrite of concurrent edits; every conflict must be resolved with an explicit audit trail and human-visible review when needed.
- **Repository pattern**: all database operations must use the type-safe `BaseRepository<T>` pattern with auto-generated IDs, timestamps, and validation before persistence.
- **Index strategy**: required indexes must exist for `type + status`, `type + department`, `type + barcode`, `type + cycleCode`, `type + schoolId`, `type + patronId + status`, and `type + dueDate`.

---

## 2. 📅 Sprint Plan Overview

| Sprint | Weeks | Theme | Tickets | Goal |
|--------|-------|-------|---------|------|
| **1** | 1-2 | Core Infrastructure | LMS-CORE-01, LMS-CORE-02, LMS-CORE-03, LMS-CORE-04 | Zero data loss after 24h simulated outage; PouchDB + SQLite working |
| **2** | 3-4 | Database Foundation + Backup System | LMS-CORE-07, LMS-CORE-08, LMS-CORE-09, LMS-CORE-10, LMS-CORE-11, LMS-BACK-01, LMS-BACK-02, LMS-BACK-03 | All domain databases initialized; Zod validation enforced; Repository pattern implemented; Sync and conflict handling operational; Backup pipeline fully automated with cloud storage |
| **3** | 5-6 | Acquisitions + Ghana Compliance | LMS-ACQ-01, LMS-ACQ-02, LMS-ACQ-03, LMS-ACQ-10, LMS-ACQ-11, LMS-GH-01, LMS-GH-02, LMS-GH-10, LMS-GH-11, LMS-GH-12 | 247 curriculum tags load offline in <2s; Orders sync on reconnect; Country profiles configurable for multi-country deployment |
| **4** | 7-8 | Processing + Extension Routing | LMS-PROC-01, LMS-PROC-02, LMS-PROC-03, LMS-PROC-04, LMS-PROC-10, LMS-PROC-11, LMS-PROC-12 | Mold risk ≥90% accuracy; Extension routing populates conditional fields; Seasonal calendar operational |
| **5** | 9-10 | Distribution + Extension Depot | LMS-DIST-01, LMS-DIST-02, LMS-DIST-03, LMS-DIST-04, LMS-DIST-10, LMS-DIST-11, LMS-DIST-12 | Packing slips <10s offline; depot routing includes rotation metadata; Dagbani SMS operational |
| **6** | 11-12 | Children's Section + Degradation | LMS-CHILD-01, LMS-CHILD-02, LMS-CHILD-03, LMS-CHILD-10, LMS-CHILD-11 | Batch promotion 100% accurate; degradation ≥90% accuracy; GES calendar enforced |
| **7** | 13-14 | Staff + Lending Section | LMS-STAFF-01, LMS-STAFF-02, LMS-STAFF-03, LMS-STAFF-10, LMS-LEND-01, LMS-LEND-02, LMS-LEND-03, LMS-LEND-10 | Role switching includes Extension; bulk allocation workflow tested |
| **8** | 15-16 | Extension Services + Android | LMS-EXT-01, LMS-EXT-02, LMS-EXT-03, LMS-EXT-04, LMS-EXT-05, LMS-EXT-10, LMS-EXT-11, LMS-EXT-12, LMS-EXT-13 | Department boundary enforced; rotation cycles aligned with GES; Android syncs 100 transactions offline |
| **9** | 17-18 | Data Operations & Disaster Recovery | LMS-DATA-01, LMS-DATA-02, LMS-DATA-03, LMS-DATA-04, LMS-DATA-05, LMS-DATA-06, LMS-DATA-07 | Import, export, seeding, retention, migration, and disaster recovery operational |
| **10** | 19-20 | Sync Infrastructure & Conflict Resolution | LMS-SYNC-01, LMS-SYNC-02, LMS-SYNC-03, LMS-SYNC-04, LMS-SYNC-05, LMS-SYNC-06 | Conflict UX, partitions, server validation, Android sync, and sync testing |
| **11** | 21-22 | Data Quality & Integrity | LMS-QUAL-01, LMS-QUAL-02, LMS-QUAL-03, LMS-QUAL-04, LMS-QUAL-05, LMS-QUAL-06, LMS-QUAL-07, LMS-QUAL-08, LMS-QUAL-09, LMS-QUAL-10 | Duplicate detection, collision handling, monitoring, error handling, and performance targets |

---

## 3. 🔍 Detailed Sprint Breakdown

### 3.1 Sprint 1: Core Infrastructure

**Results to achieve:**

- PouchDB offline storage with SQLite adapter operational
- National ID hashing and masking verified by DPC liaison
- Incremental backup scheduler with cloud storage integration
- 30-second auto-save for power outage resilience

**Tickets in scope:**

| Ticket | Type | Title | Effort | Dependencies |
|--------|------|-------|--------|--------------|
| LMS-CORE-01 | System | Set up PouchDB with SQLite adapter for offline storage | 5 | None |
| LMS-CORE-02 | System | Implement SHA-256 hashing for national ID storage | 3 | LMS-CORE-01 |
| LMS-CORE-03 | System | Build incremental backup scheduler | 5 | LMS-CORE-01 |
| LMS-CORE-04 | System | Implement 30-second auto-save for power outage resilience | 3 | LMS-CORE-01 |
| LMS-CORE-05 | System | Set up CouchDB server deployment for Raspberry Pi 4 | 8 | None |

**Build Focus:**

- SQLite database creation at `C:/GhanaLibraryData/`
- Indexed collections for books, patrons, staff, extension records
- National ID format validation at form boundary (country-aware)
- Hashing service in Electron main process only
- Masked display per country profile
- Backup: daily 8 PM incremental, ≤5% DB size, compressed for cloud storage upload
- 30-day retention with auto-deletion
- Auto-save every 30 seconds with checksum validation
- Recovery snapshot with timestamp display

**Verification Gate:**

- SQLite inspection confirms indexed collections
- Hashing audit: plaintext ID never in storage/logs/backups
- Backup resumes after power outage
- Auto-save recovers 99% of transactions >30s old after 4h outage

---

### 3.2 Sprint 2: Database Foundation + Backup System

**Results to achieve:**

- Shared `BaseDocument` contract enforced across all domain stores
- Zod validation at app boundary with migration gates
- Sync manager for Enterprise bi-directional replication
- Conflict resolution UI for staff review
- Data integrity monitoring and health reporting
- Backup pipeline fully automated with cloud storage

**Tickets in scope:**

| Ticket | Type | Title | Effort | Dependencies |
|--------|------|-------|--------|--------------|
| LMS-CORE-07 | System | Define the shared database contract and indexing strategy for all domain stores | 5 | LMS-CORE-01 |
| LMS-CORE-08 | System | Enforce Zod validation and migration gates for schema evolution | 4 | LMS-CORE-07 |
| LMS-CORE-09 | System | Implement sync manager for Enterprise bi-directional replication | 8 | LMS-CORE-07 |
| LMS-CORE-10 | System | Implement conflict resolution UI for staff review | 5 | LMS-CORE-09 |
| LMS-CORE-11 | System | Build data integrity monitoring and health reporting | 3 | LMS-CORE-07 |
| LMS-BACK-01 | System | Implement compression package integration | 5 | LMS-CORE-01 |
| LMS-BACK-02 | System | Implement cloud storage abstraction layer | 8 | LMS-BACK-01 |
| LMS-BACK-03 | System | Implement backup automation interface | 5 | LMS-BACK-02 |

**Build Focus:**

- BaseDocument contract: `_id`, `_rev`, `type`, `createdAt`, `updatedAt`, `_syncStatus`, `_schemaVersion`
- Required indexes: `type + status`, `type + department`, `type + barcode`, `type + cycleCode`, `type + schoolId`, `type + patronId + status`, `type + dueDate`
- Zod schemas for all domain entities
- Migration service with idempotent migrations and rollback support
- Sync state tracking: `idle`, `active`, `paused`, `error`, `offline`
- Conflict resolution: last-write-wins based on `updatedAt`, with manual review for critical conflicts
- Stale pending detection (>24h flagged)
- Clock skew detection beyond 5 minutes
- Health report generation for admin review
- Orphaned record detection
- Duplicate ISBN/barcode detection
- Compression package integration (archiver npm package)
- Cloud storage abstraction layer (Google Drive, Backblaze B2, Cloudflare R2)
- Backup automation interface with scheduling and credential management

**Verification Gate:**

- All domain databases follow BaseDocument contract
- Zod validation rejects invalid documents before write
- Sync resumes without data loss after extended offline
- Conflicts are preserved and reviewable by staff
- Health report shows orphaned records and schema violations
- Backup pipeline fully automated: backup → compress → upload → verify
- Cloud upload works with Google Drive, Backblaze B2, and Cloudflare R2

---

### 3.3 Sprint 3: Acquisitions + Ghana Compliance

**Results to achieve:**

- Vendor management with country-aware identity validation
- Budget tracking per department with country-aligned codes
- Offline order queue with sync-on-reconnect
- Ghana Data Protection Act compliance
- GES curriculum tags available offline
- Twi/Dagbani language support
- GES academic calendar with August 31 expiry
- Country profile configuration for multi-country African deployment

**Tickets in scope:**

| Ticket | Type | Title | Effort | Dependencies |
|--------|------|-------|--------|--------------|
| LMS-ACQ-01 | Feature | Vendor management with country-aware identity validation | 5 | LMS-CORE-01 |
| LMS-ACQ-02 | Feature | Budget tracking per department with country-aligned codes | 3 | LMS-CORE-01 |
| LMS-ACQ-03 | Feature | Offline order queue with sync-on-reconnect | 3 | LMS-CORE-01 |
| LMS-ACQ-10 | System | Build CSV/JSON data import pipeline | 5 | LMS-CORE-01 |
| LMS-ACQ-11 | System | Build data export pipeline | 3 | LMS-CORE-01 |
| LMS-GH-01 | System | Implement Ghana Data Protection Act 2012 (Act 843) compliance | 5 | LMS-CORE-01 |
| LMS-GH-02 | System | Integrate Ghana Education Service curriculum tags (2024/25) | 3 | LMS-CORE-01 |
| LMS-GH-10 | System | Build Twi/Dagbani language support | 5 | LMS-CORE-01 |
| LMS-GH-11 | System | Implement GES academic calendar with August 31 expiry | 3 | LMS-CORE-01 |
| LMS-GH-12 | System | Implement country profile configuration for multi-country African deployment | 8 | LMS-CORE-01 |

**Build Focus:**

- Vendor form: country-aware ID validation, hashing, masked display
- Company type taxonomy: sole_proprietorship, partnership, limited_liability, nonprofit, government, institution
- Business registration required per national policy
- Budget codes follow active country format
- Amber warning at <20% remaining
- Order queue: local save with `status: 'pending_sync'`, sync on reconnect
- Import: validate against BaseDocument contract, reject invalid rows, duplicate detection
- Export: JSON/CSV with hashed IDs preserved, includes `_schemaVersion`
- DPA compliance: auto-anonymize after 2 years inactive, purge within 72 hours
- Curriculum tags: 247 GES tags, grouped by Basic/JHS/SHS, ≤2.5MB embedded JSON
- Language support: Twi/Dagbani translations validated by UDS linguists
- Academic calendar: August 31 expiry, August 15 promotion, June 15 pre-promotion report
- Country profiles: configurable identity rules, curriculum systems, academic calendars, local labels

**Verification Gate:**

- Vendor form rejects invalid ID format per country profile
- Budget blocks orders exceeding remaining balance
- Orders sync within 60 seconds of internet restoration
- Import rejects invalid rows with clear error messages
- DPA compliance: patron records anonymized after 2 years
- 247 curriculum tags load offline in <2s
- Country profiles support Ghana, Kenya, Uganda, Tanzania

---

### 3.4 Sprint 4: Processing + Extension Routing

**Results to achieve:**

- Condition scoring sliders with climate-aware weighting
- Automatic mold risk assessment based on seasonal calendar
- PDF417 barcodes with Ghana Library Authority format
- Extension Services routing with durability scoring and corridor safety
- Barcode and QR code collision detection
- Ghana seasonal calendar service
- Barcode rotation cycle indicator for Extension

**Tickets in scope:**

| Ticket | Type | Title | Effort | Dependencies |
|--------|------|-------|--------|--------------|
| LMS-PROC-01 | Feature | Condition scoring sliders (spine/cover/pages/edges) | 5 | LMS-CORE-01 |
| LMS-PROC-02 | Feature | Automatic mold risk assessment | 3 | LMS-PROC-11 |
| LMS-PROC-03 | Feature | PDF417 barcodes with Ghana Library Authority format | 3 | LMS-PROC-12 |
| LMS-PROC-04 | Feature | Extension Services routing with durability scoring | 5 | LMS-PROC-12 |
| LMS-PROC-10 | System | Barcode and QR code collision detection | 2 | LMS-CORE-01 |
| LMS-PROC-11 | System | Ghana seasonal calendar service | 3 | LMS-CORE-01 |
| LMS-PROC-12 | System | Barcode rotation cycle indicator for Extension | 3 | LMS-CORE-01 |

**Build Focus:**

- Four 1-5 sliders: Spine (40%), Cover (25%), Pages (25%), Edges (10%)
- Climate-aware tooltips: "Critical in humid climate – check for separation"
- Mold risk: automatic based on device date, high during rainy seasons
- Seasonal calendar: Dec-Feb (dry), Mar-May/Sept-Nov (rainy), Jun-Aug (major rainy)
- Barcode format: `[SUBJECT]-[GRADE][AUTHOR_INITIAL]-[SEQUENTIAL]`
- Extension suffix: `-C[1-4]` for rotation cycles
- Extension routing conditional fields: Rotation Cycle, Mobile Handling Durability, Destination Region
- Durability ≥3 required for Tamale-Bolgatanga corridor
- Corridor safety protocols auto-trigger for Northern Region
- Collision detection: logged for audit, new unique ID generated

**Verification Gate:**

- Condition scoring works offline
- Mold risk assessment matches manual review (≥90%)
- Barcode format `SCI-6M-042-C2` generated correctly
- Extension routing shows conditional fields, hides batch assignment
- Collisions logged in audit trail

---

### 3.5 Sprint 5: Distribution + Extension Depot

**Results to achieve:**

- Batch-aware packing slips with GRADE-4A vs GRADE-4B separation
- Rural delivery mode for Tamale-Bolgatanga corridor
- Rainy season alerts on packing slips
- Extension Services depot delivery with rotation cycle metadata
- Offline PDF generation for packing slips
- Tamale-Bolgatanga corridor detection service
- Extension Services depot routing with Dagbani SMS

**Tickets in scope:**

| Ticket | Type | Title | Effort | Dependencies |
|--------|------|-------|--------|--------------|
| LMS-DIST-01 | Feature | Batch-aware packing slips | 5 | LMS-DIST-10 |
| LMS-DIST-02 | Feature | Rural delivery mode for Tamale-Bolgatanga | 3 | LMS-DIST-11 |
| LMS-DIST-03 | Feature | Rainy season alerts on packing slips | 2 | LMS-PROC-11 |
| LMS-DIST-04 | Feature | Extension depot delivery with rotation metadata | 5 | LMS-DIST-12 |
| LMS-DIST-10 | System | Offline PDF generation for packing slips | 5 | LMS-CORE-01 |
| LMS-DIST-11 | System | Tamale-Bolgatanga corridor detection service | 3 | LMS-CORE-01 |
| LMS-DIST-12 | System | Extension Services depot routing with Dagbani SMS | 5 | LMS-DIST-10 |

**Build Focus:**

- Packing slip groups books by batch with learner counts
- Repeat batch warning: "Repeat learners – 20% extra books required"
- Rural mode toggle disables GPS, requires community leader contact
- Rainy season banner: "RAINY SEASON ALERT: Use waterproof covers + silica gel"
- Glossy page books (Science/Math) flagged for extra protection
- Depot routing: rotation cycle indicator, depot location, community leader signature
- READ-ONLY rotation cycle metadata (assigned during Lending fulfillment)
- Dagbani SMS: "Zuli libri ka ti kpɛ. Cycle 2 books arriving today."
- PDF generation works offline, saves to `C:/GhanaLibraryData/packing-slips/`
- File size ≤500KB for easy sharing
- Corridor detection: school ID prefix matching against corridor list

**Verification Gate:**

- Packing slips generate offline <10s
- Rural mode disables GPS without errors
- Extension depot packing slips include rotation metadata
- PDF contains school name, batch groupings, PDF417 barcode, QR code
- Corridor list embedded in seed data (works offline)
- Dagbani SMS queues offline, sends on reconnect

---

### 3.6 Sprint 6: Children's Section + Degradation Engine

**Results to achieve:**

- GES-aligned batch promotion on August 15
- Degradation threshold enforcement blocking poor-care patrons
- "Teleporter" detection with oral tradition context
- Degradation engine with climate-aware weighting
- GES academic calendar service

**Tickets in scope:**

| Ticket | Type | Title | Effort | Dependencies |
|--------|------|-------|--------|--------------|
| LMS-CHILD-01 | Feature | GES-aligned batch promotion workflow | 5 | LMS-CHILD-11 |
| LMS-CHILD-02 | Feature | Degradation threshold enforcement engine | 5 | LMS-CHILD-10 |
| LMS-CHILD-03 | Feature | "Teleporter" detection with oral tradition context | 3 | LMS-CHILD-10 |
| LMS-CHILD-10 | System | Degradation engine with climate-aware weighting | 8 | LMS-CORE-01 |
| LMS-CHILD-11 | System | GES academic calendar service | 3 | LMS-CORE-01 |

**Build Focus:**

- Degradation formula: climate-aware weighting (spine 40%, cover 25%, pages 25%, edges 10%)
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

### 3.7 Sprint 7: Staff + Lending Section

**Results to achieve:**

- Staff profiles with hashed national ID
- Department role switching (including Extension Services)
- Extension staff route certification and bulk request authority
- Lending Section bulk allocation fulfillment
- Rotation tracking and return workflow
- Cross-department book status tracking
- Data retention and archival policy engine

**Tickets in scope:**

| Ticket | Type | Title | Effort | Dependencies |
|--------|------|-------|--------|--------------|
| LMS-STAFF-01 | Feature | Staff profiles with national ID hashing | 3 | LMS-CORE-02 |
| LMS-STAFF-02 | Feature | Department role switching | 5 | LMS-CORE-06 |
| LMS-STAFF-03 | Feature | Extension staff route certification | 3 | LMS-CORE-06 |
| LMS-STAFF-10 | System | Data retention and archival policy engine | 3 | LMS-CORE-01 |
| LMS-LEND-01 | Feature | Fulfill bulk allocation requests from Extension | 5 | LMS-CORE-06 |
| LMS-LEND-02 | Feature | Rotation tracking and return workflow | 3 | LMS-CORE-06 |
| LMS-LEND-03 | Feature | Collection health monitoring for Extension-loaned books | 3 | LMS-CORE-06 |
| LMS-LEND-10 | System | Cross-department book status tracking | 5 | LMS-CORE-01 |

**Build Focus:**

- Staff form: document ID validation, hashing, masked display per country policy
- Duplicate ID prevention across staff records
- Role switcher dropdown: System Admin, Acquisitions, Processing, Distribution, Library Operations, Extension Services
- Extension role shows ONLY Extension workflows
- Lending role shows "Bulk Requests" tab alongside regular lending
- Extension staff: route certification, bulk request authority, rotation cycle access
- Bulk request fulfillment: select books from available collection
- Status change: "On Loan to Extension Services" with cycle metadata
- Books marked unavailable for regular circulation
- Return workflow: condition reassessment, status revert to "Available"
- Track: cycle history, rotation count, cumulative condition changes
- Overdue returns beyond active academic policy trigger escalation
- Collection health: rotation history, cycles served, destinations, condition at each return
- Cumulative Extension degradation tracked separately
- Withdrawal recommendation when condition drops below threshold
- Cross-department sync: real-time sync prevents double-allocation
- Data retention: patron anonymization after 2 years, audit log archival, sync queue purge, tombstone cleanup

**Verification Gate:**

- Staff roles switch without data loss
- Extension staff CANNOT access library section data
- Lending bulk allocation fulfills requests correctly
- Cross-department sync prevents double-allocation
- Collection health shows rotation history and cumulative degradation

---

### 3.8 Sprint 8: Extension Services + Android

**Results to achieve:**

- Bulk book requests for school rotation cycles
- Rotation cycle management aligned with GES calendar
- School delivery tracking via mobile van
- Dagbani SMS templates for Northern Region
- Android offline transaction app
- QR-based learner identification with smart tag design
- Extension-Lending cross-department book status sync
- Schedule management with corridor safety

**Tickets in scope:**

| Ticket | Type | Title | Effort | Dependencies |
|--------|------|-------|--------|--------------|
| LMS-EXT-01 | Feature | Bulk book requests for school rotation cycles | 5 | LMS-CORE-06 |
| LMS-EXT-02 | Feature | Rotation cycle management with GES calendar | 5 | LMS-CORE-06 |
| LMS-EXT-03 | Feature | School delivery tracking via mobile van | 3 | LMS-CORE-06 |
| LMS-EXT-04 | Feature | Dagbani SMS templates for Northern Region | 3 | LMS-GH-10 |
| LMS-EXT-05 | Feature | Dagbani SMS templates for Northern Region schools | 3 | LMS-GH-10 |
| LMS-EXT-10 | System | Android offline transaction app | 13 | LMS-CORE-06 |
| LMS-EXT-11 | System | QR-based learner identification with smart tag design | 5 | LMS-EXT-10 |
| LMS-EXT-12 | System | Extension-Lending cross-department book status sync | 8 | LMS-LEND-10 |
| LMS-EXT-13 | System | Extension schedule management with corridor safety | 3 | LMS-CORE-06 |

**Build Focus:**

- Bulk request form: school, cycle, quantity, subject areas, destination region
- Request status: Pending → Approved → Fulfilling → Ready for Delivery
- 4-cycle rotation: CYCLE-1 (Sept-Dec), CYCLE-2 (Jan-Mar), CYCLE-3 (Apr-Jun), CYCLE-4 (Jul-Aug)
- Auto-flag sets for collection 14 days before cycle end
- August 31 hard stop: ALL sets return to depot
- Schedule dashboard: scheduled/in-progress/completed/missed
- Community leader contacts pre-loaded per school
- Rainy season road alerts for affected routes
- Dagbani SMS validated by UDS linguist
- Android app: ZXing QR scanning, low-light capable
- Local SQLite encrypted at rest (Android Keystore)
- Battery optimization: 30s screen timeout, low-power mode
- Post-service sync on depot Wi-Fi
- QR smart tag: 85.6×54mm, 250-micron laminate, rounded corners
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

### 3.9 Sprint 9: Data Operations & Disaster Recovery

**Results to achieve:**

- CSV/JSON data import pipeline for existing library records
- Data export pipeline for library records
- Reference data seeding service for country profiles and curriculum tags
- Data retention and archival policy engine
- Disaster recovery and backup verification service
- Schema migration service for live database upgrades
- Soft-delete and record restoration

**Tickets in scope:**

| Ticket | Type | Title | Effort | Dependencies |
|--------|------|-------|--------|--------------|
| LMS-DATA-01 | System | Build CSV/JSON data import pipeline for existing library records | 5 | LMS-CORE-07 |
| LMS-DATA-02 | System | Build data export pipeline for library records | 3 | LMS-CORE-07 |
| LMS-DATA-03 | System | Build reference data seeding service for country profiles and curriculum tags | 5 | LMS-CORE-07 |
| LMS-DATA-04 | System | Implement data retention and archival policy engine | 3 | LMS-CORE-07 |
| LMS-DATA-05 | System | Build disaster recovery and backup verification service | 5 | LMS-CORE-03 |
| LMS-DATA-06 | System | Implement schema migration service for live database upgrades | 4 | LMS-CORE-08 |
| LMS-DATA-07 | System | Implement soft-delete and record restoration | 3 | LMS-CORE-07 |

**Build Focus:**

- Import: validate against BaseDocument contract, reject invalid rows with clear error messages, duplicate detection, works fully offline
- Export: JSON or CSV format, national ID hashes remain hashed, includes `_schemaVersion`, works fully offline
- Seeding: pre-configured country profiles available offline on first launch, curriculum tags pre-loaded per profile, seed data updatable via versioned update package
- Retention: patron records anonymized after 2 years inactive per country policy, audit logs archived after configured period, sync queue purged after successful sync, tombstones cleaned up after 90 days
- Disaster recovery: backup integrity verified before restore, point-in-time recovery supported, full restore testable without affecting production data, restore completion verified with checksum audit
- Migration: existing documents migrated to new schema on app update, migration is idempotent, migration failures logged and rolled back, old schema records flagged until migrated
- Soft-delete: deleted records visible in recycle bin for 30 days, records restorable within retention window, deletions sync across Enterprise clients

**Verification Gate:**

- Import rejects invalid rows with line number and error
- Export preserves hashed IDs and includes schema version
- Seed data loads offline on first launch
- Retention policy anonymizes records after configured period
- Backup restore verified without affecting production data
- Migration is idempotent and reversible
- Soft-deleted records restorable within 30 days

---

### 3.10 Sprint 10: Sync Infrastructure & Conflict Resolution

**Results to achieve:**

- Conflict resolution UI for staff review
- Extended offline behavior for Enterprise network partitions
- CouchDB server-side document validation
- Android app sync protocol and data contract
- Sync health monitoring and stale pending detection
- Sync testing harness for conflict and partition simulation

**Tickets in scope:**

| Ticket | Type | Title | Effort | Dependencies |
|--------|------|-------|--------|--------------|
| LMS-SYNC-01 | System | Build conflict resolution UI for staff review | 5 | LMS-CORE-09 |
| LMS-SYNC-02 | System | Implement extended offline behavior for Enterprise network partitions | 5 | LMS-CORE-09 |
| LMS-SYNC-03 | System | Implement CouchDB server-side document validation | 4 | LMS-CORE-07 |
| LMS-SYNC-04 | System | Define Android app sync protocol and data contract | 5 | LMS-EXT-10 |
| LMS-SYNC-05 | System | Implement sync health monitoring and stale pending detection | 3 | LMS-CORE-09 |
| LMS-SYNC-06 | System | Build sync testing harness for conflict and partition simulation | 5 | LMS-CORE-09 |

**Build Focus:**

- Conflict resolution: both document versions shown side-by-side, admin can choose which version to keep, losing version preserved in audit log, conflicts categorized by severity, clock skew beyond 5 minutes detected and flagged
- Extended offline: sync resumes without data loss after extended offline, large sync batches throttled on slow connections, UI shows sync progress and estimated completion, max offline duration configured (e.g., 90 days)
- Server-side validation: `validate_doc_update` checks schema contract on server, invalid documents rejected before replication, validation rules versioned alongside schema, department isolation enforced server-side
- Android sync: transactions sync via defined protocol on depot Wi-Fi, compressed batch transfer, conflicts resolved by `transactionDate`, Android app authenticates via API key or device token
- Health monitoring: stale pending records (>24h) flagged, UI shows sync success/failure rates per device, manual retry available for failed syncs
- Testing harness: simulate network partitions, inject concurrent edits from multiple clients, verify conflict resolution correctness, test large dataset replication (10k+ documents)

**Verification Gate:**

- Conflict resolution UI shows both versions side-by-side
- Sync resumes without data loss after 24h offline
- Server-side validation rejects invalid documents
- Android sync protocol works on depot Wi-Fi
- Stale pending records flagged after 24h
- Testing harness simulates partitions and conflicts

---

### 3.11 Sprint 11: Data Quality & Integrity

**Results to achieve:**

- Duplicate book detection during acquisition and processing
- Barcode and QR code collision detection
- Data integrity monitoring and health reporting
- Config database contents and sync behavior
- User-facing error messages for all failure modes
- Bulk operation performance targets
- Clock skew detection for conflict resolution
- Attachment storage strategy for images and binary data
- Anonymization for analytics and aggregate reporting
- Database backup verification and restore testing

**Tickets in scope:**

| Ticket | Type | Title | Effort | Dependencies |
|--------|------|-------|--------|--------------|
| LMS-QUAL-01 | System | Implement duplicate book detection during acquisition and processing | 3 | LMS-CORE-07 |
| LMS-QUAL-02 | System | Implement barcode and QR code collision detection | 2 | LMS-CORE-07 |
| LMS-QUAL-03 | System | Build data integrity monitoring and health reporting | 3 | LMS-CORE-11 |
| LMS-QUAL-04 | System | Define config database contents and sync behavior | 2 | LMS-CORE-07 |
| LMS-QUAL-05 | System | Implement user-facing error messages for all failure modes | 3 | LMS-CORE-07 |
| LMS-QUAL-06 | System | Define bulk operation performance targets | 2 | LMS-CORE-07 |
| LMS-QUAL-07 | System | Implement clock skew detection for conflict resolution | 3 | LMS-CORE-10 |
| LMS-QUAL-08 | System | Define attachment storage strategy for images and binary data | 3 | LMS-CORE-07 |
| LMS-QUAL-09 | System | Implement anonymization for analytics and aggregate reporting | 3 | LMS-CORE-07 |
| LMS-QUAL-10 | System | Define database backup verification and restore testing | 3 | LMS-DATA-05 |

**Build Focus:**

- Duplicate detection: ISBN/title match triggers duplicate warning, librarian can add new copy or cancel, works offline
- Collision detection: collision detected and new unique ID generated, collision logged for audit
- Integrity monitoring: orphaned records detected, invalid enum values and schema violations flagged, health report generated for admin review
- Config database: treated differently from transactional data, per-device overrides allowed, config changes audited
- Error messages: clear, actionable error messages, technical details logged but not shown to non-admin users, localized in Twi/Dagbani where applicable
- Performance targets: batch promotion of 500 patrons <30s, processing 100 books <60s, packing slips for 50 schools <120s
- Clock skew: clock skew beyond 5 minutes detected, conflicts flagged for manual review when skew detected, last-write-wins with skew awareness
- Attachments: images compressed to target size (<200KB covers, <500KB photos), external file storage for large attachments, sync bandwidth throttled on slow connections
- Anonymization: patron data anonymized in aggregate reports, individual patrons not identifiable from analytics, Ghana Data Protection Act compliance
- Backup verification: backup integrity verified before restore, full restore testable without affecting production data, restore completion verified with checksum audit

**Verification Gate:**

- Duplicate detection warns on ISBN/title match
- Collision detection generates new unique ID and logs event
- Health report shows orphaned records and schema violations
- Error messages are clear and actionable
- Bulk operations meet performance targets
- Clock skew detected beyond 5 minutes
- Attachments compressed to target size
- Analytics data is anonymized
- Backup restore verified without affecting production

---

## 4. 🚀 Development & Release Workflow: Branching, Commits, PRs & Build Tags

### 🧭 Overview

All feature development follows a branch-per-ticket model anchored to ticket IDs from `docs/jira/compression.md`. The `develop` branch is the development base and integration target for all feature work during a sprint. Pull requests are the only merge path into `develop`. Every merge commit is tagged with a lightweight build number. The `testing-main` branch serves a single, well-defined role: it is the integration target for sprint completion and the branch where the CI `minor-release` job creates the sprint annotated tag. After a full sprint is implemented on `develop` and verified with no issues, a single PR is made from `develop` to `testing-main`; the merge triggers the CI job that produces the semantic version tag and release artifacts.

### 🌿 Branch Naming Convention

```text
LMS-[XXX]/[title-or-description]
```

- `[XXX]` = the ticket ID from `compression.md` (e.g., `CORE-01`, `ACQ-01`, `PROC-04`)
- `[title-or-description]` = kebab-case summary of the ticket title

**Examples:**

| Ticket | Branch Name |
|--------|-------------|
| LMS-CORE-01 | `LMS-CORE-01/set-up-pouchdb-sqlite-offline-storage` |
| LMS-ACQ-01 | `LMS-ACQ-01/vendor-management-country-identity` |
| LMS-PROC-04 | `LMS-PROC-04/extension-routing-durability` |
| LMS-EXT-01 | `LMS-EXT-01/bulk-book-requests-rotation` |

### 🛠️ Workflow Steps (Using GitHub MCP Tools)

#### Step 1: 🌱 Create Feature Branch from `develop`

Use the GitHub MCP `create_branch` tool to create the branch on the remote, branching off `develop`:

```yaml
Tool: mcp_io_github_git_create_branch
  owner: noobix
  repo: alpha-rabbit-lms
  branch: LMS-[XXX]/[title-or-description]
  from_branch: develop
```

#### Step 2: 🔄 Sync with `develop`

If a PR already exists for the branch and `develop` has moved ahead, use the MCP `update_pull_request_branch` tool to pull the latest base branch changes into the feature branch:

```yaml
Tool: mcp_io_github_git_update_pull_request_branch
  owner: noobix
  repo: alpha-rabbit-lms
  pullNumber: <PR number>
```

This merges the latest `develop` into the feature branch on the remote — no local pull needed.

#### Step 3: 💻 Implement the Feature

Work on the ticket. Every commit message must paint a clear picture of what was built and why. Use the acceptance criteria from `compression.md` as context to inform what you write — don't copy them verbatim, describe the work you actually did.

**Commit message format:**

```text
LMS-[XXX]: <type>: <vivid summary of what was accomplished>

<Paragraph explaining what was built, how it works, and why it was
done this way. Reference the real behavior and constraints from the
ticket naturally — not as a checklist.>
```

Where `<type>` is one of: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`.

**Example (LMS-CORE-01):**

```text
LMS-CORE-01: feat: set up PouchDB with SQLite adapter for offline storage

Built the database registry with per-domain PouchDB instances for books,
patrons, loans, extensionLoans, departments, auditLog, and config. Each
domain store is initialized with the WebSQL adapter and indexed for the
critical access paths (type + status, type + department, type + barcode,
type + cycleCode, type + schoolId, type + patronId + status, type + dueDate).
The registry is a singleton initialized once at app startup and provides
type-safe access to all domain databases. Works fully offline with no
internet dependency.
```

#### Step 4: 📤 Commit and Push Feature Branch

Use the GitHub MCP `push_files` tool to commit and push all changed files to the feature branch in a single operation. Use `get_file_contents` to read current file contents from the branch if needed.

```yaml
Tool: mcp_io_github_git_push_files
  owner: noobix
  repo: alpha-rabbit-lms
  branch: LMS-[XXX]/[title-or-description]
  files:
    - path: "<relative/path/to/file>"
      content: "<full file content>"
    - path: "<relative/path/to/another-file>"
      content: "<full file content>"
  message: |
    LMS-[XXX]: <type>: <vivid summary>

    <Paragraph describing what was built, how it works,
    and why it was done this way.>
```

To read existing file contents before pushing updates:

```yaml
Tool: mcp_io_github_git_get_file_contents
  owner: noobix
  repo: alpha-rabbit-lms
  path: "<relative/path/to/file>"
  ref: "refs/heads/LMS-[XXX]/[title-or-description]"
```

#### Step 5: 🏷️ Tag the Commit with a Build Number

Before opening the PR, tag the current commit on the feature branch with a lightweight build number tag. Each commit receives exactly one build number. Build numbers are the primary traceability unit linking a commit to its delivered work.

**Build number format:**

```text
[YY###]
```

- `YY` = two-digit year (2026 → `26`)
- `###` = sequential counter starting at `1` for the year, incrementing by one per merged PR
- 2026 range: `[261]` through `[26999]`
- Build numbers are year-scoped, never reset mid-year, and never appear in the semantic version string

**Reading the next build number from `.build_counter`:**

The repo tracks the next build number to use in a plain text file at the root:

```bash
cat .build_counter   # e.g. outputs: 261
```

Read this file before tagging. The value it contains is the number you apply to your commit. After tagging, increment and write it back so the next developer gets the correct number:

```bash
# 1. Read current counter
BUILD=$(cat .build_counter)

# 2. Tag the commit
git tag "[$BUILD]"
git push origin "[$BUILD]"

# 3. Increment and commit the counter back to develop
echo $(( BUILD + 1 )) > .build_counter
git add .build_counter
git commit -m "chore: increment build counter to $(( BUILD + 1 ))"
git push origin develop
```

> **Race condition note:** If two PRs are being tagged concurrently, both may read the same counter value. In practice, serialise this step manually (one tag operation at a time) or rely on the CI automation in `docs/release.md` which handles this atomically.

#### Step 6: 🔀 Create Pull Request to `develop`

Use the GitHub MCP `create_pull_request` tool:

```yaml
Tool: mcp_io_github_git_create_pull_request
  owner: noobix
  repo: alpha-rabbit-lms
  title: "LMS-[XXX]: <ticket title>"
  head: LMS-[XXX]/[title-or-description]
  base: develop
  body: |
    ## Ticket
    **LMS-[XXX]**: <ticket title>

    ## Changes
    - Write this section as a paraphrase of the ticket's acceptance criteria, phrased as completed implementation behavior rather than a checklist.
    - Describe what the code now does, how it behaves, and why it satisfies the ticket, without copying the acceptance criteria verbatim.
    - You may reference the commit message for context, but do not lift its wording directly.
    - This section will be reused in annotated tags, so keep it clear, factual, and implementation-focused.

    ## Acceptance Criteria (from compression.md)
    - [ ] <AC 1>
    - [ ] <AC 2>
    - [ ] <AC 3>

    ## Completion Gate Checklist
    - [ ] All acceptance criteria satisfied
    - [ ] Offline behavior demonstrated
    - [ ] Security/privacy checks pass
    - [ ] Audit artifacts exist where required
    - [ ] Manager/Enterprise impact recorded
```

---

#### Step 7: 📦 Create Sprint Annotated Tag (on `testing-main`)

When every ticket in a sprint is merged into `develop` and the sprint is fully implemented with no issues, create a single PR from `develop` to `testing-main`. When that PR is merged, the CI `minor-release` job runs on `testing-main` and creates a single annotated tag covering the entire sprint. The annotated tag is the durable, human-readable record of everything delivered in the sprint; its body feeds release notes and audit records. The semantic version increments the MINOR component at sprint completion. The `testing-main` branch exists specifically for this purpose — it is the integration target for sprint completion and the branch where release tags are created.

**Annotated tag body format:**

```text
Build #[261]
Changes:
- <Paraphrased description of what was delivered — drawn from the PR ## Changes section, not copied verbatim>
- <Additional delivered behavior expressed as what the system now does as a result of this build>

Build #[262]
Changes:
- <Paraphrased description of what was delivered>
- <Additional delivered behavior>

Contributors:
@github-handle (Display Name)
@github-handle-2 (Display Name)

---

Appendix: Full PR descriptions
[Full PR description for each build, appended in chronological order]
```

**Rules:**

- Open each build entry with `Build #[YY###]`.
- `Changes:` items are paraphrased from the PR `## Changes` section. Describe what the system now does as a result of the build — implementation behavior, not requirements. Do not copy from the acceptance criteria list or lift wording from the commit message verbatim.
- Order entries chronologically by merge date.
- After all build entries, include a `Contributors:` section listing every GitHub handle (and display name where available) that authored a PR or commit merged in this sprint. Format each line as `@handle (Display Name)` — or `@handle` alone when no display name is set. Deduplicate and sort alphabetically. This section is generated automatically by `scripts/release-aggregate.sh`.
- After the contributors section, append a `---` separator followed by `Appendix: Full PR descriptions`, then the full PR description body for each build in chronological order. This appendix is the reference used by `docs/release.md` and for audit purposes.
- The tag body must be entirely self-contained — readable without accessing GitHub.

**Command:**

```bash
git tag -a v1.1.0 -F sprint-tag-body.txt
git push origin v1.1.0
```

Write the tag body to a temporary file to handle multi-line content reliably; remove the file after tagging. Automation details live in `docs/release.md`.

**Example (Sprint 1, v1.1.0):**

```text
Build #[261]
Changes:
- PouchDB offline storage with SQLite adapter is operational. The database registry initializes all domain stores (books, patrons, loans, extensionLoans, departments, auditLog, config) with the WebSQL adapter and creates required indexes for critical access paths. The system works fully offline with no internet dependency.
- National ID hashing and masking is verified. The hashing service runs exclusively in the Electron main process; plaintext IDs never reach the renderer. Masked display follows the active country profile format.

Build #[262]
Changes:
- Incremental backup scheduler fires daily at 8 PM, produces snapshots capped at 5% of database size, and resumes automatically from the last checkpoint after power interruption. Backup files are compressed and uploaded to configured cloud storage when connectivity is available.
- 30-second auto-save persists transaction drafts with checksum validation. On restart after outage, the system recovers the last valid state and displays the exact timestamp of the recovered state to the user.

Contributors:
@noobix (Kelvin Kabute)

---

Appendix: Full PR descriptions
[Full PR description for Build #[261] — LMS-CORE-01]
[Full PR description for Build #[262] — LMS-CORE-02]
[Full PR description for Build #[263] — LMS-CORE-03]
[Full PR description for Build #[264] — LMS-CORE-04]
```

### Quick Reference: MCP Tool Sequence

```text
1. mcp_io_github_git_create_branch         → Create feature branch from develop
2. mcp_io_github_git_update_pull_request_branch → Sync feature branch with develop
3. mcp_io_github_git_get_file_contents      → Read existing files before editing
4. mcp_io_github_git_push_files             → Commit and push all changes
5. mcp_io_github_git_create_pull_request    → Open PR to develop
6. After all sprint tickets merged to develop → manual testing on develop
7. mcp_io_github_git_create_pull_request    → Open PR from develop to testing-main
8. After PR merge to testing-main → CI minor-release job creates sprint annotated tag (vMAJOR.MINOR.0)
```
