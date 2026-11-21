# MailGuard AI Platform: Complete Project Guide

This guide explains the whole project: what it does, how the pieces fit
together, what every directory and file is for, and **which part of the website
each file belongs to**. Read section 1 and 2 for the big picture, then use
sections 5 and 6 as a map when you open a file and wonder "what is this?".

Comments inside the code are written in Albanian; this guide is in English.

---

## 1. What the project does

A user registers, logs in, pastes an email (subject and body) into the
**Scanner** page and presses "Scan Email". A Machine Learning model decides if
the email is **safe**, **spam** or **phishing** and returns a confidence score
for each of the three labels. The result is saved, the user gets a live
notification, and the scan appears in the **History**. The user can also search
their data, export and import it, build reports, and (if Admin) edit the text
on the homepage through a small CMS.

## 2. The big picture

```
 BROWSER (React, port 5173)                      SERVER (FastAPI, port 8000)
 ┌──────────────────────────┐   HTTP + cookies   ┌─────────────────────────────┐
 │ pages  → components      │ ─────────────────► │ controller  (receives call) │
 │   ↓                      │                    │     ↓                       │
 │ api/*.js (axios)         │ ◄───────────────── │ service     (the logic)     │
 │                          │      JSON          │     ↓                       │
 │ NotificationBell         │ ◄── WebSocket ──── │ repository  (database)      │
 └──────────────────────────┘   (live alerts)    └──────┬───────────┬──────────┘
                                                        │           │
                                                  PostgreSQL     MongoDB
                                                  (26 tables)   (full emails,
                                                                 ML details)
                                              ML model: backend/app/ml/*.joblib
```

**Backend rule:** every request flows `controller → service → repository`.
- *Controller*: receives the HTTP request, checks who is calling, passes it on.
  Contains no logic.
- *Service*: the actual logic (for example "scan an email, save it, notify the user").
- *Repository*: the only place that talks to the database.

**Frontend rule:** `page → api file → backend controller`. Pages show things
and react to clicks; `api/` files are the only code that calls the backend.

**Two databases:** PostgreSQL stores structured, related data (users, scans,
reports...). MongoDB stores big flexible data (the full email text and the full
ML prediction). If MongoDB is down, scanning still works; only these logs are skipped.

## 3. How login security works

Login tokens are **never stored where JavaScript can read them**.

1. `POST /auth/login` checks the password and the backend sets two cookies:
   - `access_token`, a JWT valid for 30 minutes, sent with every request;
   - `refresh_token`, a random string valid for 7 days, sent only to `/auth/...`.
2. Both cookies are **`HttpOnly`**: a malicious script injected into the page
   (XSS) cannot read or steal them. They are **`SameSite=Lax`**: other websites
   cannot make the browser send them along (protects against CSRF). In
   production set `COOKIE_SECURE=true` so they only travel over HTTPS.
3. The frontend never touches a token. `axios` is configured with
   `withCredentials: true`, so the browser attaches the cookies by itself.
4. When the access token expires, the next request gets a `401`. `apiClient.js`
   automatically calls `POST /auth/refresh` (which swaps the refresh token for a
   new pair and revokes the old one), then repeats the failed request. The user
   notices nothing.
5. The refresh token is stored in the database only as a SHA-256 hash.
6. After a page reload the frontend asks `GET /auth/me`. If the cookies are
   still valid the user is still logged in.
7. The WebSocket for notifications also uses the cookie, and the server
   additionally checks that the connection comes from our own website
   (`Origin` check).

**Roles and permissions:** a user has roles (`Admin`, `Manager`, `User`), a role
has permissions (`scan_email`, `manage_cms`, `import_data`, ...). The backend
checks permissions (`require_permission("manage_cms")`); the frontend only
hides buttons and links the user may not use (`userHasPermission(user, ...)`).
Hiding is for convenience; the backend is what actually enforces it.

## 4. The main flow, step by step (Scanner page)

1. `pages/ScannerPage.jsx`: the user presses "Scan Email" and calls `api/scanApi.js → scanEmail()`.
2. `POST /scans/analyze` arrives at `controllers/scan_controller.py`.
3. `services/scan_service.py → scan_email()` runs five steps:
   1. `ml_model_service.predict_email()`: the ML model returns the label and probabilities;
   2. `scan_repository.save_completed_scan()`: saved in PostgreSQL (4 tables);
   3. `scan_log_repository`: full email and prediction saved in MongoDB;
   4. `notification_service.notify_scan_completed()`: notification saved and pushed over WebSocket;
   5. `ai_explanation_service.explain_scan_result()`: optional AI explanation.
4. The result returns to the page, which shows it with `components/ScanResultCard.jsx`.
5. At the same moment the WebSocket message reaches `components/NotificationBell.jsx` and the bell updates.

---

## 5. Backend: every directory and file

All backend code is in `backend/`. Run with `uvicorn app.main:app --reload`.

### `backend/` (root files)

| File | What it is |
|---|---|
| `requirements.txt` | The Python packages to install (`pip install -r requirements.txt`). |
| `.env` | Your local settings: secret key, database URLs, optional Groq API key, `COOKIE_SECURE`. **Never commit it.** |
| `.env.example` | The same file with safe example values. Copy it to `.env` to start. |

### `backend/app/` (the application)

| File | What it does | Website part |
|---|---|---|
| `main.py` | Creates the FastAPI app, allows only our frontend (CORS) and plugs in every controller. Start reading here. | Whole backend |
| `create_tables.py` | One-time script that creates all 26 tables in PostgreSQL (`python -m app.create_tables`). | Setup |

### `backend/app/controllers/` (the API endpoints, "the doors")

One file per part of the website. Each endpoint has a comment with its URL and
the button or page that uses it.

| File | Endpoints | Website part |
|---|---|---|
| `auth_controller.py` | register, login, refresh, logout, me | **Login**, **Register** pages, **Logout** button |
| `scan_controller.py` | analyze, history list, stats | **Scanner**, **History**, **Dashboard** pages |
| `notification_controller.py` | list notifications, mark as read | **Notification bell** (top right) |
| `notification_websocket_controller.py` | live WebSocket connection | **Notification bell** (live updates) |
| `search_controller.py` | search across 5 lists | **Search** page |
| `import_export_controller.py` | export a list, import a file | **Import/Export** page |
| `report_controller.py` | preview, save, list, open reports | **Reports** page |
| `cms_controller.py` | read a public page; create/edit/delete pages and blocks | **CMS** page; **Homepage** (reads the `home` page) |
| `health_controller.py` | `GET /health` | Not on the website; checks the server is alive |

### `backend/app/services/` (the logic, "the brain")

| File | What it does | Website part |
|---|---|---|
| `auth_service.py` | Register, login, token refresh, logout, builds the user with roles and permissions. | Login, Register, Logout |
| `scan_service.py` | The main flow (section 4), history and dashboard numbers. | Scanner, History, Dashboard |
| `ml_model_service.py` | Loads the `.joblib` model once and predicts safe/spam/phishing. | Scanner |
| `ai_explanation_service.py` | Asks Groq for a short explanation of the result (only if `GROQ_API_KEY` is set). | Scanner ("Why? (AI explanation)") |
| `notification_service.py` | Saves a notification and pushes it live to the user. | Notification bell |
| `search_service.py` | Chooses the right query for one of the 5 lists and shapes the rows. Also used by export. | Search, Import/Export |
| `export_service.py` | Turns a list into a CSV, JSON or XLSX file. | Import/Export ("Export") |
| `import_service.py` | Reads a CSV/JSON/XLSX file and inserts the valid rows of one of 5 lists. | Import/Export ("Import") |
| `report_service.py` | Calculates the 3 report types and saves/reopens reports. | Reports |
| `cms_service.py` | Rules for CMS pages and blocks (unique slugs, published only for the public). | CMS, Homepage |

### `backend/app/repositories/` (database access, "the hands")

| File | What it does | Website part |
|---|---|---|
| `user_repository.py` | Find/create users, roles and permissions of a user. | Login, Register, permissions everywhere |
| `refresh_token_repository.py` | Save, validate and revoke refresh tokens (as hashes). | Login, silent token renewal, Logout |
| `audit_log_repository.py` | Writes register/login/logout to `audit_logs`. | Login, Register, Logout |
| `scan_repository.py` | Saves a scan across 4 tables, history, counts per label. | Scanner, History, Dashboard |
| `scan_log_repository.py` | Saves full email text and prediction details in MongoDB. | Scanner |
| `notification_repository.py` | Create/list/mark-read notifications. | Notification bell |
| `search_repository.py` | One query function per searchable list (shared helpers for text, dates, sorting). | Search, Export |
| `report_repository.py` | Saved reports and the counting queries behind them. | Reports |
| `cms_repository.py` | CMS pages and content blocks. | CMS, Homepage |

### `backend/app/models/` (the database tables as Python classes)

Together they define the 26 tables. They mirror `database/schema.sql`.

| File | Tables | Used for |
|---|---|---|
| `user.py` | `users` | Accounts |
| `roles_and_permissions.py` | `roles`, `user_roles`, `permissions`, `role_permissions` | Who may do what |
| `refresh_token.py` | `refresh_tokens` | Staying logged in |
| `audit_log.py` | `audit_logs` | Record of register/login/logout |
| `email.py` | `email_messages`, `email_headers`, `email_recipients`, `email_links`, `email_attachments` | The scanned emails |
| `scan.py` | `model_versions`, `scan_requests`, `scan_results`, `classification_scores`, `user_feedback` | Scans and their results |
| `notification.py` | `notifications` | Notification bell |
| `report.py` | `reports`, `report_filters` | Reports |
| `cms.py` | `cms_pages`, `cms_content_blocks` | CMS |
| `setting.py` | `settings` | Global key/value settings |
| `import_export_job.py` | `import_jobs`, `export_jobs` | A record of each import/export |
| `uploaded_file.py` | `files` | File metadata (reserved for future use) |
| `__init__.py` | – | Lets other files write `from app.models import User, ScanRequest` |

### `backend/app/schemas/` (the shape of requests and responses)

Pydantic classes that validate incoming data (a password must have 8+
characters) and define what the API returns. The names say the page:
`auth.py` (Login/Register), `scan.py` (Scanner/History/Dashboard),
`notification.py` (bell), `search.py` (Search), `import_export.py`
(Import/Export), `report.py` (Reports), `cms.py` (CMS).

### `backend/app/core/` (shared building blocks)

| File | What it does |
|---|---|
| `config.py` | Reads `.env` into one `settings` object used everywhere. |
| `database.py` | The PostgreSQL connection and `get_db()`, which gives each request its own session. |
| `mongo.py` | The MongoDB connection. |
| `security.py` | Password hashing (bcrypt), creating and reading the JWT access token, generating and hashing refresh tokens. |
| `cookies.py` | Sets and clears the two login cookies (`HttpOnly`, `SameSite`). Section 3. |
| `auth_dependencies.py` | `get_current_user` (who is calling?) and `require_permission(...)` (may they do this?). Used by controllers. |
| `constants.py` | The three email labels shared by the backend. |

### `backend/app/websockets/`

`notification_connections.py` keeps the open WebSocket connection of each
logged-in user so the server can push a notification to them.

### `backend/app/ml/`

`mail_detection_pipeline.joblib` is the trained model exported from the
`mailguard-ml` project (TF-IDF + Logistic Regression). The platform never
retrains it; it only loads it. Refresh it by copying a new file here.

---

## 6. Frontend: every directory and file

All frontend code is in `frontend/`. Run with `npm run dev`.

### `frontend/` (root files)

| File | What it is |
|---|---|
| `index.html` | The single HTML page. Its `<title>` is the browser tab name. |
| `package.json` | The list of JavaScript packages and the `npm run dev/build` commands. |
| `vite.config.js` | Settings for Vite (the dev server) and Tailwind. |
| `.env` / `.env.example` | `VITE_API_URL` and `VITE_WS_URL`, the addresses of the backend. |

### `frontend/src/` (top level)

| File | What it does |
|---|---|
| `main.jsx` | Starts React and mounts `App` into the page. |
| `App.jsx` | On load asks the backend "am I still logged in?", then shows the routes. |
| `index.css` | **All colours** (the `@theme` block) and the reusable CSS classes (`card`, `btn-primary`, `input-field`...). |

### `frontend/src/config/` (things you change often, all in one place)

These four files are the place to edit content without touching page code.

| File | What you can change there |
|---|---|
| `emailLabels.js` | **The order of safe/spam/phishing everywhere** (one line, `LABEL_ORDER`), plus each label's title, description, result message, example score and colour classes. |
| `siteText.js` | The brand name, tagline, default homepage intro, example email and footer text. |
| `menuLinks.js` | The sidebar menu: add, remove or reorder links, or require a permission. |
| `dropdownOptions.js` | The options of dropdowns in Search, Import/Export and Reports (lists, formats, report types, sort order). |

Examples:
- Swap the order of spam and phishing: edit `LABEL_ORDER` in `emailLabels.js`.
- Rename "Scanner" in the menu: edit `menuLinks.js`.
- Change the green of "safe": edit `--color-safe` in `index.css`.
- Add a report type: add it in `dropdownOptions.js` *and* in the backend `report_service.py`.

### `frontend/src/pages/` (one file per page of the website)

| File | URL | What the user sees |
|---|---|---|
| `HomePage.jsx` | `/` | Public intro, example result, three label cards. Text from the CMS `home` page if published. |
| `LoginPage.jsx` | `/login` | Login form. |
| `RegisterPage.jsx` | `/register` | Registration form. |
| `DashboardPage.jsx` | `/dashboard` | Number cards: total scans, count per label, latest scan. |
| `ScannerPage.jsx` | `/scanner` | Form to paste an email (left) and the result card (right). |
| `ScanHistoryPage.jsx` | `/history` | Table of previous scans. |
| `SearchPage.jsx` | `/search` | Filters on top, results table below. |
| `ImportExportPage.jsx` | `/import-export` | "Export data" card and "Import data" card. |
| `ReportsPage.jsx` | `/reports` | Report form, the numbers, and the saved reports list. |
| `CmsManagementPage.jsx` | `/cms` | Admin only: list, create and edit content pages. |

### `frontend/src/components/` (pieces used inside pages)

| File | What it is | Used in |
|---|---|---|
| `AppLogo.jsx` | The "MailGuard AI" logo | Navbar, sidebar |
| `EmailLabelBadge.jsx` | Small coloured tag (safe/spam/phishing) | Dashboard, History, Search, Reports, Scanner, Homepage |
| `LabelScoreBar.jsx` | One bar: label name, coloured bar, percentage | Scanner result, Homepage example |
| `ScanResultCard.jsx` | The whole "Result" card | Scanner |
| `NotificationBell.jsx` | The bell with the unread count and dropdown list; opens the WebSocket | Top bar after login |
| `form/FormField.jsx` | A label above an input | Search, Reports, Import/Export |
| `form/SelectField.jsx` | A label plus a dropdown | Search, Reports, Import/Export |
| `search/SearchForm.jsx` | The filter form | Search |
| `search/SearchResultsTable.jsx` | The results table | Search |
| `importExport/ExportCard.jsx` | The export card | Import/Export |
| `importExport/ImportCard.jsx` | The import card and result message | Import/Export |
| `reports/ReportForm.jsx` | Type, dates, label, Preview and Save buttons | Reports |
| `reports/ReportNumbers.jsx` | Number cards and the distribution table | Reports |
| `reports/SavedReportsList.jsx` | The "Saved reports" list | Reports |
| `cms/ContentPageList.jsx` | The "Pages" list | CMS |
| `cms/NewContentPageForm.jsx` | The "New page" form | CMS |
| `cms/ContentPageEditor.jsx` | The "Edit page" card with its text blocks | CMS |

### `frontend/src/layouts/` (the frame around every page)

| File | What it is |
|---|---|
| `MainLayout.jsx` | Chooses which frame to use: logged in or not. |
| `VisitorLayout.jsx` | Frame for visitors: top navbar (Login, Register) and footer. |
| `LoggedInLayout.jsx` | Frame after login: sidebar, top bar with the bell, mobile menu, Logout. |

### `frontend/src/routes/`

| File | What it does |
|---|---|
| `AppRoutes.jsx` | The map: which URL shows which page. |
| `RequireLogin.jsx` | Protects pages: sends visitors to `/login`, and optionally requires a permission (CMS needs `manage_cms`). |

### `frontend/src/api/` (every call to the backend)

One file per backend controller. A page never calls `axios` directly.

| File | Calls | Backend controller |
|---|---|---|
| `apiClient.js` | The shared axios client: sends cookies, **silently renews expired logins**, and has `getErrorMessage()`. | – |
| `authApi.js` | register, login, me, logout | `auth_controller.py` |
| `scanApi.js` | scan, history, stats | `scan_controller.py` |
| `notificationApi.js` | list, mark as read, open the live WebSocket | `notification_*controller.py` |
| `searchApi.js` | search | `search_controller.py` |
| `importExportApi.js` | download export, upload import | `import_export_controller.py` |
| `reportApi.js` | preview, save, list, open | `report_controller.py` |
| `cmsApi.js` | pages and blocks | `cms_controller.py` |

### `frontend/src/store/`

`authStore.js` is the global "who is logged in" state (Zustand). It holds the
`user` and has `checkLogin`, `login`, `register`, `logout`. Also exports
`userHasPermission(user, "manage_cms")`. It stores **no tokens**.

### `frontend/src/utils/`

`formatting.js` decides how dates (`formatDateTime`) and percentages
(`formatPercent`) are shown everywhere.

---

## 7. Other top-level directories

| Path | What it is |
|---|---|
| `database/schema.sql` | The full SQL definition of the 26 tables (same as the Python models). |
| `database/seed.sql` | Starting data: roles, permissions, which role has which permission, settings, the ML model row. **Run it before registering users.** |
| `docs/ERD.png`, `ERD.drawio`, `ERD.mmd` | The database diagram (image, editable draw.io file, text/Mermaid version). |
| `README.md` | How to install and run. |
| `PROJECT_GUIDE.md` | This file. |
| `.gitignore` | Files git must not track (`.env`, `venv`, `node_modules`). |

## 8. The five course features and where they live

| Feature | Backend | Frontend page |
|---|---|---|
| Machine Learning integration | `ml_model_service.py`, `scan_service.py` | Scanner |
| Advanced search | `search_controller/service/repository.py` | Search |
| Import / Export | `import_export_controller.py`, `import_service.py`, `export_service.py` | Import/Export |
| Dynamic reports | `report_controller/service/repository.py` | Reports |
| Simple CMS | `cms_controller/service/repository.py` | CMS and Homepage |

## 9. Common changes: where to go

| I want to... | Edit this |
|---|---|
| Reorder safe / spam / phishing | `frontend/src/config/emailLabels.js` → `LABEL_ORDER` |
| Change a label's wording or colour classes | `frontend/src/config/emailLabels.js` |
| Change the site name or homepage text | `frontend/src/config/siteText.js` |
| Add or hide a menu link | `frontend/src/config/menuLinks.js` |
| Change a dropdown's choices | `frontend/src/config/dropdownOptions.js` |
| Change the colours of the whole site | `frontend/src/index.css` (`@theme`) |
| Change how dates are shown | `frontend/src/utils/formatting.js` |
| Change how long a login lasts | `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS` in `backend/.env` |
| Make a role able to do something new | `database/seed.sql` (role ↔ permission), then protect the endpoint with `require_permission("...")` |
| Add a new page | 1) page in `pages/`, 2) route in `AppRoutes.jsx`, 3) link in `menuLinks.js`, 4) an `api/` file, 5) a controller → service → repository on the backend |
