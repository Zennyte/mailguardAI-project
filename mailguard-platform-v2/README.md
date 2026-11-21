# MailGuard AI Platform

Full-stack email scanning platform powered by Machine Learning — the Lab
Course 2 project.

This folder is a cleaned-up recreation of `mailguard-platform/`. It does the
same things and uses the same database, but the code is named and organised so
that someone who did not write it can find their way around quickly.

## Project Description

A user logs in, pastes an email (subject and body), scans it, and instantly
receives a classification: **safe**, **spam**, or **phishing** — together with
a confidence score for each label. Every scan is saved, triggers a real-time
notification, and can be reviewed later in the scan history, searched,
exported, and summarized in dynamic reports.

## Main App Flow

```
login → scan email → ML prediction → save result → real-time notification → view history
```

The whole flow is one function you can read top to bottom:
`scan_email()` in `backend/app/services/scan_service.py`.

> **New to this code?** [`PROJECT_GUIDE.md`](PROJECT_GUIDE.md) explains the whole
> project and every file and directory, and which part of the website each one
> belongs to. It also has a "where do I change X?" table.

## Where Is the Code for Each Page?

Every page of the website maps to one frontend page file, one file of API
calls, and one backend controller. Start from the page you are looking at:

| Page (URL)                  | Frontend page                    | API calls (frontend)        | Backend controller                      |
|-----------------------------|----------------------------------|-----------------------------|-----------------------------------------|
| Homepage (`/`)              | `pages/HomePage.jsx`             | `api/cmsApi.js`             | `cms_controller.py`                     |
| Login (`/login`)            | `pages/LoginPage.jsx`            | `api/authApi.js`            | `auth_controller.py`                    |
| Register (`/register`)      | `pages/RegisterPage.jsx`         | `api/authApi.js`            | `auth_controller.py`                    |
| Dashboard (`/dashboard`)    | `pages/DashboardPage.jsx`        | `api/scanApi.js`            | `scan_controller.py`                    |
| Scanner (`/scanner`)        | `pages/ScannerPage.jsx`          | `api/scanApi.js`            | `scan_controller.py`                    |
| History (`/history`)        | `pages/ScanHistoryPage.jsx`      | `api/scanApi.js`            | `scan_controller.py`                    |
| Search (`/search`)          | `pages/SearchPage.jsx`           | `api/searchApi.js`          | `search_controller.py`                  |
| Import/Export (`/import-export`) | `pages/ImportExportPage.jsx` | `api/importExportApi.js`    | `import_export_controller.py`           |
| Reports (`/reports`)        | `pages/ReportsPage.jsx`          | `api/reportApi.js`          | `report_controller.py`                  |
| CMS (`/cms`)                | `pages/CmsManagementPage.jsx`    | `api/cmsApi.js`             | `cms_controller.py`                     |
| Notification bell (top right) | `components/NotificationBell.jsx` | `api/notificationApi.js` | `notification_controller.py`, `notification_websocket_controller.py` |
| Sidebar and top bar         | `layouts/LoggedInLayout.jsx`     | —                           | —                                       |
| Public navbar and footer    | `layouts/VisitorLayout.jsx`      | —                           | —                                       |

From a backend controller the path is always the same:

```
controller (receives the request) → service (business logic) → repository (database)
```

For example `scan_controller.py` → `scan_service.py` → `scan_repository.py`.
The files share the same prefix, so the next file is easy to guess.

## Stack

| Layer            | Technology                     |
|------------------|--------------------------------|
| Backend          | Python FastAPI                 |
| Frontend         | React + Vite                   |
| SQL database     | PostgreSQL (26 tables)         |
| NoSQL database   | MongoDB                        |
| Styling          | Tailwind CSS                   |
| State management | Zustand                        |
| Real-time        | FastAPI native WebSockets      |
| Auth             | JWT + bcrypt password hashing  |
| ML               | scikit-learn pipeline (joblib) |

## Relation to the ML Project

The Machine Learning project (`mailguard-ml/`) trained and compared several
classifiers (Naive Bayes, Logistic Regression, Linear SVM, Random Forest, MLP)
on a combined dataset of ~68,000 emails and exported the best model
(Logistic Regression, accuracy 0.9913) as a scikit-learn pipeline:

```
mailguard-ml/models/mail_detection_pipeline.joblib
```

This platform does **not** retrain the model — it only loads the exported file
and calls `predict()` / `predict_proba()` (see `services/ml_model_service.py`).

## Features

- JWT authentication where the tokens live in `HttpOnly` cookies (JavaScript can
  never read them, so XSS cannot steal them); an expired access token is
  renewed silently with the refresh token; roles and permissions
- Email scanning with the ML model (label + confidence + a score per label)
- Optional AI explanation of the result (Groq, only if `GROQ_API_KEY` is set)
- Scan history and a statistics dashboard
- Real-time notifications through WebSockets (saved in PostgreSQL too)
- MongoDB logging of full emails and ML prediction details
- Audit logging of register / login / logout

## Additional Features (course requirement)

1. **Machine Learning Integration** — scan endpoint powered by the exported pipeline
2. **Advanced Search** — one endpoint, 5 lists, text/label/date filters + sort order
3. **Data Import/Export** — 5 lists exportable and 5 importable as CSV/JSON/XLSX
4. **Dynamic Report Generation** — 3 report types with date/label filters, recalculated live
5. **Simple CMS** — content pages made of ordered text blocks; a published page
   with the slug `home` replaces the homepage intro text

## Folder Structure

```
mailguard-platform-v2/
  backend/
    app/
      controllers/     API routes — one file per part of the website
      services/        Business logic (auth, ML, scans, reports, CMS, ...)
      repositories/    Database queries (PostgreSQL + MongoDB)
      models/          SQLAlchemy models (26 tables)
      schemas/         Pydantic schemas (shape of requests and responses)
      core/            Config, database, security, login/permission checks
      ml/              mail_detection_pipeline.joblib
      websockets/      Open WebSocket connections for live notifications
      main.py          FastAPI app entrypoint
      create_tables.py Simple local table-creation script
    requirements.txt
    .env.example
  frontend/
    src/
      pages/           One file per page of the website
      components/      Pieces used inside pages, grouped by page (search/, reports/, cms/, ...)
      layouts/         The frame around pages (navbar / sidebar)
      api/             Every call to the backend, one file per backend controller
      config/          Content you change often: label order and wording, site text,
                       menu links, dropdown options
      routes/          AppRoutes (URL → page) + RequireLogin (protected pages)
      store/           Zustand auth store (who is logged in; holds no tokens)
      utils/           How dates and percentages are formatted
      index.css        Colors (one @theme block) and reusable CSS classes
    package.json
    .env.example
  database/
    schema.sql         Full SQL schema (26 tables)
    seed.sql           Seed data (roles, permissions, settings, ML model row)
  docs/                ERD (draw.io, mermaid, png)
  README.md
```

## Requirements

- Python 3.11 to 3.14 (3.15 is too new: some packages have no build for it yet)
- Node.js 18+
- PostgreSQL 14+
- MongoDB 6+ (optional for scanning — only the logs are skipped without it)

## Environment Setup

Both apps read configuration from `.env` files — copy the examples first:

```bash
copy backend\.env.example backend\.env
copy frontend\.env.example frontend\.env
```

Backend `.env` holds the secret key, token lifetimes, PostgreSQL and MongoDB
URLs, the allowed frontend URL (CORS), the optional Groq API key and
`COOKIE_SECURE` (keep `false` on `http://localhost`; set `true` when the site is
served over HTTPS). Frontend `.env` holds the API and WebSocket URLs. No secrets
are committed to git.

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
and `backend/app/models/` (SQLAlchemy models used by the app). It is the same
schema as `mailguard-platform/`, so an existing database keeps working.

```bash
psql -U postgres -c "CREATE DATABASE mailguard_platform;"
cd backend
python -m app.create_tables
psql -U postgres -d mailguard_platform -f ../database/seed.sql
```

If your PostgreSQL user/password differ, change `DATABASE_URL` in `backend/.env`
first. **Run `seed.sql` before registering users** — new accounts get the
default role `User` from the seed data.

### Making a user an Admin

New accounts are plain users. The CMS page and importing need the Admin role:

```sql
INSERT INTO user_roles (user_id, role_id)
SELECT u.id, r.id FROM users u, roles r
WHERE u.email = 'you@example.com' AND r.name = 'Admin';
```

## MongoDB Setup

MongoDB must run locally at `mongodb://localhost:27017` (or change
`MONGODB_URL` in `backend/.env`). No schema setup is needed — the collections
(`raw_email_documents`, `scan_payload_logs`) are created automatically on
first insert. If MongoDB is down, scanning still works (a few seconds slower);
only the logs are skipped with a warning.

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
   confidence and a score bar per label; the notification bell updates live
4. **Dashboard**: totals per label and the latest result
5. **History**: all previous scans, newest first
6. **Search**: pick a list, filter by text/label/dates, choose the sort order
7. **Import/Export**: export scans as CSV/JSON/XLSX; import emails from a file (Admin/Manager)
8. **Reports**: choose type + date range → Preview → Save Report → View
9. **CMS** (Admin): create a page with slug `home`, add a block, publish it →
   the homepage now shows your text

Everything can also be tested API-first in Swagger (`/docs`): call
`POST /auth/login` there. The browser keeps the login cookies, so every other
endpoint then works with "Try it out".

## API Documentation

- Swagger UI (interactive): `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database / ERD Documentation

- Editable ERD (draw.io): [`docs/ERD.drawio`](docs/ERD.drawio)
- Mermaid ERD diagram: [`docs/ERD.mmd`](docs/ERD.mmd)
- ERD image: [`docs/ERD.png`](docs/ERD.png)
- Full SQL schema: [`database/schema.sql`](database/schema.sql)

## Notes for Presentation

- The layered flow to explain on any endpoint: controller → service → repository
  (e.g. `scan_controller.py` → `scan_service.py` + `ml_model_service.py` → `scan_repository.py`)
- Why Logistic Regression: simple, fast, explainable, supports `predict_proba()`
- Why two databases: PostgreSQL for structured/related data, MongoDB for large
  flexible payloads (full email text, ML prediction details)
- Real-time = WebSockets (server pushes), not polling
- Login security: tokens are `HttpOnly` + `SameSite=Lax` cookies, never in
  `localStorage`; see section 3 of `PROJECT_GUIDE.md`
- Roles → permissions: a user has roles, a role has permissions; the backend
  checks permissions (`require_permission("manage_cms")`) and the frontend
  hides what the user may not use (`userHasPermission(user, "manage_cms")`)
