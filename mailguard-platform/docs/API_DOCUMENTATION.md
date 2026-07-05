# API Documentation - MailGuard AI Platform

Dokumentimi i API-se do te plotesohet gjate zhvillimit.

FastAPI generates interactive documentation automatically at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### Health

| Method | Path      | Description                    |
|--------|-----------|--------------------------------|
| GET    | `/health` | Check that the backend is running |

### Auth

| Method | Path             | Auth required | Description                                        |
|--------|------------------|---------------|----------------------------------------------------|
| POST   | `/auth/register` | No            | Create a new account (gets the default role `User`) |
| POST   | `/auth/login`    | No            | Returns an access token and a refresh token       |
| POST   | `/auth/refresh`  | No            | Exchanges a valid refresh token for a new token pair |
| POST   | `/auth/logout`   | Yes           | Revokes the given refresh token                    |
| GET    | `/auth/me`       | Yes           | Returns the current logged-in user with roles     |

**How authentication works:**

1. `POST /auth/login` with email and password returns two tokens.
2. The short-lived **access token** (JWT, 30 min) is sent on every request in the
   header: `Authorization: Bearer <access_token>`.
3. When the access token expires, `POST /auth/refresh` with the long-lived
   **refresh token** (7 days) returns a new pair. The old refresh token is
   revoked (rotation).
4. `POST /auth/logout` revokes the refresh token so it cannot be used again.

Refresh tokens are stored **hashed** in the `refresh_tokens` table, never in
plain text. Register, login, and logout are recorded in `audit_logs`.

**Testing in Swagger** (`http://localhost:8000/docs`):

1. Call `POST /auth/register`, then `POST /auth/login` and copy the `access_token`.
2. Click the **Authorize** button (top right) and paste the token.
3. Now the protected endpoints like `GET /auth/me` work.

**Testing from the frontend** (`http://localhost:5173`):

- Register a user from the `/register` page — after registration the frontend
  logs in automatically and opens the dashboard.
- Login works from the `/login` page.
- Protected pages (require login, otherwise redirect to `/login`):
  - `/dashboard` — scan statistics cards and quick links
  - `/scanner` — scan an email and see the result with confidence scores
  - `/history` — table of previous scans, newest first
- The notification bell in the navbar shows live notifications (WebSocket)
  and lets you mark them as read.

### Scans

| Method | Path                  | Auth required | Description                                  |
|--------|-----------------------|---------------|----------------------------------------------|
| POST   | `/scans/analyze`      | Yes (JWT)     | Scan an email with the ML model              |
| GET    | `/scans`              | Yes (JWT)     | Scan history of the current user, newest first |
| GET    | `/scans/stats`        | Yes (JWT)     | Simple stats: total/safe/spam/phishing counts + latest label |
| GET    | `/scans/{scan_id}`    | Yes (JWT)     | Get a saved scan result (own scans only)     |

**Note:** the model file must exist at
`backend/app/ml/mail_detection_pipeline.joblib`, otherwise the endpoint
returns `503 ML model is not available`.

**Request example** (`POST /scans/analyze`):

```json
{
  "subject": "Urgent: your account will be suspended",
  "body": "Dear customer, verify your bank account immediately by clicking this link.",
  "input_type": "manual"
}
```

**Response example:**

```json
{
  "scan_request_id": 1,
  "predicted_label": "phishing",
  "confidence_score": 0.9994,
  "scores": [
    { "label": "phishing", "score": 0.9994 },
    { "label": "safe", "score": 0.0001 },
    { "label": "spam", "score": 0.0005 }
  ],
  "message": "Warning: this email looks like a phishing attempt!"
}
```

Every scan is saved in PostgreSQL: the email in `email_messages`, the request
in `scan_requests`, the result in `scan_results`, and the probability of each
class in `classification_scores`.

### Notifications

| Method | Path                                  | Auth required | Description                          |
|--------|---------------------------------------|---------------|--------------------------------------|
| GET    | `/notifications`                      | Yes (JWT)     | List current user notifications      |
| PATCH  | `/notifications/{notification_id}/read` | Yes (JWT)  | Mark one notification as read        |

Notifications are created automatically when a scan completes, for example:

```json
{
  "id": 1,
  "title": "Email scan completed",
  "message": "The email was classified as phishing with 99% confidence.",
  "notification_type": "scan_completed",
  "is_read": false,
  "created_at": "2026-07-05T14:30:00"
}
```

### WebSocket (real-time notifications)

Connect to:

```
ws://localhost:8000/ws/notifications?user_id=1
```

While connected, every completed scan pushes a JSON notification instantly —
no polling. The same notification is also saved in the `notifications` table,
so it is not lost if the user was offline.

**Note:** for simplicity in this student project the WebSocket identifies the
user with a `user_id` query parameter. A production system should validate the
JWT token in the WebSocket connection as well.

### Reports

_To be added in a later commit._

### CMS

_To be added in a later commit._
