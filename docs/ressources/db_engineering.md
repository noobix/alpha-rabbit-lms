---
Author: Kelvin Kabute
Last-updated: 2026-10-03
---

# 📚 PouchDB + CouchDB Technical Implementation Guide

_For the Alpha Rabbit LMS (Offline-First Library Management System)_

---

## 🏗️ 1. Architecture Overview

Before diving into code, understand the two deployment modes from `product_specs.md`:

```mermaid
graph TB
    subgraph "Manager Mode (Single Library)"
        A[Electron App] --> B[PouchDB<br/>websql adapter]
        B --> C[SQLite File<br/>library_data.db]
    end

    subgraph "Enterprise Mode (Multi-Department)"
        D[Electron Client 1] --> E[PouchDB Local]
        F[Electron Client 2] --> G[PouchDB Local]
        H[Electron Client N] --> I[PouchDB Local]
        E <-->|Bi-directional Sync| J[CouchDB Server<br/>Central Database]
        G <-->|Bi-directional Sync| J
        I <-->|Bi-directional Sync| J
    end

    style J fill:#006B3F,color:#fff
    style B fill:#FCD116,color:#000
```

**Key Insight:** PouchDB and CouchDB speak the **exact same protocol**. A document written to PouchDB locally is byte-for-byte compatible with CouchDB. This is why replication "just works."

---

## 🧰 2. Toolchain & Libraries

### Core Libraries

| Library                       | Purpose                                                         | Install                                |
| ----------------------------- | --------------------------------------------------------------- | -------------------------------------- |
| `pouchdb`                     | Core database engine                                            | `pnpm add pouchdb`                     |
| `pouchdb-adapter-node-websql` | SQLite-backed adapter for Electron (pure JS, no native modules) | `pnpm add pouchdb-adapter-node-websql` |
| `pouchdb-find`                | Mango query support (like SQL WHERE clauses)                    | `pnpm add pouchdb-find`                |
| `pouchdb-adapter-memory`      | In-memory adapter for testing                                   | `pnpm add -D pouchdb-adapter-memory`   |
| `@types/pouchdb`              | TypeScript definitions                                          | `pnpm add -D @types/pouchdb`           |
| `zod`                         | Runtime schema validation                                       | `pnpm add zod`                         |
| `use-pouchdb`                 | React hooks for PouchDB (optional)                              | `pnpm add use-pouchdb`                 |

### Installation for Alpha Rabbit LMS

```bash
# Core dependencies
pnpm add pouchdb pouchdb-adapter-node-websql pouchdb-find zod

# TypeScript types
pnpm add -D @types/pouchdb

# Optional React integration
pnpm add use-pouchdb
```

### Registering the WebSQL Adapter (Critical for Electron)

```typescript
// src/lib/database/setup.ts
import PouchDB from "pouchdb";
import PouchDBFind from "pouchdb-find";
import websqlAdapter from "pouchdb-adapter-node-websql";

// Register plugins ONCE at app startup
PouchDB.plugin(websqlAdapter);
PouchDB.plugin(PouchDBFind);

export { PouchDB };
```

> ⚠️ **Why WebSQL adapter?** The default PouchDB adapter (LevelDB) uses native modules that break across Electron versions. WebSQL uses SQLite under the hood, is pure JavaScript, and works reliably on Windows 7+ (common in Ghana schools).

---

## 🚀 3. Provisioning & Environment Setup

### Database Initialization Strategy

For the LMS, we use a **single database per logical domain** rather than one giant database. This keeps sync efficient and allows per-department security in Enterprise mode.

```typescript
// src/lib/database/index.ts
import { PouchDB } from "./setup";

export interface DatabaseRegistry {
  books: PouchDB.Database;
  patrons: PouchDB.Database;
  loans: PouchDB.Database;
  extensionLoans: PouchDB.Database;
  departments: PouchDB.Database;
  auditLog: PouchDB.Database;
}

class DatabaseManager {
  private static instance: DatabaseManager;
  private databases: Partial<DatabaseRegistry> = {};
  private remoteUrl: string | null = null;

  private constructor() {}

  static getInstance(): DatabaseManager {
    if (!DatabaseManager.instance) {
      DatabaseManager.instance = new DatabaseManager();
    }
    return DatabaseManager.instance;
  }

  /**
   * Initialize all databases with WebSQL adapter
   * Called once during Electron app startup
   */
  async initialize(
    mode: "manager" | "enterprise",
    remoteUrl?: string,
  ): Promise<void> {
    if (mode === "enterprise" && remoteUrl) {
      this.remoteUrl = remoteUrl;
    }

    const dbNames: (keyof DatabaseRegistry)[] = [
      "books",
      "patrons",
      "loans",
      "extensionLoans",
      "departments",
      "auditLog",
    ];

    for (const name of dbNames) {
      this.databases[name] = new PouchDB(`lms_${name}`, {
        adapter: "websql",
        // WebSQL-specific options
        size: 50, // 50MB max (WebSQL limit on some browsers)
        location: "default",
      });

      // Create indexes for common queries (performance critical)
      await this.createIndexes(name);
    }
  }

  private async createIndexes(dbName: keyof DatabaseRegistry): Promise<void> {
    const db = this.databases[dbName]!;

    switch (dbName) {
      case "books":
        await db.createIndex({ index: { fields: ["type", "status"] } });
        await db.createIndex({ index: { fields: ["type", "department"] } });
        await db.createIndex({ index: { fields: ["type", "barcode"] } });
        break;
      case "patrons":
        await db.createIndex({ index: { fields: ["type", "ghanaCardHash"] } });
        await db.createIndex({ index: { fields: ["type", "patronType"] } });
        break;
      case "loans":
        await db.createIndex({
          index: { fields: ["type", "patronId", "status"] },
        });
        await db.createIndex({ index: { fields: ["type", "dueDate"] } });
        break;
      case "extensionLoans":
        await db.createIndex({ index: { fields: ["type", "cycleCode"] } });
        await db.createIndex({ index: { fields: ["type", "schoolId"] } });
        break;
    }
  }

  get<K extends keyof DatabaseRegistry>(name: K): PouchDB.Database {
    const db = this.databases[name];
    if (!db) throw new Error(`Database ${name} not initialized`);
    return db;
  }

  /**
   * Setup bi-directional sync for Enterprise mode
   */
  setupSync<K extends keyof DatabaseRegistry>(
    dbName: K,
  ): PouchDB.Replication.Sync<{}> {
    if (!this.remoteUrl) {
      throw new Error("Cannot sync in Manager mode");
    }

    const localDb = this.get(dbName);
    const remoteDb = new PouchDB(`${this.remoteUrl}/lms_${dbName}`, {
      skip_setup: true,
      auth: this.getAuthCredentials(),
    });

    return localDb.sync(remoteDb, {
      live: true,
      retry: true,
      batch_size: 50, // Tune for slow Ghana connections
      batches_limit: 3,
    });
  }

  private getAuthCredentials(): { username: string; password: string } {
    // Retrieve from secure Electron store (not shown)
    return { username: "", password: "" };
  }
}

export const dbManager = DatabaseManager.getInstance();
```

### Environment Configuration

```typescript
// src/config/environment.ts
export interface EnvironmentConfig {
  mode: "manager" | "enterprise";
  remoteCouchUrl?: string;
  syncIntervalMs: number;
  backupPath: string;
}

export const config: EnvironmentConfig = {
  mode: process.env.NODE_ENV === "production" ? "manager" : "enterprise",
  remoteCouchUrl: process.env.COUCHDB_URL || "http://localhost:5984",
  syncIntervalMs: 30000, // 30 seconds
  backupPath: process.env.BACKUP_PATH || "C:/GhanaLibraryData/backups",
};
```

---

## 📐 4. Data Modeling & TypeScript Typing

### The CouchDB Document Contract

Every document in PouchDB/CouchDB **must** follow this base shape:

```typescript
// src/types/database.ts

/**
 * Base document - EVERY document in the system extends this
 */
export interface BaseDocument {
  _id: string; // Unique identifier (UUID or custom)
  _rev?: string; // Revision token (managed by PouchDB)
  type: string; // Document discriminator (critical for queries)
  createdAt: string; // ISO 8601 timestamp
  updatedAt: string; // ISO 8601 timestamp
  _syncStatus?: "pending" | "synced" | "conflict" | "error";
  _schemaVersion: number; // For future migrations
  _conflicts?: string[]; // Populated when conflicts exist
}
```

### Domain Models for Alpha Rabbit LMS

```typescript
// src/types/models.ts
import { BaseDocument } from "./database";

// ============ BOOKS ============
export type BookStatus =
  | "available"
  | "on_loan"
  | "on_loan_to_extension"
  | "reserved"
  | "withdrawn"
  | "lost";

export interface Book extends BaseDocument {
  type: "book";
  barcode: string; // e.g., "SCI-6M-042"
  isbn?: string;
  title: string;
  author: string;
  department: "science" | "math" | "literature" | "history" | "general";
  ageGroup: "6-12" | "12-15" | "15-18" | "adult";
  subjectTags: string[]; // e.g., ["BASIC-MATH-GRADE-6", "WASSCE-LIT"]
  condition: {
    spine: number; // 1-5 scale
    cover: number;
    pages: number;
    edges: number;
    overallScore: number; // Weighted average
    lastAssessed: string;
  };
  status: BookStatus;
  location: {
    section: string;
    shelf: string;
  };
  // Extension Services fields (optional)
  extensionServices?: {
    rotationCycle: "CYCLE-1" | "CYCLE-2" | "CYCLE-3" | "CYCLE-4";
    durabilityScore: number; // 1-5, >=3 for Tamale-Bolgatanga
    destinationRegion: string;
  };
  // Rotation tracking
  rotationHistory?: Array<{
    cycleCode: string;
    allocatedDate: string;
    returnDate: string;
    conditionAtReturn: number;
  }>;
}

// ============ PATRONS ============
export interface Patron extends BaseDocument {
  type: "patron";
  patronType: "CHILD" | "ADULT" | "STAFF" | "EXTENSION_LEARNER";
  // Ghana Card - NEVER store plaintext
  ghanaCardHash: string; // SHA-256 hash
  ghanaCardMasked: string; // "GHA-123***89-0"
  fullName: string;
  // Extension learners have minimal profiles
  contact?: {
    phone?: string;
    address?: string;
    communityLeader?: string; // For rural delivery
  };
  membership: {
    joinDate: string;
    expiryDate: string;
    isActive: boolean;
    batchCode?: string; // e.g., "GRADE-4A"
  };
  // Patron intelligence (degradation tracking)
  intelligence?: {
    degradationRate: number; // 0.0 - 0.5
    teleporterWatch: boolean;
    lastActivity: string;
  };
}

// ============ LOANS ============
export interface Loan extends BaseDocument {
  type: "loan";
  patronId: string;
  bookId: string;
  status: "active" | "returned" | "overdue" | "lost";
  checkoutDate: string;
  dueDate: string;
  returnDate?: string;
  issuedBy: string; // Staff ID
  // Extension loan metadata
  extensionLoan?: {
    department: "extension_services";
    cycleCode: string;
    schoolId: string;
    allocatedDate: string;
    dueReturn: string;
    staffId: string;
  };
}

// ============ DEPARTMENTS ============
export interface Department extends BaseDocument {
  type: "department";
  name:
    | "acquisitions"
    | "processing"
    | "distribution"
    | "library_operations"
    | "extension_services"
    | "system_admin";
  securityPrincipal: boolean;
  allowedRoles: string[];
}
```

### Runtime Validation with Zod

PouchDB doesn't enforce schemas. We validate at the **application boundary** using Zod:

```typescript
// src/lib/validation/schemas.ts
import { z } from "zod";

// Ghana Card format: GHA-000000000-0
const ghanaCardRegex = /^GHA-\d{9}-\d$/;

export const bookSchema = z.object({
  _id: z.string().optional(),
  _rev: z.string().optional(),
  type: z.literal("book"),
  barcode: z.string().regex(/^[A-Z]{2,5}-\d+[A-Z]-\d{3}(-C\d)?$/),
  title: z.string().min(1).max(500),
  author: z.string().min(1).max(200),
  department: z.enum(["science", "math", "literature", "history", "general"]),
  ageGroup: z.enum(["6-12", "12-15", "15-18", "adult"]),
  subjectTags: z.array(z.string()),
  condition: z.object({
    spine: z.number().min(1).max(5),
    cover: z.number().min(1).max(5),
    pages: z.number().min(1).max(5),
    edges: z.number().min(1).max(5),
    overallScore: z.number().min(0).max(5),
    lastAssessed: z.string().datetime(),
  }),
  status: z.enum([
    "available",
    "on_loan",
    "on_loan_to_extension",
    "reserved",
    "withdrawn",
    "lost",
  ]),
  location: z.object({
    section: z.string(),
    shelf: z.string(),
  }),
  extensionServices: z
    .object({
      rotationCycle: z.enum(["CYCLE-1", "CYCLE-2", "CYCLE-3", "CYCLE-4"]),
      durabilityScore: z.number().min(1).max(5),
      destinationRegion: z.string(),
    })
    .optional(),
  _schemaVersion: z.number().default(1),
  createdAt: z.string().datetime(),
  updatedAt: z.string().datetime(),
});

export const patronSchema = z.object({
  _id: z.string().optional(),
  type: z.literal("patron"),
  patronType: z.enum(["CHILD", "ADULT", "STAFF", "EXTENSION_LEARNER"]),
  ghanaCardHash: z.string().min(64).max(64), // SHA-256 hex
  ghanaCardMasked: z.string().regex(/^GHA-\d{3}\*\*\*\d{2}-\d$/),
  fullName: z.string().min(1).max(200),
  contact: z
    .object({
      phone: z.string().optional(),
      address: z.string().optional(),
      communityLeader: z.string().optional(),
    })
    .optional(),
  membership: z.object({
    joinDate: z.string().datetime(),
    expiryDate: z.string().datetime(),
    isActive: z.boolean(),
    batchCode: z.string().optional(),
  }),
  _schemaVersion: z.number().default(1),
  createdAt: z.string().datetime(),
  updatedAt: z.string().datetime(),
});

export type BookInput = z.input<typeof bookSchema>;
export type PatronInput = z.input<typeof patronSchema>;
```

### Type-Safe Repository Pattern

```typescript
// src/lib/repositories/base-repository.ts
import type { PouchDB } from "pouchdb-types";
import type { BaseDocument } from "../../types/database";
import { z } from "zod";
import { v4 as uuid } from "uuid";

export abstract class BaseRepository<T extends BaseDocument> {
  protected db: PouchDB.Database;
  protected schema: z.ZodType<T>;
  protected typeName: string;

  constructor(db: PouchDB.Database, schema: z.ZodType<T>, typeName: string) {
    this.db = db;
    this.schema = schema;
    this.typeName = typeName;
  }

  /**
   * Create a new document with auto-generated ID and timestamps
   */
  async create(
    input: Omit<
      T,
      "_id" | "_rev" | "type" | "createdAt" | "updatedAt" | "_schemaVersion"
    >,
  ): Promise<T> {
    const now = new Date().toISOString();
    const doc = {
      ...input,
      _id: uuid(),
      type: this.typeName,
      createdAt: now,
      updatedAt: now,
      _schemaVersion: 1,
      _syncStatus: "pending" as const,
    };

    // Validate before persisting
    const validated = this.schema.parse(doc);
    const result = await this.db.put(validated);

    return { ...validated, _rev: result.rev };
  }

  /**
   * Get a document by ID with type safety
   */
  async getById(id: string): Promise<T | null> {
    try {
      const doc = await this.db.get(id);
      if (doc.type !== this.typeName) return null;
      return doc as T;
    } catch (err: any) {
      if (err.status === 404) return null;
      throw err;
    }
  }

  /**
   * Update a document (requires _rev for optimistic concurrency)
   */
  async update(id: string, updates: Partial<T>): Promise<T> {
    const existing = await this.getById(id);
    if (!existing) throw new Error(`Document ${id} not found`);

    const updated = {
      ...existing,
      ...updates,
      _id: id,
      updatedAt: new Date().toISOString(),
      _syncStatus: "pending" as const,
    };

    const validated = this.schema.parse(updated);
    const result = await this.db.put(validated);

    return { ...validated, _rev: result.rev };
  }

  /**
   * Soft delete (mark as deleted, preserve for audit)
   */
  async softDelete(id: string): Promise<void> {
    const doc = await this.getById(id);
    if (!doc) throw new Error(`Document ${id} not found`);

    await this.db.put({
      ...doc,
      _deleted: true,
      updatedAt: new Date().toISOString(),
    });
  }

  /**
   * Hard delete (use sparingly - breaks audit trails)
   */
  async hardDelete(id: string, rev: string): Promise<void> {
    await this.db.remove(id, rev);
  }

  /**
   * Query using Mango (pouchdb-find)
   */
  async find(
    selector: PouchDB.Find.Selector,
    limit = 100,
    skip = 0,
  ): Promise<T[]> {
    const result = await this.db.find({
      selector: {
        type: this.typeName,
        ...selector,
      },
      limit,
      skip,
    });

    return result.docs as T[];
  }
}
```

```typescript
// src/lib/repositories/book-repository.ts
import { BaseRepository } from "./base-repository";
import { bookSchema, type Book } from "../../types/models";
import type { PouchDB } from "pouchdb-types";

export class BookRepository extends BaseRepository<Book> {
  constructor(db: PouchDB.Database) {
    super(db, bookSchema, "book");
  }

  /**
   * Find books by status (common query)
   */
  async findByStatus(status: Book["status"]): Promise<Book[]> {
    return this.find({ status });
  }

  /**
   * Find books by barcode (unique lookup)
   */
  async findByBarcode(barcode: string): Promise<Book | null> {
    const results = await this.find({ barcode });
    return results[0] || null;
  }

  /**
   * Find books allocated to Extension Services
   */
  async findExtensionBooks(cycleCode?: string): Promise<Book[]> {
    const selector: any = {
      status: "on_loan_to_extension",
    };
    if (cycleCode) {
      selector["extensionServices.rotationCycle"] = cycleCode;
    }
    return this.find(selector);
  }

  /**
   * Bulk create books (for acquisitions)
   */
  async bulkCreate(
    books: Omit<
      Book,
      "_id" | "_rev" | "type" | "createdAt" | "updatedAt" | "_schemaVersion"
    >[],
  ): Promise<Book[]> {
    const now = new Date().toISOString();
    const docs = books.map((book) => ({
      ...book,
      _id: uuid(),
      type: "book" as const,
      createdAt: now,
      updatedAt: now,
      _schemaVersion: 1,
      _syncStatus: "pending" as const,
    }));

    // Validate all before bulk insert
    const validated = docs.map((doc) => this.schema.parse(doc));
    const results = await this.db.bulkDocs(validated);

    return validated.map((doc, i) => ({
      ...doc,
      _rev: results[i].rev,
    }));
  }
}
```

---

## 🔐 5. Securing the Database

### Security Model Overview

```mermaid
graph LR
    subgraph "Manager Mode"
        A[App Code] -->|Validation| B[PouchDB Local]
        B -->|No native security| C[SQLite File]
    end

    subgraph "Enterprise Mode"
        D[App Code] -->|Validation| E[PouchDB Local]
        E <-->|HTTPS| F[CouchDB Server]
        F -->|Document Security| G[Per-Department ACLs]
        F -->|Validation Functions| H[Server-Side Rules]
    end
```

**Critical Insight:** PouchDB has **no security model** — it's a local file. All security is enforced by:

1. **Application-layer validation** (Zod schemas)
2. **CouchDB server-side security** (when syncing)
3. **Electron main process isolation** (for Ghana Card hashing)

### CouchDB Security Configuration

```javascript
// server/scripts/setup-couchdb-security.js
// Run once during Enterprise deployment

const CouchDB = require("nano")("http://admin:GhanaLib2026!@localhost:5984");

async function setupSecurity() {
  // 1. Create per-department databases
  const databases = [
    "lms_books",
    "lms_patrons",
    "lms_loans",
    "lms_extensionLoans",
  ];

  for (const dbName of databases) {
    try {
      await CouchDB.db.create(dbName);
    } catch (err) {
      if (err.statusCode !== 412) throw err; // 412 = already exists
    }

    // 2. Set security object (who can read/write)
    const db = CouchDB.use(dbName);
    await db.security({
      admins: {
        names: ["admin"],
        roles: ["system_admin"],
      },
      members: {
        names: [],
        roles: getRolesForDb(dbName),
      },
    });

    // 3. Add validation function (server-side schema enforcement)
    const designDoc = {
      _id: "_design/validation",
      validate_doc_update: getValidationFunction(dbName),
    };

    try {
      await db.insert(designDoc);
    } catch (err) {
      // Update existing
      const existing = await db.get("_design/validation");
      await db.insert({ ...designDoc, _rev: existing._rev });
    }
  }
}

function getRolesForDb(dbName) {
  const roleMap = {
    lms_books: [
      "acquisitions",
      "processing",
      "distribution",
      "library_operations",
      "extension_services",
    ],
    lms_patrons: ["library_operations", "extension_services"],
    lms_loans: ["library_operations"],
    lms_extensionLoans: ["extension_services", "library_operations"],
  };
  return roleMap[dbName] || [];
}

function getValidationFunction(dbName) {
  // Returns a string containing a JavaScript function
  // CouchDB executes this server-side on every write
  return `function(newDoc, oldDoc, context) {
    // Enforce type field
    if (!newDoc.type) {
      throw({ forbidden: 'Document must have a type field' });
    }

    // Enforce required fields based on type
    if (newDoc.type === 'book') {
      if (!newDoc.barcode || !newDoc.title || !newDoc.author) {
        throw({ forbidden: 'Book requires barcode, title, and author' });
      }
      // Prevent plaintext Ghana Card storage
      if (JSON.stringify(newDoc).includes('GHA-') && !newDoc.ghanaCardMasked) {
        throw({ forbidden: 'Plaintext Ghana Card detected' });
      }
    }

    // Enforce department isolation
    var userRoles = context.roles || [];
    if (newDoc.type === 'book' && newDoc.department) {
      // Extension Services cannot access library section data
      if (userRoles.includes('extension_services') && !newDoc.extensionServices) {
        throw({ unauthorized: 'Extension Services cannot access library section data' });
      }
    }

    // Enforce schema version
    if (!newDoc._schemaVersion) {
      throw({ forbidden: 'Document must have _schemaVersion' });
    }
  }`;
}

setupSecurity().catch(console.error);
```

### Ghana Card Hashing in Electron Main Process

```typescript
// main/hash-service.ts (Electron main process)
import { createHash, randomBytes } from "crypto";
import { ipcMain } from "electron";

const SALT = process.env.GHANA_CARD_SALT || "your-secure-salt-here";

function hashGhanaCard(plainId: string): { hash: string; masked: string } {
  // Validate format first
  if (!/^GHA-\d{9}-\d$/.test(plainId)) {
    throw new Error("Invalid Ghana Card format");
  }

  // SHA-256 with salt
  const hash = createHash("sha256")
    .update(SALT + plainId)
    .digest("hex");

  // Masked display: GHA-123***89-0
  const masked = plainId.replace(/^(GHA-\d{3})\d{4}(\d{2}-\d)$/, "$1***$2");

  return { hash, masked };
}

// Expose to renderer via IPC (never expose hashing to renderer)
ipcMain.handle("hash-ghana-card", (event, plainId: string) => {
  return hashGhanaCard(plainId);
});
```

```typescript
// src/lib/services/ghana-card.ts (Renderer process)
import { ipcRenderer } from "electron";

export async function hashGhanaCard(
  plainId: string,
): Promise<{ hash: string; masked: string }> {
  // Delegate to main process (never do crypto in renderer)
  return ipcRenderer.invoke("hash-ghana-card", plainId);
}
```

---

## 📝 6. CRUD Operations with Real Examples

### Creating a Book (Acquisitions Flow)

```typescript
// src/features/acquisitions/create-book.ts
import { dbManager } from "../../lib/database";
import { BookRepository } from "../../lib/repositories/book-repository";

export async function acquireBook(input: {
  barcode: string;
  title: string;
  author: string;
  department: Book["department"];
  ageGroup: Book["ageGroup"];
  subjectTags: string[];
}) {
  const booksDb = dbManager.get("books");
  const repo = new BookRepository(booksDb);

  // Check for duplicate barcode
  const existing = await repo.findByBarcode(input.barcode);
  if (existing) {
    throw new Error(`Book with barcode ${input.barcode} already exists`);
  }

  // Calculate initial condition score (all 5s for new book)
  const condition = {
    spine: 5,
    cover: 5,
    pages: 5,
    edges: 5,
    overallScore: 5.0,
    lastAssessed: new Date().toISOString(),
  };

  const book = await repo.create({
    ...input,
    condition,
    status: "available",
    location: { section: "pending", shelf: "N/A" },
  });

  // Audit log
  await logAuditEvent("BOOK_CREATED", {
    bookId: book._id,
    barcode: book.barcode,
  });

  return book;
}
```

### Checking Out a Book (Lending Flow)

```typescript
// src/features/lending/checkout-book.ts
import { dbManager } from "../../lib/database";
import { BookRepository } from "../../lib/repositories/book-repository";
import type { Loan, Book } from "../../types/models";

export async function checkoutBook(
  patronId: string,
  bookId: string,
  staffId: string,
) {
  const booksDb = dbManager.get("books");
  const loansDb = dbManager.get("loans");
  const bookRepo = new BookRepository(booksDb);

  // 1. Get book and validate availability
  const book = await bookRepo.getById(bookId);
  if (!book) throw new Error("Book not found");
  if (book.status !== "available") {
    throw new Error(`Book is ${book.status}, cannot checkout`);
  }

  // 2. Check degradation threshold (LMS-602)
  if (book.condition.overallScore < 1.5) {
    throw new Error("Book condition too poor for issuance");
  }
  if (book.condition.overallScore < 2.5) {
    // Yellow zone - warning but allowed
    console.warn("Handle with care: book condition is fair");
  }

  // 3. Create loan record
  const loanRepo = new LoanRepository(loansDb);
  const dueDate = new Date();
  dueDate.setDate(dueDate.getDate() + 14); // 14-day loan

  const loan = await loanRepo.create({
    patronId,
    bookId,
    status: "active",
    checkoutDate: new Date().toISOString(),
    dueDate: dueDate.toISOString(),
    issuedBy: staffId,
  });

  // 4. Update book status (must use _rev for optimistic concurrency)
  await bookRepo.update(bookId, {
    status: "on_loan",
    _rev: book._rev, // Critical: prevents lost updates
  });

  return loan;
}
```

### Bulk Operations (Extension Services Allocation)

```typescript
// src/features/extension/bulk-allocate.ts
import { dbManager } from "../../lib/database";
import { BookRepository } from "../../lib/repositories/book-repository";

export async function allocateBooksToExtension(
  bookIds: string[],
  cycleCode: "CYCLE-1" | "CYCLE-2" | "CYCLE-3" | "CYCLE-4",
  schoolId: string,
  region: string,
) {
  const booksDb = dbManager.get("books");
  const bookRepo = new BookRepository(booksDb);

  // Fetch all books
  const books = await Promise.all(bookIds.map((id) => bookRepo.getById(id)));

  // Validate all are available
  const unavailable = books.filter((b) => b?.status !== "available");
  if (unavailable.length > 0) {
    throw new Error(`${unavailable.length} books are not available`);
  }

  // Enforce durability threshold for Tamale-Bolgatanga corridor (LMS-404)
  if (region === "northern") {
    const lowDurability = books.filter(
      (b) => (b?.extensionServices?.durabilityScore || 3) < 3,
    );
    if (lowDurability.length > 0) {
      throw new Error("Books for Northern Region must have durability >= 3");
    }
  }

  // Bulk update using bulkDocs (single write operation = atomic)
  const updates = books.map((book) => ({
    ...book!,
    status: "on_loan_to_extension" as const,
    extensionServices: {
      rotationCycle: cycleCode,
      durabilityScore: book!.condition.overallScore,
      destinationRegion: region,
    },
    updatedAt: new Date().toISOString(),
    _syncStatus: "pending" as const,
  }));

  const results = await booksDb.bulkDocs(updates);

  // Check for conflicts
  const conflicts = results.filter((r) => r.error);
  if (conflicts.length > 0) {
    throw new Error(`${conflicts.length} books had conflicts during update`);
  }

  return results;
}
```

---

## 🔄 7. Offline Strategy & Conflict Resolution

### Sync Lifecycle Flow

```mermaid
sequenceDiagram
    participant App as Electron App
    participant Pouch as PouchDB (Local)
    participant Sync as Sync Engine
    participant Couch as CouchDB (Server)

    App->>Pouch: Write document
    Pouch-->>App: {_id, _rev}
    Note over Pouch: _syncStatus: 'pending'

    App->>Sync: startSync()
    Sync->>Couch: Check connection
    alt Online
        Sync->>Couch: Push local changes
        Couch-->>Sync: ACK + new _rev
        Sync->>Pouch: Update _syncStatus: 'synced'
        Sync->>Couch: Pull remote changes
        Couch-->>Sync: New/updated docs
        Sync->>Pouch: Apply changes
        alt Conflict detected
            Pouch-->>Sync: Document has _conflicts array
            Sync->>Sync: Run conflict resolver
            Sync->>Pouch: Write resolved document
        end
    else Offline
        Sync->>Sync: Queue changes locally
        Note over Sync: Retry with exponential backoff
    end
```

### Sync Manager Implementation

```typescript
// src/lib/sync/sync-manager.ts
import { dbManager } from "../database";
import type { PouchDB } from "pouchdb-types";

export type SyncState = "idle" | "active" | "paused" | "error" | "offline";

interface SyncHandler {
  onChange: (info: PouchDB.Core.ChangesResponseChange<any>) => void;
  onPaused: (err?: Error) => void;
  onActive: () => void;
  onError: (err: Error) => void;
  onConflict: (docId: string, conflicts: string[]) => void;
}

class SyncManager {
  private syncHandlers: Map<string, PouchDB.Replication.Sync<{}>> = new Map();
  private state: SyncState = "idle";
  private handler: SyncHandler | null = null;

  setHandler(handler: SyncHandler) {
    this.handler = handler;
  }

  /**
   * Start bi-directional sync for a specific database
   */
  startSync(dbName: string): void {
    if (this.syncHandlers.has(dbName)) {
      console.warn(`Sync already active for ${dbName}`);
      return;
    }

    const sync = dbManager.setupSync(dbName as any);

    sync
      .on("change", (info) => {
        this.state = "active";
        this.handler?.onChange(info as any);
      })
      .on("paused", (err) => {
        this.state = err ? "error" : "paused";
        this.handler?.onPaused(err as Error | undefined);
      })
      .on("active", () => {
        this.state = "active";
        this.handler?.onActive();
      })
      .on("error", (err) => {
        this.state = "error";
        this.handler?.onError(err as Error);
      })
      .on("denied", (err) => {
        // User doesn't have permission for this document
        console.error("Sync denied:", err);
      })
      .on("complete", (info) => {
        console.log("Sync complete:", info);
      });

    this.syncHandlers.set(dbName, sync);
  }

  /**
   * Stop sync for a database
   */
  stopSync(dbName: string): void {
    const sync = this.syncHandlers.get(dbName);
    if (sync) {
      sync.cancel();
      this.syncHandlers.delete(dbName);
    }
  }

  /**
   * Stop all sync operations
   */
  stopAll(): void {
    for (const [name, sync] of this.syncHandlers) {
      sync.cancel();
    }
    this.syncHandlers.clear();
    this.state = "idle";
  }

  getState(): SyncState {
    return this.state;
  }
}

export const syncManager = new SyncManager();
```

### Conflict Resolution Strategy

```mermaid
flowchart TD
    A[Conflict Detected<br/>_conflicts array populated] --> B{Is this a<br/>soft delete?}
    B -->|Yes| C[Keep delete<br/>Winner = deleted rev]
    B -->|No| D{Same _schemaVersion?}
    D -->|No| E[Upgrade schema<br/>Apply migration]
    D -->|Yes| F{Auto-mergeable<br/>fields?}
    F -->|Yes| G[Merge non-conflicting<br/>fields]
    F -->|No| H{Last-write-wins<br/>policy applies?}
    H -->|Yes| I[Pick most recent<br/>updatedAt]
    H -->|No| J[Flag for manual<br/>resolution]
    J --> K[Add to conflict<br/>queue UI]
    G --> L[Write resolved doc]
    I --> L
    E --> L
    C --> L
    L --> M[Replicate winner<br/>to other nodes]
```

```typescript
// src/lib/sync/conflict-resolver.ts
import type { BaseDocument } from "../../types/database";

export interface ConflictResolution {
  winner: BaseDocument;
  losers: BaseDocument[];
  strategy: "last-write-wins" | "manual" | "merged";
}

/**
 * Resolve conflicts using last-write-wins strategy
 * (Configured per document type in product_specs.md)
 */
export async function resolveConflict(
  db: PouchDB.Database,
  docId: string,
): Promise<ConflictResolution> {
  // 1. Fetch document with conflicts
  const doc = await db.get(docId, { conflicts: true });

  if (!doc._conflicts || doc._conflicts.length === 0) {
    throw new Error("No conflicts to resolve");
  }

  // 2. Fetch all conflicting revisions
  const revisions = await Promise.all(
    doc._conflicts.map((rev) => db.get(docId, { rev })),
  );

  const allVersions = [doc, ...revisions] as BaseDocument[];

  // 3. Apply resolution strategy
  let winner: BaseDocument;
  let strategy: ConflictResolution["strategy"];

  // Check if one is a deletion
  const deleted = allVersions.find((v) => v._deleted);
  if (deleted) {
    winner = deleted;
    strategy = "last-write-wins";
  } else {
    // Last-write-wins based on updatedAt
    winner = allVersions.reduce((latest, current) => {
      return new Date(current.updatedAt) > new Date(latest.updatedAt)
        ? current
        : latest;
    });
    strategy = "last-write-wins";
  }

  // 4. Remove losing revisions
  const losers = allVersions.filter((v) => v._rev !== winner._rev);
  for (const loser of losers) {
    try {
      await db.remove(loser._id, loser._rev!);
    } catch (err) {
      console.error("Failed to remove losing revision:", err);
    }
  }

  // 5. Clean up _conflicts array from winner
  delete (winner as any)._conflicts;
  await db.put(winner);

  return { winner, losers, strategy };
}

/**
 * Find all documents with conflicts
 */
export async function findConflicts(db: PouchDB.Database): Promise<string[]> {
  const result = await db.allDocs({
    conflicts: true,
    include_docs: true,
  });

  return result.rows
    .filter((row) => row.doc?._conflicts && row.doc._conflicts.length > 0)
    .map((row) => row.id);
}
```

### React Hook for Sync Status

```typescript
// src/hooks/use-sync-status.ts
import { useEffect, useState } from "react";
import { syncManager, type SyncState } from "../lib/sync/sync-manager";

export function useSyncStatus() {
  const [state, setState] = useState<SyncState>(syncManager.getState());
  const [lastSync, setLastSync] = useState<Date | null>(null);
  const [pendingChanges, setPendingChanges] = useState(0);

  useEffect(() => {
    syncManager.setHandler({
      onChange: () => setPendingChanges((p) => p + 1),
      onPaused: () => setState("paused"),
      onActive: () => {
        setState("active");
        setLastSync(new Date());
        setPendingChanges(0);
      },
      onError: () => setState("error"),
      onConflict: () => setState("error"),
    });

    return () => syncManager.stopAll();
  }, []);

  return { state, lastSync, pendingChanges };
}
```

---

## ⚡ 8. Performance Tuning

### Key Performance Strategies

| Strategy              | Implementation                                  | Impact                              |
| --------------------- | ----------------------------------------------- | ----------------------------------- |
| **Indexes**           | `db.createIndex()` on frequently queried fields | 10-100x faster queries              |
| **Batch size tuning** | `batch_size: 50` for slow connections           | Prevents timeouts on Ghana networks |
| **Pagination**        | `skip` + `limit` for large result sets          | Prevents memory exhaustion          |
| **Attachments**       | Store images as attachments, not base64 in docs | Keeps docs small for sync           |
| **View collation**    | Use `startkey`/`endkey` for range queries       | Efficient sorted retrieval          |
| **Change feeds**      | Use `db.changes()` for reactive UI              | Avoids polling                      |

### Index Strategy for LMS

```typescript
// src/lib/database/indexes.ts
import { dbManager } from "./index";

export async function ensureAllIndexes(): Promise<void> {
  const booksDb = dbManager.get("books");

  // Compound index for common query: "available books in science dept"
  await booksDb.createIndex({
    index: {
      fields: ["type", "department", "status"],
      name: "books-dept-status-index",
      ddoc: "books-dept-status-index",
    },
  });

  // Index for overdue loans query
  const loansDb = dbManager.get("loans");
  await loansDb.createIndex({
    index: {
      fields: ["type", "status", "dueDate"],
      name: "loans-overdue-index",
    },
  });

  // Index for Extension Services rotation tracking
  const extDb = dbManager.get("extensionLoans");
  await extDb.createIndex({
    index: {
      fields: ["type", "cycleCode", "schoolId"],
      name: "ext-cycle-school-index",
    },
  });
}
```

### Efficient Querying with Pagination

```typescript
// src/lib/repositories/base-repository.ts (addition)
export async function findPaginated(
  selector: PouchDB.Find.Selector,
  page: number,
  pageSize: number,
): Promise<{ docs: T[]; total: number; hasMore: boolean }> {
  // Get total count first
  const countResult = await this.db.find({
    selector: { type: this.typeName, ...selector },
    fields: ["_id"],
  });

  const total = countResult.docs.length;

  // Get paginated results
  const result = await this.db.find({
    selector: { type: this.typeName, ...selector },
    limit: pageSize,
    skip: page * pageSize,
  });

  return {
    docs: result.docs as T[],
    total,
    hasMore: (page + 1) * pageSize < total,
  };
}
```

### Change Feed for Reactive UI

```typescript
// src/hooks/use-books.ts
import { useEffect, useState } from "react";
import { dbManager } from "../lib/database";
import type { Book } from "../types/models";

export function useBooks(filter?: {
  status?: Book["status"];
  department?: Book["department"];
}) {
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const db = dbManager.get("books");

    // Initial load
    async function load() {
      const selector: any = { type: "book" };
      if (filter?.status) selector.status = filter.status;
      if (filter?.department) selector.department = filter.department;

      const result = await db.find({ selector });
      setBooks(result.docs as Book[]);
      setLoading(false);
    }

    load();

    // Subscribe to changes (reactive updates)
    const changes = db
      .changes({
        since: "now",
        live: true,
        include_docs: true,
        selector: { type: "book" },
      })
      .on("change", (change) => {
        setBooks((prev) => {
          if (change.deleted) {
            return prev.filter((b) => b._id !== change.id);
          }
          const existing = prev.findIndex((b) => b._id === change.id);
          if (existing >= 0) {
            const updated = [...prev];
            updated[existing] = change.doc as Book;
            return updated;
          }
          return [...prev, change.doc as Book];
        });
      });

    return () => changes.cancel();
  }, [filter?.status, filter?.department]);

  return { books, loading };
}
```

### Backup Service (WhatsApp-Compatible)

```typescript
// src/lib/backup/backup-service.ts
import { dbManager } from "../database";
import * as fs from "fs";
import * as path from "path";
import { createGzip } from "zlib";
import { pipeline } from "stream/promises";

export class BackupService {
  private backupPath: string;

  constructor(backupPath: string) {
    this.backupPath = backupPath;
  }

  /**
   * Create incremental backup (only changed docs since last backup)
   * Target: <5% of main DB size (3MB for 60MB DB)
   */
  async createIncrementalBackup(dbName: string): Promise<string> {
    const db = dbManager.get(dbName as any);
    const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
    const backupFile = path.join(
      this.backupPath,
      `lms_${dbName}_${timestamp}.incremental.json.gz`,
    );

    // Get last backup checkpoint
    const checkpointFile = path.join(this.backupPath, `.checkpoint_${dbName}`);
    let since = "0";
    if (fs.existsSync(checkpointFile)) {
      since = fs.readFileSync(checkpointFile, "utf-8");
    }

    // Stream changes since last backup
    const changes = db.changes({
      since,
      include_docs: true,
      live: false,
    });

    const writeStream = fs.createWriteStream(backupFile);
    const gzip = createGzip();

    // Write changes as JSONL (one doc per line)
    changes.on("change", (change) => {
      gzip.write(JSON.stringify(change.doc) + "\n");
    });

    await new Promise<void>((resolve, reject) => {
      changes.on("complete", () => {
        gzip.end();
        resolve();
      });
      changes.on("error", reject);
      pipeline(gzip, writeStream).catch(reject);
    });

    // Save new checkpoint (last_seq)
    fs.writeFileSync(checkpointFile, changes.last_seq.toString());

    // Cleanup old backups (>30 days)
    await this.cleanupOldBackups(30);

    return backupFile;
  }

  /**
   * Compress backup for WhatsApp transfer (<10MB target)
   */
  async compressForWhatsApp(backupFile: string): Promise<string> {
    const whatsappFile = backupFile.replace(".json.gz", ".whatsapp.gz");
    // Additional compression pass if needed
    await pipeline(
      fs.createReadStream(backupFile),
      createGzip({ level: 9 }), // Max compression
      fs.createWriteStream(whatsappFile),
    );
    return whatsappFile;
  }

  private async cleanupOldBackups(retentionDays: number): Promise<void> {
    const files = fs.readdirSync(this.backupPath);
    const cutoff = Date.now() - retentionDays * 24 * 60 * 60 * 1000;

    for (const file of files) {
      const filePath = path.join(this.backupPath, file);
      const stat = fs.statSync(filePath);
      if (stat.mtimeMs < cutoff) {
        fs.unlinkSync(filePath);
      }
    }
  }
}
```

---

## 🎯 9. Common Pitfalls & Best Practices

### ❌ Pitfalls to Avoid

| Pitfall                              | Why It's Bad                     | Solution                                   |
| ------------------------------------ | -------------------------------- | ------------------------------------------ |
| **Storing plaintext Ghana Card**     | Violates Data Protection Act 843 | Hash in main process, store only hash      |
| **Not using `_rev` on updates**      | Lost updates / conflicts         | Always pass `_rev` from last read          |
| **Querying without indexes**         | 10-100x slower on large datasets | `createIndex()` on all query fields        |
| **Syncing huge attachments inline**  | Blocks sync, wastes bandwidth    | Use PouchDB attachments API                |
| **Handling conflicts in renderer**   | Race conditions                  | Resolve in a dedicated service             |
| **Using `db.allDocs()` for queries** | Loads entire DB into memory      | Use `db.find()` with selectors             |
| **Forgetting `_schemaVersion`**      | Impossible to migrate later      | Always include, increment on schema change |

### ✅ Best Practices

1. **Always validate with Zod before writing** — PouchDB has no schema enforcement
2. **Use the `type` field consistently** — It's the foundation of all queries
3. **Treat `_rev` as sacred** — Never modify or discard it
4. **Test offline scenarios** — Use `pouchdb-adapter-memory` for fast tests
5. **Monitor sync state in UI** — Users need to know when data is safe
6. **Keep documents small** — Under 1MB per doc for efficient sync
7. **Use bulk operations** — `bulkDocs()` is atomic and faster than N individual writes
8. **Plan for schema migrations** — Use `_schemaVersion` + migration functions

---

## 📚 10. Recommended Learning Resources

Since YouTube tutorials are sparse, here are the **definitive technical resources**:

| Resource                                                                                               | Type          | Focus                                           |
| ------------------------------------------------------------------------------------------------------ | ------------- | ----------------------------------------------- |
| [PouchDB Official Guide](https://pouchdb.com/guides/)                                                  | Documentation | Core concepts, replication, conflicts           |
| [CouchDB Definitive Guide](https://docs.couchdb.org/en/stable/)                                        | Book          | Server-side security, validation, clustering    |
| [pouchdb-find docs](https://github.com/pouchdb/pouchdb/tree/master/packages/node_modules/pouchdb-find) | README        | Mango queries (SQL-like)                        |
| [Horizontal Systems: PouchDB/CouchDB](https://horizon-systems.gitbook.io/)                             | Guide         | Real-world sync patterns                        |
| [IBM Cloudant Blog](https://cloudant.com/blog/)                                                        | Blog          | Production patterns (Cloudant = hosted CouchDB) |
| [Source: Alpha Rabbit LMS codebase](./src/lib/)                                                        | Code          | Your own implementation as reference            |

---

## 🎓 Teaching Strategy: How to Approach This

```mermaid
graph TD
    A[Week 1: Foundation] --> B[Week 2: CRUD + Types]
    B --> C[Week 3: Sync & Offline]
    C --> D[Week 4: Security & Conflicts]
    D --> E[Week 5: Performance & Polish]

    A --> A1[PouchDB basics<br/>Document model<br/>Adapter setup]
    B --> B1[Repository pattern<br/>Zod validation<br/>TypeScript types]
    C --> C1[Replication<br/>Sync events<br/>Offline detection]
    D --> D1[CouchDB security<br/>Conflict resolution<br/>Ghana Card hashing]
    E --> E1[Indexing<br/>Pagination<br/>Backup service]
```

**Week-by-week approach:**

1. **Week 1**: Get PouchDB running in Electron with WebSQL adapter. Write/read a simple document.
2. **Week 2**: Build the repository pattern with Zod. Implement Book and Patron CRUD.
3. **Week 3**: Add CouchDB server, configure sync, handle online/offline transitions.
4. **Week 4**: Lock down security, implement conflict resolution, hash Ghana Cards properly.
5. **Week 5**: Add indexes, pagination, backup service, and performance monitoring.

This gives you a working offline-first LMS that meets all the requirements in `product_specs.md` and `compression.md`, ready for the Ghana pilot.
