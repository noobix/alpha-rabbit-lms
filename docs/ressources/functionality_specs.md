# Library Management System: Workflow & Departmental Functionality Specification

*End-to-end acquisition-to-distribution workflow with role-based access for Manager (standalone) and Enterprise (multi-department) versions*

---

## 📚 Core Workflow Architecture

*Physical book lifecycle from selection to shelf placement*

```mermaid
flowchart TD
    A[Acquisitions Department] -->|Orders placed| B[Processing Department]
    B -->|Cataloged & classified| C[Distribution Department]
    C -->|Routed by classification| D{Library Sections}
    D --> E[Children's Library]
    D --> F[Adult Library]
    D --> G[Reference Section]
    D --> H[Lending Section]
    D --> I[Extension Services]
    D --> J[Digital Library]
    subgraph “External Departments”
        A
        B
        C
    end
    subgraph “Library Sections”
        E
        F
        G
        H
        I
        J
    end
```

---

## 👥 Department Roles & Responsibilities

### 1. Acquisitions Department (External to Library)

| Role | Responsibilities | Key Data Captured | Manager vs Enterprise |
|------|------------------|-------------------|------------------------|
| **Acquisitions Librarian** | • Selects titles based on curriculum needs<br>• Places orders with publishers/vendors<br>• Tracks budget allocation per department<br>• Manages Ghana Card ID for vendor verification | • ISBN/ISSN<br>• Title, author, publisher<br>• Publication year<br>• Ghana Curriculum Tag (e.g., `BASIC-MATH-GRADE-6`)<br>• Vendor details + Ghana Card ID<br>• Budget code (e.g., `CHILDREN-2024-Q1`)<br>• Expected delivery date | **Manager**: Single user handles all acquisitions<br>**Enterprise**: Dedicated role with budget approval workflows |
| **Vendor Coordinator** | • Verifies vendor credentials<br>• Tracks shipment status<br>• Receives physical deliveries<br>• Logs condition on arrival | • Shipment tracking number<br>• Delivery date/time<br>• Condition on arrival (1-5 scale)<br>• Discrepancy notes | **Manager**: Combined with Acquisitions Librarian role<br>**Enterprise**: Separate role with vendor portal access |

### 2. Processing Department (External to Library)

| Role | Responsibilities | Key Data Captured | Manager vs Enterprise |
|------|------------------|-------------------|------------------------|
| **Cataloging Specialist** | • Assigns Dewey Decimal + Ghana Curriculum Tags<br>• Creates MARC21 records (simplified)<br>• Attaches RFID/barcode labels<br>• Records physical attributes | • Dewey Decimal classification<br>• Ghana Curriculum Tag (required)<br>• Barcode/RFID ID<br>• Spine condition (1-5)<br>• Cover condition (1-5)<br>• Page quality (1-5)<br>• Language (English/Twi/Ga) | **Manager**: All cataloging done by single user<br>**Enterprise**: Specialized roles per material type (children's vs academic) |
| **Quality Controller** | • Verifies cataloging accuracy<br>• Inspects physical condition<br>• Flags damaged items for return<br>• Approves books for distribution | • Quality check timestamp<br>• Inspector name/service number<br>• Approval status (approved/returned/repair)<br>• Notes on discrepancies | **Manager**: Optional step (toggle in settings)<br>**Enterprise**: Mandatory approval workflow with audit trail |

### 3. Distribution Department (External to Library)

| Role | Responsibilities | Key Data Captured | Manager vs Enterprise |
|------|------------------|-------------------|------------------------|
| **Distribution Manager** | • Routes books to library sections based on classification<br>• Generates packing slips per section<br>• Coordinates delivery logistics<br>• Tracks section inventory levels | • Destination section (children's/adult/reference/etc.)<br>• Packing slip ID<br>• Delivery date/time<br>• Transport method (internal cart/van)<br>• Section inventory threshold alerts | **Manager**: Manual routing via dropdown selection<br>**Enterprise**: Auto-routing rules + delivery scheduling |
| **Logistics Coordinator** | • Physically transports materials<br>• Confirms delivery receipt<br>• Reports delivery issues | • Delivery confirmation timestamp<br>• Recipient signature (digital)<br>• Condition on delivery notes | **Manager**: Combined with Distribution Manager<br>**Enterprise**: Mobile app for delivery confirmation |

---

## 📖 Library Sections & Their Functions

| Section | Classification Rules | Key Responsibilities | Interaction with Distribution |
|---------|----------------------|----------------------|------------------------------|
| **Children's Library** | • Ghana Curriculum Tags: `KG-*`, `PRIMARY-1` to `PRIMARY-6`<br>• Dewey: 000-099 (General), 398 (Folktales)<br>• Language: Twi/Ga prioritized | • Age-appropriate shelving (low shelves)<br>• Storytime scheduling<br>• Parent/guardian registration<br>• Batch management (Grade 1-6) | Receives packing slips tagged `SECTION:CHILDREN`<br>Confirms receipt via mobile scanner |
| **Adult Library** | • Ghana Curriculum Tags: `JHS-*`, `SHS-*`, `TERTIARY`<br>• Dewey: 100-999 (all subjects)<br>• Language: English primary | • Subject-based shelving<br>• Reading room management<br>• Patron research assistance | Receives packing slips tagged `SECTION:ADULT`<br>Updates shelf location in system |
| **Reference Section** | • Dewey: 030 (Encyclopedias), 300-399 (Social Sciences)<br>• Non-circulating materials<br>• Ghana-specific resources (Constitution, District Maps) | • In-library use only<br>• Photocopy services<br>• Research assistance | Receives packing slips tagged `SECTION:REFERENCE`<br>Flags non-circulating status |
| **Lending Section** | • All circulating materials<br>• High-demand titles<br>• New arrivals display | • Checkout/return processing<br>• Due date management<br>• Overdue notices | Receives packing slips tagged `SECTION:LENDING`<br>Updates availability status |
| **Extension Services** | • Mobile library materials<br>• Community outreach kits<br>• Rural school support | • Route planning<br>• Community schedule management<br>• Damage tracking from field use | Receives packing slips tagged `SECTION:EXTENSION`<br>Logs field usage conditions |
| **Digital Library** | • ISBN with digital format flag<br>• E-book/PDF/Audio formats<br>• DRM status | • Digital access management<br>• Device lending<br>• Usage analytics | Receives digital assets via secure transfer<br>Generates access codes per patron type |

---

## 🔑 User Role Matrix & Permissions

| Role | Acquisitions | Processing | Distribution | Library Sections | Manager Version | Enterprise Version |
|------|--------------|------------|--------------|------------------|-----------------|-------------------|
| **System Admin** | View only | View only | View only | Full access | Single user | District-level oversight |
| **Acquisitions Librarian** | ✅ Full | View only | View only | View only | Combined role | Dedicated department |
| **Cataloging Specialist** | View only | ✅ Full | View only | View only | Combined role | Specialized per material type |
| **Distribution Manager** | View only | View only | ✅ Full | View only | Combined role | Dedicated department |
| **Section Head** | View only | View only | Receive only | ✅ Full for section | Combined role | Department head with analytics |
| **Library Assistant** | ❌ No access | ❌ No access | ❌ No access | ✅ Checkout/checkin only | Single role | Section-specific access |

> 💡 **Critical Design Principle**:
>
> - **Manager Version**: All roles exist within single installation; user switches roles via profile dropdown
> - **Enterprise Version**: Role enforced at database level via CouchDB security objects; users cannot access other departments' data

---

## ⚙️ Functionality Specification by Version

### Manager Version (Standalone Desktop)

| Workflow Stage | Core Functionality | Technical Implementation |
|----------------|-------------------|--------------------------|
| **Acquisitions** | • Manual order entry form<br>• CSV import for bulk orders<br>• Budget tracking (simple ledger)<br>• Vendor list with Ghana Card ID storage | PouchDB documents:<br>`{ type: 'order', vendorGhanaCard: 'hashed', items: [...] }` |
| **Processing** | • Simplified cataloging form<br>• Barcode generation (PDF417)<br>• Health scoring sliders (1-5)<br>• Batch assignment for schools | PouchDB documents:<br>`{ type: 'book', ghanaCurriculumTag: 'BASIC-MATH-GRADE-6', spineCondition: 4, ... }` |
| **Distribution** | • Manual section assignment dropdown<br>• Packing slip PDF generator<br>• Delivery confirmation checkbox | PouchDB documents:<br>`{ type: 'distribution', destinationSection: 'children', packingSlipId: 'PS-2024-001', ... }` |
| **Library Sections** | • Unified interface for all sections<br>• Role switcher in header<br>• Section filter toggle | Single React component with `currentSection` state |

### Enterprise Version (Multi-Department)

| Workflow Stage | Core Functionality | Technical Implementation |
|----------------|-------------------|--------------------------|
| **Acquisitions** | • Budget approval workflows<br>• Vendor portal integration<br>• Automated ISBN lookup<br>• Ghana Education Service curriculum alignment checks | CouchDB design docs:<br>`_design/acquisitions` with validation functions enforcing Ghana Card ID format |
| **Processing** | • MARC21 import/export<br>• Auto-classification via ISBN<br>• Quality control approval chains<br>• RFID batch programming | CouchDB replication filters:<br>`processing-only` filter replicates only `type: 'book'` docs to processing clients |
| **Distribution** | • Auto-routing rules engine<br>• Delivery scheduling calendar<br>• Mobile delivery confirmation app<br>• Section inventory threshold alerts | CouchDB update handlers:<br>Trigger `distribution-ready` event when book status changes to `approved` |
| **Library Sections** | • Department-specific dashboards<br>• Real-time inventory sync<br>• Section head analytics<br>• Mobile scanner integration | CouchDB security objects:<br>`members: { roles: ['children_section'] }` restricts data access |

---

## 🔄 Workflow Data Model (PouchDB/CouchDB Documents)

### Acquisition Order Document

```json
{
  "_id": "order-2024-001",
  "type": "acquisition_order",
  "status": "placed",
  "placedAt": "2024-02-15T08:30:00Z",
  "vendor": {
    "name": "Accra Educational Publishers",
    "ghanaCardId": "GHA-123456789-0", // Stored hashed
    "contactPhone": "+233241234567"
  },
  "items": [
    {
      "isbn": "978-9964-883-15-2",
      "title": "Basic Science for Primary 6",
      "author": "Kofi Mensah",
      "quantity": 50,
      "unitPrice": 15.50,
      "ghanaCurriculumTag": "BASIC-SCIENCE-GRADE-6",
      "targetSection": "children"
    }
  ],
  "budgetCode": "CHILDREN-2024-Q1",
  "totalAmount": 775.00,
  "placedBy": "user:librarian-001"
}
```

### Processed Book Document

```json
{
  "_id": "book-BASIC-SCI-G6-001",
  "type": "processed_book",
  "acquisitionOrderId": "order-2024-001",
  "status": "approved",
  "cataloging": {
    "isbn": "978-9964-883-15-2",
    "title": "Basic Science for Primary 6",
    "author": "Kofi Mensah",
    "deweyDecimal": "500",
    "ghanaCurriculumTag": "BASIC-SCIENCE-GRADE-6",
    "language": "en",
    "barcode": "BASIC-SCI-G6-001"
  },
  "physicalAttributes": {
    "spineCondition": 5,
    "coverCondition": 4,
    "pagesCondition": 5,
    "healthScore": 4.7 // Auto-calculated average
  },
  "classification": {
    "primarySection": "children",
    "ageGroup": "10-12",
    "readingLevel": "grade-6"
  },
  "qualityControl": {
    "inspectedBy": "user:qc-specialist-003",
    "inspectedAt": "2024-02-20T14:22:00Z",
    "approved": true,
    "notes": "Minor cover wear on 3 copies"
  }
}
```

### Distribution Record

```json
{
  "_id": "dist-2024-001",
  "type": "distribution_record",
  "status": "delivered",
  "processedBookIds": [
    "book-BASIC-SCI-G6-001",
    "book-BASIC-SCI-G6-002",
    // ... 48 more
  ],
  "routing": {
    "source": "processing-center-accra",
    "destinationSection": "children",
    "destinationLocation": "St. Peter's School Library",
    "schoolId": "ACCRA-GREATER-001",
    "batchCode": "GRADE-6A"
  },
  "logistics": {
    "packingSlipId": "PS-2024-001",
    "dispatchedAt": "2024-02-22T09:15:00Z",
    "deliveredAt": "2024-02-22T11:45:00Z",
    "deliveredBy": "user:logistics-005",
    "receivedBy": "user:section-head-children-002",
    "conditionOnDelivery": "good"
  }
}
```

---

## 🌍 Ghana-Specific Workflow Adaptations

| Workflow Element | Standard Practice | Ghana Adaptation |
|------------------|-------------------|------------------|
| **Vendor Verification** | Business license check | Ghana Card ID validation + Education Service vendor registry cross-check |
| **Curriculum Tagging** | Dewey Decimal only | Dual classification: Dewey + Ghana Education Service syllabus tags |
| **School Distribution** | Generic "children" section | Batch-aware routing: `GRADE-6A` at St. Peter's ≠ `GRADE-6B` at Presby School |
| **Language Support** | English primary | Twi/Ga language flags for children's materials; section heads can filter by language |
| **Rural Delivery** | Standard courier | Extension Services workflow with mobile library routes (Tamale → Bolgatanga corridor) |
| **Budget Tracking** | Fiscal year | Aligns with Ghana academic calendar (September–August) + Ministry of Education budget cycles |

---

## 🔐 Security & Access Control Implementation

### Manager Version (PouchDB Security)

```javascript
// Role enforcement at application layer
const canAccessSection = (userRole, requestedSection) => {
  if (userRole === 'admin') return true;
  if (userRole === 'librarian') return true; // Combined role has full access
  if (userRole === 'assistant' && requestedSection === currentUserSection) return true;
  return false;
};
// Data isolation via PouchDB query filters
db.createIndex({
  index: { fields: ['type', 'section'] }
});
// Section heads only see their section's books
db.find({
  selector: {
    type: 'processed_book',
    section: currentUserSection // e.g., 'children'
  }
});
```

### Enterprise Version (CouchDB Security Objects)

```json
// Database security for 'books' database
{
  "_id": "_security",
  "admins": {
    "roles": ["admin"],
    "names": ["system-admin"]
  },
  "members": {
    "roles": [
      "acquisitions_dept",
      "processing_dept",
      "distribution_dept",
      "children_section",
      "adult_section",
      "reference_section"
    ]
  }
}
// Design document validation function
{
  "_id": "_design/validation",
  "validate_doc_update": "function(newDoc, oldDoc, userCtx) {
    // Acquisitions can only create order documents
    if (newDoc.type === 'acquisition_order' && !userCtx.roles.includes('acquisitions_dept')) {
      throw { forbidden: 'Acquisitions role required' };
    }
    // Section heads can only update books in their section
    if (newDoc.type === 'processed_book' && newDoc.section !== userCtx.section) {
      throw { forbidden: 'Cannot modify books outside your section' };
    }
    // Ghana Card ID must be hashed before storage
    if (newDoc.vendor?.ghanaCardId && !newDoc.vendor.ghanaCardId.startsWith('hashed:')) {
      throw { forbidden: 'Ghana Card ID must be hashed' };
    }
  }"
}
```

---

## 📊 Departmental Analytics & Reporting

| Department | Key Reports | Manager Version | Enterprise Version |
|------------|-------------|-----------------|-------------------|
| **Acquisitions** | • Budget vs actual spending<br>• Vendor performance (on-time delivery)<br>• Curriculum coverage gaps | Basic CSV export | Real-time dashboards + Ministry of Education compliance reports |
| **Processing** | • Cataloging throughput<br>• Quality rejection rates<br>• Health score distribution | Simple charts | Predictive analytics: "Books likely to need repair in 6 months" |
| **Distribution** | • Delivery timeliness<br>• Section inventory levels<br>• Route efficiency | Manual logs | GPS-tracked deliveries + automated restocking alerts |
| **Children's Section** | • Batch reading progress<br>• Popular titles by grade<br>• Repeat borrowers | Patron history view | Integration with Ghana Education Service literacy metrics |
| **All Sections** | • Collection health report<br>• Withdrawal recommendations<br>• Patron engagement scores | Manual health scoring | AI-assisted withdrawal flags based on spine/cover degradation patterns |

---

## ✅ Implementation Roadmap by Version

### Manager Version (Weeks 1-8)

| Week | Focus Area | Key Deliverables |
|------|------------|------------------|
| 1-2 | Core database setup | PouchDB initialization + document schemas |
| 3-4 | Acquisitions module | Order entry form + vendor management |
| 5-6 | Processing module | Cataloging interface + health scoring |
| 7-8 | Distribution + Sections | Role switcher + section assignment workflow |

### Enterprise Version (Weeks 9-16)

| Week | Focus Area | Key Deliverables |
|------|------------|------------------|
| 9-10 | CouchDB server setup | Security objects + replication filters |
| 11-12 | Department clients | Role-specific UIs + sync engines |
| 13-14 | Workflow automation | Auto-routing rules + approval chains |
| 15-16 | Ghana integration | Curriculum tag database + Twi/Ga localization |

---

## ⚠️ Critical Success Factors for Ghana Deployment

1. **Offline-First Processing**

   - Processing centers often have unstable internet → All cataloging must work offline with sync-on-connect

2. **Ghana Card ID Handling**

   - Never store plaintext Ghana Card IDs → Always hash with salt before storage

3. **Batch-Aware Distribution**

   - School libraries need grade-specific routing → Distribution must preserve batch context (`GRADE-6A` ≠ `GRADE-6B`)

4. **Low-Spec Hardware Support**

   - Processing centers use aging Windows PCs → Manager version must run on 4GB RAM devices

5. **Ministry of Education Alignment**

   - Curriculum tags must match Ghana Education Service syllabus → Quarterly updates via OTA

---

## 📥 Ready-to-Implement Specifications

This document provides:

- ✅ Clear departmental responsibilities with Ghana-specific adaptations

- ✅ Role-based access control patterns for both Manager and Enterprise versions

- ✅ Document schemas ready for PouchDB/CouchDB implementation

- ✅ Workflow automation rules for distribution routing

- ✅ Security patterns compliant with Ghana Data Protection Act

**Next Step**: Begin implementation with Manager version acquisition module using the provided document schema. Enterprise version can be built incrementally by adding CouchDB security objects atop the same data model.
