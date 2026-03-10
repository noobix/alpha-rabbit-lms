# ��� Library Management System: Jira Ticket Specification (Extension Services Department Update)

*User-centric tickets separated into Features (user value) vs System Tasks (infrastructure) for achievable 2-week sprints*

*Critical correction: Extension Services is a full external department (not library section) that borrows books from Lending section via bulk allocation workflow*

---

## ���️ LABELING CONVENTION

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

---

## ��� EPIC: CORE INFRASTRUCTURE (`LMS-CORE`)

*Foundation for offline-first operation, security, and Ghana compliance*

### System Tasks (Infrastructure)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-CORE-01** | Set up PouchDB with SQLite adapter for offline storage | System Task | `system-task` `manager` `offline-first` | High | **Given** a Windows 10 device with 4GB RAM<br>**When** the application launches for the first time<br>**Then** a SQLite database file `library_data.db` is created in `C:/GhanaLibraryData/`<br>**And** the database contains indexed collections for books, patrons, staff, and extension records |
| **LMS-CORE-02** | Implement SHA-256 hashing for Ghana Card ID storage | System Task | `system-task` `ghana-compliance` `security` | High | **Given** a staff member enters Ghana Card ID `GHA-123456789-0`<br>**When** the record is saved<br>**Then** the database stores only the hashed value `hashed:a3f8d2...`<br>**And** the UI displays a masked version `GHA-123***89-0`<br>**And** plaintext ID is never written to logs or backups |
| **LMS-CORE-03** | Build incremental backup scheduler with WhatsApp compression | System Task | `system-task` `manager` `offline-first` | High | **Given** the library closes at 8:00 PM daily<br>**When** the backup scheduler triggers<br>**Then** an incremental backup file is created containing only changes since last backup<br>**And** the file size is ≤5% of main database (e.g., 3MB for 60MB DB)<br>**And** a "Send via WhatsApp" button compresses the file to <10MB for transfer |
| **LMS-CORE-04** | Implement 30-second auto-save for power outage resilience | System Task | `system-task` `offline-first` `ghana-compliance` | High | **Given** a librarian is cataloging a book<br>**When** power fails unexpectedly<br>**Then** upon restart, the system recovers the last valid state from ≤30 seconds before outage<br>**And** displays "Recovered your work from [timestamp]"<br>**And** zero data loss occurs for transactions older than 30 seconds |
| **LMS-CORE-05** | Set up CouchDB server deployment for Raspberry Pi 4 | System Task | `system-task` `enterprise` `infrastructure` | Medium | **Given** a Raspberry Pi 4 with 4GB RAM and 128GB SD card<br>**When** the deployment script `setup-rpi-server.sh` is executed<br>**Then** CouchDB 3.3 starts on port 5984 with admin credentials<br>**And** data persists across reboots in `/home/pi/couchdb/data`<br>**And** the server consumes ≤15% CPU during idle state |
| **LMS-CORE-06** | Implement department security objects for 6 departments | System Task | `system-task` `enterprise` `department-boundary` | High | **Given** the system has 6 departments (Acquisitions, Processing, Distribution, Library Operations, Extension Services, System Admin)<br>**When** security objects are configured<br>**Then** Extension Services staff CANNOT access library section data<br>**And** Lending section staff see ONLY "Bulk Requests" tab for Extension requests<br>**And** cross-department data access is blocked by security objects |

---

## ��� EPIC: ACQUISITIONS MODULE (`LMS-ACQ`)

*Order books from Ghanaian vendors aligned with GES curriculum*

### Features (User Value)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-ACQ-01** | As an Acquisitions Librarian, I want to enter vendor details with Ghana Card ID validation so that I comply with Ghana procurement regulations | Feature | `feature` `manager` `ghana-compliance` | High | **Given** I am creating a new vendor record<br>**When** I enter Ghana Card ID `GHA-987654321-0`<br>**Then** the system validates the format matches `GHA-000000000-0`<br>**And** saves only the hashed value to the database<br>**And** displays a tooltip: "Ghana Card ID required per Public Procurement Act 2003 (Act 663)" |
| **LMS-ACQ-02** | As an Acquisitions Librarian, I want to select Ghana Curriculum Tags during order creation so that books align with GES syllabus | Feature | `feature` `manager` `ghana-compliance` | High | **Given** I am placing an order for "Basic Science Grade 6"<br>**When** I reach the curriculum tag field<br>**Then** I see a searchable dropdown with 247 pre-loaded GES tags<br>**And** tags are grouped by level (Basic/JHS/SHS)<br>**And** selecting `BASIC-SCIENCE-GRADE-6` auto-fills Dewey Decimal `500` |
| **LMS-ACQ-03** | As an Acquisitions Librarian, I want to track budget allocation per department so that I stay within quarterly spending limits | Feature | `feature` `manager` `finance` | Medium | **Given** my budget code is `CHILDREN-2024-Q1` with GHS 5,000 allocation<br>**When** I add 50 books at GHS 15 each (GHS 750)<br>**Then** the UI shows remaining budget: GHS 4,250<br>**And** changes color to amber when <20% remains<br>**And** blocks orders exceeding remaining budget |

### System Tasks (Infrastructure)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-ACQ-10** | Pre-load Ghana Education Service curriculum tags database | System Task | `system-task` `ghana-compliance` `offline-first` | High | **Given** the application is installed on a device with no internet<br>**When** the Acquisitions module loads<br>**Then** 247 curriculum tags are available offline<br>**And** tags match MoE 2024/25 academic year validation certificate<br>**And** the database file size is ≤2.5MB |
| **LMS-ACQ-11** | Implement offline order queue with sync-on-reconnect | System Task | `system-task` `offline-first` `manager` | High | **Given** internet is unavailable during order placement<br>**When** I submit an order for 50 books<br>**Then** the order saves locally with status "Pending Sync"<br>**And** when connection restores, orders sync automatically within 60 seconds<br>**And** conflict resolution uses timestamp-based "last write wins" |

---

## ��� EPIC: PROCESSING MODULE (`LMS-PROC`)

*Inspect, classify, and prepare books for distribution with Ghana climate adaptations and Extension Services routing*

### Features (User Value)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-PROC-01** | As a Cataloging Specialist, I want to rate book condition on spine/cover/pages/edges so that I track degradation in Ghana's tropical climate | Feature | `feature` `manager` `ghana-compliance` | High | **Given** I receive a new copy of "Basic Science Grade 6"<br>**When** I inspect the physical book<br>**Then** I see four 1-5 sliders labeled Spine, Cover, Pages, Edges<br>**And** spine slider has tooltip: "Critical in humid climate – check for separation"<br>**And** the system calculates overall health score as average of four components |
| **LMS-PROC-02** | As a Cataloging Specialist, I want automatic mold risk assessment based on season so that I protect books during rainy periods | Feature | `feature` `manager` `ghana-compliance` | High | **Given** today is May 15 (rainy season in Accra)<br>**When** I complete book inspection<br>**Then** the system flags mold risk as "Medium"<br>**And** displays recommendation: "Store in elevated shelving with silica gel packets"<br>**And** the risk level updates automatically based on Ghana seasonal calendar |
| **LMS-PROC-03** | As a Cataloging Specialist, I want to assign books to school batches (GRADE-4A) so that materials reach the correct learners | Feature | `feature` `manager` `ghana-compliance` | High | **Given** I am processing 50 copies of "Basic Science Grade 6"<br>**When** I reach the batch assignment field<br>**Then** I see a dropdown with active batches for my school<br>**And** selecting `GRADE-4A` auto-sets expiry date to August 31, 2025 (GES calendar)<br>**And** the system warns if batch expiry is <30 days away |
| **LMS-PROC-04** | As a Cataloging Specialist, I want to route books to Extension Services department with durability scoring so that books survive mobile library rotation cycles | Feature | `feature` `manager` `extension-services` | High | **Given** I am processing 50 copies of "Basic Science Grade 6" for Extension Services<br>**When** I select section routing "Extension Services" (top-level department)<br>**Then** the system displays conditional Extension Services fields:<br>• Rotation Cycle dropdown (CYCLE-1 to CYCLE-4)<br>• Mobile Handling Durability slider (1-5)<br>• Destination Region selector<br>**And** hides batch assignment fields (not applicable to Extension)<br>**And** validates durability ≥3 required for Tamale-Bolgatanga corridor<br>**And** Tamale-Bolgatanga corridor safety protocols auto-trigger for Northern Region destinations |

### System Tasks (Infrastructure)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-PROC-10** | Implement PDF417 barcode generator with Ghana Library Authority format | System Task | `system-task` `manager` `offline-first` | High | **Given** a processed book with curriculum tag `BASIC-SCIENCE-GRADE-6`<br>**When** I click "Generate Barcode"<br>**Then** the system creates barcode `SCI-6M-042`<br>**And** the format follows Ghana Library Authority standard: `[SUBJECT]-[GRADE][AUTHOR_INITIAL]-[SEQUENTIAL]`<br>**And** barcode image saves locally as PNG for printing without internet |
| **LMS-PROC-11** | Build Ghana seasonal calendar service for automatic mold risk assessment | System Task | `system-task` `ghana-compliance` `offline-first` | Medium | **Given** the device has no internet connection<br>**When** the Processing module initializes<br>**Then** it loads embedded seasonal calendar data<br>**And** determines current season based on device date:<br>• Dec-Feb: Dry (low mold risk)<br>• Mar-May/Sept-Nov: Rainy (high mold risk)<br>• Jun-Aug: Major rainy (critical mold risk)<br>**And** the calendar updates automatically on January 1 each year |
| **LMS-PROC-12** | Implement barcode rotation cycle indicator for Extension Services books | System Task | `system-task` `extension-services` `offline-first` | High | **Given** a book routed to Extension Services with rotation cycle CYCLE-2<br>**When** I click "Generate Barcode"<br>**Then** the barcode appends `-C2` suffix: `SCI-6M-042-C2`<br>**And** the cycle indicator follows format `-C[1-4]`<br>**And** barcode is scannable by Android app during Extension Services field transactions |

---

## ��� EPIC: DISTRIBUTION MODULE (`LMS-DIST`)

*Route books to correct sections and Extension Services depot with batch-aware delivery for Ghana schools*

### Features (User Value)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-DIST-01** | As a Distribution Manager, I want batch-aware packing slips that separate GRADE-4A from GRADE-4B so that repeat learners receive appropriate materials | Feature | `feature` `manager` `ghana-compliance` | High | **Given** 50 books processed for St. Peter's School<br>**When** I generate a packing slip<br>**Then** the system groups books by batch (`GRADE-4A`: 42 books, `GRADE-4B`: 8 books)<br>**And** the PDF shows batch-specific headers with learner counts<br>**And** repeat batch (`GRADE-4B`) has visual indicator: "Repeat learners – 20% extra books required" |
| **LMS-DIST-02** | As a Distribution Manager, I want rural delivery mode that disables GPS requirements so that I can deliver to Tamale-Bolgatanga corridor areas with poor signal | Feature | `feature` `manager` `ghana-compliance` | High | **Given** I am delivering to Bolgatanga Senior High (Upper East Region)<br>**When** I enable "Rural Delivery Mode"<br>**Then** GPS tracking fields become optional<br>**And** the system requires community leader contact details instead<br>**And** displays warning: "Ghana Library Authority Policy: Community leader notification mandatory for rural deliveries" |
| **LMS-DIST-03** | As a Distribution Manager, I want automatic rainy season alerts on packing slips so that books are protected during transport | Feature | `feature` `manager` `ghana-compliance` | Medium | **Given** today is April 20 (major rainy season)<br>**When** I generate a packing slip<br>**Then** the PDF includes red banner: "RAINY SEASON ALERT: Use waterproof covers + silica gel"<br>**And** lists books with glossy pages (Science/Math) requiring extra protection<br>**And** the alert disappears automatically on September 1 |
| **LMS-DIST-04** | As a Distribution Manager, I want to deliver books to Extension Services depot with rotation cycle metadata so that Extension staff receive correctly tagged book sets | Feature | `feature` `manager` `extension-services` | High | **Given** Lending section has fulfilled a bulk allocation request for Bolgatanga Extension depot<br>**When** I generate a packing slip for destination "Extension Services Depot"<br>**Then** the packing slip includes:<br>• Rotation cycle indicator (e.g., CYCLE-2)<br>• Depot location and contact details<br>• Community leader signature field for rural depot locations<br>• READ-ONLY rotation cycle metadata (assigned during Lending fulfillment)<br>**And** Dagbani SMS template sent to depot contact: "Zuli libri ka ti kpɛ. Cycle 2 books arriving today."<br>**And** distribution NEVER handles school-level delivery details (that is Extension Services' responsibility) |

### System Tasks (Infrastructure)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-DIST-10** | Implement offline PDF generation for packing slips | System Task | `system-task` `offline-first` `manager` | High | **Given** internet is unavailable<br>**When** I click "Generate Packing Slip"<br>**Then** a PDF file saves to `C:/GhanaLibraryData/packing-slips/`<br>**And** the PDF contains:<br>• School name and address<br>• Batch groupings with book counts<br>• PDF417 barcode in Ghana Library Authority format<br>• QR code for section scanning<br>**And** file size is ≤500KB for WhatsApp transfer |
| **LMS-DIST-11** | Build Tamale-Bolgatanga corridor detection service | System Task | `system-task` `ghana-compliance` `offline-first` | Medium | **Given** a destination school ID `BOLGATANGA-UE-001`<br>**When** routing logic executes<br>**Then** the system identifies this as Tamale-Bolgatanga corridor school<br>**And** automatically enables rural delivery mode requirements<br>**And** adds corridor-specific notes to packing slip:<br>"Road conditions may affect delivery – confirm route with district office" |
| **LMS-DIST-12** | Implement Extension Services depot routing with Dagbani SMS | System Task | `system-task` `extension-services` `offline-first` | High | **Given** destination type is "Extension Services Depot"<br>**When** routing logic executes<br>**Then** the system routes to depot location (NOT directly to schools)<br>**And** populates depot-specific packing slip fields (rotation cycle, depot contact)<br>**And** queues Dagbani SMS notification to depot contact<br>**And** community leader signature workflow activates for rural depot locations |

---

## ��� EPIC: EXTENSION SERVICES DEPARTMENT (`LMS-EXT`)

*Top-level department (peer to Acquisitions/Processing/Distribution/Library Operations) managing mobile library services for underserved schools via rotating book sets*

> **Critical Boundary**: Extension Services is a DEPARTMENT, not a library section. Books are temporarily loaned FROM the Lending Section via bulk allocation workflow. Extension Services does NOT maintain permanent collections.

### Features (User Value)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-EXT-01** | As an Extension Services Leader, I want to create bulk book requests for school rotation cycles so that rural schools receive curriculum-aligned materials | Feature | `feature` `manager` `extension-services` | High | **Given** Bolgatanga Upper East schools need 50 Basic Science books for CYCLE-2 (Jan-Mar)<br>**When** I create a bulk request<br>**Then** the system sends request to Lending Section "Pending Requests" dashboard<br>**And** request includes: school name, cycle, quantity, subject areas, destination region<br>**And** request status tracks through: Pending → Approved → Fulfilling → Ready for Delivery<br>**And** I can ONLY see Extension Services workflows (no library section access) |
| **LMS-EXT-02** | As an Extension Services Leader, I want rotation cycle management aligned with GES calendar so that book sets return before academic year end | Feature | `feature` `manager` `extension-services` `ges-calendar` | High | **Given** GES 4-cycle annual rotation:<br>• Cycle 1: Sept 1 – Dec 15<br>• Cycle 2: Jan 10 – Mar 28<br>• Cycle 3: Apr 15 – Jun 20<br>• Cycle 4: Jul 15 – Aug 31<br>**When** I manage rotation cycles<br>**Then** the system auto-flags sets for collection 14 days before cycle end<br>**And** ALL book sets MUST return to depot by August 31 (hard stop)<br>**And** Cycle 2 prioritizes WASSCE/BECE exam materials with Tamale-Bolgatanga safety alerts<br>**And** Cycle 3 includes rainy season mold prevention kits |
| **LMS-EXT-03** | As an Extension Services staff member, I want school delivery tracking via mobile library van so that I know which schools have been serviced this cycle | Feature | `feature` `manager` `extension-services` | High | **Given** I am planning service visits for Bolgatanga corridor schools<br>**When** I view the schedule dashboard<br>**Then** I see a list of schools with service status (scheduled/in-progress/completed/missed)<br>**And** community leader contacts are pre-loaded for each school<br>**And** rainy season road alerts display for affected routes<br>**And** the schedule works fully offline with sync when connection restores |
| **LMS-EXT-04** | As an Extension Services staff member, I want QR-based learner checkout/return on the Android app so that I can process transactions during school visits without internet | Feature | `feature` `manager` `extension-services` `android-app` | High | **Given** I am at a rural school with no internet<br>**When** a learner presents their QR smart tag<br>**Then** I scan the QR code with the Android device camera<br>**And** the app displays learner name and current books (from pre-synced data)<br>**And** I scan book barcode to checkout (max 2 books enforced)<br>**And** NO condition scoring fields shown (high-traffic, <5 min/learner)<br>**And** NO interaction scores recorded (degradation tracking disabled for Extension learners)<br>**And** transaction saves to local SQLite (encrypted at rest) |
| **LMS-EXT-05** | As an Extension Services Leader, I want Dagbani SMS templates for Northern Region schools so that community leaders receive notifications in their language | Feature | `feature` `manager` `extension-services` `ghana-compliance` | High | **Given** I am scheduling a service visit to Bolgatanga<br>**When** I send community leader notification<br>**Then** the system shows Dagbani template: "Zuli libri ka ti kpɛ. Yɛlsim cycle 2 books."<br>**And** English fallback is available<br>**And** messages queue locally when offline and send when connection restores via Vodafone/MTN/AirtelTigo |

### System Tasks (Infrastructure)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-EXT-10** | Build Android offline transaction app for Extension Services | System Task | `system-task` `extension-services` `android-app` `offline-first` | High | **Given** an Android device with camera<br>**When** the app launches at a school with no internet<br>**Then** all pre-synced learner records and book barcodes are available<br>**And** QR scanning works in low-light rural school conditions (ZXing library)<br>**And** local SQLite database is encrypted at rest (Android Keystore)<br>**And** battery optimization: screen timeout 30s, low-power mode for all-day van service<br>**And** post-service sync uploads all transactions when depot Wi-Fi available |
| **LMS-EXT-11** | Implement QR-based learner identification with smart tag design | System Task | `system-task` `extension-services` `offline-first` | High | **Given** a new Extension Services learner at Bolgatanga school<br>**When** a smart tag is generated<br>**Then** QR contains ONLY `qrCodeId` (e.g., "EXT-QR-BOL-00042") – NO personal data<br>**And** physical format: laminated 85.6×54mm with 250-micron laminate + rounded corners<br>**And** visual elements: learner name + school in large font (low literacy contexts)<br>**And** if tag is lost, same `qrCodeId` reused to preserve borrowing history |
| **LMS-EXT-12** | Implement Extension-Lending cross-department book status sync | System Task | `system-task` `extension-services` `lending-section` `department-boundary` | High | **Given** Lending section fulfills a bulk allocation for Extension Services<br>**When** books are allocated<br>**Then** book status changes to "On Loan to Extension Services" with cycle tracking<br>**And** Lending section shows books as unavailable for regular circulation<br>**And** real-time sync prevents double-allocation<br>**And** return workflow triggers condition reassessment in Lending section |
| **LMS-EXT-13** | Build Extension Services schedule management with corridor safety | System Task | `system-task` `extension-services` `ghana-compliance` | Medium | **Given** a service schedule for Tamale-Bolgatanga corridor<br>**When** schedule is created<br>**Then** corridor safety protocols auto-trigger (road condition alerts, rainy season warnings)<br>**And** community leader contact workflow activates<br>**And** schedule syncs to Android app during pre-service depot Wi-Fi connection<br>**And** works fully offline using cached route data |

---

## ��� EPIC: LENDING SECTION (`LMS-LEND`)

*Library section responsible for bulk allocation fulfillment to Extension Services department*

> **Critical Boundary**: Lending Section OWNS the books. Extension Services BORROWS them temporarily for rotation cycles. Books return to Lending after each cycle.

### Features (User Value)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-LEND-01** | As a Lending Section Leader, I want to fulfill bulk allocation requests from Extension Services so that rural schools receive books on schedule | Feature | `feature` `manager` `lending-section` | High | **Given** Extension Services has submitted a bulk request for 50 Basic Science books, CYCLE-2, Bolgatanga<br>**When** I view the "Pending Requests" tab on my dashboard<br>**Then** I see the request with details: school, cycle, quantity, subject areas<br>**And** I can select books from available Lending collection to fulfill the request<br>**And** fulfilled books change status to "On Loan to Extension Services" with cycle metadata<br>**And** fulfilled books are marked unavailable for regular circulation<br>**And** I CANNOT access Extension Services workflows (department boundary enforced) |
| **LMS-LEND-02** | As a Lending Section Leader, I want rotation tracking and return workflow so that books come back in assessed condition after each cycle | Feature | `feature` `manager` `lending-section` | High | **Given** CYCLE-2 books are due to return from Extension Services by March 28<br>**When** books are returned to the Lending section<br>**Then** the system triggers condition reassessment workflow<br>**And** book status changes from "On Loan to Extension Services" back to "Available"<br>**And** the system tracks: cycle history, number of rotations, cumulative condition changes<br>**And** overdue returns (past August 31 hard stop) trigger escalation alerts |
| **LMS-LEND-03** | As a Lending Section Leader, I want collection health monitoring for Extension-loaned books so that I track cumulative wear from rotation cycles | Feature | `feature` `manager` `lending-section` | Medium | **Given** a book has completed 3 rotation cycles to Extension Services<br>**When** I view the book's record<br>**Then** I see rotation history: cycles served, destinations, condition at each return<br>**And** cumulative degradation is tracked separately from regular circulation degradation<br>**And** the system recommends withdrawal when condition drops below threshold after Extension use |

### System Tasks (Infrastructure)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-LEND-10** | Implement cross-department book status tracking for Extension loans | System Task | `system-task` `lending-section` `department-boundary` `offline-first` | High | **Given** a book is allocated to Extension Services<br>**When** the allocation is confirmed<br>**Then** book record updates: `status: "on_loan_to_extension"` with `extensionLoan` object<br>**And** `extensionLoan` includes: department, cycle code, allocated date, due return date, allocated-by staff ID<br>**And** Lending section never shows allocated books as available<br>**And** works offline with sync on reconnect |

---

## ��� EPIC: CHILDREN'S LIBRARY SECTION (`LMS-CHILD`)

*Grade-specific batch management with degradation enforcement for young learners*

### Features (User Value)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-CHILD-01** | As a Children's Section Leader, I want automatic batch promotion on August 15 so that learners progress with GES academic calendar | Feature | `feature` `manager` `ghana-compliance` | High | **Given** today is August 15, 2024<br>**When** the nightly job runs at 2:00 AM<br>**Then** all batches with >80% attendance are auto-promoted (GRADE-4A → GRADE-5A)<br>**And** learners with <70% attendance move to repeat batch (GRADE-5B)<br>**And** SMS notifications in Twi/English send to all parents<br>**And** the system logs promotion details for GES audit |
| **LMS-CHILD-02** | As a Children's Librarian, I want degradation threshold enforcement that blocks issuance to poor-care patrons so that our collection remains usable | Feature | `feature` `manager` `ghana-compliance` | High | **Given** patron Ama has degradation rate 0.35 (Red Zone)<br>**When** she requests "Ghana Folktales"<br>**Then** the system blocks issuance with message:<br>"Book care review required. Please see librarian for handling tips."<br>**And** requires staff override with reason field<br>**And** logs the block event with timestamp and staff ID |
| **LMS-CHILD-03** | As a Children's Librarian, I want to detect "Teleporter" patrons who return books with pristine spines after long checkouts so that I can address oral tradition contexts appropriately | Feature | `feature` `manager` `patron-intelligence` | Medium | **Given** patron Kwame returned 3 books with >7 days checkout and zero spine degradation<br>**When** I view his profile<br>**Then** the system shows "Teleporter Risk: Low (1/5 books flagged)"<br>**And** displays staff note: "Oral tradition context detected – likely reading aloud to siblings"<br>**And** does NOT block issuance (avoids stigmatizing Ghanaian household practices) |

### System Tasks (Infrastructure)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-CHILD-10** | Implement degradation engine with climate-aware weighting | System Task | `system-task` `offline-first` `ghana-compliance` | High | **Given** a book return with condition scores (spine:4, cover:5, pages:4, edges:5)<br>**When** the degradation engine calculates score<br>**Then** spine component weighted at 40% (critical in humid climate)<br>**And** cover at 25%, pages at 25%, edges at 10%<br>**And** the formula: `(spine_loss*0.4 + cover_loss*0.25 + pages_loss*0.25 + edges_loss*0.1)`<br>**And** works offline with no network dependency |
| **LMS-CHILD-11** | Build GES academic calendar service with August 31 expiry enforcement | System Task | `system-task` `ghana-compliance` `offline-first` | High | **Given** a batch `GRADE-4A` created on September 1, 2024<br>**When** the calendar service initializes<br>**Then** it sets expiry date to August 31, 2025<br>**And** on August 1, 2025 displays warning: "Batch expires in 30 days"<br>**And** on September 1, 2025 auto-marks batch as "inactive"<br>**And** the calendar works offline using device date |

---

## ���‍��� EPIC: STAFF GOVERNANCE (`LMS-STAFF`)

*Department hierarchy with Ghana Card ID verification for Manager version – updated for Extension Services as peer department*

### Features (User Value)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-STAFF-01** | As a System Admin, I want to create staff accounts with Ghana Card ID verification so that I comply with Ghana Data Protection Act | Feature | `feature` `manager` `ghana-compliance` | High | **Given** I am creating a new staff account for librarian Kwame Mensah<br>**When** I enter Ghana Card ID `GHA-123456789-0`<br>**Then** the system validates format and hashes the ID before storage<br>**And** displays masked version `GHA-123***89-0` in UI<br>**And** prevents duplicate IDs across staff records<br>**And** requires supervisor assignment before activation |
| **LMS-STAFF-02** | As a System Admin, I want department role switching within single installation so that small libraries can operate with minimal devices | Feature | `feature` `manager` `offline-first` | High | **Given** I am logged in as System Admin<br>**When** I open the role switcher dropdown<br>**Then** I see options: System Admin, Acquisitions, Processing, Distribution, Library Operations (Children's/Adult/Reference/Lending), **Extension Services**<br>**And** selecting Extension Services shows ONLY Extension workflows (bulk requests, rotation management, schedule)<br>**And** selecting Lending shows "Bulk Requests" tab alongside regular lending workflows<br>**And** all data remains on the same device with no sync required |
| **LMS-STAFF-03** | As a System Admin, I want Extension Services staff profile configuration with route certification and bulk request authority so that department boundaries are enforced | Feature | `feature` `manager` `extension-services` `department-boundary` | High | **Given** I am creating a staff profile for Extension Services department<br>**When** I configure the profile<br>**Then** the system requires: department (Extension Services), route certification (Tamale-Bolgatanga/other), bulk request authority level<br>**And** Extension Services staff CANNOT access library section workflows<br>**And** staff profile includes rotation cycle access permissions<br>**And** department field value is "extension_services" (NOT a section code) |

### System Tasks (Infrastructure)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-STAFF-10** | Implement role-based UI filtering for Manager version | System Task | `system-task` `manager` `security` | High | **Given** a user switches to "Extension Services" role<br>**When** the application reloads the UI<br>**Then** only Extension Services features are visible (bulk requests, rotation management, schedules)<br>**And** library section menus are completely hidden<br>**And** Lending section role shows "Bulk Requests" tab for Extension fulfillment<br>**And** data access is restricted per department security objects<br>**And** works offline with no permission checks requiring network |

---

## ��� EPIC: GHANA COMPLIANCE (`LMS-GH`)

*Ghana-specific workflows required by law and cultural practice – updated with Dagbani language support*

### Features (User Value)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-GH-01** | As a Librarian, I want Twi/Dagbani language SMS templates for rural patrons so that I communicate effectively in low-literacy areas | Feature | `feature` `manager` `ghana-compliance` | High | **Given** a book is due tomorrow for patron in rural Tamale<br>**When** I trigger SMS reminder<br>**Then** the system shows Twi template:<br>"Nkwa! Wo nkwan 'Basic Science' rea ba. Mfa no kɔ dan no."<br>**And** Dagbani template available for Northern Region: "Zuli libri ka ti kpɛ"<br>**And** English fallback is available<br>**And** messages queue locally when offline and send when connection restores |
| **LMS-GH-02** | As a Distribution Manager, I want community leader notification workflow for rural deliveries so that I comply with Ghana Library Authority policy | Feature | `feature` `manager` `ghana-compliance` | High | **Given** I enable rural delivery mode for Bolgatanga school<br>**When** I prepare the delivery<br>**Then** the system requires community leader name and phone number<br>**And** provides Twi/Dagbani SMS templates based on destination region<br>**And** blocks delivery confirmation until leader contact is recorded |

### System Tasks (Infrastructure)

| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |
|-----------|-------|------|--------|----------|---------------------|
| **LMS-GH-10** | Implement offline SMS queue with Ghana network provider support | System Task | `system-task` `offline-first` `ghana-compliance` | High | **Given** internet is unavailable during delivery<br>**When** I confirm delivery with SMS notification<br>**Then** the message saves to local queue in `sms-queue.json`<br>**And** when connection restores, messages send via Vodafone/MTN/AirtelTigo APIs<br>**And** delivery reports show success/failure per network provider<br>**And** queue retains last 100 messages with 7-day expiry |
| **LMS-GH-11** | Embed Ghana seasonal calendar with automatic mold risk updates | System Task | `system-task` `ghana-compliance` `offline-first` | Medium | **Given** the device date is April 15<br>**When** any module accesses seasonal data<br>**Then** the service returns "major_rainy_season"<br>**And** mold risk defaults to "high" for all new books<br>**And** the calendar requires no internet to function<br>**And** updates automatically on January 1 without user intervention |
| **LMS-GH-12** | Implement Dagbani language support for Extension Services Northern Region operations | System Task | `system-task` `ghana-compliance` `extension-services` | High | **Given** Extension Services operates in Northern Region (Tamale-Bolgatanga corridor)<br>**When** the Android app or desktop module loads for Northern Region<br>**Then** Dagbani translations available for: checkout button ("Zuli Libri"), return button, SMS templates<br>**And** language toggle in Android app: English/Twi/Dagbani<br>**And** Dagbani translations validated by University for Development Studies linguist |

---

## ��� SPRINT PLANNING RECOMMENDATIONS

### Sprint 1 (Weeks 1-2): Core Infrastructure + Basic Acquisitions

| Ticket ID | Type | Effort | Dependencies |
|-----------|------|--------|--------------|
| LMS-CORE-01 | System Task | 5 pts | None |
| LMS-CORE-02 | System Task | 3 pts | LMS-CORE-01 |
| LMS-ACQ-10 | System Task | 3 pts | LMS-CORE-01 |
| LMS-ACQ-01 | Feature | 3 pts | LMS-ACQ-10 |
| LMS-ACQ-02 | Feature | 5 pts | LMS-ACQ-10 |
| **Sprint Goal** | *Deliver offline-capable acquisitions module that validates Ghana Card IDs and curriculum tags* | | |

### Sprint 2 (Weeks 3-4): Processing + Climate Adaptations + Extension Routing

| Ticket ID | Type | Effort | Dependencies |
|-----------|------|--------|--------------|
| LMS-CORE-04 | System Task | 5 pts | LMS-CORE-01 |
| LMS-PROC-10 | System Task | 5 pts | LMS-CORE-01 |
| LMS-PROC-11 | System Task | 3 pts | LMS-CORE-01 |
| LMS-PROC-12 | System Task | 3 pts | LMS-PROC-10 |
| LMS-PROC-01 | Feature | 5 pts | LMS-PROC-10 |
| LMS-PROC-02 | Feature | 3 pts | LMS-PROC-11 |
| LMS-PROC-03 | Feature | 3 pts | LMS-PROC-01 |
| LMS-PROC-04 | Feature | 5 pts | LMS-PROC-12 |
| **Sprint Goal** | *Deliver processing workflow with climate-aware condition scoring, batch assignment, and Extension Services routing* | | |

### Sprint 3 (Weeks 5-6): Distribution + Rural Delivery + Extension Depot

| Ticket ID | Type | Effort | Dependencies |
|-----------|------|--------|--------------|
| LMS-CORE-03 | System Task | 8 pts | LMS-CORE-01 |
| LMS-DIST-10 | System Task | 5 pts | LMS-CORE-01 |
| LMS-DIST-11 | System Task | 3 pts | LMS-CORE-01 |
| LMS-DIST-12 | System Task | 5 pts | LMS-DIST-10 |
| LMS-DIST-01 | Feature | 5 pts | LMS-DIST-10 |
| LMS-DIST-02 | Feature | 3 pts | LMS-DIST-11 |
| LMS-DIST-03 | Feature | 2 pts | LMS-PROC-11 |
| LMS-DIST-04 | Feature | 5 pts | LMS-DIST-12 |
| **Sprint Goal** | *Deliver batch-aware distribution with rural delivery mode and Extension Services depot routing* | | |

### Sprint 4 (Weeks 7-8): Children's Section + Degradation Engine

| Ticket ID | Type | Effort | Dependencies |
|-----------|------|--------|--------------|
| LMS-CHILD-10 | System Task | 8 pts | LMS-CORE-01 |
| LMS-CHILD-11 | System Task | 3 pts | LMS-CORE-01 |
| LMS-CHILD-01 | Feature | 5 pts | LMS-CHILD-11 |
| LMS-CHILD-02 | Feature | 5 pts | LMS-CHILD-10 |
| LMS-CHILD-03 | Feature | 3 pts | LMS-CHILD-10 |
| **Sprint Goal** | *Deliver children's section with GES-aligned batch promotion and degradation enforcement* | | |

### Sprint 5 (Weeks 9-10): Staff Governance + Ghana Compliance + Lending Section

| Ticket ID | Type | Effort | Dependencies |
|-----------|------|--------|--------------|
| LMS-STAFF-10 | System Task | 5 pts | LMS-CORE-01 |
| LMS-STAFF-01 | Feature | 3 pts | LMS-CORE-02 |
| LMS-STAFF-02 | Feature | 5 pts | LMS-STAFF-10 |
| LMS-STAFF-03 | Feature | 3 pts | LMS-STAFF-10 |
| LMS-LEND-10 | System Task | 5 pts | LMS-CORE-01 |
| LMS-LEND-01 | Feature | 5 pts | LMS-LEND-10 |
| LMS-LEND-02 | Feature | 3 pts | LMS-LEND-10 |
| LMS-GH-10 | System Task | 5 pts | LMS-CORE-01 |
| LMS-GH-01 | Feature | 3 pts | LMS-GH-10 |
| **Sprint Goal** | *Deliver staff governance with Extension Services roles, Lending section bulk allocation, and Twi/Dagbani SMS* | | |

### Sprint 6 (Weeks 11-12): Extension Services Department + Android App

| Ticket ID | Type | Effort | Dependencies |
|-----------|------|--------|--------------|
| LMS-CORE-06 | System Task | 5 pts | LMS-CORE-01 |
| LMS-EXT-10 | System Task | 13 pts | LMS-EXT-12 |
| LMS-EXT-11 | System Task | 5 pts | LMS-EXT-10 |
| LMS-EXT-12 | System Task | 8 pts | LMS-LEND-10 |
| LMS-EXT-13 | System Task | 3 pts | LMS-CORE-01 |
| LMS-EXT-01 | Feature | 5 pts | LMS-EXT-12 |
| LMS-EXT-02 | Feature | 5 pts | LMS-EXT-13 |
| LMS-EXT-03 | Feature | 3 pts | LMS-EXT-13 |
| **Sprint Goal** | *Deliver Extension Services department with bulk request creation, rotation cycle management, and Android offline app foundation* | | |

### Sprint 7 (Weeks 13-14): Extension Android App + Pilot Prep

| Ticket ID | Type | Effort | Dependencies |
|-----------|------|--------|--------------|
| LMS-EXT-04 | Feature | 8 pts | LMS-EXT-10, LMS-EXT-11 |
| LMS-EXT-05 | Feature | 3 pts | LMS-GH-10 |
| LMS-GH-11 | System Task | 3 pts | LMS-CORE-01 |
| LMS-GH-12 | System Task | 5 pts | LMS-GH-10 |
| LMS-GH-02 | Feature | 3 pts | LMS-GH-10 |
| LMS-LEND-03 | Feature | 3 pts | LMS-LEND-10 |
| LMS-CORE-05 | System Task | 8 pts | None |
| **Sprint Goal** | *Complete Extension Services Android app, Dagbani language support, and prepare for St. Peter's School + Tamale-Bolgatanga corridor pilot* | | |

---

## ✅ QUALITY GATES PER SPRINT

| Sprint | Gate Criteria | Validation Method |
|--------|---------------|-------------------|
| **Sprint 1** | • Offline acquisitions workflow functional<br>• Ghana Card ID hashing verified by DPC liaison | SQLite inspection + hashing audit |
| **Sprint 2** | • Condition scoring works offline<br>• Mold risk assessment matches manual review (≥90%)<br>• Extension Services routing populates conditional fields correctly | 50-book processing test with librarian panel + Extension routing verification |
| **Sprint 3** | • Packing slips generate offline <10s<br>• Rural mode disables GPS without errors<br>• Extension Services depot packing slips include rotation metadata | Tamale library field test (simulated offline) + depot routing test |
| **Sprint 4** | • Batch promotion accurate (100% learner assignment)<br>• Degradation engine ≥90% accuracy vs manual review | 50-learner promotion test + 100-book degradation audit |
| **Sprint 5** | • Staff roles switch without data loss (including Extension Services)<br>• Lending section bulk allocation fulfills requests correctly<br>• Twi/Dagbani SMS delivers ≥95% success rate | Role-switching stress test + bulk allocation workflow test + 100 SMS delivery test |
| **Sprint 6** | • Extension Services department boundary enforced (CANNOT access library sections)<br>• Bulk allocation workflow: request → fulfillment → delivery → return<br>• Cross-department sync prevents double-allocation | Department boundary security audit + end-to-end bulk allocation test |
| **Sprint 7** | • Android app processes 100 transactions offline without data loss<br>• QR smart tag scanning works in low-light conditions<br>• Full offline resilience (24h outage)<br>• DPC submission package complete | Android field test at Bolgatanga school + simulated outage + compliance review |

---

## ℹ️ IMPLEMENTATION NOTES FOR PRODUCT OWNERS

1. **Feature vs System Task Separation**
   - Features deliver direct user value (e.g., "bulk request creation")
   - System tasks enable features but have no standalone user value (e.g., "cross-department sync")
   - Never schedule a Feature without its dependent System Tasks in same/previous sprint

2. **Ghana Context is Non-Negotiable**
   - Every ticket includes Ghana-specific acceptance criteria
   - Offline capability required for all features (no "requires internet" exceptions)
   - Twi/Dagbani language support prioritized for rural-facing features

3. **Manager Version First**
   - All sprints deliver Manager version functionality first
   - Enterprise features built atop Manager foundation in later phases
   - Migration path ("Promote to Enterprise") validated in Sprint 7

4. **Extension Services Department Boundary (CRITICAL)**
   - Extension Services is a TOP-LEVEL DEPARTMENT (peer to Acquisitions/Processing/Distribution/Library Operations)
   - Extension Services is NOT a library section – separate security objects, distinct staff department field values
   - Books remain owned by Lending Section; Extension Services has temporary custody via bulk allocation
   - Extension staff see ONLY Extension workflows; Lending staff see "Bulk Requests" tab

5. **Ethical Safeguards Built-In**
   - Reader categories never shown to patrons (staff-only)
   - Degradation enforcement includes coaching pathways (not punishment)
   - Oral tradition contexts respected in Teleporter detection
   - Extension learners tagged `extension_service: true` with minimal profiles (privacy + high volume)

6. **Pilot-Ready Definition**
   A sprint is "done" only when:
   - All acceptance criteria pass on Ghana-spec hardware (Windows 10, 4GB RAM)
   - Offline capability validated with 24-hour simulated outage
   - Ghana compliance verified by DPC liaison or MoE curriculum officer
   - Extension Services department boundary verified via security audit

---

*Document Version: 1.2 (Extension Services Department Update) • Prepared for Ghana Library Authority • March 2026*
✅ **User-centric tickets** • ✅ **Clear feature/system separation** • ✅ **Extension Services as peer department** • ✅ **Bulk allocation workflow defined** • ✅ **Android app specified** • ✅ **Achievable 2-week sprints**
*Ready for import into Jira via CSV with columns: Issue Type, Summary, Description, Labels, Priority, Component*
