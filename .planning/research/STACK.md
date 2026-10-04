---
Author: Kelvin Kabute
Last-updated: 2026-10-04
---

# Technology Stack

**Project:** Alpha Rabbit LMS
**Researched:** 2026-10-03

## Recommended Stack

### Core Framework

| Technology         | Version        | Purpose                                                                | Why                                                                          |
| ------------------ | -------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Electron           | current stable | Desktop client for Manager and Enterprise modes                        | Works well for offline-first libraries running on low-power Windows desktops |
| React + TypeScript | current stable | UI layer for forms, dashboards, reports, and mobile-adjacent workflows | Keeps the same codebase for desktop and shared components                    |
| PouchDB            | current stable | Local database in offline mode                                         | Excellent for resilient, local-first record handling                         |
| CouchDB            | current stable | Sync and central server side                                           | Supports multi-branch or multi-department replication                        |

### Database and Storage

| Technology                  | Version          | Purpose                                      | Why                                                               |
| --------------------------- | ---------------- | -------------------------------------------- | ----------------------------------------------------------------- |
| SQLite adapter for PouchDB  | current stable   | Local persistence for desktop installations  | Good fit for unstable power and low-bandwidth environments        |
| CouchDB replication         | current stable   | Multi-site sync and data sharing             | Enables enterprise sync without breaking offline-first operations |
| Object storage / file vault | local filesystem | PDFs, scans, service photos, backup archives | Keeps critical artifacts available offline                        |

### Infrastructure

| Technology                             | Version        | Purpose                                      | Why                                                    |
| -------------------------------------- | -------------- | -------------------------------------------- | ------------------------------------------------------ |
| Local filesystem + incremental backups | current stable | Safe recovery in areas with unreliable power | Critical for daily operational continuity              |
| Optional Android app layer             | current stable | Mobile service and outreach transactions     | Handles field work without forcing a full branch app   |
| SMS / WhatsApp gateway integration     | provider SDK   | Notifications and field coordination         | Common in African market conditions and rural outreach |

### Supporting Libraries

| Library              | Version        | Purpose                                        | When to Use                              |
| -------------------- | -------------- | ---------------------------------------------- | ---------------------------------------- |
| PDF generation       | current stable | Packing slips, receipts, and clearing reports  | For delivery, issue, and return records  |
| QR + barcode tooling | current stable | Book IDs, service IDs, learner IDs             | For high-volume circulation and outreach |
| Validation libraries | current stable | Identity, curriculum, and school policy checks | For country-aware configuration          |
| Crypto library       | current stable | Hashing identity data before persistence       | Required for privacy compliance          |

## Alternatives Considered

| Category             | Recommended         | Alternative              | Why Not                                                                               |
| -------------------- | ------------------- | ------------------------ | ------------------------------------------------------------------------------------- |
| Desktop runtime      | Electron            | Tauri or native desktop  | Electron remains easier to standardize across teams and low-spec Windows environments |
| Local database       | PouchDB             | LevelDB or direct SQLite | PouchDB works better with replication and offline-first syncing                       |
| Mobile field support | Android helper app  | full cross-platform app  | An auxiliary app keeps operational overhead lower while preserving desktop core       |
| Sync model           | CouchDB replication | custom API sync          | CouchDB is proven for resilient conflict handling and local-first patterns            |

## Installation

```bash
# Core
pnpm add electron react react-dom pouchdb pouchdb-adapter-node-websql

# Sync and utilities
pnpm add couchdb-pouchdb-resp-comet # or project-specific sync package
pnpm add uuid crypto-js

# Dev dependencies
pnpm add -D typescript vite electron-builder eslint prettier
```

## Sources

- Project documentation in repo and operational workflow notes
- Offline-first library system patterns from multi-site organizational software architecture
- African mobile outreach and low-bandwidth field service practices
