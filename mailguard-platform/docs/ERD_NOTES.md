# ERD Notes - MailGuard AI Platform

Shenime per diagramin ERD. Diagrami final do te krijohet pasi te definohet skema e plote.

## Planned main relationships

- `users` -> `user_roles` <- `roles` (many-to-many)
- `roles` -> `role_permissions` <- `permissions` (many-to-many)
- `users` -> `refresh_tokens` (one-to-many)
- `users` -> `scan_requests` -> `email_messages` (a scan belongs to a user and an email)
- `scan_requests` -> `scan_results` -> `classification_scores` (one result, one score per class)
- `email_messages` -> `email_headers` / `email_recipients` / `email_links` / `email_attachments` (one-to-many)
- `scan_results` -> `model_versions` (which model version produced the result)
- `users` -> `notifications`, `audit_logs`, `user_feedback`, `import_jobs`, `export_jobs`, `reports` (one-to-many)
- `reports` -> `report_filters` (one-to-many)
- `cms_pages` -> `cms_content_blocks` (one-to-many)

## Tools

The final ERD image will be created with a diagram tool (e.g. dbdiagram.io or draw.io)
and exported here in `docs/`.
