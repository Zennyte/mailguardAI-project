# Database Design - MailGuard AI Platform

## Two Databases

### PostgreSQL (relational)

PostgreSQL stores all structured data with fixed relationships: users, roles,
scans, results, reports, CMS pages, etc. It is the main database of the platform.
All 26 tables are normalized (3NF), connected with foreign keys, and indexed on
the columns that are queried most often.

### MongoDB (NoSQL)

MongoDB stores flexible data that does not fit well in fixed table columns.
PostgreSQL keeps the structured entities (users, scans, results, notifications);
MongoDB keeps the raw payloads — the full email text can be very large and
unstructured, so it fits a document store better than a SQL column.

Collections **in use now**:

| Collection             | Content                                              |
|------------------------|------------------------------------------------------|
| `raw_email_documents`  | Full raw email text (subject + body) per scan        |
| `scan_payload_logs`    | ML prediction payload per scan (label, all scores)   |

Planned as future extensions (documented, not implemented):

| Collection             | Content                                              |
|------------------------|------------------------------------------------------|
| `imported_batches`     | Raw rows of bulk imports before processing           |
| `report_snapshots`     | Generated report data as flexible JSON documents     |
| `cms_revision_logs`    | Old versions of CMS content after edits              |

If MongoDB is not running, the scan still works — only the raw log is skipped
with a warning. PostgreSQL remains the source of truth.

---

## The 26 SQL Tables (grouped by module)

### 1. Auth & Users (6 tables - required base tables)

| Table              | Purpose                                        |
|--------------------|------------------------------------------------|
| `users`            | User accounts (name, email, password hash)     |
| `roles`            | Roles: Admin, Manager, User                    |
| `user_roles`       | Many-to-many: which user has which role        |
| `permissions`      | Individual permissions (scan_email, ...)       |
| `role_permissions` | Many-to-many: which role has which permission  |
| `refresh_tokens`   | JWT refresh tokens per user                    |

### 2. System (4 tables - required base tables)

| Table           | Purpose                                            |
|-----------------|----------------------------------------------------|
| `audit_logs`    | Record of important actions (who did what, when)   |
| `notifications` | User notifications (also pushed live by WebSocket) |
| `settings`      | Global key/value application settings              |
| `files`         | Metadata of uploaded files                         |

### 3. Email Data (5 tables)

| Table               | Purpose                                    |
|---------------------|--------------------------------------------|
| `email_messages`    | The scanned email (subject, body preview)  |
| `email_headers`     | Headers of an email (one row per header)   |
| `email_recipients`  | Recipients (to/cc/bcc, one row each)       |
| `email_links`       | Links found in the email body              |
| `email_attachments` | Attachment metadata                        |

### 4. Scanning & ML (5 tables)

| Table                   | Purpose                                            |
|-------------------------|----------------------------------------------------|
| `scan_requests`         | A scan requested by a user (status, input type)    |
| `scan_results`          | Final result: predicted label + confidence         |
| `classification_scores` | Probability per class (safe/spam/phishing)         |
| `model_versions`        | Which ML model version produced the result         |
| `user_feedback`         | User feedback when a prediction looks wrong        |

### 5. Import / Export (2 tables)

| Table         | Purpose                                     |
|---------------|---------------------------------------------|
| `import_jobs` | Bulk email import jobs (progress, status)   |
| `export_jobs` | Data export jobs (CSV/JSON)                 |

### 6. Reports (2 tables)

| Table            | Purpose                              |
|------------------|--------------------------------------|
| `reports`        | Generated reports (name, type)       |
| `report_filters` | Filters applied to a report          |

### 7. CMS (2 tables)

| Table                | Purpose                                      |
|----------------------|----------------------------------------------|
| `cms_pages`          | Simple CMS pages (help, tips, announcements) |
| `cms_content_blocks` | Ordered content blocks inside a page         |

---

## The 10 Required Base Tables

The course requires these 10 tables, all included above:
`users`, `roles`, `user_roles`, `permissions`, `role_permissions`,
`refresh_tokens`, `audit_logs`, `notifications`, `settings`, `files`.

Together they cover authentication (JWT with refresh tokens), authorization
(role-based access control with permissions), auditing, notifications,
configuration, and file uploads.

---

## Design Standards

- **Primary keys**: every table has a `BIGSERIAL` primary key named `id`.
- **Foreign keys**: every relationship uses `REFERENCES`. Child rows of an email
  or scan are deleted together with their parent (`ON DELETE CASCADE`).
- **Indexes**: added on foreign key columns that are queried often
  (e.g. `user_id` on scans and notifications, `status` on scan requests,
  `predicted_label` on results). `UNIQUE` columns are indexed automatically.
- **Timestamps**: every table has `created_at` and `updated_at`.
- **created_by / updated_by**: only on tables managed by an administrator
  (`roles`, `permissions`, `settings`, `model_versions`, `cms_pages`) —
  the other tables already track their owner through `user_id`.
- **Normalization (3NF)**: repeated data is split into separate tables — for
  example email recipients are one row each instead of a comma-separated string,
  and per-class probabilities live in `classification_scores` instead of three
  columns in `scan_results`.

---

## Files

- Full SQL schema: [`database/schema.sql`](../database/schema.sql)
- Seed data (roles, permissions, settings, ML model row): [`database/seed.sql`](../database/seed.sql)
- SQLAlchemy models: `backend/app/models/`
- Relationships overview: [`ERD_NOTES.md`](ERD_NOTES.md)
