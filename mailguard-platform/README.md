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

In a later commit, this file will be copied to `backend/app/ml/` and the backend
will load it to classify emails.

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

## Frontend Setup

Requires Node.js 18+.

```bash
cd frontend
npm install
copy .env.example .env       # Windows (or: cp .env.example .env)
npm run dev
```

The frontend runs at `http://localhost:5173` and shows the starter page with a
live backend status check (Online/Offline).

---

## Notes

- Database setup (PostgreSQL + MongoDB), authentication, ML integration, and the
  remaining features will be completed in later commits.
- The planned 26 relational tables are listed in `database/schema.sql`.
- Documentation skeletons are in `docs/`.
