# ChemLabViz — Chemical Equipment Parameter Visualizer

> **FOSSEE Web-Hybrid Application | Internship Submission**

A sophisticated hybrid application featuring independent Web and Desktop frontends seamlessly integrated with a Django REST API backend for comprehensive visualization and analysis of chemical equipment operational data.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Screenshots](#-screenshots)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [System Requirements](#-system-requirements)
- [Installation](#-installation)
  - [Linux Installation](#linux-installation)
  - [Windows Installation](#windows-installation)
- [Project Architecture](#-project-architecture)
- [Database Configuration](#-database-configuration)
- [Troubleshooting](#-troubleshooting)
- [Demo & Submission](#-demo--submission)
- [Author](#-author)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)
- [Support](#-support)

---

## 🎯 Overview

**ChemLabViz** is a comprehensive data analysis platform designed for chemical equipment parameter visualization and reporting. Users can upload CSV files containing equipment operational data and receive:

- **Real-time visualization** via interactive charts (Bar & Pie)
- **Statistical analysis** with automated calculations
- **Historical data management** with per-user isolation
- **Professional reports** in PDF format with embedded visualizations
- **Multi-platform access** through Web and Desktop clients
- **Secure authentication** with token-based authorization

### Problem Solved

Chemical facilities generate vast amounts of equipment parameter data (flowrate, pressure, temperature). Without proper visualization tools, this data becomes difficult to analyze and report. ChemLabViz provides an intuitive interface for data scientists and facility managers to:
1. Upload operational data in CSV format
2. Instantly visualize equipment distribution and performance metrics
3. Generate professional PDF reports for stakeholders
4. Maintain secure per-user data audit trails

---

## 📸 Screenshots

### Desktop Application

![Desktop Application](desktop-app.png)

> **⚠️ Important:** Some UI features may not be visible in this screenshot as I am using Arch-based Linux (EndeavourOS) with a custom Desktop Environment (DWM).

### Desktop Login

![Desktop Login](desktop-login.png)

### Web Application

![Web Application](web-app.png)

### Web Login

![Web Login](web-login.png)

---

## ✨ Features

| Category | Feature | Status |
|----------|---------|--------|
| **Data Input** | CSV file upload (Web & Desktop) | ✅ Complete |
| | Drag-and-drop file upload (Web) | ✅ Complete |
| | Sample data included | ✅ Complete |
| **Visualization** | Bar charts (equipment type distribution) | ✅ Complete |
| | Pie charts (percentage breakdown) | ✅ Complete |
| | Responsive chart sizing | ✅ Complete |
| **Analytics** | Count statistics | ✅ Complete |
| | Average calculations (flowrate, pressure) | ✅ Complete |
| | Type distribution analysis | ✅ Complete |
| **User Management** | User registration | ✅ Complete |
| | Secure login (Token-based) | ✅ Complete |
| | Per-user data isolation | ✅ Complete |
| | Session management | ✅ Complete |
| **History & Reports** | Upload history (last 5 datasets per user) | ✅ Complete |
| | Delete dataset from history | ✅ Complete |
| | PDF report generation | ✅ Complete |
| | Embedded charts in PDF | ✅ Complete |
| **Cross-Platform** | Web frontend (React) | ✅ Complete |
| | Desktop frontend (PyQt5) | ✅ Complete |
| | API backend (Django) | ✅ Complete |
| | Real-time synchronization | ✅ Complete |

---

## 🛠️ Technology Stack

### Frontend (Web)

| Technology | Version | Purpose | Icon |
|-----------|---------|---------|------|
| React ⚛️ | 19.2.0 | UI framework with modern hooks | ![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black) |
| Vite ⚡ | 7.2.4 | Lightning-fast build tool | ![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat&logo=vite&logoColor=white) |
| Chart.js 📊 | 4.5.1 | Interactive chart library | ![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=flat&logo=chartdotjs&logoColor=white) |
| react-chartjs-2 | 5.3.1 | React wrapper for Chart.js | ![React](https://img.shields.io/badge/React_Chart-61DAFB?style=flat&logo=react&logoColor=black) |
| TailwindCSS 🎨 | 4.1.18 | Utility-first CSS framework | ![TailwindCSS](https://img.shields.io/badge/Tailwind-06B6D4?style=flat&logo=tailwindcss&logoColor=white) |
| Axios 🌐 | 1.13.2 | HTTP client with interceptors | ![Axios](https://img.shields.io/badge/Axios-5A29E4?style=flat&logo=axios&logoColor=white) |

### Backend (Django)

| Technology | Version | Purpose | Icon |
|-----------|---------|---------|------|
| Django 🎸 | 6.0.1 | Web framework | ![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white) |
| Django REST Framework 🔌 | 3.16.1 | REST API toolkit | ![DRF](https://img.shields.io/badge/DRF-A30000?style=flat&logo=django&logoColor=white) |
| django-cors-headers 🔐 | 4.9.0 | Cross-Origin Resource Sharing | ![CORS](https://img.shields.io/badge/CORS-092E20?style=flat&logo=django&logoColor=white) |
| Pandas 🐼 | 3.0.0 | Data processing & CSV parsing | ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white) |
| NumPy 🔢 | 2.4.1 | Numerical computing | ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white) |
| Matplotlib 📈 | 3.10.8 | Chart generation (server-side) | ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat&logo=python&logoColor=white) |
| ReportLab 📄 | 4.4.9 | PDF generation | ![ReportLab](https://img.shields.io/badge/ReportLab-8B0000?style=flat&logo=adobe&logoColor=white) |
| Pillow 🖼️ | 12.1.0 | Image processing | ![Pillow](https://img.shields.io/badge/Pillow-3776AB?style=flat&logo=python&logoColor=white) |

### Frontend (Desktop)

| Technology | Version | Purpose | Icon |
|-----------|---------|---------|------|
| Python 🐍 | 3.14 | Programming language | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) |
| PyQt5 🖥️ | 5.15.11 | Cross-platform GUI framework | ![Qt](https://img.shields.io/badge/Qt-41CD52?style=flat&logo=qt&logoColor=white) |
| Matplotlib 📊 | 3.10.8 | Data visualization | ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat&logo=python&logoColor=white) |
| Requests 🌍 | 2.32.3 | HTTP library | ![Requests](https://img.shields.io/badge/Requests-3776AB?style=flat&logo=python&logoColor=white) |

### Database & Tools

| Technology | Version | Purpose | Icon |
|-----------|---------|---------|------|
| SQLite 🗄️ | 3.0+ | Default embedded database | ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white) |
| PostgreSQL 🐘 | 12+ | Optional relational database | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white) |
| Git 📝 | 2.0+ | Version control | ![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white) |
| VS Code 💻 | 1.95+ | Development environment | ![VSCode](https://img.shields.io/badge/VS_Code-007ACC?style=flat&logo=visualstudiocode&logoColor=white) |

---

## 📦 System Requirements

### Common Requirements
- **Python:** 3.10 or higher
- **Git:** Latest version
- **RAM:** 2GB minimum (4GB recommended)
- **Storage:** 500MB available space
- **Internet:** Required for package installation

### Linux-Specific
- **OS:** Ubuntu 20.04+ / Fedora 35+ / Arch Linux
- **Package Manager:** apt/dnf/pacman
- **Compiler:** GCC/Clang for building Python packages

### Windows-Specific
- **OS:** Windows 10 or higher
- **Powershell:** 5.0+ or use Command Prompt
- **Visual C++:** Build tools (optional, some packages may need it)
- **.NET Framework:** 4.5+ (for certain dependencies)

### macOS-Specific
- **OS:** macOS 10.14 or higher
- **Xcode Command Line Tools:** Required
- **Homebrew:** Recommended package manager

---

## 🚀 Installation

### Clone Repository (All Platforms)

```bash
git clone https://github.com/smitpatil06/FOSSEE-Hybrid_Web_Application.git
cd FOSSEE-Hybrid_Web_Application
```

---

## Linux Installation

### Step 1: Backend Setup

```bash
cd chemical_project

# Create Python virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install backend dependencies
pip install django==6.0.1 \
    djangorestframework==3.16.1 \
    django-cors-headers==4.9.0 \
    pandas==3.0.0 \
    matplotlib==3.10.8 \
    reportlab==4.4.9 \
    pillow==12.1.0 \
    requests==2.32.3

# Configure environment (SQLite by default)
export USE_SQLITE=True

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser account
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

**Expected Output:**
```
Starting development server at http://127.0.0.1:8000/
```

### Step 2: Web Frontend Setup

*Open a new terminal window*

```bash
cd frontend-web

# Install Node.js dependencies
npm install

# Start development server
npm run dev
```

**Expected Output:**
```
➜  Local:   http://localhost:5173/
```

### Step 3: Desktop Frontend Setup

*Open a new terminal window*

```bash
cd frontend-desktop

# Activate backend virtual environment
source ../chemical_project/venv/bin/activate

# Install desktop dependencies
pip install PyQt5==5.15.11 \
    matplotlib==3.10.8 \
    requests==2.32.3

# Run desktop application
python main.py
```

### Optional: PostgreSQL Setup (Linux)

```bash
# Install PostgreSQL client
sudo apt-get install postgresql postgresql-contrib

# Install Python PostgreSQL adapter
pip install psycopg2-binary

# Run setup script
cd chemical_project
chmod +x setup_postgres.sh
./setup_postgres.sh

# Update environment variable
export USE_POSTGRESQL=True
python manage.py migrate
```

---

## Windows Installation

### Step 1: Backend Setup

```powershell
# Open PowerShell as Administrator

cd chemical_project

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Upgrade pip
python -m pip install --upgrade pip

# Install backend dependencies
pip install django==6.0.1 `
    djangorestframework==3.16.1 `
    django-cors-headers==4.9.0 `
    pandas==3.0.0 `
    matplotlib==3.10.8 `
    reportlab==4.4.9 `
    pillow==12.1.0 `
    requests==2.32.3

# Configure environment (SQLite by default)
$env:USE_SQLITE = 'True'

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser account
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

**Expected Output:**
```
Starting development server at http://127.0.0.1:8000/
```

### Step 2: Web Frontend Setup

*Open a new PowerShell window*

```powershell
cd frontend-web

# Install Node.js dependencies
npm install

# Start development server
npm run dev
```

**Expected Output:**
```
➜  Local:   http://localhost:5173/
```

### Step 3: Desktop Frontend Setup

*Open a new PowerShell window*

```powershell
cd frontend-desktop

# Activate backend virtual environment
..\chemical_project\venv\Scripts\Activate.ps1

# Install desktop dependencies
pip install PyQt5==5.15.11 `
    matplotlib==3.10.8 `
    requests==2.32.3

# Run desktop application
python main.py
```

### Optional: PostgreSQL Setup (Windows)

1. **Install PostgreSQL:**
   - Download from [postgresql.org](https://www.postgresql.org/download/windows/)
   - Run installer with default settings
   - Remember the superuser password

2. **Configure Python:**
   ```powershell
   pip install psycopg2-binary
   $env:USE_POSTGRESQL = 'True'
   python manage.py migrate
   ```

---

## 🏗️ Project Architecture

```
ChemLabViz/
│
├── 📁 chemical_project/          [Django REST Backend]
│   ├── api/
│   │   ├── models.py             # Database models (UploadBatch, EquipmentData, User)
│   │   ├── serializers.py        # DRF serializers (validation & transformation)
│   │   ├── views.py              # REST API views (upload, stats, PDF)
│   │   ├── urls.py               # URL routing (/api/upload, /api/summary, etc.)
│   │   ├── auth_views.py         # Authentication views (login, register, logout)
│   │   └── migrations/           # Database migration files
│   │
│   ├── chemical_project/
│   │   ├── settings.py           # Django configuration (DB, CORS, auth)
│   │   ├── urls.py               # Project-level URL routing
│   │   ├── asgi.py               # ASGI configuration
│   │   └── wsgi.py               # WSGI configuration
│   │
│   ├── manage.py                 # Django management script
│   ├── db.sqlite3                # SQLite database (local development)
│   └── venv/                     # Python virtual environment
│
├── 📁 frontend-web/              [React Web Client]
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.jsx         # Authentication page (register/login tabs)
│   │   │   └── Upload.jsx        # Data upload & visualization page
│   │   │
│   │   ├── components/
│   │   │   ├── Charts.jsx        # Bar & Pie chart components
│   │   │   └── History.jsx       # Upload history list
│   │   │
│   │   ├── api.js                # Axios instance (base URL, interceptors, auth)
│   │   ├── App.jsx               # Main application component
│   │   ├── main.jsx              # React DOM render entry point
│   │   ├── index.css             # Global styles
│   │   └── App.css               # Component styles
│   │
│   ├── public/                   # Static assets
│   ├── index.html                # HTML template
│   ├── package.json              # npm dependencies
│   ├── vite.config.js            # Vite build configuration
│   ├── tailwind.config.js        # TailwindCSS configuration
│   └── postcss.config.js         # PostCSS configuration
│
├── 📁 desktop/                   [PyQt5 Desktop Client]
│   ├── main.py                   # Application entry point
│   │
│   ├── core/
│   │   └── api_client.py         # HTTP requests handler (session mgmt, endpoints)
│   │
│   ├── ui/
│   │   ├── views/
│   │   │   ├── login_window.py   # Qt login/register dialog
│   │   │   └── upload_window.py  # Main application window (tabs: upload, history, charts)
│   │   │
│   │   └── components/
│   │       ├── history_widget.py # History list with delete functionality
│   │       └── charts_widget.py  # Matplotlib chart rendering
│   │
│   └── requirements.txt          # pip dependencies
│
├── 📄 sample_equipment_data.csv  # Test dataset (15 equipment records)
├── 📄 README.md                  # This file

```

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      User Layer                                 │
├─────────────────────┬─────────────────────┬─────────────────────┤
│  Web Browser        │  Desktop App        │  PDF Reports        │
│  (React + Chart.js) │  (PyQt5 + Mpl)      │  (ReportLab)        │
└────────────┬────────┴────────────┬────────┴───────────┬─────────┘
             │                     │                    │
             │  Axios (Requests)   │  Requests          │ API Call
             │  HTTP/JSON          │  HTTP/JSON         │
┌────────────▼─────────────────────▼────────────────────▼─────────┐
│                    API Gateway Layer                            │
│                 (Django REST Framework)                         │
├─────────────────────────────────────────────────────────────────┤
│  • Token Authentication  • CORS Headers  • Request Validation   │
└──────┬─────────────────────────────────────────────────────┬────┘
       │                                                     │
┌──────▼─────────────────────────────────────────────────────▼────┐
│                    Application Layer                            │
│              (Django Views & Serializers)                       │
├─────────────────────────────────────────────────────────────────┤
│  • AuthView (register/login/logout)                             │
│  • UploadView (CSV processing → EquipmentData records)          │
│  • SummaryView (aggregation, type distribution)                 │
│  • HistoryView (per-user upload tracking)                       │
│  • PDFView (matplotlib charts → ReportLab → PDF)                │
└──────┬──────────────────────────────────────────────────┬───────┘
       │                                                  │
┌──────▼──────────────────────────────────────────────────▼────────┐
│                    Data Processing Layer                         │
│                  (Pandas • Matplotlib)                           │
├──────────────────────────────────────────────────────────────────┤
│  • CSV Parsing & Validation (Pandas)                             │
│  • Statistical Calculations (Pandas/NumPy)                       │
│  • Chart Generation (Matplotlib → PNG)                           │
└──────┬───────────────────────────────────────────────────────────┘
       │
┌──────▼───────────────────────────────────────────────────────────┐
│                   Persistence Layer                              │
├──────────────────────────────────────────────────────────────────┤
│  SQLite (Default)          │  PostgreSQL (Optional)              │
│  ├─ users table            │  ├─ users table                     │
│  ├─ upload_batch table     │  ├─ upload_batch table              │
│  └─ equipment_data table   │  └─ equipment_data table            │
└──────────────────────────────────────────────────────────────────┘
```

### Data Flow Diagram

**User Registration:**
```
User Input (Register)
    ↓
Web/Desktop Form Validation
    ↓
POST /api/auth/register/ {email, username, password}
    ↓
Django: Check user existence
    ↓
Hash password (PBKDF2)
    ↓
Create User record
    ↓
Response: {user_id, token}
    ↓
Store token in client storage
    ↓
Auto-redirect to login page
```

**CSV Upload & Analysis:**
```
User selects CSV file
    ↓
File validation (Web: drag-drop, Desktop: file dialog)
    ↓
POST /api/upload/ with CSV file + token
    ↓
Django:
  1. Parse CSV with Pandas
  2. Validate column names & data types
  3. Create UploadBatch record
  4. Create EquipmentData records (one per row)
    ↓
GET /api/summary/<batch_id>/ with token
    ↓
Django:
  1. Aggregate equipment counts (pandas groupby)
  2. Calculate statistics (mean, sum, count)
  3. Generate type distribution
  4. Return JSON response
    ↓
Frontend: Render charts (Chart.js bar + pie)
    ↓
Display dashboard with visualizations
```

**PDF Generation:**
```
User clicks "Download Report"
    ↓
GET /api/report/<batch_id>/ with auth token
    ↓
Django:
  1. Fetch UploadBatch & EquipmentData from DB
  2. Generate Matplotlib figure (bar + pie chart)
  3. Render chart as PNG to BytesIO
  4. Create ReportLab PDF document
  5. Add title, summary table, embedded PNG
  6. Render to bytes
    ↓
HTTP Response: PDF file (content-type: application/pdf)
    ↓
Browser: Download or open PDF
```

---

## 💾 Database Configuration

### SQLite (Recommended for Development)

**Advantages:**
- No external server required
- Zero configuration
- Ideal for development/testing

**Setup:**
```bash
export USE_SQLITE=True
python manage.py migrate
```

**Location:**
```
chemical_project/db.sqlite3
```

### PostgreSQL (Optional for Production)

**Advantages:**
- Multi-user support
- Better for concurrent access
- Production-ready
- Advanced query capabilities

**Setup (Linux):**
```bash
./setup_postgres.sh
export USE_POSTGRESQL=True
python manage.py migrate
```

**Setup (Windows):**
1. Install PostgreSQL from [postgresql.org](https://www.postgresql.org/)
2. Run installer (remember superuser password)
3. Update Django settings to connect

**Connection String:**
```
postgresql://postgres:password@localhost:5432/chemlab_db
```


## 🔧 Troubleshooting

### Python/Environment Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'django'` | Run `pip install django==6.0.1` in active venv |
| `python: command not found` | Use `python3` on Linux or check PATH on Windows |
| Virtual environment not activating | Linux: Check `source venv/bin/activate`, Windows: Check `.\.venv\Scripts\Activate.ps1` |
| Permission denied running script | Windows: Run PowerShell as Administrator, Linux: Use `sudo` if needed |

### Backend Issues

| Issue | Solution |
|-------|----------|
| `django.db.utils.OperationalError: no such table` | Run `python manage.py migrate` |
| Port 8000 already in use | Run `python manage.py runserver 8001` or kill process |
| CORS errors in browser console | Ensure backend is running at `http://localhost:8000` |
| Static files not loading | Run `python manage.py collectstatic` |

### Frontend Issues

| Issue | Solution |
|-------|----------|
| `npm install` fails | Delete `node_modules/` and `package-lock.json`, then retry |
| Port 5173 not accessible | Check firewall, try `npm run dev -- --host` |
| Charts not rendering | Check browser console for errors, verify Chart.js is imported |
| Login fails with 401 | Verify token format in localStorage, check backend logs |

### Desktop App Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: PyQt5` | Run `pip install PyQt5==5.15.11` in activated venv |
| Login page text invisible | Update stylesheet in `login_window.py` with explicit colors |
| Charts not displaying | Ensure Matplotlib backend is 'Agg' or 'Qt5Agg' |
| Connection refused to backend | Verify backend is running (`http://localhost:8000`), check firewall |

### Database Issues

| Issue | Solution |
|-------|----------|
| SQLite locked error | Ensure only one process accessing db.sqlite3, restart server |
| PostgreSQL connection failed | Check if PostgreSQL service is running, verify credentials |
| Migration errors | Run `python manage.py makemigrations`, then `migrate` |

---

## 🎬 Demo & Submission

### Recording Demo Video

Demonstrate complete workflow:
1. **Registration** - Create new account (Web)
2. **Login** - Authentication flow (Desktop)
3. **CSV Upload** - File selection and processing
4. **Data Visualization** - Interacting with charts
5. **PDF Download** - Report generation with charts
6. **History Management** - Delete datasets

**Suggested Duration:** 2-3 minutes


## 👨‍💻 Author

**Smit Patil**  
- GitHub: [@smitpatil06](https://github.com/smitpatil06)
- Project: FOSSEE Hybrid Web Application
- Submission Date: February 2026

---

## 📄 License

Submitted as part of FOSSEE (Free/Libre and Open Source Software for Education) internship program.

---

## 🙏 Acknowledgments

- **FOSSEE** - Open Source Software for Education Initiative
- **Django Community** - Web framework & REST framework
- **React Community** - Frontend framework & ecosystem
- **PyQt Community** - Cross-platform GUI toolkit
- **Open Source Contributors** - All dependencies used

---

## 📞 Support

For issues or questions:
1. Check **Troubleshooting** section above
2. Check project GitHub issues
3. Review Django & React official documentation

**Last Updated:** February 2, 2026  
**Status:** Production Ready ✅
