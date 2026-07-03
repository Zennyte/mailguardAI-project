# Database Design - MailGuard AI Platform

Dizajni i detajuar i databazes do te plotesohet kur te krijohet skema e plote.

## Databases

- **PostgreSQL** - relational data (users, scans, reports, CMS, ...)
- **MongoDB** - flexible/NoSQL data (raw email content, logs, ...)

## Planned Tables (26)

The full list of planned tables is in [`database/schema.sql`](../database/schema.sql).

Groups:

1. Auth & users (users, roles, user_roles, permissions, role_permissions, refresh_tokens)
2. System (audit_logs, notifications, settings, files)
3. Email data (email_messages, email_headers, email_recipients, email_links, email_attachments)
4. Scanning & ML (scan_requests, scan_results, classification_scores, model_versions, user_feedback)
5. Import/Export (import_jobs, export_jobs)
6. Reports (reports, report_filters)
7. CMS (cms_pages, cms_content_blocks)

## Standards

All important tables will have primary keys, foreign keys, indexes where needed,
`created_at` / `updated_at` timestamps, `created_by` / `updated_by` where it makes
sense, and a normalized (3NF) structure.

## MongoDB Collections

_To be defined in a later commit._
