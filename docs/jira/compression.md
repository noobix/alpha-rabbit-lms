---
Author: Kelvin Kabute
Last-updated: 2026-10-10
---

# 📚 Library Management System: Jira Ticket Specification (Extension Services Department Update)

_User-centric tickets with African context, offline resilience, and Manager/Enterprise differentiation – PM-friendly format with narrative acceptance criteria_

_Critical correction: Extension Services is a full external department (not library section) that borrows books from Lending section via bulk allocation workflow_

---

## 🏷️ LABELING CONVENTION

| Label | Purpose | Example |
|-------|---------|---------|
| `feature` | User-facing functionality with clear value | Patron dashboard, batch promotion |
| `system-task` | Infrastructure/database/security work | PouchDB setup, backup scheduler |
| `manager` | Manager version only | Single-library workflows |
| `enterprise` | Enterprise version only | Multi-branch sync |
| `ghana-compliance` | Ghana Data Protection Act requirements | Ghana Card ID hashing |
| `offline-first` | Critical offline capability | Power outage recovery |
| `extension-services` | Extension Services department workflows | Bulk allocation, rotation cycles |
| `lending-section` | Lending section bulk allocation | Book loans to Extension Services |
| `department-boundary` | Cross-department boundary enforcement | Extension ↔ Lending isolation |
| `android-app` | External Android application | Extension Services offline transactions |
| `priority:high` | Blocks subsequent work | Core database setup |
| `data-ops` | Data import, export, seeding, migration, archival | Data lifecycle operations |
| `sync-infra` | Sync behavior, conflict handling, partitions, Android sync | Sync infrastructure |
| `data-quality` | Duplicate detection, collision handling, monitoring, error handling | Data integrity and quality |
| `database-model` | Schema design, indexing, contract enforcement | Database architecture |
| `migration-ready` | Schema evolution, version bumps, migration gates | Migration infrastructure |
| `african-adaptation` | Country-specific policy configuration | Multi-country identity rules |

---

## 🌐 EPIC: CORE INFRASTRUCTURE (`LMS-CORE`)

_Foundation for offline-first operation, security, Ghana compliance, and database architecture. ALL tickets in this epic MUST be completed before any feature work begins. This epic is the bedrock of the project._

### System Tasks (Infrastructure)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-CORE-01** | Set up PouchDB with SQLite adapter for offline storage | System Task | `system-task` `manager` `offline-first` `database-model` | High | **Given** a Windows 10 device with 4GB RAM<br>**When** the application launches for the first time<br>**Then** a SQLite database file `library_data.db` is created in `C:/GhanaLibraryData/`<br>**And** the database contains indexed collections for books, patrons, staff, and extension records<br>**And** the database registry initializes all domain stores (books, patrons, loans, extensionLoans, departments, auditLog, config)<br>**And** required indexes are created for type + status, type + department, type + barcode, type + cycleCode, type + schoolId, type + patronId + status, and type + dueDate<br>**And** the system works fully offline with no internet dependency |
| **LMS-CORE-02** | Implement SHA-256 hashing for national ID storage | System Task | `system-task` `ghana-compliance` `security` | High | **Given** a staff member enters a national ID (e.g., Ghana Card ID `GHA-123456789-0` or Kenya ID `KE-#######`)<br>**When** the record is saved<br>**Then** the database stores only the hashed value<br>**And** the UI displays a masked version (e.g., `GHA-123***89-0`)<br>**And** plaintext ID is never written to logs, backups, or any persistent store<br>**And** hashing occurs ONLY in the Electron main process (never renderer)<br>**And** the hashing strategy is configurable per country profile (idFormat, hashingStrategy)<br>**And** the system validates ID format against the active country profile before hashing |
| **LMS-CORE-03** | Build incremental backup scheduler with cloud storage integration | System Task | `system-task` `manager` `offline-first` | High | **Given** the library closes at 8:00 PM daily<br>**When** the backup scheduler triggers<br>**Then** an incremental backup file is created containing only changes since last checkpoint<br>**And** the file size is ≤5% of main database (e.g., 3MB for 60MB DB)<br>**And** the backup is compressed using the compression package<br>**And** backup resumes automatically from last checkpoint after power outage<br>**And** 30-day retention policy is enforced with auto-deletion<br>**And** backup integrity is verified via checksum audit<br>**And** the system works fully offline with no API calls<br>**And** compressed backups can be uploaded to configured cloud storage (Dropbox, Google Drive, etc.)<br>**And** cloud upload happens automatically when connectivity is available |
| **LMS-CORE-04** | Implement 30-second auto-save for power outage resilience | System Task | `system-task` `offline-first` `ghana-compliance` | High | **Given** a librarian is cataloging a book<br>**When** power fails unexpectedly<br>**Then** upon restart, the system recovers the last valid state from ≤30 seconds before outage<br>**And** displays "Recovered your work from [timestamp]"<br>**And** zero data loss occurs for transactions older than 30 seconds<br>**And** recovery time is <10 seconds after restart<br>**And** the auto-save interval is configurable per country policy |
| **LMS-CORE-05** | Set up CouchDB server deployment for Raspberry Pi 4 | System Task | `system-task` `enterprise` `infrastructure` | Medium | **Given** a Raspberry Pi 4 with 4GB RAM and 128GB SD card<br>**When** the deployment script is executed<br>**Then** CouchDB 3.3 starts on port 5984 with admin credentials<br>**And** data persists across reboots in `/home/pi/couchdb/data`<br>**And** the server consumes ≤15% CPU during idle state<br>**And** department-based security objects are configured<br>**And** the server supports bi-directional replication with PouchDB clients |
| **LMS-CORE-06** | Implement department security objects for 6 departments | System Task | `system-task` `enterprise` `department-boundary` | High | **Given** the system has 6 departments (Acquisitions, Processing, Distribution, Library Operations, Extension Services, System Admin)<br>**When** security objects are configured<br>**Then** Extension Services staff CANNOT access library section data<br>**And** Lending section staff see ONLY "Bulk Requests" tab for Extension requests<br>**And** cross-department data access is blocked by security objects at sync and app layers<br>**And** department isolation is enforced via CouchDB security objects and app-layer guards<br>**And** the system passes a role-switching penetration test |
| **LMS-CORE-07** | Define the shared database contract and indexing strategy for all domain stores | System Task | `system-task` `database-model` `offline-first` `enterprise` | High | **Given** the application initializes its local PouchDB stores<br>**When** the database layer starts for Manager or Enterprise mode<br>**Then** every domain database follows the shared `BaseDocument` contract (`_id`, `_rev`, `type`, `createdAt`, `updatedAt`, `_syncStatus`, `_schemaVersion`)<br>**And** required indexes are created for `type + status`, `type + department`, `type + barcode`, `type + cycleCode`, `type + schoolId`, `type + patronId + status`, `type + dueDate`<br>**And** documents missing a schema version or default contract are rejected before write<br>**And** offline conflicts are preserved and logged rather than silently overwritten<br>**And** the repository pattern is enforced for all domain operations |
| **LMS-CORE-08** | Enforce Zod validation and migration gates for schema evolution | System Task | `system-task` `migration-ready` `database-model` | High | **Given** a schema change is required<br>**When** the change is implemented<br>**Then** all writes pass Zod validation at the app boundary<br>**And** any schema change requires a `_schemaVersion` increment and migration strategy<br>**And** old records are upgraded or flagged with clear migration notes<br>**And** audit log records schema migration and validation events<br>**And** migration failures are logged and rolled back<br>**And** the migration service is idempotent |
| **LMS-CORE-09** | Implement sync manager for Enterprise bi-directional replication | System Task | `system-task` `sync-infra` `enterprise` | High | **Given** the application is in Enterprise mode<br>**When** sync is initiated<br>**Then** bi-directional sync with CouchDB is established for all domain databases<br>**And** sync state is tracked (`idle`, `active`, `paused`, `error`, `offline`)<br>**And** conflicts are detected and resolved via last-write-wins based on `updatedAt`<br>**And** stale pending records (>24h) are flagged for manual review<br>**And** large sync batches are throttled on slow connections<br>**And** sync resumes without data loss after extended offline periods |
| **LMS-CORE-10** | Implement conflict resolution UI for staff review | System Task | `system-task` `sync-infra` `enterprise` | Medium | **Given** a sync conflict is detected<br>**When** the conflict resolution UI is opened<br>**Then** both document versions are shown side-by-side<br>**And** admin can choose which version to keep<br>**And** losing version is preserved in audit log<br>**And** conflicts are categorized by severity<br>**And** clock skew beyond 5 minutes is detected and flagged for manual review |
| **LMS-CORE-11** | Build data integrity monitoring and health reporting | System Task | `system-task` `data-quality` `offline-first` | Medium | **Given** the database is in use<br>**When** integrity monitoring runs<br>**Then** orphaned records are detected<br>**And** invalid enum values and schema violations are flagged<br>**And** health report is generated for admin review<br>**And** duplicate ISBN/barcode entries are detected during acquisition and processing |

---

## 📦 EPIC: ACQUISITIONS MODULE (`LMS-ACQ`)

_Book ordering workflow with African vendor management and country-aware identity validation_

### Features (User Value)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-ACQ-01** | As an Acquisitions Manager, I want to manage vendors with country-aware identity validation so that I can maintain a verified supplier list across African jurisdictions | Feature | `feature` `manager` `ghana-compliance` `african-adaptation` | High | **Given** I am adding a new vendor<br>**When** I enter their business registration and national ID (if applicable)<br>**Then** the system validates the ID format against the active country profile (e.g., `GHA-000000000-0` for Ghana, `KE-#######` for Kenya)<br>**And** the national ID is hashed before storage; plaintext is never persisted<br>**And** the vendor record captures company type (sole_proprietorship, partnership, limited_liability, nonprofit, government, institution)<br>**And** business registration number is required per national policy<br>**And** vendor specialties are tagged (e.g., children's books, reference, local_language, school_textbooks)<br>**And** the system works offline with local vendor list sync on reconnect |
| **LMS-ACQ-02** | As an Acquisitions Manager, I want budget tracking per department with country-aligned codes so that I can control spending | Feature | `feature` `manager` `ghana-compliance` | High | **Given** I am creating an order<br>**When** I select a department<br>**Then** the system shows remaining budget in real-time<br>**And** warns at <20% remaining (amber alert)<br>**And** blocks orders exceeding remaining budget with Department Head override<br>**And** budget codes follow the active country format<br>**And** all budget operations are logged in the audit trail |
| **LMS-ACQ-03** | As an Acquisitions Manager, I want offline order queue with sync-on-reconnect so that I can work without internet | Feature | `feature` `manager` `offline-first` | High | **Given** internet is unavailable<br>**When** I create an order<br>**Then** it saves locally with `status: 'pending_sync'`<br>**And** syncs within 60 seconds of internet restoration<br>**And** conflicts use timestamp-based last-write-wins<br>**And** failed syncs retry with exponential backoff (1s → 30s)<br>**And** all sync events are logged in the audit trail |

### System Tasks (Infrastructure)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-ACQ-10** | Build CSV/JSON data import pipeline for existing library records | System Task | `system-task` `data-ops` `offline-first` | High | **Given** I have a CSV of existing records<br>**When** I run the import wizard<br>**Then** records are validated against the `BaseDocument` contract<br>**And** invalid rows are rejected with clear error messages<br>**And** duplicate detection prevents re-importing existing records<br>**And** the import works fully offline<br>**And** country-specific fields are validated against the active country profile |
| **LMS-ACQ-11** | Build data export pipeline for library records | System Task | `system-task` `data-ops` `offline-first` | Medium | **Given** I need to export library data<br>**When** I select export format (JSON or CSV)<br>**Then** all records are exported<br>**And** national ID hashes remain hashed in export<br>**And** the export works fully offline<br>**And** the export includes `_schemaVersion` for migration tracking |

---

## 🌍 EPIC: GHANA COMPLIANCE (`LMS-GH`)

_Ghana-specific legal requirements and cultural adaptations_

### System Tasks (Infrastructure)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-GH-01** | Implement Ghana Data Protection Act 2012 (Act 843) compliance | System Task | `system-task` `ghana-compliance` `data-ops` | High | **Given** a patron has been inactive for 2 years<br>**When** the retention policy runs<br>**Then** their record is anonymized<br>**And** closed accounts are purged within 72 hours<br>**And** an audit log entry is created<br>**And** staff records are retained exactly 7 years post-employment per Ghana law |
| **LMS-GH-02** | Integrate Ghana Education Service curriculum tags (2024/25) | System Task | `system-task` `ghana-compliance` `offline-first` | High | **Given** the application launches for the first time<br>**When** seed data is loaded<br>**Then** 247 GES curriculum tags are available offline<br>**And** tags are grouped by level: Basic/JHS/SHS<br>**And** auto-suggest works based on curriculum tag<br>**And** the seed data is updatable via versioned update package |
| **LMS-GH-10** | Build Twi/Dagbani language support for rural library and Extension staff | System Task | `system-task` `ghana-compliance` `offline-first` | High | **Given** I am using the system in a rural Ghanaian library<br>**When** I select Twi or Dagbani language<br>**Then** critical screens (checkout, batch management) are fully translated<br>**And** Dagbani translations are available for Extension Services Northern Region operations<br>**And** SMS templates in Twi/Dagbani are validated by University of Ghana + UDS linguists<br>**And** language toggle persists across app restarts |
| **LMS-GH-11** | Implement GES academic calendar with August 31 expiry | System Task | `system-task` `ghana-compliance` `ges-calendar` | High | **Given** the academic year is active<br>**When** batches are created<br>**Then** all batches auto-expire August 31 per Ghana Education Service standard<br>**And** Extension Services rotation cycles are aligned: Cycle 1 (Sept-Dec), Cycle 2 (Jan-Mar), Cycle 3 (Apr-Jun), Cycle 4 (Jul-Aug)<br>**And** ALL Extension book sets MUST return to depot by August 31 (hard stop)<br>**And** pre-promotion report is generated June 15 listing batches expiring Aug 31<br>**And** auto-promotion occurs August 15 for batches with >80% attendance |
| **LMS-GH-12** | Implement country profile configuration for multi-country African deployment | System Task | `system-task` `african-adaptation` `database-model` | High | **Given** the system is deployed in a new African country (e.g., Kenya, Uganda, Tanzania)<br>**When** the country profile is configured<br>**Then** the system supports country-specific identity rules (idFormat, hashingStrategy)<br>**And** curriculum tagging follows the national or regional system<br>**And** academic terms and expiry dates follow the country's school calendar<br>**And** local language labels are configurable<br>**And** the profile can be saved and reused for batch promotions, expiry checks, and curriculum tagging |

---

## 🔍 EPIC: PROCESSING MODULE (`LMS-PROC`)

_Physical inspection and classification with Ghana climate adaptations and Extension Services routing_

### Features (User Value)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-PROC-01** | As a Processing Librarian, I want condition scoring sliders for spine/cover/pages/edges so that I can assess book health | Feature | `feature` `manager` `offline-first` | High | **Given** I am inspecting a book<br>**When** I adjust the condition sliders<br>**Then** the system calculates overall health score using climate-aware weighting (spine 40%, cover 25%, pages 25%, edges 10%)<br>**And** visual indicators show red=1 (poor) → green=5 (excellent)<br>**And** spine crease counter (0-5) includes a tooltip noting "Critical in humid climate"<br>**And** the overall health score is auto-calculated as a weighted average |
| **LMS-PROC-02** | As a Processing Librarian, I want mold risk assessment based on Ghana seasonal calendar so that I can protect books from humidity damage | Feature | `feature` `manager` `ghana-compliance` | High | **Given** today is April 20 (major rainy season)<br>**When** I process a book<br>**Then** the system shows "high" risk with recommendation "Use silica gel packets"<br>**And** December-February shows "low" risk with "Standard shelving sufficient"<br>**And** the assessment works offline using an embedded seasonal calendar<br>**And** no API calls are required for risk calculation |
| **LMS-PROC-03** | As a Processing Librarian, I want PDF417 barcodes with Ghana Library Authority format so that I can label books for circulation | Feature | `feature` `manager` `offline-first` | High | **Given** I am labeling a book<br>**When** I generate a barcode<br>**Then** the format is `SCI-6M-042` = `[SUBJECT]-[GRADE][AUTHOR_INITIAL]-[SEQUENTIAL]`<br>**And** Extension Services books append rotation cycle suffix: `SCI-6M-042-C2`<br>**And** the PDF saves locally ≤500KB for easy sharing<br>**And** the barcode includes a QR code for section scanning upon delivery<br>**And** generation works offline with no internet dependency |
| **LMS-PROC-04** | As a Processing Librarian, I want to route books to Extension Services with durability scoring so that books survive rural delivery | Feature | `feature` `manager` `extension-services` | High | **Given** I am routing a book to Extension Services<br>**When** I select "Extension Services" in the routing dropdown<br>**Then** conditional fields appear: Rotation Cycle (CYCLE-1 to CYCLE-4), Mobile Handling Durability (1-5), Destination Region<br>**And** durability ≥3 is required for Tamale-Bolgatanga corridor<br>**And** corridor safety protocols auto-trigger for Northern Region<br>**And** batch assignment fields are hidden when routing to Extension (not applicable)<br>**And** the `extensionServices` object is populated with rotation cycle, durability score, and destination region |

### System Tasks (Infrastructure)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-PROC-10** | Implement barcode and QR code collision detection | System Task | `system-task` `data-quality` `offline-first` | Medium | **Given** a barcode collision is detected<br>**When** the system generates a new ID<br>**Then** the collision is logged for audit<br>**And** a new unique ID is generated<br>**And** the collision event is recorded in the audit trail |

---

## 📦 EPIC: DISTRIBUTION MODULE (`LMS-DIST`)

_Batch-aware routing, rural delivery, and Extension Services depot workflows_

### Features (User Value)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-DIST-01** | As a Distribution Manager, I want batch-aware packing slips that separate GRADE-4A from GRADE-4B so that repeat learners receive appropriate materials | Feature | `feature` `manager` `ghana-compliance` | High | **Given** 50 books processed for St. Peter's School<br>**When** I generate a packing slip<br>**Then** the system groups books by batch (`GRADE-4A`: 42 books, `GRADE-4B`: 8 books)<br>**And** the PDF shows batch-specific headers with learner counts<br>**And** repeat batch (`GRADE-4B`) has visual indicator: "Repeat learners – 20% extra books required"<br>**And** the PDF is generated offline and saves to `C:/GhanaLibraryData/packing-slips/`<br>**And** file size is ≤500KB for easy sharing |
| **LMS-DIST-02** | As a Distribution Manager, I want rural delivery mode that disables GPS requirements so that I can deliver to Tamale-Bolgatanga corridor areas with poor signal | Feature | `feature` `manager` `ghana-compliance` | High | **Given** I am delivering to Bolgatanga Senior High (Upper East Region)<br>**When** I enable "Rural Delivery Mode"<br>**Then** GPS tracking fields become optional<br>**And** the system requires community leader contact details instead<br>**And** displays warning: "Ghana Library Authority Policy: Community leader notification mandatory for rural deliveries"<br>**And** the corridor detection auto-triggers for known corridor schools |
| **LMS-DIST-03** | As a Distribution Manager, I want automatic rainy season alerts on packing slips so that books are protected during transport | Feature | `feature` `manager` `ghana-compliance` | Medium | **Given** today is April 20 (major rainy season)<br>**When** I generate a packing slip<br>**Then** the PDF includes red banner: "RAINY SEASON ALERT: Use waterproof covers + silica gel"<br>**And** lists books with glossy pages (Science/Math) requiring extra protection<br>**And** the alert disappears automatically on September 1<br>**And** the seasonal calendar is embedded in seed data (no API calls) |
| **LMS-DIST-04** | As a Distribution Manager, I want to deliver books to Extension Services depot with rotation cycle metadata so that Extension staff receive correctly tagged book sets | Feature | `feature` `manager` `extension-services` | High | **Given** Lending section has fulfilled a bulk allocation request for Bolgatanga Extension depot<br>**When** I generate a packing slip for destination "Extension Services Depot"<br>**Then** the packing slip includes:<br>• Rotation cycle indicator (e.g., CYCLE-2)<br>• Depot location and contact details<br>• Community leader signature field for rural depot locations<br>• READ-ONLY rotation cycle metadata (assigned during Lending fulfillment)<br>**And** Dagbani SMS template is sent to depot contact: "Zuli libri ka ti kpɛ. Cycle 2 books arriving today."<br>**And** distribution NEVER handles school-level delivery details (that is Extension Services' responsibility) |

### System Tasks (Infrastructure)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-DIST-10** | Implement offline PDF generation for packing slips | System Task | `system-task` `offline-first` `manager` | High | **Given** internet is unavailable<br>**When** I click "Generate Packing Slip"<br>**Then** a PDF file saves to `C:/GhanaLibraryData/packing-slips/`<br>**And** the PDF contains school name, batch groupings, PDF417 barcode, QR code<br>**And** file size is ≤500KB for easy sharing |
| **LMS-DIST-11** | Build Tamale-Bolgatanga corridor detection service | System Task | `system-task` `ghana-compliance` `offline-first` | Medium | **Given** a destination school ID `BOLGATANGA-UE-001`<br>**When** routing logic executes<br>**Then** the system identifies this as Tamale-Bolgatanga corridor school<br>**And** automatically enables rural delivery mode requirements<br>**And** adds corridor-specific notes to packing slip<br>**And** the corridor list is embedded in seed data (works offline) |

---

## 👧 EPIC: LENDING SECTION (`LMS-LEND`)

_Lending Section manages bulk allocation fulfillment to Extension Services and tracks book rotation health_

> **Critical Boundary**: Lending Section OWNS the books. Extension Services BORROWS them temporarily. Books return to Lending after each cycle for condition reassessment.

### Features (User Value)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-LEND-01** | As a Lending Section Leader, I want to fulfill bulk allocation requests from Extension Services so that schools receive their book sets | Feature | `feature` `manager` `extension-services` `lending-section` | High | **Given** Extension Services has submitted a bulk request for Bolgatanga school<br>**When** I open the "Pending Requests" tab<br>**Then** I see the request with school, cycle, quantity, subjects<br>**And** I can select books from available Lending collection to fulfill<br>**And** fulfilled books change status to "On Loan to Extension Services"<br>**And** Lending staff CANNOT access Extension Services workflows<br>**And** the status change is reflected in the book record with `extensionLoan` metadata |
| **LMS-LEND-02** | As a Lending Section Leader, I want rotation tracking and return workflow so that I can monitor book health after Extension use | Feature | `feature` `manager` `extension-services` `lending-section` | High | **Given** books have returned from Extension cycle<br>**When** I process the return<br>**Then** condition reassessment triggers automatically<br>**And** book status changes from "On Loan to Extension Services" back to "Available"<br>**And** cycle history, number of rotations, and cumulative condition changes are tracked<br>**And** overdue returns (past August 31) trigger escalation alerts |
| **LMS-LEND-03** | As a Lending Section Leader, I want collection health monitoring for Extension-loaned books so that I can track cumulative wear from rotation cycles | Feature | `feature` `manager` `extension-services` `lending-section` | Medium | **Given** a book has completed 3 rotation cycles to Extension Services<br>**When** I view the book's record<br>**Then** I see rotation history: cycles served, destinations, condition at each return<br>**And** cumulative Extension degradation is tracked separately from regular circulation<br>**And** system recommends withdrawal when condition drops below threshold after Extension use |

### System Tasks (Infrastructure)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-LEND-10** | Implement cross-department book status tracking | System Task | `system-task` `sync-infra` `department-boundary` | High | **Given** books are allocated to Extension Services<br>**When** the allocation is confirmed<br>**Then** book status changes to "On Loan to Extension Services" with cycle tracking<br>**And** Lending section shows books as unavailable for regular circulation<br>**And** real-time sync prevents double-allocation<br>**And** return workflow triggers condition reassessment in Lending section |

---

## 👧 EPIC: CHILDREN'S LIBRARY SECTION (`LMS-CHILD`)

_Grade-specific batch management with degradation enforcement_

### Features (User Value)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-CHILD-01** | As a Children's Librarian, I want GES-aligned batch promotion workflow so that learners advance to the next grade | Feature | `feature` `manager` `ghana-compliance` `ges-calendar` | High | **Given** a batch has >80% attendance<br>**When** August 15 arrives<br>**Then** learners are auto-promoted<br>**And** learners with <70% attendance moved to repeat batch (`GRADE-5B`)<br>**And** SMS notifications in Twi/English sent to all parents<br>**And** zero data loss verified across 50-learner promotion test |
| **LMS-CHILD-02** | As a Children's Librarian, I want degradation threshold enforcement engine so that damaged books are flagged | Feature | `feature` `manager` `offline-first` | High | **Given** a book has condition score ≤0.15<br>**When** I attempt to issue it<br>**Then** the system blocks issuance<br>**And** scores 0.16-0.29 show "Handle with care" warning<br>**And** scores 0.30-0.44 require staff override with 10-char reason<br>**And** scores ≥0.45 block issuance + auto-schedule coaching workshop<br>**And** all overrides are logged in the audit trail with mandatory reason |
| **LMS-CHILD-03** | As a Children's Librarian, I want "Teleporter" detection with oral tradition context so that I can identify unusual borrowing patterns | Feature | `feature` `manager` `offline-first` | Medium | **Given** a patron has 3+ pristine returns after >7 days checkout<br>**When** the system analyzes the pattern<br>**Then** it flags the patron as "Teleporter Watch"<br>**And** does NOT flag if staff notes contain "read aloud" or "sibling"<br>**And** never blocks issuance for Teleporter category (avoids stigmatizing Ghanaian household practices) |

---

## 👨‍💼 EPIC: STAFF GOVERNANCE (`LMS-STAFF`)

_Department hierarchy with national ID verification – updated for Extension Services as peer department_

### Features (User Value)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-STAFF-01** | As a System Admin, I want staff profile management with national ID hashing so that I can maintain verified staff records | Feature | `feature` `manager` `ghana-compliance` | High | **Given** I am creating a staff profile<br>**When** I enter their national ID<br>**Then** the format is validated against the active country profile<br>**And** the ID is hashed before storage; masked display is shown<br>**And** duplicate IDs are prevented across staff records<br>**And** supervisor assignment is required before activation |
| **LMS-STAFF-02** | As a System Admin, I want role switcher for Manager version single-device operation so that staff can switch departments | Feature | `feature` `manager` `department-boundary` | High | **Given** I am logged in as System Admin<br>**When** I switch roles<br>**Then** the dropdown includes: System Admin, Acquisitions, Processing, Distribution, Library Operations, Extension Services<br>**And** Extension Services role shows ONLY Extension workflows<br>**And** Lending role shows "Bulk Requests" tab alongside regular lending<br>**And** data isolation is enforced per department security objects<br>**And** works offline with no permission checks requiring network |
| **LMS-STAFF-03** | As a System Admin, I want Extension Services staff profiles with route certification so that department boundaries are enforced | Feature | `feature` `manager` `extension-services` `department-boundary` | High | **Given** I am creating a staff profile for Extension Services<br>**When** I configure the profile<br>**Then** the system requires: department (Extension Services), route certification, bulk request authority level<br>**And** Extension Services staff CANNOT access library section workflows<br>**And** staff profile includes rotation cycle access permissions |

### System Tasks (Infrastructure)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-STAFF-10** | Implement data retention and archival policy engine | System Task | `system-task` `data-ops` `ghana-compliance` | Medium | **Given** a patron has been inactive for 2 years<br>**When** the retention policy runs<br>**Then** their record is anonymized<br>**And** audit logs are archived after configured period<br>**And** sync queue is purged after successful sync<br>**And** tombstones are cleaned up after 90 days |

---

## 📦 EPIC: EXTENSION SERVICES DEPARTMENT (`LMS-EXT`)

_Top-level department managing mobile library services for underserved schools via rotating book sets_

### Features (User Value)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-EXT-01** | As an Extension Services Leader, I want to create bulk book requests with rotation cycle management so that schools receive their book sets | Feature | `feature` `manager` `extension-services` | High | **Given** I am planning for Bolgatanga school<br>**When** I create a bulk request<br>**Then** I specify school, cycle, quantity, subjects<br>**And** the request is sent to Lending section for fulfillment<br>**And** rotation cycles align with GES calendar<br>**And** the request tracks country context (country code, academic year, term name, delivery region) |
| **LMS-EXT-02** | As an Extension Services Leader, I want rotation cycle management with GES calendar alignment so that book sets return on schedule | Feature | `feature` `manager` `extension-services` `ges-calendar` | High | **Given** a rotation cycle is active<br>**When** the cycle end date approaches<br>**Then** the system alerts me to prepare for return<br>**And** all book sets MUST return by August 31 (hard stop)<br>**And** rotation history is tracked per book<br>**And** book sets track cycle history including books present, missing, and degradation delta |
| **LMS-EXT-03** | As an Extension Services Leader, I want school delivery tracking for mobile van operations so that I can monitor field operations | Feature | `feature` `manager` `extension-services` | Medium | **Given** I have a delivery scheduled for Tamale<br>**When** I open the schedule<br>**Then** I see route, schools, and community leader contacts<br>**And** the schedule syncs to Android app during depot Wi-Fi<br>**And** works fully offline using cached route data |
| **LMS-EXT-04** | As an Extension Services Leader, I want Dagbani SMS templates for Northern Region operations so that I communicate effectively with rural communities | Feature | `feature` `manager` `extension-services` | High | **Given** I am sending SMS to Northern Region community<br>**When** I select Dagbani language<br>**Then** the system shows validated Dagbani templates<br>**And** templates are validated by University for Development Studies linguists<br>**And** SMS sends when connection restores via Vodafone/MTN/AirtelTigo |

### System Tasks (Infrastructure)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-EXT-10** | Implement Extension Services Android app sync protocol | System Task | `system-task` `android-app` `sync-infra` | High | **Given** the Android app is in the field<br>**When** the device connects to depot Wi-Fi<br>**Then** transactions sync via defined protocol<br>**And** compressed batch transfer is used<br>**And** conflicts are resolved by `transactionDate`<br>**And** Android app authenticates via API key or device token<br>**And** the app processes 100 transactions offline with zero data loss |
| **LMS-EXT-11** | Implement QR-based learner identification with smart tag design | System Task | `system-task` `android-app` `offline-first` | High | **Given** an Extension learner needs identification<br>**When** I generate a QR code<br>**Then** the QR contains ONLY `qrCodeId` (e.g., "EXT-QR-BOL-00042") — NO personal data<br>**And** physical tag is laminated 85.6×54mm, 250-micron laminate, rounded corners<br>**And** visual includes learner name + school in large font (low-literacy contexts)<br>**And** lost tag reuses same `qrCodeId` to preserve borrowing history |
| **LMS-EXT-12** | Implement Extension-Lending cross-department book status sync | System Task | `system-task` `sync-infra` `department-boundary` | High | **Given** books are allocated to Extension Services<br>**When** the allocation is confirmed<br>**Then** book status changes to "On Loan to Extension Services" with cycle tracking<br>**And** Lending section shows books as unavailable for regular circulation<br>**And** real-time sync prevents double-allocation<br>**And** return workflow triggers condition reassessment in Lending section |
| **LMS-EXT-13** | Build Extension Services schedule management with corridor safety | System Task | `system-task` `extension-services` `offline-first` | High | **Given** a delivery is scheduled for Tamale-Bolgatanga corridor<br>**When** the schedule is created<br>**Then** corridor safety protocols auto-trigger<br>**And** community leader contact workflow activates<br>**And** schedule syncs to Android app during pre-service depot Wi-Fi<br>**And** works fully offline using cached route data |

---

## 📊 SPRINT PLANNING RECOMMENDATIONS

| Sprint | Focus Area | Key Deliverables | Success Metrics |
|--------|------------|------------------|-----------------|
| **Sprint 1** | Core Infrastructure | LMS-CORE-01, LMS-CORE-02, LMS-CORE-03, LMS-CORE-04 | Zero data loss after 24h simulated outage; PouchDB + SQLite working |
| **Sprint 2** | Database Foundation + Backup System | LMS-CORE-07, LMS-CORE-08, LMS-CORE-09, LMS-CORE-10, LMS-CORE-11, LMS-BACK-01, LMS-BACK-02, LMS-BACK-03 | All domain databases initialized; Zod validation enforced; Repository pattern implemented; Backup pipeline fully automated with cloud storage |
| **Sprint 3** | Acquisitions + Ghana Compliance | LMS-ACQ-01, LMS-ACQ-02, LMS-ACQ-03, LMS-ACQ-10, LMS-ACQ-11, LMS-GH-01, LMS-GH-10, LMS-GH-11, LMS-GH-12 | 247 curriculum tags load offline in <2s; Orders sync on reconnect; Country profiles configurable |
| **Sprint 4** | Processing + Extension Routing | LMS-PROC-01, LMS-PROC-02, LMS-PROC-03, LMS-PROC-04, LMS-PROC-10 | Mold risk ≥90% accuracy; Extension routing populates conditional fields |
| **Sprint 5** | Distribution + Extension Depot | LMS-DIST-01, LMS-DIST-02, LMS-DIST-03, LMS-DIST-04, LMS-DIST-10, LMS-DIST-11 | Packing slips <10s offline; depot routing includes rotation metadata |
| **Sprint 6** | Children's Section + Degradation | LMS-CHILD-01, LMS-CHILD-02, LMS-CHILD-03 | Batch promotion 100% accurate; degradation ≥90% accuracy |
| **Sprint 7** | Staff + Lending Section | LMS-STAFF-01, LMS-STAFF-02, LMS-STAFF-03, LMS-STAFF-10, LMS-LEND-01, LMS-LEND-02, LMS-LEND-03, LMS-LEND-10 | Role switching includes Extension; bulk allocation workflow tested |
| **Sprint 8** | Extension Services + Android | LMS-EXT-01, LMS-EXT-02, LMS-EXT-03, LMS-EXT-04, LMS-EXT-10, LMS-EXT-11, LMS-EXT-12, LMS-EXT-13 | Department boundary enforced; rotation cycles aligned with GES; Android syncs 100 transactions offline |

---

## ✅ QUALITY GATES PER SPRINT

| Gate | Criteria | Validation Method |
|------|----------|-------------------|
| **Offline Resilience Gate** | Zero data loss after 24h simulated outage | Jest test with mock power loss + restart |
| **Ghana Compliance Gate** | No plaintext national IDs anywhere | Codebase grep + security audit script |
| **Degradation Accuracy Gate** | ≥90% match with manual librarian review | 100-book degradation audit with 3 librarians |
| **GES Calendar Gate** | All batches expire August 31; Extension cycles aligned | Date validation across 50 test batches + 4 rotation cycles |
| **Backup Size Gate** | Backups ≤10MB for cloud storage upload | Automated size validation in CI pipeline |
| **Bulk Allocation Gate** | Request → fulfillment → delivery → return with zero stranded books | End-to-end workflow test with 50-book simulated allocation |
| **Department Boundary Gate** | Extension staff CANNOT access library sections; Lending staff CANNOT access Extension workflows | Security object audit + role-switching penetration test |
| **Android Offline Gate** | 100 transactions processed offline with zero data loss | Field test at Bolgatanga rural school with no internet |

---

## ℹ️ IMPLEMENTATION NOTES FOR TEAMS

### 1. PM Guidance
- All tickets include Ghana-specific context in Acceptance Criteria
- Offline behavior explicitly stated (no "works offline" assumptions)
- Manager/Enterprise differentiation called out where applicable
- Extension Services tickets clearly marked (NEW) for sprint planning visibility

### 2. Developer Guidance
- **Database per domain**: Use the database registry pattern from `db_engineering.md`
- **Schema validation**: All writes pass Zod validation at the app boundary
- **Repository pattern**: Extend `BaseRepository<T>` for all domain operations
- **National ID hashing**: ONLY in Electron main process via IPC; hashing strategy is country-configurable
- **Department security**: Enforced at sync (CouchDB) and app (Zod) layers
- **Extension Services**: TOP-LEVEL DEPARTMENT — separate security objects, distinct `department` field values
- **Book status model**: `"available" | "on_loan" | "on_loan_to_extension" | "reserved" | "withdrawn" | "lost"`
- **Sync status**: `"pending" | "synced" | "conflict" | "error"`
- **Schema version**: `_schemaVersion` required on all documents
- **Country profiles**: Support Ghana, Kenya, Uganda, Tanzania with configurable identity rules, curriculum systems, and academic calendars

### 3. QA Guidance
- Success metrics quantifiable (≥90%, 100%, ≤500KB)
- Validation methods specified (manual review, automated test)
- Ghana context included in test scenarios (rainy season, power outage)
- Department boundary testing: verify Extension staff see ONLY Extension workflows
- Bulk allocation testing: verify zero double-allocations via concurrent request simulation

### 4. African Reality Checks
- Power outage duration based on Ghana Statistical Service 2023 data (3.2hr avg)
- Hardware specs reflect actual devices in Ghana schools (4GB RAM Windows 10)
- Twi translations validated by University of Ghana linguists (not Google Translate)
- Dagbani translations validated by University for Development Studies linguists
- Extension Services reality: 78% of Ghanaian basic schools have library space but lack books (GES 2023 survey)
- Country profiles must support custom institutions not covered by preloaded templates

### 5. Extension Services Boundary Rules (CRITICAL)
- Extension Services = DEPARTMENT (peer to Library Operations), NOT a library section
- Books remain owned by Lending Section; Extension has temporary custody
- Extension learners: minimal profiles (QR ID only, `extension_service: true`), no condition scoring, no degradation tracking
- Bulk Allocation Flow: Extension request → Lending fulfillment → Distribution delivery → Extension rotation → Return to Lending
- Android app is EXTERNAL tool – syncs to main database post-service, not real-time

### 6. Database Implementation Checklist (Per Ticket)
- [ ] Domain database identified (`books`, `patrons`, `loans`, `extensionLoans`, `departments`, `auditLog`, `config`)
- [ ] `BaseDocument` contract followed (`_id`, `_rev`, `type`, `createdAt`, `updatedAt`, `_syncStatus`, `_schemaVersion`)
- [ ] Zod schema defined and validated at app boundary
- [ ] Repository class extends `BaseRepository<T>`
- [ ] Indexes created for query patterns
- [ ] Department security objects respected
- [ ] Audit log entries created for sensitive operations
- [ ] Conflict resolution strategy implemented
- [ ] Offline behavior verified (no API calls)
- [ ] Country profile validated for identity rules and academic calendar

---

_Document Version: 3.0 (African Adaptation) • Prepared for Ghana Library Authority • October 2026_
_PM-friendly acceptance criteria • Extension Services as peer department • Bulk allocation workflow defined • Android app specified • Ghana context embedded • Offline resilience guaranteed • Database engineering foundation • Schema contracts defined • African country profiles supported_
_Ready for import into Jira with columns: Issue Type, Summary, Description, Labels, Acceptance Criteria_
