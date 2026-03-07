# Alpha Rabbit LMS Build Prompt (Compression-Aligned)

<!-- markdownlint-disable MD032 MD060 -->

This file is the implementation control document used with `prompt_main.md`.
Primary objective: keep all build decisions anchored to `docs/jira/compression.md` while using docs in `docs/ressources` as the source assets.

---

## 0) Source Assets Table (Read First)

| Asset                                               | Purpose in Build                                         | Required Use                                                                              |
| --------------------------------------------------- | -------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `docs/jira/compression.md`                          | Canonical ticket scope and acceptance criteria           | Must be treated as source of truth for every ticket in this file                          |
| `docs/prompt_main.md`                               | Architecture constraints and project structure           | Use for codebase layout, mode split (Manager/Enterprise), and non-functional constraints  |
| `docs/ressources/product_specs.md`                  | Stack and deployment decisions                           | Use to enforce offline-first stack, packaging assumptions, and Ghana hardware constraints |
| `docs/ressources/system_specs.md`                   | Manager vs Enterprise setup detail                       | Use for environment-specific behavior and operational boundaries                          |
| `docs/ressources/functionality_specs.md`            | End-to-end module behavior                               | Use for flow details across acquisitions → processing → distribution → sections           |
| `docs/ressources/module_functionality_specs.md`     | User-centric module acceptance examples                  | Use for user stories and offline behavior specifics                                       |
| `docs/ressources/functionality_specs_expanded_1.md` | Patron intelligence and governance extensions            | Use for degradation engine, badges, and patron profile signals                            |
| `docs/ressources/functionality_specs_expanded_2.md` | Additional expanded specs copy                           | Use as cross-check only when needed (avoid duplicating contradictory details)             |
| `docs/database.md`                                  | Canonical schema contracts                               | Use for doc types, retention fields, sync state, and audit fields                         |
| `docs/research_dmp/aquisisions_module.md`           | Deep implementation notes for acquisitions               | Use for forms, metadata shape, and offline create/sync patterns                           |
| `docs/research_dmp/processing_module.md`            | Deep implementation notes for processing                 | Use for condition model, mold risk logic, and barcode behavior                            |
| `docs/research_dmp/distribution_module.md`          | Deep implementation notes for distribution               | Use for packing slips, rural mode, and delivery confirmation queue                        |
| `docs/research_dmp/library_sections_pi_sg.md`       | Deep implementation notes for sections + PI + governance | Use for degradation enforcement and section workflows                                     |
| `docs/research_dmp/deploy_doc.md`                   | Pilot/deployment/validation package                      | Use for pilot validation checks and packaging constraints                                 |

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

### LMS-203 — Build Twi language support for rural library staff

Build focus:

- Translate critical task flows and SMS templates.
- Persist language setting.

Acceptance criteria (from compression):

- Critical screens (checkout, batch management) fully translated to Twi.
- SMS templates in Twi validated by University of Ghana linguist.
- Language toggle in Settings with persistent selection.
- RTL support NOT required (Twi uses Latin script).

---

### LMS-204 — Implement GES academic calendar with August 31 expiry

Build focus:

- Batch expiry enforcement.
- Promotion/report scheduler.
- Repeat-batch warning state.

Acceptance criteria (from compression):

- All batches auto-expire August 31 per Ghana Education Service standard.
- Pre-promotion report generated June 15 listing batches expiring Aug 31.
- Auto-promotion August 15 for batches with >80% attendance.
- Repeat batches (`GRADE-4B`) flagged with "20% extra books required" warning.

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

### LMS-403 — Generate PDF417 barcodes with Ghana Library Authority format

Build focus:

- Barcode format encoder.
- Local file save with size target.
- Include QR for downstream scanning.

Acceptance criteria (from compression):

- Barcode format `SCI-6M-042` = `[SUBJECT]-[GRADE][AUTHOR_INITIAL]-[SEQUENTIAL]`.
- PDF saves locally <=500KB for WhatsApp transfer.
- Works offline with no internet dependency.
- Includes QR code for section scanning upon delivery.

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
- Twi SMS template: "Naa, Ghana Library Authority delivery arriving today".
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

### LMS-702 — Build role switcher for Manager version single-device operation

Build focus:

- Role switch control and immediate workflow filtering.
- Local-only enforcement for Manager mode.

Acceptance criteria (from compression):

- Dropdown allows switching between System Admin/Acquisitions/Processing/Distribution/Sections.
- UI instantly updates to show only relevant workflows.
- Data isolation: Acquisitions staff cannot see patron records.
- Works offline with no permission checks requiring network.

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

### LMS-NA-003 — Translate critical screens to Twi

Acceptance criteria (from compression):

- Checkout screen, batch management, degradation alerts in Twi.
- Translations validated by 2 University of Ghana linguists.
- Zero grammatical errors per validation report.

### LMS-NA-004 — Implement language toggle in Settings

Acceptance criteria (from compression):

- Persistent selection across app restarts.
- Reloads UI immediately on change.
- Default to device language with Ghana fallback (English).

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

---

## 4) Ticket Completion Gate

A ticket is complete only if all conditions are true:

- Its listed acceptance criteria in this file are fully satisfied.
- Offline behavior for the ticket has been demonstrated.
- Security/privacy checks pass for sensitive fields.
- Audit artifacts exist where required (identity updates, overrides, purge actions).
- Manager/Enterprise impact is recorded in implementation notes.
