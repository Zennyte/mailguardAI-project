# MailGuard AI Platform

Full-stack email scanning platform powered by Machine Learning — the Lab
Course 2 project.

## Project Description

A user logs in, pastes an email (subject and body), scans it, and instantly
receives a classification: **safe**, **spam**, or **phishing** — together with
a confidence score for each class. Every scan is saved, triggers a real-time
notification, and can be reviewed later in the scan history, searched,
exported, and summarized in dynamic reports.

## Main App Flow

```
login → scan email → ML prediction → save result → real-time notification → view history
```

## Stack

| Layer            | Technology                  |
|------------------|-----------------------------|
| Backend          | Python FastAPI              |
| Frontend         | React + Vite                |
| SQL database     | PostgreSQL (26 tables)      |
| NoSQL database   | MongoDB                     |
| Styling          | Tailwind CSS                |
| State management | Zustand                     |
| Real-time        | FastAPI native WebSockets   |
| Auth             | JWT + bcrypt password hashing |
| ML               | scikit-learn pipeline (joblib) |

The backend uses a simple layered architecture:

```
controller (receives request) → service (business logic) → repository (database)
```

## Relation to the ML Project

The Machine Learning project (`mailguard-ml/`) trained and compared several
classifiers (Naive Bayes, Logistic Regression, Linear SVM, Random Forest, MLP)
on a combined dataset of ~68,000 emails and exported the best model
(Logistic Regression, accuracy 0.9913) as a scikit-learn pipeline:

```
mailguard-ml/models/mail_detection_pipeline.joblib
```

This platform does **not** retrain the model — it only loads the exported file
and calls `predict()` / `predict_proba()`.

## Features

- JWT authentication with refresh tokens and role-based access foundation
- Email scanning with the ML model (label + confidence + per-class scores)
- Scan history and a statistics dashboard
- Real-time notifications through WebSockets (saved in PostgreSQL too)
- MongoDB logging of raw emails and ML payloads
- Audit logging of auth actions

## Additional Features (course requirement)

1. **Machine Learning Integration** — scan endpoint powered by the exported pipeline
2. **Advanced Search** — one endpoint, 5 lists, text/label/status/date filters + sorting
3. **Data Import/Export** — 5 lists exportable and 5 importable as CSV/JSON/XLSX
4. **Dynamic Report Generation** — 3 report types with date/label filters, regenerated live
5. **Simple CMS** — static content pages with ordered blocks; published `home` page replaces the homepage text

## Folder Structure

```
mailguard-platform/
  backend/
    app/
      controllers/     API routes (receive requests)
      services/        Business logic (auth, ML, scans, reports, CMS, ...)
      repositories/    Database queries (PostgreSQL + MongoDB)
      models/          SQLAlchemy models (26 tables)
      schemas/         Pydantic schemas (request/response validation)
      core/            Config, database, security, dependencies
      ml/              mail_detection_pipeline.joblib
      websockets/      WebSocket connection manager
      main.py          FastAPI app entrypoint
      create_tables.py Simple local table-creation script
    requirements.txt
    .env.example
  frontend/
    src/
      components/      Reusable UI (LabelBadge, NotificationBell)
      pages/           Home, Login, Register, Dashboard, Scanner, History,
                       Search, ImportExport, Reports, CMS
      services/        API calls (axios)
      store/           Zustand auth store
      routes/          AppRoutes + ProtectedRoute
      layouts/         MainLayout with navbar
    package.json
    .env.example
  database/
    schema.sql         Full SQL schema (26 tables)
    seed.sql           Seed data (roles, permissions, settings, ML model row)
  docs/                API docs, database design, ERD, project report, checklists
  README.md
```

## Requirements

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- MongoDB 6+ (optional for scanning — only raw logs are skipped without it)

## Environment Setup

Both apps read configuration from `.env` files — copy the examples first:

```bash
copy backend\.env.example backend\.env
copy frontend\.env.example frontend\.env
```

Backend `.env` holds the secret key, token lifetimes, PostgreSQL and MongoDB
URLs, and the allowed frontend URL (CORS). Frontend `.env` holds the API and
WebSocket URLs. No secrets are committed to git.

## Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows (Linux/macOS: source venv/bin/activate)
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The backend runs at `http://localhost:8000`. Health check: `GET /health`.

## Database Setup (PostgreSQL)

The schema is defined in two equivalent ways: `database/schema.sql` (plain SQL)
and `backend/app/models/` (SQLAlchemy models used by the app).

```bash
psql -U postgres -c "CREATE DATABASE mailguard_platform;"
cd backend
python -m app.create_tables
psql -U postgres -d mailguard_platform -f ../database/seed.sql
```

If your PostgreSQL user/password differ, change `DATABASE_URL` in `backend/.env`
first. **Run `seed.sql` before registering users** — new accounts get the
default role `User` from the seed data.

## MongoDB Setup

MongoDB must run locally at `mongodb://localhost:27017` (or change
`MONGODB_URL` in `backend/.env`). No schema setup is needed — the collections
(`raw_email_documents`, `scan_payload_logs`) are created automatically on
first insert. If MongoDB is down, scanning still works; only raw logs are
skipped with a warning.

## ML Model Setup

The exported model must exist at:

```
backend/app/ml/mail_detection_pipeline.joblib
```

It is committed in this repository. To refresh it from the ML project:

```bash
copy ..\mailguard-ml\models\mail_detection_pipeline.joblib backend\app\ml\
```

If the file is missing, `POST /scans/analyze` returns
`503 ML model is not available`.

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at `http://localhost:5173` (API URL comes from `VITE_API_URL`).

## How to Test the App

1. Start PostgreSQL (and MongoDB if available), the backend, and the frontend
2. Open `http://localhost:5173` and **register** — you land on the dashboard
3. **Scanner**: paste a suspicious text like *"Verify your bank account
   immediately by clicking this link"* → result shows **phishing** with
   confidence and per-class score bars; the notification bell updates live
4. **Dashboard**: totals per label and the latest result
5. **History**: all previous scans, newest first
6. **Search**: pick a list, filter by text/label/dates
7. **Import/Export**: export scans as CSV/JSON/XLSX; import emails from a file
8. **Reports**: choose type + date range → Preview → Save Report → View
9. **CMS**: create a page with slug `home`, add a block, publish it → the
   homepage now shows your text

Everything can also be tested API-first in Swagger: register/login, click
**Authorize**, paste the access token, and call any endpoint.

## API Documentation

- Swagger UI (interactive): `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Written reference with examples: [`docs/API_DOCUMENTATION.md`](docs/API_DOCUMENTATION.md)

## Database / ERD Documentation

- Design and table groups: [`docs/DATABASE_DESIGN.md`](docs/DATABASE_DESIGN.md)
- Relationships explained: [`docs/ERD_NOTES.md`](docs/ERD_NOTES.md)
- Mermaid ERD diagram: [`docs/ERD.mmd`](docs/ERD.mmd)
- Project report: [`docs/PROJECT_REPORT.md`](docs/PROJECT_REPORT.md)

## Notes for Presentation

- The layered flow to explain on any endpoint: controller → service → repository
  (e.g. `scan_controller.py` → `scan_service.py` + `ml_service.py` → `scan_repository.py`)
- Why Logistic Regression: simple, fast, explainable, supports `predict_proba()`
- Why two databases: PostgreSQL for structured/related data, MongoDB for large
  flexible payloads (raw email text, ML logs)
- Real-time = WebSockets (server pushes), not polling
- The 10 required base tables and the full 26-table list are in
  `docs/DATABASE_DESIGN.md`
- Checklists: [`docs/FINAL_SUBMISSION_CHECKLIST.md`](docs/FINAL_SUBMISSION_CHECKLIST.md),
  [`docs/PROJECT_MANAGEMENT.md`](docs/PROJECT_MANAGEMENT.md)
