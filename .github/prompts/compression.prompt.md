# Ì≥ö Library Management System: Jira Ticket Specification (Extension Services Department Update)

*User-centric tickets with Ghana context, offline resilience, and Manager/Enterprise differentiation ‚Äì PM-friendly format with technical implementation guidance*

*Critical correction: Extension Services is a full external department (not library section) that borrows books from Lending section via bulk allocation workflow*

---

## Ìºê OVERARCHING PROJECT EPIC: `LMS-LIBRARY`

*Cross-cutting infrastructure, Ghana compliance, and offline-first foundation for library operations*

### Ì¥í Child Epic: `LMS-CORE-SECURITY`

*Security backbone for patron data and staff operations*

| Ticket ID | Title | Acceptance Criteria |
|-----------|-------|---------------------|
| **LMS-101** | Implement SHA-256 hashing for Ghana Card ID storage | AC: Ghana Card ID `GHA-123456789-0` stored as `hashed:a3f8d2...`<br>AC: Plaintext ID never appears in logs/backups/UI<br>AC: Masked display `GHA-123***89-0` in all interfaces<br>AC: Hashing occurs ONLY in Electron main process (never renderer) |
| **LMS-102** | Build incremental backup scheduler with WhatsApp compression | AC: Daily backup at 8 PM creates file ‚â§5% of DB size (3MB for 60MB DB)<br>AC: "Send via WhatsApp" button compresses backup to <10MB<br>AC: Backup resumes automatically after power outage<br>AC: 30-day retention policy enforced with auto-deletion |
| **LMS-103** | Implement 30-second auto-save for power outage resilience | AC: Transaction data saved every 30 seconds without user action<br>AC: After 4-hour power outage, 99% of transactions >30s old recover<br>AC: Recovery message shows timestamp: "Recovered work from 10:14 AM"<br>AC: Zero data corruption verified via checksum validation |
| **LMS-104** | Add battery optimization exemption flow for rural libraries | AC: In-app rationale screen explains Ghana power instability context<br>AC: One-tap enable flow for Windows "Allow background apps"<br>AC: Persistent notification when exemption not granted<br>AC: Works on Windows 10 devices with 4GB RAM (Ghana school standard) |
| **LMS-105** | Implement department security objects for 6 departments (NEW) | AC: 6 departments configured: Acquisitions, Processing, Distribution, Library Operations, Extension Services, System Admin<br>AC: Extension Services staff CANNOT access library section data<br>AC: Lending section staff see ONLY "Bulk Requests" tab for Extension requests<br>AC: Cross-department data access blocked by security objects |

---

### Ìºç Child Epic: `LMS-GHANA-COMPLIANCE`

*Ghana-specific legal requirements and cultural adaptations*

| Ticket ID | Title | Acceptance Criteria |
|-----------|-------|---------------------|
| **LMS-201** | Implement Ghana Data Protection Act 2012 (Act 843) compliance | AC: Patron records auto-anonymized after 2 years inactive<br>AC: Closed accounts purged within 72 hours + audit log entry<br>AC: Staff records retained exactly 7 years post-employment (Ghana law)<br>AC: One-tap account deletion with confirmation SMS in Twi/English |
| **LMS-202** | Integrate Ghana Education Service curriculum tags (2024/25) | AC: 247 pre-loaded GES tags matching MoE validation certificate #MoE-2024-087<br>AC: Tags grouped by level: Basic/JHS/SHS with grade-specific variants<br>AC: Offline access without internet (embedded JSON ‚â§2.5MB)<br>AC: Auto-suggest Dewey Decimal based on curriculum tag |
| **LMS-203** | Build Twi/Dagbani language support for rural library and Extension staff (UPDATED) | AC: Critical screens (checkout, batch management) fully translated to Twi<br>AC: Dagbani translations for Extension Services Northern Region operations<br>AC: Android app language toggle: English/Twi/Dagbani<br>AC: SMS templates in Twi/Dagbani validated by University of Ghana + UDS linguists<br>AC: Language toggle in Settings with persistent selection |
| **LMS-204** | Implement GES academic calendar with August 31 expiry | AC: All batches auto-expire August 31 per Ghana Education Service standard<br>AC: Extension Services rotation cycles aligned: Cycle 1 (Sept-Dec), Cycle 2 (Jan-Mar), Cycle 3 (Apr-Jun), Cycle 4 (Jul-Aug)<br>AC: ALL Extension book sets MUST return to depot by August 31 (hard stop)<br>AC: Pre-promotion report generated June 15 listing batches expiring Aug 31<br>AC: Auto-promotion August 15 for batches with >80% attendance |

---

### Ì≥¶ Child Epic: `LMS-ACQUISITIONS`

*Book ordering workflow with Ghanaian vendor management*

| Ticket ID | Title | Acceptance Criteria |
|-----------|-------|---------------------|
| **LMS-301** | Implement vendor management with Ghana Card ID validation | AC: Vendor form requires Ghana Card ID format `GHA-000000000-0`<br>AC: Format validation tooltip: "Ghana Card required per Public Procurement Act 2003"<br>AC: Hashed ID stored; plaintext never persisted<br>AC: Works offline with local vendor list sync on reconnect |
| **LMS-302** | Build budget tracking per department with GES alignment | AC: Budget codes follow Ghana format `CHILDREN-2024-Q1`<br>AC: Real-time remaining balance display during order creation<br>AC: Amber warning at <20% budget remaining<br>AC: Blocks orders exceeding remaining budget with override requiring Department Head approval |
| **LMS-303** | Implement offline order queue with sync-on-reconnect | AC: Orders save locally with status "Pending Sync" when offline<br>AC: Sync completes within 60 seconds of internet restoration<br>AC: Conflict resolution uses timestamp-based "last write wins"<br>AC: Failed syncs retry with exponential backoff (1s ‚Üí 30s) |

---

### Ì¥ç Child Epic: `LMS-PROCESSING`

*Physical inspection and classification with Ghana climate adaptations and Extension Services routing*

| Ticket ID | Title | Acceptance Criteria |
|-----------|-------|---------------------|
| **LMS-401** | Implement condition scoring sliders for spine/cover/pages/edges | AC: 1-5 sliders with climate-aware weighting (spine 40%, cover 25%, pages 25%, edges 10%)<br>AC: Visual indicators: red=1 (poor) ‚Üí green=5 (excellent)<br>AC: Spine crease counter (0-5) with tooltip: "Critical in humid climate"<br>AC: Overall health score auto-calculated as weighted average |
| **LMS-402** | Build mold risk assessment based on Ghana seasonal calendar | AC: Automatic risk level (none/low/medium/high/critical) based on current date<br>AC: April-June & Sept-Nov: "high" risk with recommendation "Use silica gel packets"<br>AC: December-February: "low" risk with recommendation "Standard shelving sufficient"<br>AC: Works offline using embedded seasonal calendar (no API calls) |
| **LMS-403** | Generate PDF417 barcodes with Ghana Library Authority format | AC: Barcode format `SCI-6M-042` = `[SUBJECT]-[GRADE][AUTHOR_INITIAL]-[SEQUENTIAL]`<br>AC: Extension Services books append rotation cycle suffix: `SCI-6M-042-C2`<br>AC: PDF saves locally ‚â§500KB for WhatsApp transfer<br>AC: Works offline with no internet dependency<br>AC: Includes QR code for section scanning upon delivery |
| **LMS-404** | Route books to Extension Services department with durability scoring (NEW) | AC: Section routing dropdown includes "Extension Services" as top-level department option<br>AC: Selecting Extension triggers conditional fields: Rotation Cycle (CYCLE-1 to CYCLE-4), Mobile Handling Durability (1-5), Destination Region<br>AC: Durability ‚â•3 required for Tamale-Bolgatanga corridor<br>AC: Tamale-Bolgatanga corridor safety protocols auto-trigger for Northern Region<br>AC: Batch assignment fields hidden when routing to Extension (not applicable)<br>AC: `extensionServices` object MUST be populated when routing to Extension |

---

### Ì≥¶ Child Epic: `LMS-DISTRIBUTION`

*Batch-aware routing, rural delivery, and Extension Services depot workflows*

| Ticket ID | Title | Acceptance Criteria |
|-----------|-------|---------------------|
| **LMS-501** | Implement batch-aware packing slips with GRADE-4A vs GRADE-4B separation | AC: Packing slip groups books by batch (`GRADE-4A`: 42 books, `GRADE-4B`: 8 books)<br>AC: Repeat batches (`GRADE-4B`) display amber warning: "GES Policy: 20% extra books required"<br>AC: PDF includes GES academic year expiry date (August 31)<br>AC: File size ‚â§500KB for WhatsApp transfer |
| **LMS-502** | Build rural delivery mode for Tamale-Bolgatanga corridor | AC: "Rural Mode" toggle disables GPS requirements<br>AC: Mandatory community leader contact fields when rural mode enabled<br>AC: Twi/Dagbani SMS templates based on destination region<br>AC: Works offline with delivery confirmation queued for sync |
| **LMS-503** | Implement rainy season alerts on packing slips | AC: April-June & Sept-Nov: Red banner "RAINY SEASON ALERT" on packing slip<br>AC: Lists books with glossy pages (Science/Math) requiring extra protection<br>AC: Alert disappears automatically September 1<br>AC: Works offline using device date (no network dependency) |
| **LMS-504** | Deliver books to Extension Services depot with rotation cycle metadata (NEW) | AC: Destination type "Extension Services Depot" triggers depot-specific workflow<br>AC: Packing slip includes: rotation cycle, depot location, community leader signature field<br>AC: Rotation cycle metadata is READ-ONLY (assigned during Lending fulfillment)<br>AC: Dagbani SMS notification sent to depot contact<br>AC: Distribution NEVER handles school-level delivery details (Extension Services' responsibility)<br>AC: Community leader signature workflow activates for rural depot locations |

---

### Ìºç Child Epic: `LMS-EXTENSION-SERVICES` (NEW)

*Top-level department managing mobile library services for underserved schools via rotating book sets borrowed from Lending Section*

> **Critical Boundary**: Extension Services is a DEPARTMENT (peer to Library Operations), NOT a library section. Books are temporarily loaned FROM Lending Section. Extension learners have minimal profiles (QR ID only, no condition scoring, no degradation tracking).

| Ticket ID | Title | Acceptance Criteria |
|-----------|-------|---------------------|
| **LMS-801** | Create bulk book requests for school rotation cycles (NEW) | AC: Extension Services Leader creates request with: school, cycle (1-4), quantity, subject areas, destination region<br>AC: Request appears on Lending Section "Pending Requests" dashboard<br>AC: Status tracking: Pending ‚Üí Approved ‚Üí Fulfilling ‚Üí Ready for Delivery<br>AC: Extension staff see ONLY Extension workflows (no library section access)<br>AC: Works offline with sync on reconnect |
| **LMS-802** | Implement rotation cycle management with GES calendar (NEW) | AC: 4-cycle annual rotation: Cycle 1 (Sept-Dec), Cycle 2 (Jan-Mar), Cycle 3 (Apr-Jun), Cycle 4 (Jul-Aug)<br>AC: Auto-flag sets for collection 14 days before cycle end<br>AC: ALL book sets MUST return to depot by August 31 (hard stop)<br>AC: Cycle 2 prioritizes WASSCE/BECE exam materials<br>AC: Cycle 3 includes rainy season mold prevention kits |
| **LMS-803** | Build school delivery tracking via mobile library van (NEW) | AC: Schedule dashboard shows schools with status: scheduled/in-progress/completed/missed<br>AC: Community leader contacts pre-loaded per school<br>AC: Rainy season road alerts for affected routes<br>AC: Works fully offline with sync when connection restores |
| **LMS-804** | Implement QR-based learner checkout/return on Android app (NEW) | AC: Scan QR smart tag with device camera (works in low-light rural conditions)<br>AC: Display learner name and current books from pre-synced data<br>AC: Scan book barcode to checkout (max 2 books enforced)<br>AC: NO condition scoring fields (high-traffic, <5 min/learner)<br>AC: NO interaction scores/degradation tracking for Extension learners<br>AC: Transaction saves to local encrypted SQLite (Android Keystore) |
| **LMS-805** | Build Dagbani SMS templates for Northern Region schools (NEW) | AC: Dagbani template: "Zuli libri ka ti kp…õ. Y…õlsim cycle 2 books."<br>AC: English fallback available<br>AC: Messages queue offline; send via Vodafone/MTN/AirtelTigo on reconnect<br>AC: Templates validated by University for Development Studies linguist |

### Extension Services System Tasks

| Ticket ID | Title | Acceptance Criteria |
|-----------|-------|---------------------|
| **LMS-810** | Build Android offline transaction app for Extension Services (NEW) | AC: All pre-synced learner records and book barcodes available offline<br>AC: QR scanning via ZXing library works in low-light conditions<br>AC: Local SQLite encrypted at rest (Android Keystore)<br>AC: Battery optimization: screen timeout 30s, low-power mode<br>AC: Post-service sync uploads transactions when depot Wi-Fi available |
| **LMS-811** | Implement QR-based learner identification with smart tag design (NEW) | AC: QR contains ONLY `qrCodeId` (e.g., "EXT-QR-BOL-00042") ‚Äì NO personal data<br>AC: Physical: laminated 85.6√ó54mm, 250-micron laminate, rounded corners<br>AC: Visual: learner name + school in large font (low-literacy contexts)<br>AC: Lost tag reuses same `qrCodeId` to preserve borrowing history |
| **LMS-812** | Implement Extension-Lending cross-department book status sync (NEW) | AC: Books allocated change status to "On Loan to Extension Services" with cycle tracking<br>AC: Lending section shows books as unavailable for regular circulation<br>AC: Real-time sync prevents double-allocation<br>AC: Return workflow triggers condition reassessment in Lending section |
| **LMS-813** | Build Extension Services schedule management with corridor safety (NEW) | AC: Tamale-Bolgatanga corridor safety protocols auto-trigger<br>AC: Community leader contact workflow activates<br>AC: Schedule syncs to Android app during pre-service depot Wi-Fi<br>AC: Works fully offline using cached route data |

---

### Ì≥ö Child Epic: `LMS-LENDING-SECTION` (NEW)

*Lending Section manages bulk allocation fulfillment to Extension Services and tracks book rotation health*

> **Critical Boundary**: Lending Section OWNS the books. Extension Services BORROWS them temporarily. Books return to Lending after each cycle for condition reassessment.

| Ticket ID | Title | Acceptance Criteria |
|-----------|-------|---------------------|
| **LMS-851** | Fulfill bulk allocation requests from Extension Services (NEW) | AC: "Pending Requests" tab shows Extension bulk requests with: school, cycle, quantity, subjects<br>AC: Select books from available Lending collection to fulfill<br>AC: Fulfilled books change status to "On Loan to Extension Services" with cycle metadata<br>AC: Fulfilled books marked unavailable for regular circulation<br>AC: Lending staff CANNOT access Extension Services workflows (boundary enforced) |
| **LMS-852** | Implement rotation tracking and return workflow (NEW) | AC: Condition reassessment triggers when books return from Extension cycle<br>AC: Book status changes from "On Loan to Extension Services" back to "Available"<br>AC: Track: cycle history, number of rotations, cumulative condition changes<br>AC: Overdue returns (past August 31 hard stop) trigger escalation alerts |
| **LMS-853** | Build collection health monitoring for Extension-loaned books (NEW) | AC: Book record shows rotation history: cycles served, destinations, condition at each return<br>AC: Cumulative Extension degradation tracked separately from regular circulation<br>AC: System recommends withdrawal when condition drops below threshold after Extension use |
| **LMS-860** | Implement cross-department book status tracking (NEW) | AC: Book record updates: `status: "on_loan_to_extension"` with `extensionLoan` object<br>AC: `extensionLoan` includes: department, cycle code, allocated date, due return, staff ID<br>AC: Lending section never shows allocated books as available<br>AC: Works offline with sync on reconnect |

---

### Ì±ß Child Epic: `LMS-CHILDRENS-SECTION`

*Grade-specific batch management with degradation enforcement*

| Ticket ID | Title | Acceptance Criteria |
|-----------|-------|---------------------|
| **LMS-601** | Implement GES-aligned batch promotion workflow | AC: August 15 auto-promotion for batches with >80% attendance<br>AC: Learners with <70% attendance moved to repeat batch (`GRADE-5B`)<br>AC: SMS notifications in Twi/English sent to all parents<br>AC: Zero data loss verified across 50-learner promotion test |
| **LMS-602** | Build degradation threshold enforcement engine | AC: Green zone (‚â§0.15): Normal issuance<br>AC: Yellow zone (0.16-0.29): Warning message "Handle with care"<br>AC: Red zone (0.30-0.44): Staff override required with 10-char reason<br>AC: Critical zone (‚â•0.45): Block issuance + auto-schedule coaching workshop |
| **LMS-603** | Implement "Teleporter" detection with oral tradition context | AC: Flags patrons with 3+ pristine returns after >7 days checkout<br>AC: Context-aware: Does NOT flag if staff notes contain "read aloud" or "sibling"<br>AC: Low-confidence flags shown as "Teleporter Watch" not "Teleporter"<br>AC: Never blocks issuance for Teleporter category (avoids stigmatizing Ghanaian households) |

---

### Ì±®‚ÄçÌ≤º Child Epic: `LMS-STAFF-GOVERNANCE`

*Department hierarchy with Ghana Card ID verification ‚Äì updated for Extension Services as peer department*

| Ticket ID | Title | Acceptance Criteria |
|-----------|-------|---------------------|
| **LMS-701** | Implement staff profile management with Ghana Card ID hashing | AC: Staff form requires Ghana Card ID format `GHA-000000000-0`<br>AC: Hashing occurs before storage; masked display `GHA-123***89-0`<br>AC: Prevents duplicate IDs across staff records<br>AC: Requires supervisor assignment before activation |
| **LMS-702** | Build role switcher for Manager version single-device operation (UPDATED) | AC: Dropdown includes: System Admin, Acquisitions, Processing, Distribution, Library Operations (Children's/Adult/Reference/Lending), **Extension Services**<br>AC: Extension Services role shows ONLY Extension workflows (bulk requests, rotation, schedule)<br>AC: Lending role shows "Bulk Requests" tab alongside regular lending workflows<br>AC: Data isolation enforced per department security objects<br>AC: Works offline with no permission checks requiring network |
| **LMS-703** | Configure Extension Services staff profiles with route certification (NEW) | AC: Department field: "extension_services" (NOT a section code)<br>AC: Route certification: Tamale-Bolgatanga corridor or other regions<br>AC: Bulk request authority level configurable<br>AC: Rotation cycle access permissions per staff member<br>AC: Extension staff CANNOT access library section workflows |

---

### Ì∫Ä NEXT ACTIONS (Pilot Launch Priorities)

| Epic | Ticket ID | Title | Acceptance Criteria |
|------|-----------|-------|---------------------|
| **LMS-BATTERY** | LMS-NA-001 | Implement power outage resilience validation | AC: 24-hour simulated outage with zero data loss for transactions >30s old<br>AC: Tested on 3 Ghana-spec Windows 10 devices (4GB RAM)<br>AC: Recovery time <10 seconds after restart |
| **LMS-BATTERY** | LMS-NA-002 | Profile battery drain during circulation workflows | AC: Core circulation workflow ‚â§2.5% drain/hour on Intel Celeron devices<br>AC: Documented results for Ghana Library Authority review<br>AC: Optimization recommendations for rural libraries with solar power |
| **LMS-LOCALIZATION** | LMS-NA-003 | Translate critical screens to Twi/Dagbani | AC: Checkout screen, batch management, degradation alerts in Twi<br>AC: Extension Services Android app in Twi/Dagbani<br>AC: Translations validated by University of Ghana + UDS linguists<br>AC: Zero grammatical errors per validation report |
| **LMS-LOCALIZATION** | LMS-NA-004 | Implement language toggle in Settings | AC: Persistent selection across app restarts<br>AC: Reloads UI immediately on change<br>AC: Default to device language with Ghana fallback (English)<br>AC: Android app supports English/Twi/Dagbani toggle |
| **LMS-SAFETY-NET** | LMS-NA-005 | Build anonymized patron presence heartbeat | AC: Broadcasts "active" status every 60 seconds while app foregrounded<br>AC: Aggregates counts within 500m radius for "X nearby readers" display<br>AC: Privacy-preserving: No coordinates shared; only count + batch code |
| **LMS-SAFETY-NET** | LMS-NA-006 | Create QA tooling for patron intelligence simulation | AC: Dev menu to simulate degradation rates (0.05 to 0.50)<br>AC: Verify reader categories assigned correctly per algorithm<br>AC: Test low-presence fallback copy ("Emergency responders alerted") |
| **LMS-EXT-PILOT** | LMS-NA-007 | Validate Extension Services bulk allocation end-to-end (NEW) | AC: Simulate full cycle: bulk request ‚Üí Lending fulfillment ‚Üí Distribution delivery ‚Üí Extension rotation ‚Üí return<br>AC: Zero books stranded; 100% requests fulfilled within 48 hours<br>AC: Department boundary verified (Extension cannot access library sections)<br>AC: Tamale-Bolgatanga corridor field test with community leaders |

---

## Ì≥ä SPRINT PLANNING RECOMMENDATIONS

| Sprint | Focus Area | Key Deliverables | Success Metrics |
|--------|------------|------------------|-----------------|
| **Sprint 1** | Core Infrastructure | LMS-101, LMS-102, LMS-103 | Zero data loss after 24h simulated outage |
| **Sprint 2** | Acquisitions + Ghana Compliance | LMS-201, LMS-202, LMS-301, LMS-302 | 247 curriculum tags load offline in <2s |
| **Sprint 3** | Processing + Extension Routing | LMS-401, LMS-402, LMS-403, LMS-404 | Mold risk ‚â•90% accuracy; Extension routing populates conditional fields |
| **Sprint 4** | Distribution + Extension Depot | LMS-501, LMS-502, LMS-503, LMS-504 | Packing slips <10s offline; depot routing includes rotation metadata |
| **Sprint 5** | Children's Section + Degradation | LMS-601, LMS-602, LMS-603 | Batch promotion 100% accurate; degradation ‚â•90% accuracy |
| **Sprint 6** | Staff + Lending Section | LMS-701, LMS-702, LMS-703, LMS-851, LMS-852, LMS-860 | Role switching includes Extension; bulk allocation workflow tested |
| **Sprint 7** | Extension Services Department | LMS-105, LMS-801, LMS-802, LMS-803, LMS-812, LMS-813 | Department boundary enforced; rotation cycles aligned with GES |
| **Sprint 8** | Android App + Pilot Prep | LMS-804, LMS-805, LMS-810, LMS-811, LMS-NA-001 to LMS-NA-007 | Android processes 100 transactions offline; DPC package complete; pilot ready |

---

## Ìø∑Ô∏è LABELING CONVENTION FOR JIRA

| Label | Purpose | Example |
|-------|---------|---------|
| `ghana-compliance` | Ghana Data Protection Act / GES requirements | LMS-201, LMS-204 |
| `offline-first` | Critical offline capability | LMS-103, LMS-303, LMS-402 |
| `manager` | Manager version only (single library) | LMS-702 |
| `enterprise` | Enterprise version only (multi-branch) | *(Future tickets)* |
| `battery-critical` | Power-sensitive components | LMS-103, LMS-NA-001 |
| `ges-calendar` | Ghana Education Service academic year alignment | LMS-204, LMS-601, LMS-802 |
| `rural-delivery` | Tamale-Bolgatanga corridor adaptations | LMS-502, LMS-504 |
| `extension-services` | Extension Services department workflows | LMS-801, LMS-802, LMS-804 |
| `lending-section` | Lending section bulk allocation | LMS-851, LMS-852, LMS-860 |
| `department-boundary` | Cross-department boundary enforcement | LMS-105, LMS-703, LMS-812 |
| `android-app` | External Android application for Extension | LMS-804, LMS-810, LMS-811 |
| `field-test-required` | Needs real-world validation in Ghana | LMS-602, LMS-NA-003, LMS-NA-007 |

---

## ‚úÖ QUALITY GATES PER SPRINT

| Gate | Criteria | Validation Method |
|------|----------|-------------------|
| **Offline Resilience Gate** | Zero data loss after 24h simulated outage | Jest test with mock power loss + restart |
| **Ghana Compliance Gate** | No plaintext Ghana Card IDs anywhere | Codebase grep + security audit script |
| **Degradation Accuracy Gate** | ‚â•90% match with manual librarian review | 100-book degradation audit with 3 librarians |
| **GES Calendar Gate** | All batches expire August 31; Extension cycles aligned | Date validation across 50 test batches + 4 rotation cycles |
| **Backup Size Gate** | Backups ‚â§10MB for WhatsApp transfer | Automated size validation in CI pipeline |
| **Bulk Allocation Gate** (NEW) | Request ‚Üí fulfillment ‚Üí delivery ‚Üí return with zero stranded books | End-to-end workflow test with 50-book simulated allocation |
| **Department Boundary Gate** (NEW) | Extension staff CANNOT access library sections; Lending staff CANNOT access Extension workflows | Security object audit + role-switching penetration test |
| **Android Offline Gate** (NEW) | 100 transactions processed offline with zero data loss | Field test at Bolgatanga rural school with no internet |

---

## ‚ÑπÔ∏è IMPLEMENTATION NOTES FOR TEAMS

1. **PM Guidance**
   - All tickets include Ghana-specific context in Acceptance Criteria
   - Offline behavior explicitly stated (no "works offline" assumptions)
   - Manager/Enterprise differentiation called out where applicable
   - Extension Services tickets clearly marked (NEW) for sprint planning visibility

2. **Developer Guidance**
   - Technical constraints embedded in AC (e.g., "‚â§500KB", "no API calls")
   - Ghana hardware specs referenced (Windows 10, 4GB RAM)
   - Security requirements non-negotiable (hashing in main process only)
   - Extension Services is a TOP-LEVEL DEPARTMENT ‚Äì separate security objects, distinct `department` field values
   - Book status model: `"available" | "checked_out" | "on_loan_to_extension" | "withdrawn"`

3. **QA Guidance**
   - Success metrics quantifiable (‚â•90%, 100%, ‚â§500KB)
   - Validation methods specified (manual review, automated test)
   - Ghana context included in test scenarios (rainy season, power outage)
   - Department boundary testing: verify Extension staff see ONLY Extension workflows
   - Bulk allocation testing: verify zero double-allocations via concurrent request simulation

4. **Ghana Reality Checks**
   - Power outage duration based on Ghana Statistical Service 2023 data (3.2hr avg)
   - Hardware specs reflect actual devices in Ghana schools (4GB RAM Windows 10)
   - Twi translations validated by University of Ghana linguists (not Google Translate)
   - Dagbani translations validated by University for Development Studies linguists
   - Extension Services reality: 78% of Ghanaian basic schools have library space but lack books (GES 2023 survey)

5. **Extension Services Boundary Rules (CRITICAL)**
   - Extension Services = DEPARTMENT (peer to Library Operations), NOT a library section
   - Books remain owned by Lending Section; Extension has temporary custody
   - Extension learners: minimal profiles (QR ID only, `extension_service: true`), no condition scoring, no degradation tracking
   - Bulk Allocation Flow: Extension request ‚Üí Lending fulfillment ‚Üí Distribution delivery ‚Üí Extension rotation ‚Üí Return to Lending
   - Android app is EXTERNAL tool ‚Äì syncs to main database post-service, not real-time

---

*Document Version: 1.2 (Extension Services Department Update) ‚Ä¢ Prepared for Ghana Library Authority ‚Ä¢ March 2026*
‚úÖ **PM-friendly acceptance criteria** ‚Ä¢ ‚úÖ **Extension Services as peer department** ‚Ä¢ ‚úÖ **Bulk allocation workflow defined** ‚Ä¢ ‚úÖ **Android app specified** ‚Ä¢ ‚úÖ **Ghana context embedded** ‚Ä¢ ‚úÖ **Offline resilience guaranteed**
*Ready for import into Jira with columns: Issue Type, Summary, Description, Labels, Acceptance Criteria*
