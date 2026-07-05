# MailGuard AI Platform

Full-stack email scanning platform powered by Machine Learning.

A user can log in, paste or upload an email, scan it, and receive a classification
result: **safe**, **spam**, or **phishing** — together with a confidence score.

This is the Lab Course 2 project. It uses the trained model from the completed
Machine Learning project (`mailguard-ml/`).

---

## Main App Flow

```
login → scan email → ML prediction → save result → real-time notification → view history
```

---

## Stack

| Layer            | Technology                  |
|------------------|-----------------------------|
| Backend          | Python FastAPI              |
| Frontend         | React + Vite                |
| SQL database     | PostgreSQL                  |
| NoSQL database   | MongoDB                     |
| Styling          | Tailwind CSS                |
| State management | Zustand                     |
| Real-time        | FastAPI native WebSockets   |
| Auth             | JWT + password hashing      |

---

## Relation to the ML Project

The Machine Learning project (`mailguard-ml/`) trained and compared several
classifiers on a combined dataset of ~68,000 emails and exported the best model
(Logistic Regression) as a scikit-learn pipeline:

```
mailguard-ml/models/mail_detection_pipeline.joblib
```

This file is copied to `backend/app/ml/` and the backend loads it to classify
emails (see "ML Model Setup" below).

---

## Folder Structure

```
mailguard-platform/
  backend/
    app/
      controllers/     API routes (receive requests)
      services/        Business logic
      repositories/    Database access
      models/          SQLAlchemy models (later)
      schemas/         Pydantic schemas (validation)
      core/            Configuration
      ml/              ML model file (later)
      websockets/      Real-time notifications (later)
      main.py          FastAPI app entrypoint
    requirements.txt
    .env.example
  frontend/
    src/
      components/      Reusable UI components
      pages/           Page components
      services/        API calls
      store/           Zustand state (later)
      routes/          Routing (later)
      layouts/         Page layouts (later)
  database/
    schema.sql         Planned SQL schema (26 tables)
    seed.sql           Seed data (later)
  docs/                Project documentation
  README.md
```

---

## Backend Setup

Requires Python 3.11+.

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env       # Windows (or: cp .env.example .env)
uvicorn app.main:app --reload
```

The backend runs at `http://localhost:8000`.

Test the health check:

- Open `http://localhost:8000/health` in the browser, or:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{ "status": "ok", "app": "MailGuard AI Platform", "message": "Backend is running" }
```

Interactive API docs (Swagger): `http://localhost:8000/docs`

---

## Database Setup (PostgreSQL)

The relational schema with all 26 tables is defined in two equivalent ways:

- `database/schema.sql` — plain SQL, can be run directly with `psql`
- `backend/app/models/` — SQLAlchemy models used by the backend

Requires PostgreSQL 14+ installed and running locally.

1. Create the database once:

```bash
psql -U postgres -c "CREATE DATABASE mailguard_platform;"
```

2. Create all tables with the simple Python script (uses the SQLAlchemy models):

```bash
cd backend
python -m app.create_tables
```

3. Load the seed data (roles, permissions, settings, ML model row):

```bash
psql -U postgres -d mailguard_platform -f database/seed.sql
```

If your PostgreSQL user or password is different, change `DATABASE_URL` in
`backend/.env` first.

**Important:** run `seed.sql` before registering users — new accounts get the
default role `User`, which comes from the seed data.

---

## ML Model Setup

The scan feature needs the exported model from the ML project. Copy it into
the backend (already done if the file is committed in this repository):

```bash
copy ..\mailguard-ml\models\mail_detection_pipeline.joblib backend\app\ml\
```

- The platform does **not** retrain the model — it only loads it for predictions.
- The model is loaded once, on the first scan, and kept in memory.
- If the file is missing, `POST /scans/analyze` returns `503 ML model is not available`.

---

## Testing the Scan Endpoint

1. Start the backend and open Swagger: `http://localhost:8000/docs`
2. Register and log in (see Authentication above), click **Authorize** and paste
   the access token.
3. Call `POST /scans/analyze` with a subject and body, for example a suspicious
   text like *"Verify your bank account immediately by clicking this link"*.
4. The response contains the predicted label (safe/spam/phishing), the
   confidence score, and the probability of each class.
5. `GET /scans/{scan_request_id}` returns a saved scan (only your own).

---

## Using the App

1. Start the backend (`uvicorn app.main:app --reload` in `backend/`)
2. Start the frontend (`npm run dev` in `frontend/`)
3. Open `http://localhost:5173`, register or log in
4. Open the **Scanner** page, paste an email subject and body, click **Scan Email**
5. The result appears with the predicted label (safe/spam/phishing), the
   confidence, and a score bar per class — and the notification bell in the
   navbar receives a live notification
6. The **Dashboard** shows your totals per label and the latest result
7. The **History** page lists all your previous scans, newest first

The ML model file must exist at `backend/app/ml/mail_detection_pipeline.joblib`.
If it is missing, the scanner shows the backend error
"ML model is not available..." — copy the file as described in "ML Model Setup".

---

## Advanced Search

Logged-in users can search across five lists from the **Search** page
(`/search` in the frontend, `GET /search` in the API):

- **Scans** — filter by text, predicted label (safe/spam/phishing), status, dates
- **Email Messages** — text and date filters
- **Notifications** — text and date filters
- **Reports** — text and date filters
- **CMS Pages** — public content, only published pages are searched

All searches support sorting (newest first by default) and return only the
current user's own data.

---

## Import and Export

The **Import/Export** page (`/import-export`) works for logged-in users:

- **Export** downloads a list as **CSV**, **JSON**, or **XLSX**:
  scans, email_messages, notifications, reports, cms_pages
- **Import** uploads a CSV/JSON/XLSX file into one of:
  email_messages, cms_pages, user_feedback, settings, notifications
- Invalid rows are skipped and reported in the import summary
  (imported/skipped counts); existing data is never overwritten
- Every import is recorded in the `import_jobs` table

---

## Dynamic Reports

On the **Reports** page (`/reports`) a logged-in user can generate reports
from their own scans:

- report types: **Scan Summary**, **Label Distribution**, **Phishing Activity**
- filters: date range and label (safe/spam/phishing)
- **Preview** shows the data without saving; **Save Report** stores the report
  with its filters in the `reports` / `report_filters` tables
- opening a saved report regenerates the data live from the stored filters

---

## Simple CMS

On the **CMS** page (`/cms`) a logged-in user manages static app content —
pages with ordered content blocks (this is content management, not business CRUD):

- create/edit/delete pages (title, slug, published flag)
- add/edit/delete text blocks with a sort order
- unpublished pages are drafts: hidden from the public endpoints
- if a published page with slug `home` exists, the homepage shows its blocks
  instead of the default static text (with automatic fallback)

---

## MongoDB and Real-Time Notifications

Besides PostgreSQL, the platform uses **MongoDB** for flexible log data:

- every scan saves the **full raw email** in the `raw_email_documents` collection
- and the **ML prediction payload** (label + all class scores) in `scan_payload_logs`
- structured data (users, scans, results, notifications) stays in PostgreSQL
- if MongoDB is not running, scans still work — only the raw logs are skipped

After every completed scan the backend also:

1. saves a notification in the `notifications` table (PostgreSQL)
2. pushes it **live** to the user through the WebSocket at
   `ws://localhost:8000/ws/notifications?user_id=<id>`

MongoDB must be running locally at `mongodb://localhost:27017` (change
`MONGODB_URL` in `backend/.env` if different).

**Test flow:**

1. Start PostgreSQL, MongoDB, and the backend
2. Register/login in Swagger (`http://localhost:8000/docs`) and click **Authorize**
3. Open a WebSocket client (e.g. the browser console or Postman) and connect to
   `ws://localhost:8000/ws/notifications?user_id=1`

   Browser console example:

   ```js
   const ws = new WebSocket("ws://localhost:8000/ws/notifications?user_id=1");
   ws.onmessage = (event) => console.log("Notification:", JSON.parse(event.data));
   ```

4. Call `POST /scans/analyze` in Swagger
5. The WebSocket client instantly receives the scan notification
6. `GET /notifications` shows the same notification saved in the database

---

## Authentication

The backend uses JWT authentication:

- `POST /auth/register` — create an account (first name, last name, email, password)
- `POST /auth/login` — returns an access token (30 min) and a refresh token (7 days)
- `POST /auth/refresh` — get a new token pair using the refresh token
- `POST /auth/logout` — revoke the refresh token
- `GET /auth/me` — returns the current user (protected)

Passwords are hashed with bcrypt. Refresh tokens are stored hashed in the
database. Auth actions are recorded in `audit_logs`.

To test it: open Swagger at `http://localhost:8000/docs`, register and log in,
then click **Authorize** and paste the access token to call protected endpoints.
See `docs/API_DOCUMENTATION.md` for details.

---

## Frontend Setup

Requires Node.js 18+.

```bash
cd frontend
npm install
copy .env.example .env       # Windows (or: cp .env.example .env)
npm run dev
```

The frontend runs at `http://localhost:5173`. The API URL comes from
`VITE_API_URL` in `frontend/.env` (default `http://localhost:8000`).

Pages available:

- `/` — home page with the project description
- `/register` — create an account (auto-login after registration)
- `/login` — log in with email and password
- `/dashboard` — protected page; opening it while logged out redirects to `/login`

To test: start the backend first, then register a new account from the frontend —
you land on the dashboard automatically. Logout from the navbar, then log in
again with the same credentials.

---

## Notes

- The full relational schema (26 tables) is in `database/schema.sql`; the design
  is explained in `docs/DATABASE_DESIGN.md` and `docs/ERD_NOTES.md`.
- Authentication (JWT), MongoDB setup, ML integration, and the remaining
  features will be completed in later commits.
- Documentation skeletons are in `docs/`.
