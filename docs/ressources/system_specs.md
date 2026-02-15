\# Library Management System: Manager vs Enterprise – Setup Comparison  

\*Clear differentiation of requirements, packages, and environments for both versions\*



---



\## 📊 QUICK COMPARISON TABLE



| Feature | \*\*Manager Version\*\* (Standalone) | \*\*Enterprise Version\*\* (Multi-Department) |

|---------|----------------------------------|-------------------------------------------|

| \*\*Target Users\*\* | Single library (school/community) | University/district with multiple departments |

| \*\*Architecture\*\* | Single Electron app with embedded database | Client-server: Electron clients + CouchDB server |

| \*\*Database\*\* | PouchDB (SQLite file embedded in app) | CouchDB server + PouchDB clients (sync-enabled) |

| \*\*Hardware Required\*\* | Any Windows/macOS/Linux PC | Server (Raspberry Pi 4+) + client devices |

| \*\*Internet Required\*\* | No (100% offline) | Optional (syncs when available) |

| \*\*Installation Complexity\*\* | Simple (single installer) | Moderate (server setup + client installs) |

| \*\*Cost\*\* | $0 (free software) | ~$50 (Raspberry Pi server) |

| \*\*Best For\*\* | Rural schools, community libraries, mobile libraries | Universities, district offices, national archives |



---



\## 📦 MANAGER VERSION: Standalone Desktop Setup



\### System Requirements



\#### Hardware

| Component | Minimum | Recommended |

|-----------|---------|-------------|

| \*\*OS\*\* | Windows 7 / macOS 10.13 / Linux | Windows 10 / macOS 12 / Ubuntu 20.04 |

| \*\*CPU\*\* | Intel Celeron / AMD A4 | Intel i3 / AMD Ryzen 3 |

| \*\*RAM\*\* | 2 GB | 4 GB |

| \*\*Storage\*\* | 100 MB free space | 500 MB free space |

| \*\*Display\*\* | 1024×768 | 1366×768 or higher |



\#### Software Dependencies

| Component | Version | Purpose |

|-----------|---------|---------|

| \*\*Node.js\*\* | 18.x or higher | JavaScript runtime |

| \*\*pnpm\*\* | 8.x or higher | Package manager |

| \*\*Electron\*\* | 28.x or higher | Desktop runtime |

| \*\*SQLite\*\* | Built-in via PouchDB | Embedded database engine |



---



\### Required Packages (`package.json`)



```json

{

&nbsp; "name": "library-manager",

&nbsp; "version": "1.0.0",

&nbsp; "main": "src/main/index.js",

&nbsp; "scripts": {

&nbsp;   "dev": "vite",

&nbsp;   "build": "tsc \&\& vite build",

&nbsp;   "build:win": "electron-builder --win",

&nbsp;   "build:mac": "electron-builder --mac",

&nbsp;   "build:linux": "electron-builder --linux"

&nbsp; },

&nbsp; "dependencies": {

&nbsp;   "react": "^18.2.0",

&nbsp;   "react-dom": "^18.2.0",

&nbsp;   "react-router-dom": "^6.21.0",

&nbsp;   "pouchdb": "^8.0.1",

&nbsp;   "pouchdb-adapter-node-websql": "^7.3.1",

&nbsp;   "zustand": "^4.4.7",

&nbsp;   "react-hook-form": "^7.49.3",

&nbsp;   "zod": "^3.22.4",

&nbsp;   "date-fns": "^3.0.6",

&nbsp;   "phosphor-react": "^1.4.1",

&nbsp;   "@headlessui/react": "^1.7.17",

&nbsp;   "file-saver": "^2.0.5",

&nbsp;   "jszip": "^3.10.1"

&nbsp; },

&nbsp; "devDependencies": {

&nbsp;   "@types/react": "^18.2.47",

&nbsp;   "@types/react-dom": "^18.2.18",

&nbsp;   "@vitejs/plugin-react": "^4.2.1",

&nbsp;   "vite": "^5.0.11",

&nbsp;   "typescript": "^5.3.3",

&nbsp;   "tailwindcss": "^3.4.1",

&nbsp;   "postcss": "^8.4.33",

&nbsp;   "autoprefixer": "^10.4.16",

&nbsp;   "electron": "^28.1.0",

&nbsp;   "electron-builder": "^24.9.1",

&nbsp;   "electron-rebuild": "^3.2.13"

&nbsp; }

}

```



---



\### Installation Steps



\#### 1. Clone \& Install Dependencies

```bash

\# Clone repository

git clone https://github.com/your-org/library-manager.git

cd library-manager



\# Install dependencies

pnpm install



\# Install Tailwind CSS

npx tailwindcss init -p

```



\#### 2. Configure Tailwind (`tailwind.config.js`)

```javascript

/\*\* @type {import('tailwindcss').Config} \*/

export default {

&nbsp; content: \[

&nbsp;   "./index.html",

&nbsp;   "./src/\*\*/\*.{js,ts,jsx,tsx}",

&nbsp; ],

&nbsp; theme: {

&nbsp;   extend: {

&nbsp;     colors: {

&nbsp;       ghanaGreen: '#006B3F',

&nbsp;       ghanaGold: '#FCD116',

&nbsp;       ghanaRed: '#CE1126'

&nbsp;     }

&nbsp;   },

&nbsp; },

&nbsp; plugins: \[],

}

```



\#### 3. Build \& Package

```bash

\# Development mode

pnpm dev



\# Build for production

pnpm build



\# Package for Windows

pnpm build:win



\# Package for macOS

pnpm build:mac



\# Package for Linux

pnpm build:linux

```



\#### 4. Install on Target Machine

\- \*\*Windows\*\*: Run `library-manager-setup.exe`

\- \*\*macOS\*\*: Drag `Library Manager.app` to Applications folder

\- \*\*Linux\*\*: Install `.AppImage` or `.deb` package



---



\### Environment Configuration (`.env`)



```env

\# Application Settings

APP\_NAME="Library Manager"

APP\_VERSION="1.0.0"

ENVIRONMENT="production"



\# Database Settings (PouchDB)

DB\_NAME="library\_data"

DB\_ADAPTER="websql"

DB\_LOCATION="./data/library\_data.db"



\# Backup Settings

BACKUP\_PATH="./backups"

BACKUP\_INTERVAL="daily"  # daily, weekly

BACKUP\_RETENTION\_DAYS=30



\# UI Settings

THEME="light"  # light, dark, auto

LANGUAGE="en"  # en, tw, ga

```



---



\### Data Storage Structure



```

Library Manager Installation/

├── library-manager.exe (or .app / .AppImage)

├── data/

│   └── library\_data.db  ← SQLite database file (PouchDB)

├── backups/

│   ├── library\_20240212\_1430.incremental

│   ├── library\_20240213\_1430.incremental

│   └── library\_20240214\_1430.full

├── config/

│   └── settings.json

└── logs/

&nbsp;   └── app.log

```



---



\## 🌍 ENTERPRISE VERSION: Multi-Department Setup



\### System Requirements



\#### Server Hardware (Central Database)

| Component | Minimum | Recommended |

|-----------|---------|-------------|

| \*\*OS\*\* | Ubuntu Server 20.04 | Ubuntu Server 22.04 |

| \*\*CPU\*\* | ARM Cortex-A72 (Raspberry Pi 4) | Intel i3 / AMD Ryzen 3 |

| \*\*RAM\*\* | 2 GB | 4 GB |

| \*\*Storage\*\* | 32 GB SD card | 128 GB SSD |

| \*\*Network\*\* | Ethernet/WiFi | Gigabit Ethernet |

| \*\*Power\*\* | Standard USB-C | UPS backup recommended |



\#### Client Hardware (Library Workstations)

| Component | Minimum | Recommended |

|-----------|---------|-------------|

| \*\*OS\*\* | Windows 7 / macOS 10.13 / Linux | Windows 10 / macOS 12 / Ubuntu 20.04 |

| \*\*CPU\*\* | Intel Celeron / AMD A4 | Intel i3 / AMD Ryzen 3 |

| \*\*RAM\*\* | 2 GB | 4 GB |

| \*\*Storage\*\* | 100 MB free space | 500 MB free space |

| \*\*Network\*\* | WiFi or Ethernet | Gigabit Ethernet |



---



\### Server-Side Packages (`docker-compose.yml`)



```yaml

version: '3.8'



services:

&nbsp; couchdb:

&nbsp;   image: apache/couchdb:3.3

&nbsp;   container\_name: library-couchdb

&nbsp;   ports:

&nbsp;     - "5984:5984"

&nbsp;   volumes:

&nbsp;     - couchdb\_data:/opt/couchdb/data

&nbsp;     - ./config/couchdb:/opt/couchdb/etc/local.d

&nbsp;     - ./backups:/backups

&nbsp;   environment:

&nbsp;     - COUCHDB\_USER=admin

&nbsp;     - COUCHDB\_PASSWORD=${COUCHDB\_PASSWORD}

&nbsp;     - NODENAME=couchdb@library-server

&nbsp;   restart: unless-stopped

&nbsp;   networks:

&nbsp;     - library-network



&nbsp; backup-service:

&nbsp;   image: library-backup:latest

&nbsp;   container\_name: library-backup

&nbsp;   volumes:

&nbsp;     - ./backups:/backups

&nbsp;     - /var/run/docker.sock:/var/run/docker.sock

&nbsp;   environment:

&nbsp;     - COUCHDB\_URL=http://couchdb:5984

&nbsp;     - BACKUP\_INTERVAL=86400  # 24 hours in seconds

&nbsp;     - RETENTION\_DAYS=30

&nbsp;   restart: unless-stopped

&nbsp;   networks:

&nbsp;     - library-network



volumes:

&nbsp; couchdb\_data:



networks:

&nbsp; library-network:

&nbsp;   driver: bridge

```



---



\### Client-Side Packages (`package.json`)



```json

{

&nbsp; "name": "library-enterprise-client",

&nbsp; "version": "1.0.0",

&nbsp; "main": "src/main/index.js",

&nbsp; "scripts": {

&nbsp;   "dev": "vite",

&nbsp;   "build": "tsc \&\& vite build",

&nbsp;   "build:win": "electron-builder --win",

&nbsp;   "build:mac": "electron-builder --mac",

&nbsp;   "build:linux": "electron-builder --linux"

&nbsp; },

&nbsp; "dependencies": {

&nbsp;   "react": "^18.2.0",

&nbsp;   "react-dom": "^18.2.0",

&nbsp;   "react-router-dom": "^6.21.0",

&nbsp;   "pouchdb": "^8.0.1",

&nbsp;   "pouchdb-adapter-http": "^8.0.1",

&nbsp;   "pouchdb-replication": "^8.0.1",

&nbsp;   "zustand": "^4.4.7",

&nbsp;   "react-hook-form": "^7.49.3",

&nbsp;   "zod": "^3.22.4",

&nbsp;   "date-fns": "^3.0.6",

&nbsp;   "phosphor-react": "^1.4.1",

&nbsp;   "@headlessui/react": "^1.7.17",

&nbsp;   "file-saver": "^2.0.5",

&nbsp;   "jszip": "^3.10.1",

&nbsp;   "node-schedule": "^2.1.1",

&nbsp;   "axios": "^1.6.5"

&nbsp; },

&nbsp; "devDependencies": {

&nbsp;   "@types/react": "^18.2.47",

&nbsp;   "@types/react-dom": "^18.2.18",

&nbsp;   "@vitejs/plugin-react": "^4.2.1",

&nbsp;   "vite": "^5.0.11",

&nbsp;   "typescript": "^5.3.3",

&nbsp;   "tailwindcss": "^3.4.1",

&nbsp;   "postcss": "^8.4.33",

&nbsp;   "autoprefixer": "^10.4.16",

&nbsp;   "electron": "^28.1.0",

&nbsp;   "electron-builder": "^24.9.1",

&nbsp;   "electron-rebuild": "^3.2.13"

&nbsp; }

}

```



\*\*Key Differences from Manager:\*\*

\- `pouchdb-adapter-http` – Connects to remote CouchDB server

\- `pouchdb-replication` – Handles sync between client and server

\- `node-schedule` – Manages automatic sync intervals

\- `axios` – HTTP client for server communication



---



\### Server Setup Steps



\#### 1. Install Docker \& Docker Compose

```bash

\# Ubuntu/Debian

sudo apt update

sudo apt install docker.io docker-compose



\# Enable Docker service

sudo systemctl enable docker

sudo systemctl start docker



\# Add user to docker group

sudo usermod -aG docker $USER

```



\#### 2. Create Server Configuration

```bash

\# Create project directory

mkdir library-enterprise-server

cd library-enterprise-server



\# Create config directory

mkdir -p config/couchdb backups



\# Create CouchDB local.ini

cat > config/couchdb/local.ini << EOF

\[chttpd]

bind\_address = 0.0.0.0

port = 5984



\[couchdb]

max\_dbs\_open = 500



\[httpd]

enable\_cors = true



\[cors]

origins = \*

credentials = true

methods = GET, PUT, POST, HEAD, DELETE

headers = accept, authorization, content-type, origin, referer

EOF

```



\#### 3. Create Environment File (`.env`)

```env

\# CouchDB Configuration

COUCHDB\_USER=admin

COUCHDB\_PASSWORD=YourSecurePassword123!

COUCHDB\_PORT=5984



\# Server Configuration

SERVER\_HOST=0.0.0.0

SERVER\_PORT=5984



\# Backup Configuration

BACKUP\_PATH=/backups

BACKUP\_INTERVAL=86400

RETENTION\_DAYS=30



\# Security

ADMIN\_EMAIL=admin@library.edu.gh

SSL\_ENABLED=false

```



\#### 4. Deploy Server

```bash

\# Start services

docker-compose up -d



\# Check status

docker-compose ps



\# View logs

docker-compose logs -f couchdb



\# Create initial databases

curl -X PUT http://admin:YourSecurePassword123!@localhost:5984/books

curl -X PUT http://admin:YourSecurePassword123!@localhost:5984/patrons

curl -X PUT http://admin:YourSecurePassword123!@localhost:5984/loans

curl -X PUT http://admin:YourSecurePassword123!@localhost:5984/users

```



\#### 5. Configure Security \& Roles

```bash

\# Create admin user in CouchDB

curl -X PUT http://localhost:5984/\_users/org.couchdb.user:admin\_user \\

&nbsp; -H "Content-Type: application/json" \\

&nbsp; -d '{

&nbsp;   "name": "admin\_user",

&nbsp;   "password": "secure\_password",

&nbsp;   "roles": \["admin"],

&nbsp;   "type": "user"

&nbsp; }'



\# Set database security

curl -X PUT http://admin:YourSecurePassword123!@localhost:5984/books/\_security \\

&nbsp; -H "Content-Type: application/json" \\

&nbsp; -d '{

&nbsp;   "admins": { "roles": \["admin"] },

&nbsp;   "members": { "roles": \["librarian", "science\_dept", "children\_section"] }

&nbsp; }'

```



---



\### Client Setup Steps



\#### 1. Clone \& Install Dependencies

```bash

\# Clone repository

git clone https://github.com/your-org/library-enterprise-client.git

cd library-enterprise-client



\# Install dependencies

pnpm install

```



\#### 2. Configure Client Environment (`.env`)

```env

\# Application Settings

APP\_NAME="Library Enterprise Client"

APP\_VERSION="1.0.0"

ENVIRONMENT="production"



\# Server Connection

SERVER\_URL="http://192.168.1.100:5984"  # Replace with your server IP

SYNC\_INTERVAL=300  # Sync every 5 minutes (seconds)



\# Database Settings (Local PouchDB)

LOCAL\_DB\_NAME="library\_local"

LOCAL\_DB\_ADAPTER="websql"



\# User Settings

DEFAULT\_DEPARTMENT="general"

AUTO\_SYNC=true

OFFLINE\_MODE=false



\# Backup Settings

BACKUP\_PATH="./backups"

BACKUP\_ON\_SYNC=true

```



\#### 3. Build \& Install Client

```bash

\# Development mode

pnpm dev



\# Build for production

pnpm build



\# Package for Windows

pnpm build:win



\# Install on workstation

\# Windows: Run installer

\# macOS: Drag to Applications

\# Linux: Install package

```



---



\### Environment Configuration Comparison



| Setting | Manager Version | Enterprise Version |

|---------|----------------|-------------------|

| \*\*Database Type\*\* | Embedded SQLite | Remote CouchDB + Local PouchDB |

| \*\*Connection String\*\* | `./data/library\_data.db` | `http://server-ip:5984/books` |

| \*\*Sync Mode\*\* | N/A (single device) | Bidirectional replication |

| \*\*Backup Location\*\* | Local folder | Server + Local |

| \*\*User Authentication\*\* | Local accounts | CouchDB `\_users` database |

| \*\*Role Management\*\* | Hardcoded in app | CouchDB security objects |

| \*\*Data Isolation\*\* | N/A | Department-based views |

| \*\*Offline Capability\*\* | Full functionality | Limited (local cache only) |



---



\## 🔧 DEPLOYMENT WORKFLOWS



\### Manager Version Deployment



```mermaid

flowchart TD

&nbsp;   A\[Download Installer] --> B\[Run Setup]

&nbsp;   B --> C\[Choose Installation Path]

&nbsp;   C --> D\[Create Data Directory]

&nbsp;   D --> E\[Initialize Database]

&nbsp;   E --> F\[Launch Application]

&nbsp;   F --> G\[Start Using Library Manager]

```



\*\*Steps:\*\*

1\. Download installer from release page

2\. Run installer (no admin rights required)

3\. Choose installation directory (default: `C:\\Program Files\\Library Manager`)

4\. Application creates `data/` folder automatically

5\. First launch initializes empty database

6\. Ready to use immediately



---



\### Enterprise Version Deployment



```mermaid

flowchart TD

&nbsp;   A\[Set Up Server] --> B\[Install Docker]

&nbsp;   B --> C\[Deploy CouchDB]

&nbsp;   C --> D\[Configure Security]

&nbsp;   D --> E\[Create Databases]

&nbsp;   E --> F\[Install Client on Workstations]

&nbsp;   F --> G\[Configure Server URL]

&nbsp;   G --> H\[Sync Initial Data]

&nbsp;   H --> I\[Start Using Enterprise System]

```



\*\*Server Setup (One-Time):\*\*

1\. Install Ubuntu Server on Raspberry Pi 4 or dedicated machine

2\. Install Docker \& Docker Compose

3\. Deploy CouchDB using `docker-compose.yml`

4\. Configure admin user and security settings

5\. Create databases: `books`, `patrons`, `loans`, `users`

6\. Set up backup schedule (daily incremental)



\*\*Client Setup (Per Workstation):\*\*

1\. Download client installer

2\. Run installer on each library workstation

3\. Configure server URL during first launch

4\. Authenticate with admin credentials

5\. Initial sync pulls all data from server

6\. Ready to use with offline capability



---



\## 📋 PRE-DEPLOYMENT CHECKLIST



\### Manager Version

\- \[ ] Verify target PC meets minimum requirements

\- \[ ] Ensure 100 MB free disk space available

\- \[ ] Test installer on clean Windows/macOS/Linux VM

\- \[ ] Validate database creation on first launch

\- \[ ] Confirm backup functionality works

\- \[ ] Test on low-spec hardware (Celeron, 2GB RAM)



\### Enterprise Version

\- \[ ] Server hardware meets minimum specs

\- \[ ] Network connectivity between server and clients

\- \[ ] Docker installed and running on server

\- \[ ] CouchDB accessible from client machines

\- \[ ] Security roles configured correctly

\- \[ ] Backup system tested and verified

\- \[ ] Client sync tested on multiple workstations

\- \[ ] Offline mode validated on client devices



---



\## 🔐 SECURITY CONSIDERATIONS



\### Manager Version

| Aspect | Implementation |

|--------|----------------|

| \*\*Data Encryption\*\* | SQLite file encrypted at rest (optional) |

| \*\*User Authentication\*\* | Local password hashing (bcrypt) |

| \*\*Access Control\*\* | Role-based within single application |

| \*\*Audit Trail\*\* | Local logs stored in `logs/` directory |

| \*\*Backup Security\*\* | Encrypted backup files (optional) |



\### Enterprise Version

| Aspect | Implementation |

|--------|----------------|

| \*\*Data Encryption\*\* | TLS/SSL for server communication |

| \*\*User Authentication\*\* | CouchDB `\_users` database with hashed passwords |

| \*\*Access Control\*\* | Database-level security objects per department |

| \*\*Audit Trail\*\* | Server logs + client sync logs |

| \*\*Backup Security\*\* | Encrypted backups stored on server |

| \*\*Network Security\*\* | Firewall rules, VPN option for remote access |



---



\## 💡 RECOMMENDATIONS BY USE CASE



\### Choose \*\*Manager Version\*\* if:

\- ✅ Single library location

\- ✅ Limited or no IT support

\- ✅ Budget constraints (free solution)

\- ✅ Unreliable internet connectivity

\- ✅ Small collection (<10,000 items)

\- ✅ Rural school or community library



\### Choose \*\*Enterprise Version\*\* if:

\- ✅ Multiple departments or branches

\- ✅ Need centralized data management

\- ✅ Real-time data sharing between locations

\- ✅ Large collection (>10,000 items)

\- ✅ University or district-level deployment

\- ✅ IT support available for server maintenance



---



\## 🚀 NEXT STEPS



\### For Manager Version:

1\. Clone repository: `git clone https://github.com/your-org/library-manager.git`

2\. Install dependencies: `pnpm install`

3\. Build installer: `pnpm build:win` (or mac/linux)

4\. Test on target hardware

5\. Deploy to library workstations



\### For Enterprise Version:

1\. Set up server hardware (Raspberry Pi 4 recommended)

2\. Install Ubuntu Server + Docker

3\. Deploy CouchDB: `docker-compose up -d`

4\. Configure security and databases

5\. Build client installer: `pnpm build:win`

6\. Install client on all workstations

7\. Configure server URL on each client

8\. Test sync and offline functionality



---



This comparison provides clear, actionable guidance for setting up either version of the Library Management System. The Manager version is ideal for quick deployment with minimal overhead, while the Enterprise version offers scalability and multi-department support for larger institutions.

