# API Documentation - MailGuard AI Platform

Dokumentimi i plote i API-se, me shembuj per cdo grup endpointesh.

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

### Advanced Search

| Method | Path      | Auth required | Description                       |
|--------|-----------|---------------|-----------------------------------|
| GET    | `/search` | Yes (JWT)     | Search across 5 application lists |

Query parameters:

- `entity` (required): `scans`, `email_messages`, `notifications`, `reports`, `cms_pages`
- `q`: text query (searched in subject/body, title/message, name, slug — depending on entity)
- `label`: `safe` / `spam` / `phishing` (scans only)
- `status`: scan status (scans only)
- `date_from`, `date_to`: date range (inclusive)
- `sort_by`: `created_at` (default) or `id`
- `sort_order`: `desc` (default) or `asc`
- `limit`: max results (default 50)

Example:

```
/search?entity=scans&q=invoice&label=phishing&date_from=2026-01-01&date_to=2026-12-31&sort_order=desc
```

Users only see their own data. `cms_pages` is the exception — it is public
content, so only **published** pages are searchable.

### Import / Export

| Method | Path                     | Auth required | Description                          |
|--------|--------------------------|---------------|--------------------------------------|
| GET    | `/data/export/{entity}`  | Yes (JWT)     | Download a list as a file            |
| POST   | `/data/import/{entity}`  | Yes (JWT)     | Upload a file and import its rows    |

**Export** — entities: `scans`, `email_messages`, `notifications`, `reports`,
`cms_pages`. Formats via `?format=`: `csv`, `json`, `xlsx`. The response is a
downloadable file with the current user's data.

**Import** — entities: `email_messages`, `cms_pages`, `user_feedback`,
`settings`, `notifications`. The uploaded file can be `.csv`, `.json`, or
`.xlsx` (format detected from the extension). Invalid rows are skipped, and the
response is a summary:

```json
{ "entity": "email_messages", "imported_count": 10, "skipped_count": 2,
  "message": "Imported 10 rows, skipped 2 invalid rows." }
```

Import rules: required fields are validated per entity (e.g. `body` for emails,
`title`+`slug` for CMS pages); duplicate slugs and existing settings keys are
skipped, never overwritten; users and passwords cannot be imported. Every
import creates a row in the `import_jobs` table.

### Reports

| Method | Path                    | Auth required | Description                                  |
|--------|-------------------------|---------------|----------------------------------------------|
| GET    | `/reports/preview`      | Yes (JWT)     | Generate report data without saving          |
| POST   | `/reports`              | Yes (JWT)     | Generate and save a report with its filters  |
| GET    | `/reports`              | Yes (JWT)     | List current user's saved reports            |
| GET    | `/reports/{report_id}`  | Yes (JWT)     | Get a saved report (data regenerated live)   |

Report types: `scan_summary`, `label_distribution`, `phishing_activity`.
Filters: `date_from`, `date_to`, `label` — reports are dynamic because the
data is computed from the user's scans using the chosen filters.

**Request example** (`POST /reports`):

```json
{
  "report_name": "Monthly phishing report",
  "report_type": "phishing_activity",
  "date_from": "2026-01-01",
  "date_to": "2026-12-31"
}
```

**Response example:**

```json
{
  "id": 1,
  "report_name": "Monthly phishing report",
  "report_type": "phishing_activity",
  "created_at": "2026-07-06T17:32:08",
  "filters": [
    { "filter_key": "date_from", "filter_value": "2026-01-01" },
    { "filter_key": "date_to", "filter_value": "2026-12-31" }
  ],
  "data": {
    "total_scans": 3,
    "phishing_count": 1,
    "phishing_percentage": 33.3,
    "average_phishing_confidence": 0.9994,
    "last_phishing_at": "2026-07-06 17:30:00"
  }
}
```

The filters are saved in the `report_filters` table. Opening a saved report
regenerates the data from those filters, so the numbers are always current.

### CMS

The CMS manages static app content (homepage text, phishing tips, help pages)
— it is not business CRUD.

**Public endpoints** (no login needed, published pages only):

| Method | Path                 | Description                        |
|--------|----------------------|------------------------------------|
| GET    | `/cms/pages`         | List published pages with blocks   |
| GET    | `/cms/pages/{slug}`  | Get one published page by slug     |

**Protected endpoints** (JWT required):

| Method | Path                            | Description                          |
|--------|---------------------------------|--------------------------------------|
| GET    | `/cms/pages/manage`             | List all pages, including drafts     |
| POST   | `/cms/pages`                    | Create a page (title, slug, is_published) |
| PUT    | `/cms/pages/{page_id}`          | Update a page                        |
| DELETE | `/cms/pages/{page_id}`          | Delete a page (blocks cascade)       |
| POST   | `/cms/pages/{page_id}/blocks`   | Add a content block                  |
| PUT    | `/cms/blocks/{block_id}`        | Update a block                       |
| DELETE | `/cms/blocks/{block_id}`        | Delete a block                       |

Blocks are returned ordered by `sort_order`. Slugs must be unique.

**Note:** management endpoints currently require any logged-in user. In a real
production system they would be restricted with the existing role/permission
system (e.g. `require_permission("manage_cms")`) — kept simple on purpose for
this student project.

If a published page with slug `home` exists, the frontend homepage shows its
content blocks instead of the default static text.
