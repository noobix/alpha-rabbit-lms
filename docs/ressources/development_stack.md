---
Author: Kelvin Kabute
Last-updated: 2026-10-25
---

# Alpha Rabbit LMS — Stack Standard & Dependency Governance (`STACK-STANDARD-01`)

**Status:** Binding for all implementation agents. **Supersedes:** ad-hoc package selection in any ticket. **Companion docs:** `prompt_main.md`, `product_specs.md`, `functionality_specs.md`, `db_engineering.md`, `compression.md`.

**Governance rules for agents**

1. Only packages listed in §2 may be added to `package.json`. Anything else requires a written RFC appended to §6 (Contemporary Gaps) with LTS/community justification.
2. Version policy: **pin the major at scaffold time, caret within the major** (`^major.minor.patch`). No `latest`, no unpinned ranges, no transitive overrides unless a gap entry justifies it.
3. Every dependency must have: an active maintainer or maintainer-org, ≥2 years of release history, and a documented migration path. Built-ins (`node:zlib`, `node:crypto`, `fetch`, `crypto.randomUUID`) always win over packages.
4. The repository pattern (`BaseRepository<T>`) is the **only** place a database/library API may be touched, so any future swap is a one-file change.

---

## 1. Runtime & toolchain baseline

| Layer                       | Standard                                                                                 | Policy / Rationale                                                                                                                                                          |
| --------------------------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| System Node (build/CI only) | **Node 24 LTS**                                                                          | Active LTS at scaffold (Oct 2026); Vite 8-class tooling requires ≥20.19/22.12. Electron ships its own Node — never couple app code to system Node APIs.                     |
| App shell                   | **Electron — always a _supported_ major (last 3 published; ≈ v39 at Oct 2026 scaffold)** | Electron has no LTS; security support = last 3 majors. Schedule a major bump every ~2 quarters in a dedicated sprint. See Gap G2 for the Windows 7 conflict.                |
| Build orchestration         | **electron-vite** (on top of Vite)                                                       | Standardizes main/preload/renderer builds, HMR, and env handling in one maintained tool instead of hand-rolled Vite configs; Vite-team-adjacent ecosystem, large community. |
| Packaging                   | **electron-builder** + **UPX**                                                           | Kept from `product_specs.md`; the only mature cross-platform Electron packager (NSIS/DMG/AppImage).                                                                         |
| Language                    | **TypeScript ^5 (strict)**                                                               | Non-negotiable for the Zod/repository contract style already in `db_engineering.md`.                                                                                        |
| Lint/format                 | **ESLint 9 (flat config) + typescript-eslint + eslint-plugin-react-hooks + Prettier**    | Current maintained line; flat config avoids legacy resolver drift.                                                                                                          |

---

## 2. Approved dependency manifest

### 2.1 Frontend & UI

| Package                                          | Purpose                                           | LTS / community rationale                                                                      | Rejected & why                                                     |
| ------------------------------------------------ | ------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `react`, `react-dom` **^19**                     | UI core                                           | Current maintained line; update `product_specs.md` (says 18).                                  | React 18 — previous line, community has moved on.                  |
| `tailwindcss` **^4** + `@tailwindcss/vite`       | Styling                                           | Current maintained engine; Ghana palette moves to CSS `@theme`.                                | Tailwind 3.4 — legacy config model.                                |
| `@phosphor-icons/react`                          | Icons                                             | Kept from specs; MIT, active, 4,200+ icons incl. library glyphs.                               | Iconoir (smaller set), lucide (no library-specific set advantage). |
| `zustand` **^5**                                 | Client state                                      | Active, tiny, no boilerplate; matches specs.                                                   | Redux Toolkit (boilerplate vs team size).                          |
| `react-hook-form` **^7** + `@hookform/resolvers` | Forms                                             | Maintained, perf-first on low-spec hardware.                                                   | Formik (maintenance slowed).                                       |
| `zod` **^4**                                     | Runtime validation                                | De-facto TS validation standard; already embedded in `db_engineering.md`.                      | yup/io-ts (smaller ecosystem momentum).                            |
| `@tanstack/react-table` **^8**                   | Patron/book/loan grids (sort, filter, pagination) | Headless, maintained, huge community; fits Mango-query paging.                                 | ag-grid (community edition limits), hand-rolled tables.            |
| `@tanstack/react-virtual`                        | Row virtualization for 10k+ grids                 | Same org; mandatory for 4 GB RAM targets (Gap G12).                                            | react-window (maintenance slowed).                                 |
| `recharts`                                       | Analytics/report charts                           | React-native, maintained, largest React charting community.                                    | Chart.js wrapper (imperative bridge).                              |
| `i18next` + `react-i18next`                      | English/Twi/Dagbani/Ga toggle                     | The i18n standard; JSON namespaces suit offline seed bundles and linguist-validated templates. | react-intl (heavier ICU payload for low-spec devices).             |
| `date-fns` **^4**                                | GES calendar, Aug-31 expiry, cycle windows        | Immutable, tree-shakeable, pure functions = deterministic date gates (testable offline).       | moment (legacy), dayjs (plugin mutability quirks in TZ math).      |
| `minisearch`                                     | Offline fuzzy catalog search (title/author)       | Tiny, maintained, pure JS; Mango cannot fuzzy-match (Gap G11).                                 | lunr (maintenance stalled), FlexSearch (API churn).                |

### 2.2 Data layer (PouchDB / CouchDB)

| Package                                                           | Purpose                                                                                    | LTS / community rationale                                                                                                                                               | Rejected & why                                                                                                     |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `pouchdb` **^9** + `pouchdb-find`                                 | Local store + Mango queries                                                                | The only mature CouchDB-replication client; byte-compatible protocol as `db_engineering.md` notes. Risk isolated by repository pattern (§0.4, Gap G3-note).             | RxDB (premium licensing surface), raw `nano` in renderer (no offline).                                             |
| **Adapter: `indexeddb` (built-in Chromium adapter)** — _standard_ | Live store in renderer                                                                     | Zero dependencies, zero native modules (honours the "Zero Native Modules" principle), Chromium-maintained. Call `navigator.storage.persist()` at first launch (Gap G7). | `pouchdb-adapter-node-websql` — depends on **native `sqlite3`**, contradicting the zero-native principle (Gap G1). |
| `sql.js` (WASM SQLite) — _snapshot/export only_                   | Produce the physical `library_data.db`-style SQLite artifact for IT/audit on backup/export | Pure WASM = no native compile; gives Ghana IT a real `.db` file without a native live store.                                                                            | `better-sqlite3` (native, electron-rebuild churn).                                                                 |
| `pouchdb-adapter-memory` (dev)                                    | Tests/fixtures                                                                             | Already in specs; kept.                                                                                                                                                 | —                                                                                                                  |
| `nano`                                                            | CouchDB admin scripts (security objects, design docs, server dumps)                        | Long-standing CouchDB client, active.                                                                                                                                   | `pouchdb` against remote (replication semantics wrong for admin ops).                                              |
| Server: **Apache CouchDB 3.4.x** (Docker `apache/couchdb:3.4`)    | Enterprise sync                                                                            | Current stable 3.x line; update specs (say 3.3). Raspberry Pi 4 supported.                                                                                              | CouchDB 4.x (not stable-GA for production pinning).                                                                |

### 2.3 Backup, compression & scheduling — **the standardized choice**

| Component                      | Standard                                                                                                   | Why this is the CouchDB/PouchDB-ecosystem standard                                                                                                                                                                                                                                                                                           | Rejected & why                                                                                                                 |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Compression codec              | **gzip via Node built-in `node:zlib`** (`createGzip`, level 9 for cloud pass)                              | gzip is _the_ compression convention around CouchDB/PouchDB: community `couchdb-backup` tooling ships `.tar.gz`/`.gz` dumps, CouchDB serves/accepts gzip content-encoding, PouchDB attachment bodies are gzip/deflate-stored, and `db_engineering.md` already streams `createGzip`. Built-in = LTS by definition, zero supply-chain surface. |
| Archive container (multi-file) | **`tar` (node-tar) → `.tar.gz`**                                                                           | Maintained by the **npm org** (among the highest download counts on npm); produces the same `.tar.gz` shape as `couchdb-backup` + `rsync` workflows in `product_specs.md`.                                                                                                                                                                   | **`archiver`** (named in `prompt_main.md`) — slower release cadence, overlaps zlib/tar; superseded by this standard (Gap G10). |
| Backup payload format          | **JSONL.gz** (one doc/line from `db.changes()` since checkpoint) + `.checkpoint_<db>` last_seq file        | Matches `db_engineering.md` `BackupService`; incremental, resumable after power loss, ≤5% size gate testable.                                                                                                                                                                                                                                | Full `db.dump()` snapshots daily (size gate failure).                                                                          |
| Integrity                      | **SHA-256 via `node:crypto`** manifest per backup + verify-on-restore                                      | Built-in; satisfies "checksum audit" gate.                                                                                                                                                                                                                                                                                                   | External hash libs.                                                                                                            |
| Scheduler                      | **`croner`**                                                                                               | Actively maintained, zero-dep, timezone-aware cron; survives the "8 PM daily / Sunday weekly" rules and pause/resume on `powerMonitor`.                                                                                                                                                                                                      | `node-schedule` (used in spec snippet) — maintenance stalled (Gap G10).                                                        |
| Enterprise server backup       | Nightly `_replicate` → local backup DB, then `nano` dump → **tar.gz**, offsite via **rsync** (system tool) | Mirrors `couchdb-backup` conventions without shell-script fragility on Windows-managed sites.                                                                                                                                                                                                                                                | Shell-only `couchdb-backup` (bash dependency on Pi is fine, but not on Windows servers).                                       |
| CouchDB compaction             | Nightly compaction window via `_compact` endpoint + `rsync --inplace` policy                             | Prevents SD-card wear and view/db bloat in term peaks (Gap G13).                                                                                                                                                                                                                                                                            | No compaction → 128 GB SD fills, sync slows.                                                                                  |
| CouchDB backup trigger         | `croner` job on Enterprise server (or Pi) running `nano` dump → `tar.gz` → `rsync`                        | Automated, tested, resumable after power loss.                                                                                                                                                                                                                                                                                              | Manual shell scripts (fragile on Windows servers).                                                                            |
| CouchDB restore                | `nano` restore from latest verified `tar.gz` + client re-sync from server                                 | Point-in-time recovery; clients re-pull from restored server.                                                                                                                                                                                                                                                                               | No documented restore procedure.                                                                                             |                                                                                                                                                                                                                                                                               | No documented restore procedure.                                                                                             |
| Backup verification            | SHA-256 checksum manifest per backup + automated test-restore to staging DB                               | Ensures backup integrity before disaster strikes.                                                                                                                                                                                                                                                                                           | Backups may be corrupt; no verification.                                                                                    |
| Server discovery               | mDNS/Bonjour broadcast on local network + manual URL fallback                                            | Enterprise clients auto-discover CouchDB server without manual configuration.                                                                                                                                                                                                                                                               | Manual `remoteUrl` configuration required.                                                                                   |
| Sync encryption                | TLS/SSL for all CouchDB communication (HTTPS)                                                            | Protects patron data in transit per Act 843.                                                                                                                                                                                                                                                                                                 | `SSL_ENABLED=false` — sync traffic unencrypted.                                                                              |

### 2.4 Cloud storage — **three options, user chooses exactly one at setup**

Unified contract first (satisfies `prompt_main.md` "unified backup interface"):

```ts
interface CloudStorageProvider {
  readonly id: "google-drive" | "backblaze-b2" | "cloudflare-r2";
  testConnection(): Promise<{ ok: boolean; latencyMs: number }>;
  upload(
    file: string,
    remoteKey: string,
    onProgress?: (p: number) => void,
  ): Promise<string>; // returns remote URL/ID
  list(prefix: string): Promise<RemoteObject[]>;
  delete(remoteKey: string): Promise<void>;
}
```

| Option (wizard radio) | Packages                                                    | Rationale                                                                                                                                                                                                      |
| --------------------- | ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Google Drive**      | `google-auth-library` + `@googleapis/drive`                 | Google-maintained generated client + auth lib (OAuth2 refresh flow); slimmer than monolithic `googleapis`. Most familiar to Ghana school IT with existing Google accounts.                                     |
| **Backblaze B2**      | `@aws-sdk/client-s3` + `@aws-sdk/lib-storage`               | B2 is **S3-compatible**; the AWS SDK v3 modular client is the vendor-documented access path and is AWS-maintained with the largest ecosystem. `lib-storage` gives multipart/resumable uploads for flaky links. |
| **Cloudflare R2**     | `@aws-sdk/client-s3` + `@aws-sdk/lib-storage` (R2 endpoint) | Same S3-compatible story; zero egress fees suit slow/limited connections. One SDK covers **two of the three** providers — fewer moving parts long-term.                                                        |

Cross-cutting rules: credentials encrypted with **Electron `safeStorage`** (built-in, OS keychain); every artifact is **AES-256-GCM encrypted (`node:crypto`) before upload** (Gap G3); the wizard persists the choice in the `config` DB and the adapter is resolved from a registry — no provider `if/else` scattered in services.

### 2.5 Documents, barcodes, print (offline)

| Package                          | Purpose                                                            | Rationale                                                                                                                  | Rejected & why                                                        |
| -------------------------------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `pdfkit`                         | Packing slips, barcode labels, reports (PDF generation, streaming) | Actively maintained, stream-based (memory-safe on 4 GB devices), embeds PNG barcodes directly; ≤500 KB gate achievable.    | `pdf-lib` (unmaintained-ish for generation), `jspdf` (plugin sprawl). |
| `bwip-js`                        | **PDF417** + QR generation (pure JS)                               | The JS standard for PDF417 (Ghana Library Authority format `SCI-6M-042[-C2]`) and QR (EXT-QR tags); pure JS, long history. | JsBarcode (no PDF417).                                                |
| `pdfjs-dist` (optional, phase 2) | In-app slip preview                                                | Mozilla-maintained.                                                                                                        | —                                                                     |

### 2.6 Cross-cutting services

| Concern              | Standard                                                                                                                                          | Rationale                                                                                                                                                                      |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| IDs                  | `crypto.randomUUID()` (built-in)                                                                                                                  | Replaces `uuid` package in `db_engineering.md`; zero-dep, spec-compliant.                                                                                                      |
| Logging              | `electron-log`                                                                                                                                    | The maintained Electron logging standard; file rotation + main/renderer bridge; audit log stays in DB (separate concern).                                                      |
| SMS delivery         | **No SDK.** `SmsProvider` interface over built-in `fetch`; adapters: **Hubtel (Ghana)**, **Africa's Talking (pan-Africa)**, **Twilio (fallback)** | Specs name carriers directly, but delivery legally/technically runs through aggregators with registered sender IDs (Gap G4). Interface-first keeps country profiles pluggable. |
| HTTP                 | Built-in `fetch` (Chromium + Node 24)                                                                                                             | No axios/undici dependency needed.                                                                                                                                             |
| App update (phase 2) | `electron-updater`                                                                                                                                | electron-builder ecosystem; data packs (GES tags) use signed JSON manifest + sha256 gate instead (Gap G5).                                                                     |
| Bundle/perf gates    | `size-limit` in CI                                                                                                                                | Enforces the <15 MB bundle and low-spec budgets (Gap G12).                                                                                                                     |

### 2.7 Testing & quality

| Package                  | Purpose                                       | Note                                                                                       |
| ------------------------ | --------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `vitest`                 | Unit/integration                              | Vite-native; **standardizes away the Jest references** in `compression.md` gates (Gap G8). |
| `@playwright/test`       | E2E incl. **Electron** (`_electron` launcher) | Microsoft-maintained; can simulate power-loss restart flows.                               |
| `@testing-library/react` | Component tests                               | Community standard.                                                                        |
| `pouchdb-adapter-memory` | DB fixtures                                   | Kept.                                                                                      |

### 2.8 Security primitives (built-ins only — no packages)

SHA-256+salt hashing (main process IPC only), AES-256-GCM for cloud artifacts, `safeStorage` for credentials/OAuth tokens, `powerMonitor` for outage hooks. Any new crypto package = automatic RFC rejection.

---

## 3. Canonical install (scaffold command — the only sanctioned list)

```bash
# runtime
pnpm add pouchdb pouchdb-find zod zustand react react-dom react-hook-form @hookform/resolvers \
  date-fns i18next react-i18next @tanstack/react-table @tanstack/react-virtual recharts minisearch \
  pdfkit bwip-js tar croner electron-log nano sql.js \
  @aws-sdk/client-s3 @aws-sdk/lib-storage @googleapis/drive google-auth-library @phosphor-icons/react

# dev
pnpm add -D electron electron-builder electron-vite vite typescript tailwindcss @tailwindcss/vite \
  vitest @playwright/test @testing-library/react pouchdb-adapter-memory @types/pouchdb \
  eslint prettier typescript-eslint eslint-plugin-react-hooks size-limit
```

---

## 4. Resolution summary (previously open gaps, now closed)

The following items were identified as gaps or contradictions between this stack standard and companion docs. All are now resolved:

| # | Item | Resolution |
|---|------|------------|
| G1 | "Zero Native Modules" vs `pouchdb-adapter-node-websql` → native `sqlite3` | **Closed.** §2.2 now mandates IndexedDB live store + `sql.js` WASM snapshots. `db_engineering.md` updated to match. |
| G2 | "Works on Windows 7+" vs Electron ≥23 requiring Windows 10+ | **Open decision.** Minimum OS is Windows 10 per §1. Legacy machines require a read-only web fallback (not yet implemented). |
| G3 | Backups uploaded to cloud unencrypted; Act 843 encryption-at-rest | **Closed.** §2.4 mandates AES-256-GCM pre-upload via `node:crypto`; credentials in `safeStorage`. |
| G4 | SMS assumes direct carrier send (Vodafone/MTN/AirtelTigo) | **Closed.** §2.6 mandates `SmsProvider` interface with Hubtel/Africa's Talking/Twilio adapters. |
| G5 | "Quarterly OTA curriculum updates" with no signing/rollback | **Closed.** §2.6 mandates signed manifest (ed25519) + sha256 gate + atomic swap + rollback. |
| G6 | CORE-07 "conflicts preserved" vs CORE-09 "last-write-wins" auto-resolve | **Closed.** LWW only within same-department fields; cross-department docs route to conflict-review UI (LMS-CORE-10, LMS-QUAL-07). |
| G7 | 30-second RPO vs IndexedDB commit/eviction under power loss | **Closed.** `navigator.storage.persist()` at first run; fsync backup artifacts; mock-power-loss gate in CI. |
| G8 | Quality gates say Jest but stack is Vite | **Closed.** §2.7 mandates Vitest. `compression.md` gate wording updated. |
| G9 | React 18 / Tailwind 3.4 in specs vs maintained React 19 / Tailwind 4 | **Closed.** §2.1 mandates React 19 + Tailwind 4 at scaffold. |
| G10 | `archiver` named in `prompt_main.md`; "compression package" vague in tickets | **Closed.** §2.3 is binding: zlib gzip + node-tar only. `prompt_main.md` and `build.md` updated. |
| G11 | No full-text/fuzzy search in specs | **Closed.** §2.1 mandates `minisearch` for offline fuzzy catalog search. |
| G12 | No bundle/memory/CI budgets for 4 GB RAM targets | **Closed.** §2.6 mandates `size-limit` in CI + TanStack virtualization. |
| G13 | Pi 4 CouchDB: no compaction schedule, SD-card wear | **Closed.** §2.3 now mandates nightly compaction window + `rsync --inplace` policy. |
| G14 | `safeStorage` keys tie to OS user; labs share Windows accounts | **Closed.** Setup wizard exports printed/USB recovery key (encrypted blob + passphrase) per institution policy. |
| G15 | CouchDB backup trigger not implemented | **Closed.** §2.3 now mandates `croner` job for automated backup execution. |
| G16 | CouchDB restore procedure missing | **Closed.** §2.3 now documents `nano` restore + client re-sync procedure. |
| G17 | No backup verification/audit for CouchDB | **Closed.** §2.3 now mandates SHA-256 checksum manifest + automated test-restore. |
| G18 | No network discovery for CouchDB server | **Closed.** §2.3 now mandates mDNS/Bonjour broadcast + manual URL fallback. |
| G19 | SSL/TLS disabled for sync traffic | **Closed.** §2.3 now mandates TLS/SSL for all CouchDB communication. `system_specs.md` updated. |
| G20 | Auth credential storage is a stub | **Closed.** `db_engineering.md` now uses Electron `safeStorage` for credential retrieval. |

---

**Adoption:** import this file into the repo as `docs/stack_standard.md`, link it from `prompt_main.md` "Output Rules", and add a CI check that fails on any `package.json` dependency not listed in §2 (a 20-line script against this manifest). That single check is what actually stops on-the-fly picking.
