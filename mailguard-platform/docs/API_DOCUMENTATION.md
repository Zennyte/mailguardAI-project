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

### Scans

_To be added in a later commit._

### Notifications

_To be added in a later commit._

### Reports

_To be added in a later commit._

### CMS

_To be added in a later commit._
