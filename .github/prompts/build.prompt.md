# Alpha Rabbit LMS Build Prompt (Compression-Aligned v1.2)

<!-- markdownlint-disable MD032 MD060 -->

This file is the implementation control document used with `prompt_main.md`.
Primary objective: keep all build decisions anchored to `docs/jira/compression.md` while using docs in `docs/ressources` as the source assets.

*Critical correction: Extension Services is a full external department (not library section) that borrows books from Lending section via bulk allocation workflow*

---

## 0) Source Assets Table (Read First)

| Asset | Purpose in Build | Required Use |
| --- | --- | --- |
| `docs/jira/compression.md` | Canonical ticket scope and acceptance criteria (v1.2 — Extension Services update) | Must be treated as source of truth for every ticket in this file |
| `docs/jira/jira_doc.md` | Detailed ticket specification with sprint planning | Use for sprint sequencing, labeling conventions, and quality gates |
| `docs/prompt_main.md` | Architecture constraints and project structure | Use for codebase layout, mode split (Manager/Enterprise), and non-functional constraints |
| `docs/ressources/product_specs.md` | Stack and deployment decisions | Use to enforce offline-first stack, packaging assumptions, and Ghana hardware constraints |
| `docs/ressources/system_specs.md` | Manager vs Enterprise setup detail | Use for environment-specific behavior and operational boundaries |
| `docs/ressources/functionality_specs.md` | End-to-end module behavior | Use for flow details across acquisitions → processing → distribution → sections |
| `docs/ressources/module_functionality_specs.md` | User-centric module acceptance examples (updated with Extension Services) | Use for user stories, offline behavior specifics, and Extension workflows |
| `docs/ressources/functionality_specs_expanded.md` | Patron intelligence, governance extensions, and expanded specs | Use for degradation engine, badges, patron profile signals, and cross-check details |
| `docs/database.md` | Canonical schema contracts (updated with Extension Services) | Use for doc types, retention fields, sync state, audit fields, and Extension loan objects |
| `docs/research_dmp/aquisisions_module.md` | Deep implementation notes for acquisitions | Use for forms, metadata shape, and offline create/sync patterns |
| `docs/research_dmp/processing_module.md` | Deep implementation notes for processing (updated with Extension routing) | Use for condition model, mold risk logic, barcode behavior, and Extension durability scoring |
| `docs/research_dmp/distribution_module.md` | Deep implementation notes for distribution (updated with Extension depot delivery) | Use for packing slips, rural mode, delivery confirmation queue, and Extension depot workflows |
| `docs/research_dmp/extension_module.md` | Deep implementation notes for Extension Services | Use for Android app, QR learner tracking, bulk allocation workflow, schedule management |
| `docs/research_dmp/library_sections_pi_sg.md` | Deep implementation notes for sections + PI + governance (includes Lending Section) | Use for degradation enforcement, section workflows, and Lending bulk allocation fulfillment |
| `docs/research_dmp/deploy_doc.md` | Pilot/deployment/validation package | Use for pilot validation checks and packaging constraints |

---

## 1) Global Non-Negotiables

- One codebase, two modes:
  - Manager: fully offline on single device.
  - Enterprise: local-first client with resilient sync.
- No plaintext Ghana Card IDs in storage, logs, backups, exports, or UI state dumps.
- Ghana Card hashing must execute in Electron main process only.
- Core data docs include `_id`, `type`, `createdAt`, `updatedAt`, `_syncStatus`, `_schemaVersion`.
- Package manager standard: `pnpm` is the default for this project; use `pnpm` for install/run/build scripts and avoid `npm`/`yarn` commands in implementation docs.
- Device baseline: Windows 10, 4GB RAM, unstable power/internet expected.
- Offline-first means every critical workflow completes locally and sync is deferred.
- Extension Services is a top-level DEPARTMENT (peer to Acquisitions, Processing, Distribution, Library Operations, System Admin) — NOT a library section.
- Books remain owned by Lending Section; Extension Services borrows temporarily via bulk allocation workflow: `Extension Request → Lending Fulfillment → Distribution Delivery → Extension Rotation → Return to Lending`.
- Extension learners have minimal profiles (QR ID only, no condition scoring, no degradation tracking).
- Android app is an external tool for Extension Services field operations only — it is NOT part of the Electron desktop application.

---

## 2) Build Plan by Child Epic (from `compression.md`)

## Child Epic: LMS-CORE-SECURITY

### LMS-101 — Implement SHA-256 hashing for Ghana Card ID storage

Build focus:

- Validate `GHA-000000000-0` format at form boundary.
- Hash and salt in main process service only.
- Store hash only; display masked value.

Acceptance criteria (from compression):

- Ghana Card ID `GHA-123456789-0` stored as `hashed:a3f8d2...`.
- Plaintext ID never appears in logs/backups/UI.
- Masked display `GHA-123***89-0` in all interfaces.
- Hashing occurs ONLY in Electron main process (never renderer).

---

### LMS-102 — Build incremental backup scheduler with WhatsApp compression

Build focus:

- Daily incremental at 8 PM.
- Resume-safe backup after interruption.
- 30-day retention cleanup.
- WhatsApp export compressing output.

Acceptance criteria (from compression):

- Daily backup at 8 PM creates file `<=5%` of DB size (3MB for 60MB DB).
- "Send via WhatsApp" button compresses backup to `<10MB`.
- Backup resumes automatically after power outage.
- 30-day retention policy enforced with auto-deletion.

---

### LMS-103 — Implement 30-second auto-save for power outage resilience

Build focus:

- Save active drafts every 30 seconds.
- Recovery snapshot with timestamp.
- Integrity check before restore.

Acceptance criteria (from compression):

- Transaction data saved every 30 seconds without user action.
- After 4-hour power outage, 99% of transactions >30s old recover.
- Recovery message shows timestamp: "Recovered work from 10:14 AM".
- Zero data corruption verified via checksum validation.

---

### LMS-104 — Add battery optimization exemption flow for rural libraries

Build focus:

- Explain rationale in-app.
- One-tap guidance for Windows background app permissions.
- Persistent warning until handled.

Acceptance criteria (from compression):

- In-app rationale screen explains Ghana power instability context.
- One-tap enable flow for Windows "Allow background apps".
- Persistent notification when exemption not granted.
- Works on Windows 10 devices with 4GB RAM.

---

### LMS-105 — Implement department security objects for 6 departments (NEW)

Build focus:

- Configure 6 departments as security principals.
- Enforce cross-department data isolation via security objects.
- Extension Services boundary: no access to library section data.
- Lending Section boundary: only "Bulk Requests" tab visible for Extension requests.

Acceptance criteria (from compression):

- 6 departments configured: Acquisitions, Processing, Distribution, Library Operations, Extension Services, System Admin.
- Extension Services staff CANNOT access library section data.
- Lending section staff see ONLY "Bulk Requests" tab for Extension requests.
- Cross-department data access blocked by security objects.

---

## Child Epic: LMS-GHANA-COMPLIANCE

### LMS-201 — Implement Ghana Data Protection Act 2012 (Act 843) compliance

Build focus:

- Retention/anonymization/purge jobs.
- Deletion workflow with audit trails and bilingual confirmation SMS.

Acceptance criteria (from compression):

- Patron records auto-anonymized after 2 years inactive.
- Closed accounts purged within 72 hours + audit log entry.
- Staff records retained exactly 7 years post-employment.
- One-tap account deletion with confirmation SMS in Twi/English.

---

### LMS-202 — Integrate Ghana Education Service curriculum tags (2024/25)

Build focus:

- Bundle GES tags offline JSON.
- Grouped taxonomy search.
- Dewey suggestion mapping.

Acceptance criteria (from compression):

- 247 pre-loaded GES tags matching MoE validation certificate #MoE-2024-087.
- Tags grouped by level: Basic/JHS/SHS with grade-specific variants.
- Offline access without internet (embedded JSON <=2.5MB).
- Auto-suggest Dewey Decimal based on curriculum tag.

---

### LMS-203 — Build Twi/Dagbani language support for rural library and Extension staff (UPDATED)

Build focus:

- Translate critical task flows and SMS templates in Twi and Dagbani.
- Dagbani translations for Extension Services Northern Region operations.
- Android app language toggle: English/Twi/Dagbani.
- Persist language setting.

Acceptance criteria (from compression):

- Critical screens (checkout, batch management) fully translated to Twi.
- Dagbani translations for Extension Services Northern Region operations.
- Android app language toggle: English/Twi/Dagbani.
- SMS templates in Twi/Dagbani validated by University of Ghana + UDS linguists.
- Language toggle in Settings with persistent selection.

---

### LMS-204 — Implement GES academic calendar with August 31 expiry (UPDATED)

Build focus:

- Batch expiry enforcement.
- Promotion/report scheduler.
- Extension Services rotation cycles aligned with GES calendar.
- Hard stop: ALL Extension book sets return to depot by August 31.

Acceptance criteria (from compression):

- All batches auto-expire August 31 per Ghana Education Service standard.
- Extension Services rotation cycles aligned: Cycle 1 (Sept-Dec), Cycle 2 (Jan-Mar), Cycle 3 (Apr-Jun), Cycle 4 (Jul-Aug).
- ALL Extension book sets MUST return to depot by August 31 (hard stop).
- Pre-promotion report generated June 15 listing batches expiring Aug 31.
- Auto-promotion August 15 for batches with >80% attendance.

---

### LMS-GH-12 — Dagbani language support for Extension Services (NEW)

Build focus:

- Dagbani translations validated by University for Development Studies linguist.
- Northern Region Extension operations in Dagbani.
- SMS templates for depot contacts in Dagbani.

Acceptance criteria (from compression):

- Dagbani template: "Zuli libri ka ti kpɛ. Yɛlsim cycle 2 books."
- English fallback available.
- Messages queue offline; send via Vodafone/MTN/AirtelTigo on reconnect.
- Templates validated by University for Development Studies linguist.

---

## Child Epic: LMS-ACQUISITIONS

### LMS-301 — Implement vendor management with Ghana Card ID validation

Build focus:

- Vendor form validation and hint copy.
- Hash-on-save compliance flow.
- Offline vendor registry + sync.

Acceptance criteria (from compression):

- Vendor form requires Ghana Card ID format `GHA-000000000-0`.
- Format validation tooltip: "Ghana Card required per Public Procurement Act 2003".
- Hashed ID stored; plaintext never persisted.
- Works offline with local vendor list sync on reconnect.

---

### LMS-302 — Build budget tracking per department with GES alignment

Build focus:

- Budget code format enforcement.
- Live spend/remaining indicators.
- Override path with approval requirement.

Acceptance criteria (from compression):

- Budget codes follow Ghana format `CHILDREN-2024-Q1`.
- Real-time remaining balance display during order creation.
- Amber warning at <20% budget remaining.
- Blocks orders exceeding remaining budget with override requiring Department Head approval.

---

### LMS-303 — Implement offline order queue with sync-on-reconnect

Build focus:

- Queue orders locally when offline.
- Reconnect sync within SLA.
- Retry/backoff and conflict policy.

Acceptance criteria (from compression):

- Orders save locally with status "Pending Sync" when offline.
- Sync completes within 60 seconds of internet restoration.
- Conflict resolution uses timestamp-based "last write wins".
- Failed syncs retry with exponential backoff (1s -> 30s).

---

## Child Epic: LMS-PROCESSING

### LMS-401 — Implement condition scoring sliders for spine/cover/pages/edges

Build focus:

- Four sliders with weight model.
- Spine crease count and climate tooltip.
- Weighted health score calculation.

Acceptance criteria (from compression):

- 1-5 sliders with climate-aware weighting (spine 40%, cover 25%, pages 25%, edges 10%).
- Visual indicators: red=1 (poor) -> green=5 (excellent).
- Spine crease counter (0-5) with tooltip: "Critical in humid climate".
- Overall health score auto-calculated as weighted average.

---

### LMS-402 — Build mold risk assessment based on Ghana seasonal calendar

Build focus:

- Risk classification from local date only.
- Offline seasonal recommendations.

Acceptance criteria (from compression):

- Automatic risk level (none/low/medium/high/critical) based on current date.
- April-June & Sept-Nov: "high" risk with recommendation "Use silica gel packets".
- December-February: "low" risk with recommendation "Standard shelving sufficient".
- Works offline using embedded seasonal calendar (no API calls).

---

### LMS-403 — Generate PDF417 barcodes with Ghana Library Authority format (UPDATED)

Build focus:

- Barcode format encoder.
- Extension Services books append rotation cycle suffix.
- Local file save with size target.
- Include QR for downstream scanning.

Acceptance criteria (from compression):

- Barcode format `SCI-6M-042` = `[SUBJECT]-[GRADE][AUTHOR_INITIAL]-[SEQUENTIAL]`.
- Extension Services books append rotation cycle suffix: `SCI-6M-042-C2`.
- PDF saves locally <=500KB for WhatsApp transfer.
- Works offline with no internet dependency.
- Includes QR code for section scanning upon delivery.

---

### LMS-404 — Route books to Extension Services department with durability scoring (NEW)

Build focus:

- Extension Services as top-level department routing option.
- Conditional fields: Rotation Cycle, Mobile Handling Durability, Destination Region.
- Durability threshold enforcement for Northern Region corridor.
- `extensionServices` object population on routing.

Acceptance criteria (from compression):

- Section routing dropdown includes "Extension Services" as top-level department option.
- Selecting Extension triggers conditional fields: Rotation Cycle (CYCLE-1 to CYCLE-4), Mobile Handling Durability (1-5), Destination Region.
- Durability >=3 required for Tamale-Bolgatanga corridor.
- Tamale-Bolgatanga corridor safety protocols auto-trigger for Northern Region.
- Batch assignment fields hidden when routing to Extension (not applicable).
- `extensionServices` object MUST be populated when routing to Extension.

---

## Child Epic: LMS-DISTRIBUTION

### LMS-501 — Implement batch-aware packing slips with GRADE-4A vs GRADE-4B separation

Build focus:

- Batch grouping in PDF output.
- Repeat batch warning blocks.
- Include GES expiry context.

Acceptance criteria (from compression):

- Packing slip groups books by batch (`GRADE-4A`: 42 books, `GRADE-4B`: 8 books).
- Repeat batches (`GRADE-4B`) display amber warning: "GES Policy: 20% extra books required".
- PDF includes GES academic year expiry date (August 31).
- File size <=500KB for WhatsApp transfer.

---

### LMS-502 — Build rural delivery mode for Tamale-Bolgatanga corridor

Build focus:

- Rural mode switch to make GPS optional.
- Require community leader contact.
- Queue confirmations offline.

Acceptance criteria (from compression):

- "Rural Mode" toggle disables GPS requirements.
- Mandatory community leader contact fields when rural mode enabled.
- Twi/Dagbani SMS templates based on destination region.
- Works offline with delivery confirmation queued for sync.

---

### LMS-503 — Implement rainy season alerts on packing slips

Build focus:

- Seasonal alert banners in slip generator.
- Material-specific protection list for glossy pages.

Acceptance criteria (from compression):

- April-June & Sept-Nov: Red banner "RAINY SEASON ALERT" on packing slip.
- Lists books with glossy pages (Science/Math) requiring extra protection.
- Alert disappears automatically September 1.
- Works offline using device date (no network dependency).

---

### LMS-504 — Deliver books to Extension Services depot with rotation cycle metadata (NEW)

Build focus:

- Destination type "Extension Services Depot" as new workflow trigger.
- Packing slip includes rotation cycle, depot location, community leader signature field.
- Rotation cycle metadata READ-ONLY (assigned during Lending fulfillment).
- Dagbani SMS notification to depot contact.
- Distribution NEVER handles school-level delivery (Extension Services' responsibility).

Acceptance criteria (from compression):

- Destination type "Extension Services Depot" triggers depot-specific workflow.
- Packing slip includes: rotation cycle, depot location, community leader signature field.
- Rotation cycle metadata is READ-ONLY (assigned during Lending fulfillment).
- Dagbani SMS notification sent to depot contact.
- Distribution NEVER handles school-level delivery details (Extension Services' responsibility).
- Community leader signature workflow activates for rural depot locations.

---

## Child Epic: LMS-EXTENSION-SERVICES (NEW)

> **Critical Boundary**: Extension Services is a DEPARTMENT (peer to Library Operations), NOT a library section. Books are temporarily loaned FROM Lending Section. Extension learners have minimal profiles (QR ID only, no condition scoring, no degradation tracking).

### LMS-801 — Create bulk book requests for school rotation cycles (NEW)

Build focus:

- Extension Services Leader creates bulk request form.
- Request appears on Lending Section "Pending Requests" dashboard.
- Status tracking through fulfillment pipeline.
- Extension staff see ONLY Extension workflows.

Acceptance criteria (from compression):

- Extension Services Leader creates request with: school, cycle (1-4), quantity, subject areas, destination region.
- Request appears on Lending Section "Pending Requests" dashboard.
- Status tracking: Pending → Approved → Fulfilling → Ready for Delivery.
- Extension staff see ONLY Extension workflows (no library section access).
- Works offline with sync on reconnect.

---

### LMS-802 — Implement rotation cycle management with GES calendar (NEW)

Build focus:

- 4-cycle annual rotation aligned with GES academic year.
- Auto-flag sets for collection before cycle end.
- August 31 hard stop enforcement.
- WASSCE/BECE priority for Cycle 2; rainy season kits for Cycle 3.

Acceptance criteria (from compression):

- 4-cycle annual rotation: Cycle 1 (Sept-Dec), Cycle 2 (Jan-Mar), Cycle 3 (Apr-Jun), Cycle 4 (Jul-Aug).
- Auto-flag sets for collection 14 days before cycle end.
- ALL book sets MUST return to depot by August 31 (hard stop).
- Cycle 2 prioritizes WASSCE/BECE exam materials.
- Cycle 3 includes rainy season mold prevention kits.

---

### LMS-803 — Build school delivery tracking via mobile library van (NEW)

Build focus:

- Schedule dashboard with school status tracking.
- Community leader contacts pre-loaded per school.
- Rainy season road alerts for affected routes.
- Fully offline operation with sync on reconnect.

Acceptance criteria (from compression):

- Schedule dashboard shows schools with status: scheduled/in-progress/completed/missed.
- Community leader contacts pre-loaded per school.
- Rainy season road alerts for affected routes.
- Works fully offline with sync when connection restores.

---

### LMS-804 — Implement QR-based learner checkout/return on Android app (NEW)

Build focus:

- QR smart tag scanning via device camera (low-light capable).
- Minimal learner profile display from pre-synced data.
- Book barcode scanning with max 2 books checkout limit.
- NO condition scoring, NO interaction scores, NO degradation tracking.
- Local encrypted SQLite storage (Android Keystore).

Acceptance criteria (from compression):

- Scan QR smart tag with device camera (works in low-light rural conditions).
- Display learner name and current books from pre-synced data.
- Scan book barcode to checkout (max 2 books enforced).
- NO condition scoring fields (high-traffic, <5 min/learner).
- NO interaction scores/degradation tracking for Extension learners.
- Transaction saves to local encrypted SQLite (Android Keystore).

---

### LMS-805 — Build Dagbani SMS templates for Northern Region schools (NEW)

Build focus:

- Dagbani SMS templates validated by UDS linguist.
- English fallback available.
- Offline message queue with multi-carrier reconnect.

Acceptance criteria (from compression):

- Dagbani template: "Zuli libri ka ti kpɛ. Yɛlsim cycle 2 books."
- English fallback available.
- Messages queue offline; send via Vodafone/MTN/AirtelTigo on reconnect.
- Templates validated by University for Development Studies linguist.

---

### Extension Services System Tasks

### LMS-810 — Build Android offline transaction app for Extension Services (NEW)

Build focus:

- Pre-synced learner records and book barcodes available offline.
- QR scanning via ZXing library for low-light conditions.
- Local SQLite encrypted at rest (Android Keystore).
- Battery optimization and post-service sync.

Acceptance criteria (from compression):

- All pre-synced learner records and book barcodes available offline.
- QR scanning via ZXing library works in low-light conditions.
- Local SQLite encrypted at rest (Android Keystore).
- Battery optimization: screen timeout 30s, low-power mode.
- Post-service sync uploads transactions when depot Wi-Fi available.

---

### LMS-811 — Implement QR-based learner identification with smart tag design (NEW)

Build focus:

- QR contains ONLY `qrCodeId` — NO personal data.
- Physical tag spec: laminated, 85.6x54mm, 250-micron, rounded corners.
- Low-literacy design: large font learner name + school.
- Lost tag reuses same `qrCodeId` to preserve history.

Acceptance criteria (from compression):

- QR contains ONLY `qrCodeId` (e.g., "EXT-QR-BOL-00042") — NO personal data.
- Physical: laminated 85.6x54mm, 250-micron laminate, rounded corners.
- Visual: learner name + school in large font (low-literacy contexts).
- Lost tag reuses same `qrCodeId` to preserve borrowing history.

---

### LMS-812 — Implement Extension-Lending cross-department book status sync (NEW)

Build focus:

- Book status change to "On Loan to Extension Services" with cycle tracking.
- Lending section marks books unavailable for regular circulation.
- Real-time sync prevents double-allocation.
- Return workflow triggers condition reassessment in Lending.

Acceptance criteria (from compression):

- Books allocated change status to "On Loan to Extension Services" with cycle tracking.
- Lending section shows books as unavailable for regular circulation.
- Real-time sync prevents double-allocation.
- Return workflow triggers condition reassessment in Lending section.

---

### LMS-813 — Build Extension Services schedule management with corridor safety (NEW)

Build focus:

- Tamale-Bolgatanga corridor safety protocols auto-trigger.
- Community leader contact workflow integration.
- Schedule syncs to Android app during pre-service depot Wi-Fi.
- Fully offline using cached route data.

Acceptance criteria (from compression):

- Tamale-Bolgatanga corridor safety protocols auto-trigger.
- Community leader contact workflow activates.
- Schedule syncs to Android app during pre-service depot Wi-Fi.
- Works fully offline using cached route data.

---

## Child Epic: LMS-LENDING-SECTION (NEW)

> **Critical Boundary**: Lending Section OWNS the books. Extension Services BORROWS them temporarily. Books return to Lending after each cycle for condition reassessment.

### LMS-851 — Fulfill bulk allocation requests from Extension Services (NEW)

Build focus:

- "Pending Requests" tab showing Extension bulk requests.
- Book selection from available Lending collection.
- Status change to "On Loan to Extension Services" with cycle metadata.
- Fulfilled books marked unavailable for regular circulation.
- Lending staff CANNOT access Extension Services workflows.

Acceptance criteria (from compression):

- "Pending Requests" tab shows Extension bulk requests with: school, cycle, quantity, subjects.
- Select books from available Lending collection to fulfill.
- Fulfilled books change status to "On Loan to Extension Services" with cycle metadata.
- Fulfilled books marked unavailable for regular circulation.
- Lending staff CANNOT access Extension Services workflows (boundary enforced).

---

### LMS-852 — Implement rotation tracking and return workflow (NEW)

Build focus:

- Condition reassessment on book return from Extension cycle.
- Status revert from "On Loan to Extension Services" to "Available".
- Cumulative tracking: cycle history, rotation count, condition changes.
- Overdue return escalation alerts (past August 31 hard stop).

Acceptance criteria (from compression):

- Condition reassessment triggers when books return from Extension cycle.
- Book status changes from "On Loan to Extension Services" back to "Available".
- Track: cycle history, number of rotations, cumulative condition changes.
- Overdue returns (past August 31 hard stop) trigger escalation alerts.

---

### LMS-853 — Build collection health monitoring for Extension-loaned books (NEW)

Build focus:

- Book rotation history: cycles served, destinations, condition at each return.
- Cumulative Extension degradation tracked separately from regular circulation.
- Withdrawal recommendation when condition drops below threshold.

Acceptance criteria (from compression):

- Book record shows rotation history: cycles served, destinations, condition at each return.
- Cumulative Extension degradation tracked separately from regular circulation.
- System recommends withdrawal when condition drops below threshold after Extension use.

---

### LMS-860 — Implement cross-department book status tracking (NEW)

Build focus:

- Book record update with `status: "on_loan_to_extension"` and `extensionLoan` object.
- `extensionLoan` includes: department, cycle code, allocated date, due return, staff ID.
- Lending section never shows allocated books as available.
- Offline-first with sync on reconnect.

Acceptance criteria (from compression):

- Book record updates: `status: "on_loan_to_extension"` with `extensionLoan` object.
- `extensionLoan` includes: department, cycle code, allocated date, due return, staff ID.
- Lending section never shows allocated books as available.
- Works offline with sync on reconnect.

---

## Child Epic: LMS-CHILDRENS-SECTION

### LMS-601 — Implement GES-aligned batch promotion workflow

Build focus:

- Promotion and repeat placement by attendance thresholds.
- Parent notification workflow.
- Bulk safety checks for learner updates.

Acceptance criteria (from compression):

- August 15 auto-promotion for batches with >80% attendance.
- Learners with <70% attendance moved to repeat batch (`GRADE-5B`).
- SMS notifications in Twi/English sent to all parents.
- Zero data loss verified across 50-learner promotion test.

---

### LMS-602 — Build degradation threshold enforcement engine

Build focus:

- Zone logic for issue policy.
- Required override reason in red zone.
- Auto-schedule coaching in critical zone.

Acceptance criteria (from compression):

- Green zone (<=0.15): Normal issuance.
- Yellow zone (0.16-0.29): Warning message "Handle with care".
- Red zone (0.30-0.44): Staff override required with 10-char reason.
- Critical zone (>=0.45): Block issuance + auto-schedule coaching workshop.

---

### LMS-603 — Implement "Teleporter" detection with oral tradition context

Build focus:

- Detection heuristic + confidence state.
- Context exceptions from staff notes.
- Non-punitive policy enforcement.

Acceptance criteria (from compression):

- Flags patrons with 3+ pristine returns after >7 days checkout.
- Context-aware: Does NOT flag if staff notes contain "read aloud" or "sibling".
- Low-confidence flags shown as "Teleporter Watch" not "Teleporter".
- Never blocks issuance for Teleporter category.

---

## Child Epic: LMS-STAFF-GOVERNANCE

### LMS-701 — Implement staff profile management with Ghana Card ID hashing

Build focus:

- Staff onboarding with compliant identity capture.
- Duplicate prevention and activation preconditions.

Acceptance criteria (from compression):

- Staff form requires Ghana Card ID format `GHA-000000000-0`.
- Hashing occurs before storage; masked display `GHA-123***89-0`.
- Prevents duplicate IDs across staff records.
- Requires supervisor assignment before activation.

---

### LMS-702 — Build role switcher for Manager version single-device operation (UPDATED)

Build focus:

- Role switch control and immediate workflow filtering.
- Extension Services role shows ONLY Extension workflows.
- Lending role shows "Bulk Requests" tab alongside regular lending workflows.
- Local-only enforcement for Manager mode.

Acceptance criteria (from compression):

- Dropdown includes: System Admin, Acquisitions, Processing, Distribution, Library Operations (Children's/Adult/Reference/Lending), Extension Services.
- Extension Services role shows ONLY Extension workflows (bulk requests, rotation, schedule).
- Lending role shows "Bulk Requests" tab alongside regular lending workflows.
- Data isolation enforced per department security objects.
- Works offline with no permission checks requiring network.

---

### LMS-703 — Configure Extension Services staff profiles with route certification (NEW)

Build focus:

- Department field: "extension_services" (NOT a section code).
- Route certification for Tamale-Bolgatanga corridor and other regions.
- Bulk request authority level and rotation cycle access permissions.
- Extension staff CANNOT access library section workflows.

Acceptance criteria (from compression):

- Department field: "extension_services" (NOT a section code).
- Route certification: Tamale-Bolgatanga corridor or other regions.
- Bulk request authority level configurable.
- Rotation cycle access permissions per staff member.
- Extension staff CANNOT access library section workflows.

---

## 3) Pilot Next Actions (from `compression.md`)

### LMS-NA-001 — Implement power outage resilience validation

Acceptance criteria (from compression):

- 24-hour simulated outage with zero data loss for transactions >30s old.
- Tested on 3 Ghana-spec Windows 10 devices (4GB RAM).
- Recovery time <10 seconds after restart.

### LMS-NA-002 — Profile battery drain during circulation workflows

Acceptance criteria (from compression):

- Core circulation workflow <=2.5% drain/hour on Intel Celeron devices.
- Documented results for Ghana Library Authority review.
- Optimization recommendations for rural libraries with solar power.

### LMS-NA-003 — Translate critical screens to Twi/Dagbani (UPDATED)

Acceptance criteria (from compression):

- Checkout screen, batch management, degradation alerts in Twi.
- Extension Services Android app in Twi/Dagbani.
- Translations validated by University of Ghana + UDS linguists.
- Zero grammatical errors per validation report.

### LMS-NA-004 — Implement language toggle in Settings (UPDATED)

Acceptance criteria (from compression):

- Persistent selection across app restarts.
- Reloads UI immediately on change.
- Default to device language with Ghana fallback (English).
- Android app supports English/Twi/Dagbani toggle.

### LMS-NA-005 — Build anonymized patron presence heartbeat

Acceptance criteria (from compression):

- Broadcasts "active" status every 60 seconds while app foregrounded.
- Aggregates counts within 500m radius for "X nearby readers" display.
- Privacy-preserving: No coordinates shared; only count + batch code.

### LMS-NA-006 — Create QA tooling for patron intelligence simulation

Acceptance criteria (from compression):

- Dev menu to simulate degradation rates (0.05 to 0.50).
- Verify reader categories assigned correctly per algorithm.
- Test low-presence fallback copy ("Emergency responders alerted").

### LMS-NA-007 — Validate Extension Services bulk allocation end-to-end (NEW)

Acceptance criteria (from compression):

- Simulate full cycle: bulk request → Lending fulfillment → Distribution delivery → Extension rotation → return.
- Zero books stranded; 100% requests fulfilled within 48 hours.
- Department boundary verified (Extension cannot access library sections).
- Tamale-Bolgatanga corridor field test with community leaders.

---

## 4) Ticket Completion Gate

A ticket is complete only if all conditions are true:

- Its listed acceptance criteria in this file are fully satisfied.
- Offline behavior for the ticket has been demonstrated.
- Security/privacy checks pass for sensitive fields.
- Audit artifacts exist where required (identity updates, overrides, purge actions).
- Manager/Enterprise impact is recorded in implementation notes.
- Extension Services department boundary verified: Extension staff cannot access library section data, and vice versa.
- Bulk allocation workflow integrity confirmed where applicable: books tracked from Lending → Extension → return.
