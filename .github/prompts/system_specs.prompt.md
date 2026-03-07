# Library Management System: Manager vs Enterprise – Setup Comparison

_Clear differentiation of requirements, packages, and environments for both versions_

---

## 📊 QUICK COMPARISON TABLE

| Feature | **Manager Version** (Standalone) | **Enterprise Version** (Multi-Department) |

|---------|----------------------------------|-------------------------------------------|

| **Target Users** | Single library (school/community) | University/district with multiple departments |

| **Architecture** | Single Electron app with embedded database | Client-server: Electron clients + CouchDB server |

| **Database** | PouchDB (SQLite file embedded in app) | CouchDB server + PouchDB clients (sync-enabled) |

| **Hardware Required** | Any Windows/macOS/Linux PC | Server (Raspberry Pi 4+) + client devices |

| **Internet Required** | No (100% offline) | Optional (syncs when available) |

| **Installation Complexity** | Simple (single installer) | Moderate (server setup + client installs) |

| **Cost** | $0 (free software) | ~$50 (Raspberry Pi server) |

| **Best For** | Rural schools, community libraries, mobile libraries | Universities, district offices, national archives |

---

## 📦 MANAGER VERSION: Standalone Desktop Setup

### System Requirements

#### Hardware

| Component | Minimum | Recommended |

|-----------|---------|-------------|

| **OS** | Windows 7 / macOS 10.13 / Linux | Windows 10 / macOS 12 / Ubuntu 20.04 |

| **CPU** | Intel Celeron / AMD A4 | Intel i3 / AMD Ryzen 3 |

| **RAM** | 2 GB | 4 GB |

| **Storage** | 100 MB free space | 500 MB free space |

| **Display** | 1024×768 | 1366×768 or higher |

#### Software Dependencies

| Component | Version | Purpose |

|-----------|---------|---------|

| **Node.js** | 18.x or higher | JavaScript runtime |

| **pnpm** | 8.x or higher | Package manager |

| **Electron** | 28.x or higher | Desktop runtime |

| **SQLite** | Built-in via PouchDB | Embedded database engine |

---

### Required Packages (`package.json`)

```json
{
  "name": "library-manager",

  "version": "1.0.0",

  "main": "src/main/index.js",

  "scripts": {
    "dev": "vite",

    "build": "tsc && vite build",

    "build:win": "electron-builder --win",

    "build:mac": "electron-builder --mac",

    "build:linux": "electron-builder --linux"
  },

  "dependencies": {
    "react": "^18.2.0",

    "react-dom": "^18.2.0",

    "react-router-dom": "^6.21.0",

    "pouchdb": "^8.0.1",

    "pouchdb-adapter-node-websql": "^7.3.1",

    "zustand": "^4.4.7",

    "react-hook-form": "^7.49.3",

    "zod": "^3.22.4",

    "date-fns": "^3.0.6",

    "phosphor-react": "^1.4.1",

    "@headlessui/react": "^1.7.17",

    "file-saver": "^2.0.5",

    "jszip": "^3.10.1"
  },

  "devDependencies": {
    "@types/react": "^18.2.47",

    "@types/react-dom": "^18.2.18",

    "@vitejs/plugin-react": "^4.2.1",

    "vite": "^5.0.11",

    "typescript": "^5.3.3",

    "tailwindcss": "^3.4.1",

    "postcss": "^8.4.33",

    "autoprefixer": "^10.4.16",

    "electron": "^28.1.0",

    "electron-builder": "^24.9.1",

    "electron-rebuild": "^3.2.13"
  }
}
```

---

### Installation Steps

#### 1. Clone & Install Dependencies

```bash

# Clone repository

git clone https://github.com/your-org/library-manager.git

cd library-manager



# Install dependencies

pnpm install



# Install Tailwind CSS

npx tailwindcss init -p

```

#### 2. Configure Tailwind (`tailwind.config.js`)

```javascript
/** @type {import('tailwindcss').Config} */

export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],

  theme: {
    extend: {
      colors: {
        ghanaGreen: "#006B3F",

        ghanaGold: "#FCD116",

        ghanaRed: "#CE1126",
      },
    },
  },

  plugins: [],
};
```

#### 3. Build & Package

```bash

# Development mode

pnpm dev



# Build for production

pnpm build



# Package for Windows

pnpm build:win



# Package for macOS

pnpm build:mac



# Package for Linux

pnpm build:linux

```

#### 4. Install on Target Machine

- **Windows**: Run `library-manager-setup.exe`

- **macOS**: Drag `Library Manager.app` to Applications folder

- **Linux**: Install `.AppImage` or `.deb` package

---

### Environment Configuration (`.env`)

```env

# Application Settings

APP_NAME="Library Manager"

APP_VERSION="1.0.0"

ENVIRONMENT="production"



# Database Settings (PouchDB)

DB_NAME="library_data"

DB_ADAPTER="websql"

DB_LOCATION="./data/library_data.db"



# Backup Settings

BACKUP_PATH="./backups"

BACKUP_INTERVAL="daily"  # daily, weekly

BACKUP_RETENTION_DAYS=30



# UI Settings

THEME="light"  # light, dark, auto

LANGUAGE="en"  # en, tw, ga

```

---

### Data Storage Structure

```text

Library Manager Installation/

├── library-manager.exe (or .app / .AppImage)

├── data/

│   └── library_data.db  ← SQLite database file (PouchDB)

├── backups/

│   ├── library_20240212_1430.incremental

│   ├── library_20240213_1430.incremental

│   └── library_20240214_1430.full

├── config/

│   └── settings.json

└── logs/

    └── app.log

```

---

## 🌍 ENTERPRISE VERSION: Multi-Department Setup

### Enterprise System Requirements

#### Server Hardware (Central Database)

| Component | Minimum | Recommended |

|-----------|---------|-------------|

| **OS** | Ubuntu Server 20.04 | Ubuntu Server 22.04 |

| **CPU** | ARM Cortex-A72 (Raspberry Pi 4) | Intel i3 / AMD Ryzen 3 |

| **RAM** | 2 GB | 4 GB |

| **Storage** | 32 GB SD card | 128 GB SSD |

| **Network** | Ethernet/WiFi | Gigabit Ethernet |

| **Power** | Standard USB-C | UPS backup recommended |

#### Client Hardware (Library Workstations)

| Component | Minimum | Recommended |

|-----------|---------|-------------|

| **OS** | Windows 7 / macOS 10.13 / Linux | Windows 10 / macOS 12 / Ubuntu 20.04 |

| **CPU** | Intel Celeron / AMD A4 | Intel i3 / AMD Ryzen 3 |

| **RAM** | 2 GB | 4 GB |

| **Storage** | 100 MB free space | 500 MB free space |

| **Network** | WiFi or Ethernet | Gigabit Ethernet |

---

### Server-Side Packages (`docker-compose.yml`)

```yaml
version: "3.8"

services:
  couchdb:
    image: apache/couchdb:3.3

    container_name: library-couchdb

    ports:
      - "5984:5984"

    volumes:
      - couchdb_data:/opt/couchdb/data

      - ./config/couchdb:/opt/couchdb/etc/local.d

      - ./backups:/backups

    environment:
      - COUCHDB_USER=admin

      - COUCHDB_PASSWORD=${COUCHDB_PASSWORD}

      - NODENAME=couchdb@library-server

    restart: unless-stopped

    networks:
      - library-network

  backup-service:
    image: library-backup:latest

    container_name: library-backup

    volumes:
      - ./backups:/backups

      - /var/run/docker.sock:/var/run/docker.sock

    environment:
      - COUCHDB_URL=http://couchdb:5984

      - BACKUP_INTERVAL=86400 # 24 hours in seconds

      - RETENTION_DAYS=30

    restart: unless-stopped

    networks:
      - library-network

volumes:
  couchdb_data:

networks:
  library-network:
    driver: bridge
```

---

### Client-Side Packages (`package.json`)

```json
{
  "name": "library-enterprise-client",

  "version": "1.0.0",

  "main": "src/main/index.js",

  "scripts": {
    "dev": "vite",

    "build": "tsc && vite build",

    "build:win": "electron-builder --win",

    "build:mac": "electron-builder --mac",

    "build:linux": "electron-builder --linux"
  },

  "dependencies": {
    "react": "^18.2.0",

    "react-dom": "^18.2.0",

    "react-router-dom": "^6.21.0",

    "pouchdb": "^8.0.1",

    "pouchdb-adapter-http": "^8.0.1",

    "pouchdb-replication": "^8.0.1",

    "zustand": "^4.4.7",

    "react-hook-form": "^7.49.3",

    "zod": "^3.22.4",

    "date-fns": "^3.0.6",

    "phosphor-react": "^1.4.1",

    "@headlessui/react": "^1.7.17",

    "file-saver": "^2.0.5",

    "jszip": "^3.10.1",

    "node-schedule": "^2.1.1",

    "axios": "^1.6.5"
  },

  "devDependencies": {
    "@types/react": "^18.2.47",

    "@types/react-dom": "^18.2.18",

    "@vitejs/plugin-react": "^4.2.1",

    "vite": "^5.0.11",

    "typescript": "^5.3.3",

    "tailwindcss": "^3.4.1",

    "postcss": "^8.4.33",

    "autoprefixer": "^10.4.16",

    "electron": "^28.1.0",

    "electron-builder": "^24.9.1",

    "electron-rebuild": "^3.2.13"
  }
}
```

**Key Differences from Manager:**

- `pouchdb-adapter-http` – Connects to remote CouchDB server

- `pouchdb-replication` – Handles sync between client and server

- `node-schedule` – Manages automatic sync intervals

- `axios` – HTTP client for server communication

---

### Server Setup Steps

#### 1. Install Docker & Docker Compose

```bash

# Ubuntu/Debian

sudo apt update

sudo apt install docker.io docker-compose



# Enable Docker service

sudo systemctl enable docker

sudo systemctl start docker



# Add user to docker group

sudo usermod -aG docker $USER

```

#### 2. Create Server Configuration

```bash

# Create project directory

mkdir library-enterprise-server

cd library-enterprise-server



# Create config directory

mkdir -p config/couchdb backups



# Create CouchDB local.ini

cat > config/couchdb/local.ini << EOF

[chttpd]

bind_address = 0.0.0.0

port = 5984



[couchdb]

max_dbs_open = 500



[httpd]

enable_cors = true



[cors]

origins = *

credentials = true

methods = GET, PUT, POST, HEAD, DELETE

headers = accept, authorization, content-type, origin, referer

EOF

```

#### 3. Create Environment File (`.env`)

```env

# CouchDB Configuration

COUCHDB_USER=admin

COUCHDB_PASSWORD=YourSecurePassword123!

COUCHDB_PORT=5984



# Server Configuration

SERVER_HOST=0.0.0.0

SERVER_PORT=5984



# Backup Configuration

BACKUP_PATH=/backups

BACKUP_INTERVAL=86400

RETENTION_DAYS=30



# Security

ADMIN_EMAIL=admin@library.edu.gh

SSL_ENABLED=false

```

#### 4. Deploy Server

```bash

# Start services

docker-compose up -d



# Check status

docker-compose ps



# View logs

docker-compose logs -f couchdb



# Create initial databases

curl -X PUT http://admin:YourSecurePassword123!@localhost:5984/books

curl -X PUT http://admin:YourSecurePassword123!@localhost:5984/patrons

curl -X PUT http://admin:YourSecurePassword123!@localhost:5984/loans

curl -X PUT http://admin:YourSecurePassword123!@localhost:5984/users

```

#### 5. Configure Security & Roles

```bash

# Create admin user in CouchDB

curl -X PUT http://localhost:5984/_users/org.couchdb.user:admin_user \

  -H "Content-Type: application/json" \

  -d '{

    "name": "admin_user",

    "password": "secure_password",

    "roles": ["admin"],

    "type": "user"

  }'



# Set database security

curl -X PUT http://admin:YourSecurePassword123!@localhost:5984/books/_security \

  -H "Content-Type: application/json" \

  -d '{

    "admins": { "roles": ["admin"] },

    "members": { "roles": ["librarian", "science_dept", "children_section"] }

  }'

```

---

### Client Setup Steps

#### 1. Clone & Install Client Dependencies

```bash

# Clone repository

git clone https://github.com/your-org/library-enterprise-client.git

cd library-enterprise-client



# Install dependencies

pnpm install

```

#### 2. Configure Client Environment (`.env`)

```env

# Application Settings

APP_NAME="Library Enterprise Client"

APP_VERSION="1.0.0"

ENVIRONMENT="production"



# Server Connection

SERVER_URL="http://192.168.1.100:5984"  # Replace with your server IP

SYNC_INTERVAL=300  # Sync every 5 minutes (seconds)



# Database Settings (Local PouchDB)

LOCAL_DB_NAME="library_local"

LOCAL_DB_ADAPTER="websql"



# User Settings

DEFAULT_DEPARTMENT="general"

AUTO_SYNC=true

OFFLINE_MODE=false



# Backup Settings

BACKUP_PATH="./backups"

BACKUP_ON_SYNC=true

```

#### 3. Build & Install Client

```bash

# Development mode

pnpm dev



# Build for production

pnpm build



# Package for Windows

pnpm build:win



# Install on workstation

# Windows: Run installer

# macOS: Drag to Applications

# Linux: Install package

```

---

### Environment Configuration Comparison

| Setting | Manager Version | Enterprise Version |

|---------|----------------|-------------------|

| **Database Type** | Embedded SQLite | Remote CouchDB + Local PouchDB |

| **Connection String** | `./data/library_data.db` | `http://server-ip:5984/books` |

| **Sync Mode** | N/A (single device) | Bidirectional replication |

| **Backup Location** | Local folder | Server + Local |

| **User Authentication** | Local accounts | CouchDB `_users` database |

| **Role Management** | Hardcoded in app | CouchDB security objects |

| **Data Isolation** | N/A | Department-based views |

| **Offline Capability** | Full functionality | Limited (local cache only) |

---

## 🔧 DEPLOYMENT WORKFLOWS

### Manager Version Deployment

```mermaid

flowchart TD

    A[Download Installer] --> B[Run Setup]

    B --> C[Choose Installation Path]

    C --> D[Create Data Directory]

    D --> E[Initialize Database]

    E --> F[Launch Application]

    F --> G[Start Using Library Manager]

```

**Steps:**

1. Download installer from release page

2. Run installer (no admin rights required)

3. Choose installation directory (default: `C:\Program Files\Library Manager`)

4. Application creates `data/` folder automatically

5. First launch initializes empty database

6. Ready to use immediately

---

### Enterprise Version Deployment

```mermaid

flowchart TD

    A[Set Up Server] --> B[Install Docker]

    B --> C[Deploy CouchDB]

    C --> D[Configure Security]

    D --> E[Create Databases]

    E --> F[Install Client on Workstations]

    F --> G[Configure Server URL]

    G --> H[Sync Initial Data]

    H --> I[Start Using Enterprise System]

```

**Server Setup (One-Time):**

1. Install Ubuntu Server on Raspberry Pi 4 or dedicated machine

2. Install Docker & Docker Compose

3. Deploy CouchDB using `docker-compose.yml`

4. Configure admin user and security settings

5. Create databases: `books`, `patrons`, `loans`, `users`

6. Set up backup schedule (daily incremental)

**Client Setup (Per Workstation):**

1. Download client installer

2. Run installer on each library workstation

3. Configure server URL during first launch

4. Authenticate with admin credentials

5. Initial sync pulls all data from server

6. Ready to use with offline capability

---

## 📋 PRE-DEPLOYMENT CHECKLIST

### Manager Version Checklist

- [ ] Verify target PC meets minimum requirements

- [ ] Ensure 100 MB free disk space available

- [ ] Test installer on clean Windows/macOS/Linux VM

- [ ] Validate database creation on first launch

- [ ] Confirm backup functionality works

- [ ] Test on low-spec hardware (Celeron, 2GB RAM)

### Enterprise Version Checklist

- [ ] Server hardware meets minimum specs

- [ ] Network connectivity between server and clients

- [ ] Docker installed and running on server

- [ ] CouchDB accessible from client machines

- [ ] Security roles configured correctly

- [ ] Backup system tested and verified

- [ ] Client sync tested on multiple workstations

- [ ] Offline mode validated on client devices

---

## 🔐 SECURITY CONSIDERATIONS

### Manager Version Security

| Aspect | Implementation |

|--------|----------------|

| **Data Encryption** | SQLite file encrypted at rest (optional) |

| **User Authentication** | Local password hashing (bcrypt) |

| **Access Control** | Role-based within single application |

| **Audit Trail** | Local logs stored in `logs/` directory |

| **Backup Security** | Encrypted backup files (optional) |

### Enterprise Version Security

| Aspect | Implementation |

|--------|----------------|

| **Data Encryption** | TLS/SSL for server communication |

| **User Authentication** | CouchDB `_users` database with hashed passwords |

| **Access Control** | Database-level security objects per department |

| **Audit Trail** | Server logs + client sync logs |

| **Backup Security** | Encrypted backups stored on server |

| **Network Security** | Firewall rules, VPN option for remote access |

---

## 💡 RECOMMENDATIONS BY USE CASE

### Choose **Manager Version** if

- ✅ Single library location

- ✅ Limited or no IT support

- ✅ Budget constraints (free solution)

- ✅ Unreliable internet connectivity

- ✅ Small collection (<10,000 items)

- ✅ Rural school or community library

### Choose **Enterprise Version** if

- ✅ Multiple departments or branches

- ✅ Need centralized data management

- ✅ Real-time data sharing between locations

- ✅ Large collection (>10,000 items)

- ✅ University or district-level deployment

- ✅ IT support available for server maintenance

---

## 🚀 NEXT STEPS

### For Manager Version

1. Clone repository: `git clone https://github.com/your-org/library-manager.git`

2. Install dependencies: `pnpm install`

3. Build installer: `pnpm build:win` (or mac/linux)

4. Test on target hardware

5. Deploy to library workstations

### For Enterprise Version

1. Set up server hardware (Raspberry Pi 4 recommended)

2. Install Ubuntu Server + Docker

3. Deploy CouchDB: `docker-compose up -d`

4. Configure security and databases

5. Build client installer: `pnpm build:win`

6. Install client on all workstations

7. Configure server URL on each client

8. Test sync and offline functionality

---

This comparison provides clear, actionable guidance for setting up either version of the Library Management System. The Manager version is ideal for quick deployment with minimal overhead, while the Enterprise version offers scalability and multi-department support for larger institutions.
