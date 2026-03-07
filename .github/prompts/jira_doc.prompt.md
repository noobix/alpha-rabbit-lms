\# 📚 Library Management System: Jira Ticket Specification  

\*User-centric tickets separated into Features (user value) vs System Tasks (infrastructure) for achievable 2-week sprints\*



---



\## 🏷️ LABELING CONVENTION

| Label | Purpose | Example |

|-------|---------|---------|

| `feature` | User-facing functionality with clear value | Patron dashboard, batch promotion |

| `system-task` | Infrastructure/database/security work | PouchDB setup, backup scheduler |

| `manager` | Manager version only | Single-library workflows |

| `enterprise` | Enterprise version only | Multi-branch sync |

| `ghana-compliance` | Ghana Data Protection Act requirements | Ghana Card ID hashing |

| `offline-first` | Critical offline capability | Power outage recovery |

| `priority:high` | Blocks subsequent work | Core database setup |



---



\## 🌐 EPIC: CORE INFRASTRUCTURE (`LMS-CORE`)

\*Foundation for offline-first operation, security, and Ghana compliance\*



\### System Tasks (Infrastructure)



| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |

|-----------|-------|------|--------|----------|---------------------|

| \*\*LMS-CORE-01\*\* | Set up PouchDB with SQLite adapter for offline storage | System Task | `system-task` `manager` `offline-first` | High | \*\*Given\*\* a Windows 10 device with 4GB RAM<br>\*\*When\*\* the application launches for the first time<br>\*\*Then\*\* a SQLite database file `library\_data.db` is created in `C:/GhanaLibraryData/`<br>\*\*And\*\* the database contains indexed collections for books, patrons, and staff |

| \*\*LMS-CORE-02\*\* | Implement SHA-256 hashing for Ghana Card ID storage | System Task | `system-task` `ghana-compliance` `security` | High | \*\*Given\*\* a staff member enters Ghana Card ID `GHA-123456789-0`<br>\*\*When\*\* the record is saved<br>\*\*Then\*\* the database stores only the hashed value `hashed:a3f8d2...`<br>\*\*And\*\* the UI displays a masked version `GHA-123\*\*\*89-0`<br>\*\*And\*\* plaintext ID is never written to logs or backups |

| \*\*LMS-CORE-03\*\* | Build incremental backup scheduler with WhatsApp compression | System Task | `system-task` `manager` `offline-first` | High | \*\*Given\*\* the library closes at 8:00 PM daily<br>\*\*When\*\* the backup scheduler triggers<br>\*\*Then\*\* an incremental backup file is created containing only changes since last backup<br>\*\*And\*\* the file size is ≤5% of main database (e.g., 3MB for 60MB DB)<br>\*\*And\*\* a "Send via WhatsApp" button compresses the file to <10MB for transfer |

| \*\*LMS-CORE-04\*\* | Implement 30-second auto-save for power outage resilience | System Task | `system-task` `offline-first` `ghana-compliance` | High | \*\*Given\*\* a librarian is cataloging a book<br>\*\*When\*\* power fails unexpectedly<br>\*\*Then\*\* upon restart, the system recovers the last valid state from ≤30 seconds before outage<br>\*\*And\*\* displays "Recovered your work from \[timestamp]"<br>\*\*And\*\* zero data loss occurs for transactions older than 30 seconds |

| \*\*LMS-CORE-05\*\* | Set up CouchDB server deployment for Raspberry Pi 4 | System Task | `system-task` `enterprise` `infrastructure` | Medium | \*\*Given\*\* a Raspberry Pi 4 with 4GB RAM and 128GB SD card<br>\*\*When\*\* the deployment script `setup-rpi-server.sh` is executed<br>\*\*Then\*\* CouchDB 3.3 starts on port 5984 with admin credentials<br>\*\*And\*\* data persists across reboots in `/home/pi/couchdb/data`<br>\*\*And\*\* the server consumes ≤15% CPU during idle state |



---



\## 📦 EPIC: ACQUISITIONS MODULE (`LMS-ACQ`)

\*Order books from Ghanaian vendors aligned with GES curriculum\*



\### Features (User Value)



| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |

|-----------|-------|------|--------|----------|---------------------|

| \*\*LMS-ACQ-01\*\* | As an Acquisitions Librarian, I want to enter vendor details with Ghana Card ID validation so that I comply with Ghana procurement regulations | Feature | `feature` `manager` `ghana-compliance` | High | \*\*Given\*\* I am creating a new vendor record<br>\*\*When\*\* I enter Ghana Card ID `GHA-987654321-0`<br>\*\*Then\*\* the system validates the format matches `GHA-000000000-0`<br>\*\*And\*\* saves only the hashed value to the database<br>\*\*And\*\* displays a tooltip: "Ghana Card ID required per Public Procurement Act 2003 (Act 663)" |

| \*\*LMS-ACQ-02\*\* | As an Acquisitions Librarian, I want to select Ghana Curriculum Tags during order creation so that books align with GES syllabus | Feature | `feature` `manager` `ghana-compliance` | High | \*\*Given\*\* I am placing an order for "Basic Science Grade 6"<br>\*\*When\*\* I reach the curriculum tag field<br>\*\*Then\*\* I see a searchable dropdown with 247 pre-loaded GES tags<br>\*\*And\*\* tags are grouped by level (Basic/JHS/SHS)<br>\*\*And\*\* selecting `BASIC-SCIENCE-GRADE-6` auto-fills Dewey Decimal `500` |

| \*\*LMS-ACQ-03\*\* | As an Acquisitions Librarian, I want to track budget allocation per department so that I stay within quarterly spending limits | Feature | `feature` `manager` `finance` | Medium | \*\*Given\*\* my budget code is `CHILDREN-2024-Q1` with GHS 5,000 allocation<br>\*\*When\*\* I add 50 books at GHS 15 each (GHS 750)<br>\*\*Then\*\* the UI shows remaining budget: GHS 4,250<br>\*\*And\*\* changes color to amber when <20% remains<br>\*\*And\*\* blocks orders exceeding remaining budget |



\### System Tasks (Infrastructure)



| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |

|-----------|-------|------|--------|----------|---------------------|

| \*\*LMS-ACQ-10\*\* | Pre-load Ghana Education Service curriculum tags database | System Task | `system-task` `ghana-compliance` `offline-first` | High | \*\*Given\*\* the application is installed on a device with no internet<br>\*\*When\*\* the Acquisitions module loads<br>\*\*Then\*\* 247 curriculum tags are available offline<br>\*\*And\*\* tags match MoE 2024/25 academic year validation certificate<br>\*\*And\*\* the database file size is ≤2.5MB |

| \*\*LMS-ACQ-11\*\* | Implement offline order queue with sync-on-reconnect | System Task | `system-task` `offline-first` `manager` | High | \*\*Given\*\* internet is unavailable during order placement<br>\*\*When\*\* I submit an order for 50 books<br>\*\*Then\*\* the order saves locally with status "Pending Sync"<br>\*\*And\*\* when connection restores, orders sync automatically within 60 seconds<br>\*\*And\*\* conflict resolution uses timestamp-based "last write wins" |



---



\## 🔍 EPIC: PROCESSING MODULE (`LMS-PROC`)

\*Inspect, classify, and prepare books for distribution with Ghana climate adaptations\*



\### Features (User Value)



| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |

|-----------|-------|------|--------|----------|---------------------|

| \*\*LMS-PROC-01\*\* | As a Cataloging Specialist, I want to rate book condition on spine/cover/pages/edges so that I track degradation in Ghana's tropical climate | Feature | `feature` `manager` `ghana-compliance` | High | \*\*Given\*\* I receive a new copy of "Basic Science Grade 6"<br>\*\*When\*\* I inspect the physical book<br>\*\*Then\*\* I see four 1-5 sliders labeled Spine, Cover, Pages, Edges<br>\*\*And\*\* spine slider has tooltip: "Critical in humid climate – check for separation"<br>\*\*And\*\* the system calculates overall health score as average of four components |

| \*\*LMS-PROC-02\*\* | As a Cataloging Specialist, I want automatic mold risk assessment based on season so that I protect books during rainy periods | Feature | `feature` `manager` `ghana-compliance` | High | \*\*Given\*\* today is May 15 (rainy season in Accra)<br>\*\*When\*\* I complete book inspection<br>\*\*Then\*\* the system flags mold risk as "Medium"<br>\*\*And\*\* displays recommendation: "Store in elevated shelving with silica gel packets"<br>\*\*And\*\* the risk level updates automatically based on Ghana seasonal calendar |

| \*\*LMS-PROC-03\*\* | As a Cataloging Specialist, I want to assign books to school batches (GRADE-4A) so that materials reach the correct learners | Feature | `feature` `manager` `ghana-compliance` | High | \*\*Given\*\* I am processing 50 copies of "Basic Science Grade 6"<br>\*\*When\*\* I reach the batch assignment field<br>\*\*Then\*\* I see a dropdown with active batches for my school<br>\*\*And\*\* selecting `GRADE-4A` auto-sets expiry date to August 31, 2025 (GES calendar)<br>\*\*And\*\* the system warns if batch expiry is <30 days away |



\### System Tasks (Infrastructure)



| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |

|-----------|-------|------|--------|----------|---------------------|

| \*\*LMS-PROC-10\*\* | Implement PDF417 barcode generator with Ghana Library Authority format | System Task | `system-task` `manager` `offline-first` | High | \*\*Given\*\* a processed book with curriculum tag `BASIC-SCIENCE-GRADE-6`<br>\*\*When\*\* I click "Generate Barcode"<br>\*\*Then\*\* the system creates barcode `SCI-6M-042`<br>\*\*And\*\* the format follows Ghana Library Authority standard: `\[SUBJECT]-\[GRADE]\[AUTHOR\_INITIAL]-\[SEQUENTIAL]`<br>\*\*And\*\* barcode image saves locally as PNG for printing without internet |

| \*\*LMS-PROC-11\*\* | Build Ghana seasonal calendar service for automatic mold risk assessment | System Task | `system-task` `ghana-compliance` `offline-first` | Medium | \*\*Given\*\* the device has no internet connection<br>\*\*When\*\* the Processing module initializes<br>\*\*Then\*\* it loads embedded seasonal calendar data<br>\*\*And\*\* determines current season based on device date:<br>• Dec-Feb: Dry (low mold risk)<br>• Mar-May/Sept-Nov: Rainy (high mold risk)<br>• Jun-Aug: Major rainy (critical mold risk)<br>\*\*And\*\* the calendar updates automatically on January 1 each year |



---



\## 📦 EPIC: DISTRIBUTION MODULE (`LMS-DIST`)

\*Route books to correct sections with batch-aware delivery for Ghana schools\*



\### Features (User Value)



| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |

|-----------|-------|------|--------|----------|---------------------|

| \*\*LMS-DIST-01\*\* | As a Distribution Manager, I want batch-aware packing slips that separate GRADE-4A from GRADE-4B so that repeat learners receive appropriate materials | Feature | `feature` `manager` `ghana-compliance` | High | \*\*Given\*\* 50 books processed for St. Peter's School<br>\*\*When\*\* I generate a packing slip<br>\*\*Then\*\* the system groups books by batch (`GRADE-4A`: 42 books, `GRADE-4B`: 8 books)<br>\*\*And\*\* the PDF shows batch-specific headers with learner counts<br>\*\*And\*\* repeat batch (`GRADE-4B`) has visual indicator: "Repeat learners – 20% extra books required" |

| \*\*LMS-DIST-02\*\* | As a Distribution Manager, I want rural delivery mode that disables GPS requirements so that I can deliver to Tamale-Bolgatanga corridor areas with poor signal | Feature | `feature` `manager` `ghana-compliance` | High | \*\*Given\*\* I am delivering to Bolgatanga Senior High (Upper East Region)<br>\*\*When\*\* I enable "Rural Delivery Mode"<br>\*\*Then\*\* GPS tracking fields become optional<br>\*\*And\*\* the system requires community leader contact details instead<br>\*\*And\*\* displays warning: "Ghana Library Authority Policy: Community leader notification mandatory for rural deliveries" |

| \*\*LMS-DIST-03\*\* | As a Distribution Manager, I want automatic rainy season alerts on packing slips so that books are protected during transport | Feature | `feature` `manager` `ghana-compliance` | Medium | \*\*Given\*\* today is April 20 (major rainy season)<br>\*\*When\*\* I generate a packing slip<br>\*\*Then\*\* the PDF includes red banner: "RAINY SEASON ALERT: Use waterproof covers + silica gel"<br>\*\*And\*\* lists books with glossy pages (Science/Math) requiring extra protection<br>\*\*And\*\* the alert disappears automatically on September 1 |



\### System Tasks (Infrastructure)



| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |

|-----------|-------|------|--------|----------|---------------------|

| \*\*LMS-DIST-10\*\* | Implement offline PDF generation for packing slips | System Task | `system-task` `offline-first` `manager` | High | \*\*Given\*\* internet is unavailable<br>\*\*When\*\* I click "Generate Packing Slip"<br>\*\*Then\*\* a PDF file saves to `C:/GhanaLibraryData/packing-slips/`<br>\*\*And\*\* the PDF contains:<br>• School name and address<br>• Batch groupings with book counts<br>• PDF417 barcode in Ghana Library Authority format<br>• QR code for section scanning<br>\*\*And\*\* file size is ≤500KB for WhatsApp transfer |

| \*\*LMS-DIST-11\*\* | Build Tamale-Bolgatanga corridor detection service | System Task | `system-task` `ghana-compliance` `offline-first` | Medium | \*\*Given\*\* a destination school ID `BOLGATANGA-UE-001`<br>\*\*When\*\* routing logic executes<br>\*\*Then\*\* the system identifies this as Tamale-Bolgatanga corridor school<br>\*\*And\*\* automatically enables rural delivery mode requirements<br>\*\*And\*\* adds corridor-specific notes to packing slip:<br>"Road conditions may affect delivery – confirm route with district office" |



---



\## 👧 EPIC: CHILDREN'S LIBRARY SECTION (`LMS-CHILD`)

\*Grade-specific batch management with degradation enforcement for young learners\*



\### Features (User Value)



| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |

|-----------|-------|------|--------|----------|---------------------|

| \*\*LMS-CHILD-01\*\* | As a Children's Section Leader, I want automatic batch promotion on August 15 so that learners progress with GES academic calendar | Feature | `feature` `manager` `ghana-compliance` | High | \*\*Given\*\* today is August 15, 2024<br>\*\*When\*\* the nightly job runs at 2:00 AM<br>\*\*Then\*\* all batches with >80% attendance are auto-promoted (GRADE-4A → GRADE-5A)<br>\*\*And\*\* learners with <70% attendance move to repeat batch (GRADE-5B)<br>\*\*And\*\* SMS notifications in Twi/English send to all parents<br>\*\*And\*\* the system logs promotion details for GES audit |

| \*\*LMS-CHILD-02\*\* | As a Children's Librarian, I want degradation threshold enforcement that blocks issuance to poor-care patrons so that our collection remains usable | Feature | `feature` `manager` `ghana-compliance` | High | \*\*Given\*\* patron Ama has degradation rate 0.35 (Red Zone)<br>\*\*When\*\* she requests "Ghana Folktales"<br>\*\*Then\*\* the system blocks issuance with message:<br>"Book care review required. Please see librarian for handling tips."<br>\*\*And\*\* requires staff override with reason field<br>\*\*And\*\* logs the block event with timestamp and staff ID |

| \*\*LMS-CHILD-03\*\* | As a Children's Librarian, I want to detect "Teleporter" patrons who return books with pristine spines after long checkouts so that I can address oral tradition contexts appropriately | Feature | `feature` `manager` `patron-intelligence` | Medium | \*\*Given\*\* patron Kwame returned 3 books with >7 days checkout and zero spine degradation<br>\*\*When\*\* I view his profile<br>\*\*Then\*\* the system shows "Teleporter Risk: Low (1/5 books flagged)"<br>\*\*And\*\* displays staff note: "Oral tradition context detected – likely reading aloud to siblings"<br>\*\*And\*\* does NOT block issuance (avoids stigmatizing Ghanaian household practices) |



\### System Tasks (Infrastructure)



| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |

|-----------|-------|------|--------|----------|---------------------|

| \*\*LMS-CHILD-10\*\* | Implement degradation engine with climate-aware weighting | System Task | `system-task` `offline-first` `ghana-compliance` | High | \*\*Given\*\* a book return with condition scores (spine:4, cover:5, pages:4, edges:5)<br>\*\*When\*\* the degradation engine calculates score<br>\*\*Then\*\* spine component weighted at 40% (critical in humid climate)<br>\*\*And\*\* cover at 25%, pages at 25%, edges at 10%<br>\*\*And\*\* the formula: `(spine\_loss\*0.4 + cover\_loss\*0.25 + pages\_loss\*0.25 + edges\_loss\*0.1)`<br>\*\*And\*\* works offline with no network dependency |

| \*\*LMS-CHILD-11\*\* | Build GES academic calendar service with August 31 expiry enforcement | System Task | `system-task` `ghana-compliance` `offline-first` | High | \*\*Given\*\* a batch `GRADE-4A` created on September 1, 2024<br>\*\*When\*\* the calendar service initializes<br>\*\*Then\*\* it sets expiry date to August 31, 2025<br>\*\*And\*\* on August 1, 2025 displays warning: "Batch expires in 30 days"<br>\*\*And\*\* on September 1, 2025 auto-marks batch as "inactive"<br>\*\*And\*\* the calendar works offline using device date |



---



\## 👨‍💼 EPIC: STAFF GOVERNANCE (`LMS-STAFF`)

\*Department hierarchy with Ghana Card ID verification for Manager version\*



\### Features (User Value)



| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |

|-----------|-------|------|--------|----------|---------------------|

| \*\*LMS-STAFF-01\*\* | As a System Admin, I want to create staff accounts with Ghana Card ID verification so that I comply with Ghana Data Protection Act | Feature | `feature` `manager` `ghana-compliance` | High | \*\*Given\*\* I am creating a new staff account for librarian Kwame Mensah<br>\*\*When\*\* I enter Ghana Card ID `GHA-123456789-0`<br>\*\*Then\*\* the system validates format and hashes the ID before storage<br>\*\*And\*\* displays masked version `GHA-123\*\*\*89-0` in UI<br>\*\*And\*\* prevents duplicate IDs across staff records<br>\*\*And\*\* requires supervisor assignment before activation |

| \*\*LMS-STAFF-02\*\* | As a System Admin, I want department role switching within single installation so that small libraries can operate with minimal devices | Feature | `feature` `manager` `offline-first` | High | \*\*Given\*\* I am logged in as System Admin<br>\*\*When\*\* I open the role switcher dropdown<br>\*\*Then\*\* I see options: System Admin, Acquisitions, Processing, Distribution, Children's Section<br>\*\*And\*\* selecting a role immediately changes UI to that department's workflow<br>\*\*And\*\* all data remains on the same device with no sync required |



\### System Tasks (Infrastructure)



| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |

|-----------|-------|------|--------|----------|---------------------|

| \*\*LMS-STAFF-10\*\* | Implement role-based UI filtering for Manager version | System Task | `system-task` `manager` `security` | High | \*\*Given\*\* a user switches to "Children's Section" role<br>\*\*When\*\* the application reloads the UI<br>\*\*Then\*\* only Children's Section features are visible (batch management, book issuance)<br>\*\*And\*\* Acquisitions/Processing menus are hidden<br>\*\*And\*\* data access is restricted to children's books and patrons<br>\*\*And\*\* works offline with no permission checks requiring network |



---



\## 🌍 EPIC: GHANA COMPLIANCE (`LMS-GH`)

\*Ghana-specific workflows required by law and cultural practice\*



\### Features (User Value)



| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |

|-----------|-------|------|--------|----------|---------------------|

| \*\*LMS-GH-01\*\* | As a Librarian, I want Twi language SMS templates for rural patrons so that I communicate effectively in low-literacy areas | Feature | `feature` `manager` `ghana-compliance` | High | \*\*Given\*\* a book is due tomorrow for patron in rural Tamale<br>\*\*When\*\* I trigger SMS reminder<br>\*\*Then\*\* the system shows Twi template:<br>"Nkwa! Wo nkwan 'Basic Science' rea ba. Mfa no kɔ dan no."<br>\*\*And\*\* English fallback is available<br>\*\*And\*\* messages queue locally when offline and send when connection restores |

| \*\*LMS-GH-02\*\* | As a Distribution Manager, I want community leader notification workflow for rural deliveries so that I comply with Ghana Library Authority policy | Feature | `feature` `manager` `ghana-compliance` | High | \*\*Given\*\* I enable rural delivery mode for Bolgatanga school<br>\*\*When\*\* I prepare the delivery<br>\*\*Then\*\* the system requires community leader name and phone number<br>\*\*And\*\* provides Twi SMS template:<br>"Naa, Ghana Library Authority delivery arriving today. Please meet driver at school."<br>\*\*And\*\* blocks delivery confirmation until leader contact is recorded |



\### System Tasks (Infrastructure)



| Ticket ID | Title | Type | Labels | Priority | Acceptance Criteria |

|-----------|-------|------|--------|----------|---------------------|

| \*\*LMS-GH-10\*\* | Implement offline SMS queue with Ghana network provider support | System Task | `system-task` `offline-first` `ghana-compliance` | High | \*\*Given\*\* internet is unavailable during delivery<br>\*\*When\*\* I confirm delivery with SMS notification<br>\*\*Then\*\* the message saves to local queue in `sms-queue.json`<br>\*\*And\*\* when connection restores, messages send via Vodafone/MTN/AirtelTigo APIs<br>\*\*And\*\* delivery reports show success/failure per network provider<br>\*\*And\*\* queue retains last 100 messages with 7-day expiry |

| \*\*LMS-GH-11\*\* | Embed Ghana seasonal calendar with automatic mold risk updates | System Task | `system-task` `ghana-compliance` `offline-first` | Medium | \*\*Given\*\* the device date is April 15<br>\*\*When\*\* any module accesses seasonal data<br>\*\*Then\*\* the service returns "major\_rainy\_season"<br>\*\*And\*\* mold risk defaults to "high" for all new books<br>\*\*And\*\* the calendar requires no internet to function<br>\*\*And\*\* updates automatically on January 1 without user intervention |



---



\## 📅 SPRINT PLANNING RECOMMENDATIONS



\### Sprint 1 (Weeks 1-2): Core Infrastructure + Basic Acquisitions

| Ticket ID | Type | Effort | Dependencies |

|-----------|------|--------|--------------|

| LMS-CORE-01 | System Task | 5 pts | None |

| LMS-CORE-02 | System Task | 3 pts | LMS-CORE-01 |

| LMS-ACQ-10 | System Task | 3 pts | LMS-CORE-01 |

| LMS-ACQ-01 | Feature | 3 pts | LMS-ACQ-10 |

| LMS-ACQ-02 | Feature | 5 pts | LMS-ACQ-10 |

| \*\*Sprint Goal\*\* | \*Deliver offline-capable acquisitions module that validates Ghana Card IDs and curriculum tags\* | | |



\### Sprint 2 (Weeks 3-4): Processing + Climate Adaptations

| Ticket ID | Type | Effort | Dependencies |

|-----------|------|--------|--------------|

| LMS-CORE-04 | System Task | 5 pts | LMS-CORE-01 |

| LMS-PROC-10 | System Task | 5 pts | LMS-CORE-01 |

| LMS-PROC-11 | System Task | 3 pts | LMS-CORE-01 |

| LMS-PROC-01 | Feature | 5 pts | LMS-PROC-10 |

| LMS-PROC-02 | Feature | 3 pts | LMS-PROC-11 |

| LMS-PROC-03 | Feature | 3 pts | LMS-PROC-01 |

| \*\*Sprint Goal\*\* | \*Deliver processing workflow with climate-aware condition scoring and batch assignment\* | | |



\### Sprint 3 (Weeks 5-6): Distribution + Rural Delivery

| Ticket ID | Type | Effort | Dependencies |

|-----------|------|--------|--------------|

| LMS-CORE-03 | System Task | 8 pts | LMS-CORE-01 |

| LMS-DIST-10 | System Task | 5 pts | LMS-CORE-01 |

| LMS-DIST-11 | System Task | 3 pts | LMS-CORE-01 |

| LMS-DIST-01 | Feature | 5 pts | LMS-DIST-10 |

| LMS-DIST-02 | Feature | 3 pts | LMS-DIST-11 |

| LMS-DIST-03 | Feature | 2 pts | LMS-PROC-11 |

| \*\*Sprint Goal\*\* | \*Deliver batch-aware distribution with rural delivery mode for Tamale-Bolgatanga corridor\* | | |



\### Sprint 4 (Weeks 7-8): Children's Section + Degradation Engine

| Ticket ID | Type | Effort | Dependencies |

|-----------|------|--------|--------------|

| LMS-CHILD-10 | System Task | 8 pts | LMS-CORE-01 |

| LMS-CHILD-11 | System Task | 3 pts | LMS-CORE-01 |

| LMS-CHILD-01 | Feature | 5 pts | LMS-CHILD-11 |

| LMS-CHILD-02 | Feature | 5 pts | LMS-CHILD-10 |

| LMS-CHILD-03 | Feature | 3 pts | LMS-CHILD-10 |

| \*\*Sprint Goal\*\* | \*Deliver children's section with GES-aligned batch promotion and degradation enforcement\* | | |



\### Sprint 5 (Weeks 9-10): Adult/Reference Sections + Patron Intelligence

| Ticket ID | Type | Effort | Dependencies |

|-----------|------|--------|--------------|

| LMS-STAFF-10 | System Task | 5 pts | LMS-CORE-01 |

| LMS-STAFF-01 | Feature | 3 pts | LMS-CORE-02 |

| LMS-STAFF-02 | Feature | 3 pts | LMS-STAFF-10 |

| LMS-GH-10 | System Task | 5 pts | LMS-CORE-01 |

| LMS-GH-01 | Feature | 3 pts | LMS-GH-10 |

| \*\*Sprint Goal\*\* | \*Deliver staff governance with Ghana Card ID verification and Twi SMS capabilities\* | | |



\### Sprint 6 (Weeks 11-12): Ghana Compliance Finalization + Pilot Prep

| Ticket ID | Type | Effort | Dependencies |

|-----------|------|--------|--------------|

| LMS-GH-11 | System Task | 3 pts | LMS-CORE-01 |

| LMS-GH-02 | Feature | 3 pts | LMS-GH-10 |

| LMS-CORE-05 | System Task | 8 pts | None |

| \*\*Sprint Goal\*\* | \*Complete Ghana compliance requirements and prepare Manager version for St. Peter's School pilot\* | | |



---



\## ✅ QUALITY GATES PER SPRINT



| Sprint | Gate Criteria | Validation Method |

|--------|---------------|-------------------|

| \*\*Sprint 1\*\* | • Offline acquisitions workflow functional<br>• Ghana Card ID hashing verified by DPC liaison | SQLite inspection + hashing audit |

| \*\*Sprint 2\*\* | • Condition scoring works offline<br>• Mold risk assessment matches manual review (≥90%) | 50-book processing test with librarian panel |

| \*\*Sprint 3\*\* | • Packing slips generate offline <10s<br>• Rural mode disables GPS without errors | Tamale library field test (simulated offline) |

| \*\*Sprint 4\*\* | • Batch promotion accurate (100% learner assignment)<br>• Degradation engine ≥90% accuracy vs manual review | 50-learner promotion test + 100-book degradation audit |

| \*\*Sprint 5\*\* | • Staff roles switch without data loss<br>• Twi SMS delivers ≥95% success rate | Role-switching stress test + 100 SMS delivery test |

| \*\*Sprint 6\*\* | • Full offline resilience (24h outage)<br>• DPC submission package complete | Simulated power/internet outage + compliance review |



---



\## ℹ️ IMPLEMENTATION NOTES FOR PRODUCT OWNERS



1\. \*\*Feature vs System Task Separation\*\*  

&nbsp;  - Features deliver direct user value (e.g., "batch promotion")  

&nbsp;  - System tasks enable features but have no standalone user value (e.g., "GES calendar service")  

&nbsp;  - Never schedule a Feature without its dependent System Tasks in same/previous sprint



2\. \*\*Ghana Context is Non-Negotiable\*\*  

&nbsp;  - Every ticket includes Ghana-specific acceptance criteria  

&nbsp;  - Offline capability required for all features (no "requires internet" exceptions)  

&nbsp;  - Twi language support prioritized for rural-facing features



3\. \*\*Manager Version First\*\*  

&nbsp;  - All sprints deliver Manager version functionality first  

&nbsp;  - Enterprise features built atop Manager foundation in later phases  

&nbsp;  - Migration path ("Promote to Enterprise") validated in Sprint 6



4\. \*\*Ethical Safeguards Built-In\*\*  

&nbsp;  - Reader categories never shown to patrons (staff-only)  

&nbsp;  - Degradation enforcement includes coaching pathways (not punishment)  

&nbsp;  - Oral tradition contexts respected in Teleporter detection



5\. \*\*Pilot-Ready Definition\*\*  

&nbsp;  A sprint is "done" only when:  

&nbsp;  - All acceptance criteria pass on Ghana-spec hardware (Windows 10, 4GB RAM)  

&nbsp;  - Offline capability validated with 24-hour simulated outage  

&nbsp;  - Ghana compliance verified by DPC liaison or MoE curriculum officer



---



\*Document Version: 1.0 • Prepared for Ghana Library Authority • February 2026\*  

✅ \*\*User-centric tickets\*\* • ✅ \*\*Clear feature/system separation\*\* • ✅ \*\*Ghana context embedded\*\* • ✅ \*\*Achievable 2-week sprints\*  

\*Ready for import into Jira via CSV with columns: Issue Type, Summary, Description, Labels, Priority, Component\*

