# ChemLabWizard - AI Coding Agent Instructions

## Project Overview
A hybrid chemical equipment data visualization platform with **two independent frontends** (React web, PyQt5 desktop) sharing a **Django REST API backend**. Users upload CSV files containing equipment operational parameters (flowrate, pressure, temperature) to generate charts, statistics, and PDF reports. Token-based authentication ensures per-user data isolation.

## Architecture & Key Patterns

### Multi-Frontend Architecture
- **Backend:** Django REST API at `chemical_project/` (runs on port 8000)
- **Web Frontend:** React + Vite at `frontend-web/` (runs on port 5173)
- **Desktop Frontend:** PyQt5 GUI at `frontend-desktop/` (standalone app)

**Critical:** Both frontends share the same API contract but maintain completely independent codebases. Changes to API endpoints require updates across BOTH clients.

### Data Flow & User Isolation
```
CSV Upload → UploadBatch (per-user) → EquipmentData (related via batch FK)
              ↓
         Auto-delete oldest batch when user exceeds 5 datasets (FIFO queue)
```

**Pattern:** `uploaded_by` ForeignKey on `UploadBatch` enforces data isolation. All API views filter by `request.user`:
```python
# In views.py - ALWAYS filter by uploaded_by
batch = UploadBatch.objects.get(id=batch_id, uploaded_by=request.user)
```

### Authentication Flow
Token-based auth using DRF's `authtoken`. Tokens stored in `localStorage` (web) or Python session (desktop).

**Web client pattern** (`frontend-web/src/api.js`):
```javascript
// Axios interceptor auto-injects token
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) config.headers.Authorization = `Token ${token}`;
    return config;
});
```

**Desktop client pattern** (`frontend-desktop/core/api_client.py`):
```python
# Session-based persistence with requests library
self.session = requests.Session()
self.session.headers.update({'Authorization': f'Token {token}'})
```

## Critical Development Workflows

### Backend Setup (Django)
```bash
cd chemical_project
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver  # Port 8000
```

**Database:** SQLite by default. Optional PostgreSQL via `USE_POSTGRESQL=True` env var (see `settings.py`).

### Web Frontend Setup (React)
```bash
cd frontend-web
pnpm install
pnpm run dev  # Port 5173
```

**Build tool:** Vite (NOT Create React App). Config in `vite.config.js`.

### Desktop Frontend Setup (PyQt5)
```bash
cd frontend-desktop
source ../chemical_project/venv/bin/activate  # Reuse backend venv
pip install -r requirements.txt
python desktop_app.py
```

**Note:** Desktop apps use matplotlib's `'Agg'` backend (non-GUI) to avoid Qt conflicts.

## Project-Specific Conventions

### CSV Schema Requirements
**Exact column names** expected in uploaded CSVs (see `FileUploadView` validation):
```
'Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'
```
Sample data: `sample_equipment_data.csv` at project root.

### API URL Configuration
**Currently hardcoded** to `http://127.0.0.1:8000/api` across both frontends:
- Web: `frontend-web/src/api.js` → `const API_URL`
- Desktop: `frontend-desktop/desktop_app.py` → `API_URL`
- Desktop API client: `frontend-desktop/core/api_client.py` → `base_url` param

**Future improvement:** Use environment variables (`.env` files with `VITE_API_URL` for web, config files for desktop) to support multiple environments (dev/staging/production) without code changes.

### CORS Configuration
Django allows React dev server via `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",   # Vite default port
    "http://127.0.0.1:5173",
]
```
Add production domains here before deployment.

### History Limit Pattern
**Automatic FIFO deletion** in `FileUploadView.post()`:
```python
batches = UploadBatch.objects.filter(uploaded_by=request.user).order_by('uploaded_at')
if batches.count() >= 5:
    batches.first().delete()  # Cascades to EquipmentData via FK
```

### PDF Generation Specifics
`GeneratePDFView` uses ReportLab + matplotlib:
1. Generate charts with matplotlib (saved to `io.BytesIO`)
2. Embed chart PNG into PDF using `ImageReader`
3. Add stats table with first 15 equipment rows
4. Return as `FileResponse` with download attachment

**Chart backend:** Must use `matplotlib.use('Agg')` before importing `pyplot` to avoid GUI conflicts in Django.

## File Organization

### Key Backend Files
- `api/models.py` - `UploadBatch` (metadata) + `EquipmentData` (CSV rows)
- `api/views.py` - Upload, Stats, History, PDF endpoints (all class-based views)
- `api/auth_views.py` - Register, Login, Logout, Profile (separate from main views)
- `api/serializers.py` - DRF serializers with `UserSerializer` for nested user data
- `api/urls.py` - URL routing with `/auth/*` and `/summary/<id>/` patterns

### Key Frontend Files (Web)
- `src/App.jsx` - Auth state management, conditional rendering (Login vs Upload)
- `src/api.js` - Axios instance with interceptors (token injection, 401 handling)
- `src/pages/Upload.jsx` - Main dashboard with file upload, charts, history
- `src/components/Charts.jsx` - Chart.js wrapper for bar/pie visualization

### Key Frontend Files (Desktop)
- `desktop_app.py` - Main PyQt5 window with sidebar, history list, charts
- `core/api_client.py` - API abstraction layer (login, upload, fetch methods)
- `ui/views/login_window.py` - Authentication dialog
- `ui/components/history_widget.py` - History list widget component

## Common Pitfalls

1. **Forgetting per-user filtering:** Always include `uploaded_by=request.user` in ORM queries to prevent data leaks.

2. **Migration conflicts:** Adding fields to models requires:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
   Delete `db.sqlite3` and re-migrate if stuck (dev only).

3. **CORS errors:** Ensure React dev server runs on port 5173 OR update `CORS_ALLOWED_ORIGINS` in `settings.py`.

4. **Desktop API calls fail:** Check Django server is running on port 8000. Desktop apps don't auto-start backend.

5. **Chart rendering issues:** Web uses Chart.js (client-side), backend/desktop use matplotlib. Different APIs, different styling.

6. **Token persistence:** Web uses `localStorage`, desktop uses `requests.Session`. Never mix session/token auth in same client.

## Testing & Debugging

**No automated tests exist.** Validate changes via:
- Web: Browser DevTools Network tab for API calls
- Desktop: Print statements in terminal (no logging framework)
- Backend: Django admin at `/admin/` or DRF browsable API

**Sample workflow:**
1. Register user via web frontend
2. Upload `sample_equipment_data.csv`
3. Verify charts render and PDF download works
4. Check desktop app shows same data after login

## Integration Points

- **React ↔ Django:** Axios HTTP requests with Token auth headers
- **PyQt5 ↔ Django:** `requests` library with Session object
- **Django ↔ Database:** Django ORM with FK cascade deletes
- **Django ↔ File System:** CSV parsed in-memory with Pandas (no file storage)

## Version-Specific Notes

- **Django 6.0.1** - Newest version, follow official docs for breaking changes
- **React 19.2.0** - Uses modern hooks (useState, useEffect), no class components
- **Vite 7.2.4** - Fast HMR, ESM-based (not Webpack)
- **PyQt5 5.15.11** - No PyQt6 migration, stick to Qt5 APIs

## Architecture Scope

This is an **internship project** with intentionally simplified architecture:
- **Synchronous request-response** model (no WebSockets needed)
- **No background task queues** (Celery/Redis not required)
- **No caching layer** (SQLite queries are fast enough for project scope)
- **In-memory CSV processing** (no file storage, no distributed systems)

This design is appropriate for the project requirements and keeps deployment simple.

---

**Last Updated:** Auto-generated from codebase analysis  
**When in doubt:** Check `README.md` for installation steps and `sample_equipment_data.csv` for data format examples.
