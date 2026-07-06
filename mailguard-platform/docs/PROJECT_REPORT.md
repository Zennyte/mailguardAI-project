# Project Report - MailGuard AI Platform

Raporti i projektit per Lab Course 2.

## 1. Introduction

MailGuard AI Platform is a full-stack web application that scans emails and
tells the user whether they are **safe**, **spam**, or **phishing**. The user
pastes an email, the backend runs a Machine Learning model over the text, and
the result is saved, pushed live as a notification, and available later in the
scan history.

## 2. Project Goal

The goal was to build a complete, working platform that satisfies the Lab
Course 2 requirements (full stack, SQL + NoSQL databases, 24+ relational
tables, layered architecture, JWT auth, real-time communication, and several
additional features) — while reusing the model trained in our Machine Learning
course project instead of building the ML part from zero.

## 3. Technologies Used

- **Backend:** Python, FastAPI, SQLAlchemy, pymongo, python-jose (JWT), bcrypt
- **Frontend:** React with Vite, Tailwind CSS, Zustand, React Router, axios
- **Databases:** PostgreSQL (relational) and MongoDB (NoSQL)
- **ML:** scikit-learn pipeline (TF-IDF + Logistic Regression) exported with joblib
- **Real-time:** FastAPI native WebSockets

## 4. System Architecture

The backend follows a simple three-layer architecture:

```
controller (HTTP route) → service (business logic) → repository (database access)
```

Controllers only receive and return HTTP data; services contain the logic
(e.g. calling the ML model, building report data); repositories are the only
layer that talks to the databases. Pydantic schemas validate every request and
response. The frontend is a React single-page app that talks to the backend
through a small axios API layer, keeps auth state in a Zustand store, and
protects private pages with a `ProtectedRoute` component.

## 5. Database Design

PostgreSQL holds 26 normalized (3NF) tables grouped into: auth and users,
system, email data, scanning and ML, import/export, reports, and CMS. Every
table has a `BIGSERIAL` primary key, foreign keys, `created_at`/`updated_at`
timestamps, and indexes on frequently queried columns. The 10 required base
tables (users, roles, user_roles, permissions, role_permissions,
refresh_tokens, audit_logs, notifications, settings, files) are all included.

MongoDB complements PostgreSQL for flexible payloads: the full raw email text
(`raw_email_documents`) and the ML prediction payload (`scan_payload_logs`)
per scan. Details: `DATABASE_DESIGN.md`; relationships: `ERD_NOTES.md` and
the Mermaid diagram `ERD.mmd`.

## 6. Authentication and Security

- Registration and login with **JWT**: short-lived access tokens (30 min) and
  refresh tokens (7 days) with rotation on refresh
- Passwords hashed with **bcrypt**; refresh tokens stored **hashed** in the DB
- Role-based foundation: users get the `User` role; roles map to permissions
  (`user_roles`, `role_permissions` tables), with `require_role` /
  `require_permission` dependencies available
- Input validation with Pydantic (e.g. email format, password length)
- **CORS** restricted to the frontend URL; all secrets in `.env` files
- Auth actions (register/login/logout) recorded in `audit_logs`

## 7. Machine Learning Integration

The ML course project exported a scikit-learn pipeline (TF-IDF vectorizer +
Logistic Regression, accuracy 0.9913 on the test set). The backend loads the
`.joblib` file once, on the first scan, and keeps it in memory. For each scan
the subject and body are combined into one text — the same way the model was
trained — and `predict()` + `predict_proba()` return the label and the
confidence per class. Every scan is stored across four tables
(`email_messages`, `scan_requests`, `scan_results`, `classification_scores`)
and logged in MongoDB. The platform never retrains the model.

## 8. Real-Time Notifications

After each completed scan the backend creates a notification row in PostgreSQL
and pushes the same notification instantly through a WebSocket
(`/ws/notifications`) to the connected user — no polling. The frontend
notification bell listens on this socket, shows an unread counter, and lets
the user mark notifications as read.

## 9. Additional Features

1. **Machine Learning Integration** — described above.
2. **Advanced Search** — one endpoint (`GET /search`) covering 5 lists (scans,
   email messages, notifications, reports, CMS pages) with text, label,
   status, and date filters plus sorting. Users only see their own data.
3. **Data Import/Export** — 5 lists exportable as CSV/JSON/XLSX; 5 lists
   importable from the same formats with per-row validation, skip counts, and
   an `import_jobs` record per import.
4. **Dynamic Report Generation** — 3 report types (scan summary, label
   distribution, phishing activity) filtered by date range and label. Saved
   reports store only their filters, so opening one regenerates fresh data.
5. **Simple CMS** — management of static app content (not business CRUD):
   pages with ordered text blocks, draft/published states, and a live example —
   a published page with slug `home` replaces the homepage text.

## 10. Frontend Overview

Pages: Home (public, CMS-aware), Login/Register, Dashboard (stats cards),
Scanner (scan form + result with score bars), History (scan table), Search,
Import/Export, Reports, and CMS management. A shared layout provides the
navbar with the notification bell. Auth state (tokens + current user) lives in
a small Zustand store; tokens are kept in localStorage and attached to every
API call by an axios interceptor.

## 11. Backend Overview

Eight controllers (health, auth, scans, notifications, websocket, search,
data transfer, reports, CMS) map one-to-one to services, which use
repositories for PostgreSQL (SQLAlchemy ORM) and MongoDB (pymongo). The
`create_tables.py` script creates all 26 tables locally, and `seed.sql` loads
roles, permissions, settings, and the active ML model version.

## 12. Limitations

- The WebSocket identifies the user by a `user_id` query parameter instead of
  validating the JWT — simplified on purpose, documented in the API docs.
- CMS management currently requires any logged-in user; restricting it to an
  Admin role is one line (`require_permission("manage_cms")`) once an admin
  account exists.
- Token storage in localStorage is acceptable for a student project but a
  production app would consider httpOnly cookies.
- The MongoDB collections `imported_batches`, `report_snapshots`, and
  `cms_revision_logs` are documented as planned extensions and not implemented.

## 13. Future Improvements

- Admin panel for user/role management using the existing RBAC tables
- JWT validation in the WebSocket connection
- Scanning uploaded `.eml` files (the `files` and `email_attachments` tables
  are ready for it)
- Retraining pipeline that promotes a new row in `model_versions`
- Charts on the dashboard and in reports

## 14. Conclusion

The project delivers a complete, working full-stack platform that combines a
trained ML model with a modern web stack: FastAPI + React, PostgreSQL + MongoDB,
JWT security, real-time WebSockets, and five additional features — all kept
deliberately simple, layered, and explainable.
