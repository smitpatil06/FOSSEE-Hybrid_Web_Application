# ChemLabWizard — Chemical Equipment Parameter Visualizer

> **FOSSEE Web-Hybrid Application | Internship Submission**

A hybrid application featuring independent Web (React) and Desktop (PyQt5) frontends integrated with a Django REST API backend for visualization and analysis of chemical equipment operational data.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Screenshots](#-screenshots)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Database Configuration](#-database-configuration)
- [Troubleshooting](#-troubleshooting)
- [Author](#-author)
- [License](#-license)

---

## 🎯 Overview

**ChemLabWizard** is a data analysis platform for chemical equipment parameter visualization and reporting. Users upload CSV files containing equipment operational data (flowrate, pressure, temperature) and receive:

- Real-time visualization via interactive charts (Bar & Pie)
- Statistical analysis with automated calculations
- Historical data management with per-user isolation (last 5 datasets)
- PDF reports with embedded visualizations
- Multi-platform access (Web and Desktop)
- Secure token-based authentication

---

## 📸 Screenshots

| Platform | Screenshot |
|----------|------------|
| **Web Application** | ![Web Application](web-app.png) |
| **Web Login** | ![Web Login](web-login.png) |
| **Desktop Application** | ![Desktop Application](desktop-app.png) |
| **Desktop Login** | ![Desktop Login](desktop-login.png) |

---

## ✨ Features

- ✅ CSV file upload with drag-and-drop (Web)
- ✅ Bar and Pie chart visualizations
- ✅ Statistical analysis (count, average flowrate, average pressure, type distribution)
- ✅ User registration and token-based authentication
- ✅ Per-user data isolation
- ✅ Upload history (last 5 datasets per user with auto-delete)
- ✅ PDF report generation with embedded charts
- ✅ Cross-platform (Web React + Desktop PyQt5)
- ✅ Sample data included (`sample_equipment_data.csv`)

---

## 🛠️ Technology Stack

### Frontend (Web)
- **React** 19.2.0 - UI framework
- **Vite** 7.2.4 - Build tool
- **Chart.js** 4.5.1 + react-chartjs-2 5.3.1 - Data visualization
- **TailwindCSS** 4.1.18 - Styling
- **Axios** 1.13.2 - HTTP client

### Backend (Django)
- **Django** 6.0.1 - Web framework
- **Django REST Framework** 3.16.1 - REST API
- **django-cors-headers** 4.9.0 - CORS support
- **Pandas** 3.0.0 - Data processing
- **NumPy** 2.4.1 - Numerical computing
- **Matplotlib** 3.10.8 - Server-side charts
- **ReportLab** 4.4.9 - PDF generation
- **Pillow** 12.1.0 - Image processing

### Frontend (Desktop)
- **Python** 3.10+ - Programming language
- **PyQt5** 5.15.11 - GUI framework
- **Matplotlib** 3.10.8 - Data visualization
- **Requests** 2.32.3 - HTTP client

### Database
- **SQLite** 3.0+ - Default embedded database
- **PostgreSQL** 12+ - Optional production database

---

## 🚀 Installation

### Prerequisites
- **Python** 3.10 or higher
- **Node.js** 18+ and npm (for web frontend)
- **Git** (for cloning repository)

### 1. Clone Repository

```bash
git clone https://github.com/smitpatil06/FOSSEE-Hybrid_Web_Application.git
cd FOSSEE-Hybrid_Web_Application
```

### 2. Backend Setup

```bash
cd chemical_project

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# OR
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# Install dependencies
pip install django==6.0.1 djangorestframework==3.16.1 django-cors-headers==4.9.0 pandas==3.0.0 matplotlib==3.10.8 reportlab==4.4.9 pillow==12.1.0 requests==2.32.3

# Setup database (SQLite by default)
export USE_SQLITE=True  # Linux/macOS
# OR
$env:USE_SQLITE = 'True'  # Windows PowerShell

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Start backend server
python manage.py runserver
```

Backend runs at: **http://localhost:8000**

### 3. Web Frontend Setup

*Open a new terminal*

```bash
cd frontend-web

# Install dependencies
npm install

# Start development server
npm run dev
```

Web app runs at: **http://localhost:5173**

### 4. Desktop Frontend Setup

*Open a new terminal*

```bash
cd frontend-desktop

# Activate backend virtual environment
source ../chemical_project/venv/bin/activate  # Linux/macOS
# OR
..\chemical_project\venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install PyQt5==5.15.11 matplotlib==3.10.8 requests==2.32.3

# Run desktop application
python desktop_app.py
```

### Optional: PostgreSQL Setup

If you prefer PostgreSQL over SQLite:

```bash
# Install PostgreSQL (Linux)
sudo apt-get install postgresql postgresql-contrib

# Install Python adapter
pip install psycopg2-binary

# Run setup script
cd chemical_project
chmod +x setup_postgres.sh
./setup_postgres.sh

# Configure and migrate
export USE_POSTGRESQL=True
python manage.py migrate
```

---

## 📁 Project Structure

```
ChemLabWizard/
├── chemical_project/          # Django REST Backend
│   ├── api/
│   │   ├── models.py         # Database models (UploadBatch, EquipmentData)
│   │   ├── serializers.py    # DRF serializers
│   │   ├── views.py          # REST API views (upload, stats, PDF)
│   │   ├── auth_views.py     # Authentication endpoints
│   │   └── urls.py           # API routing
│   ├── chemical_project/
│   │   ├── settings.py       # Django configuration
│   │   └── urls.py           # Main URL routing
│   ├── manage.py
│   └── db.sqlite3            # SQLite database
│
├── frontend-web/             # React Web Client
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.jsx     # Authentication page
│   │   │   └── Upload.jsx    # Data upload & visualization
│   │   ├── components/
│   │   │   ├── Charts.jsx    # Bar & Pie charts
│   │   │   └── History.jsx   # Upload history
│   │   ├── api.js            # Axios HTTP client
│   │   └── App.jsx           # Main component
│   ├── package.json
│   └── vite.config.js
│
├── frontend-desktop/         # PyQt5 Desktop Client
│   ├── desktop_app.py        # Entry point
│   ├── core/
│   │   └── api_client.py     # HTTP client
│   └── ui/
│       ├── views/
│       │   ├── login_window.py
│       │   └── upload_window.py
│       └── components/
│           └── history_widget.py
│
└── sample_equipment_data.csv # Test dataset
```

---

## 🔗 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and receive token
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/profile/` - Get user profile

### Data Operations
- `POST /api/upload/` - Upload CSV file
- `GET /api/history/` - Get user's upload history
- `GET /api/summary/<batch_id>/` - Get statistics for a dataset
- `GET /api/report/<batch_id>/` - Download PDF report

---

## 💾 Database Configuration

### SQLite (Default)
Zero configuration required. Database file created at `chemical_project/db.sqlite3`.

```bash
export USE_SQLITE=True
python manage.py migrate
```

### PostgreSQL (Optional)
For production or multi-user scenarios:

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib  # Linux

# Install Python adapter
pip install psycopg2-binary

# Run setup script
cd chemical_project
chmod +x setup_postgres.sh
./setup_postgres.sh

# Configure and migrate
export USE_POSTGRESQL=True
python manage.py migrate
```

---

## 🔧 Troubleshooting

**Module not found errors:**
```bash
pip install django djangorestframework django-cors-headers pandas matplotlib reportlab pillow
```

**Database errors:**
```bash
export USE_SQLITE=True
python manage.py migrate
```

**CORS errors:**
- Ensure backend runs at `http://localhost:8000`
- Verify CORS settings in `chemical_project/chemical_project/settings.py`

**Desktop app not starting:**
```bash
pip install PyQt5 matplotlib requests
```

**Port already in use:**
```bash
# Backend (port 8000)
python manage.py runserver 8001

# Web frontend (port 5173)
npm run dev -- --port 5174
```

---

## 👨‍💻 Author

**Smit Patil**  
GitHub: [@smitpatil06](https://github.com/smitpatil06)

---

## 📄 License

Submitted as part of FOSSEE internship application.

---

## 🙏 Acknowledgments

Built for FOSSEE (Free/Libre and Open Source Software for Education)
