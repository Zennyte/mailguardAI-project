# ERD Notes - MailGuard AI Platform

Pershkrim tekstual i lidhjeve mes tabelave.

Diagrami vizual eshte ne [`ERD.mmd`](ERD.mmd) (Mermaid ERD syntax) — mund te
shikohet direkt ne GitHub, ne https://mermaid.live, ose ne VS Code me nje
Mermaid extension.

## Text-based ERD

```
users ──< user_roles >── roles
roles ──< role_permissions >── permissions

users ──< refresh_tokens
users ──< notifications
users ──< audit_logs            (user_id can be NULL)
users ──< files                 (uploaded_by)

users ──< email_messages ──< email_headers
                         ──< email_recipients
                         ──< email_links
                         ──< email_attachments

users ──< scan_requests ──── scan_results        (one-to-one)
              │                   │
              └── email_message   ├──< classification_scores
                  (optional)      ├──< user_feedback
                                  └─── model_versions   (many results -> one version)

users ──< import_jobs ─── files   (optional file_id)
users ──< export_jobs ─── files   (optional file_id)

users ──< reports ──< report_filters

cms_pages ──< cms_content_blocks
```

Legjenda: `──<` do te thote one-to-many, `>──` ana tjeter e many-to-many,
`────` one-to-one.

## Main relationships explained

- **users → roles**: many-to-many through `user_roles`. A user can be both
  Admin and User; a role belongs to many users.
- **roles → permissions**: many-to-many through `role_permissions`. What a user
  is allowed to do comes from the permissions of their roles.
- **users → email_messages / scan_requests**: a user creates emails and scan
  requests (one-to-many).
- **scan_requests → scan_results**: one-to-one. One scan produces exactly one
  result (`scan_request_id` is UNIQUE in `scan_results`).
- **scan_results → classification_scores**: one-to-many. One result has one
  score row per class (safe, spam, phishing).
- **scan_results → model_versions**: many-to-one. Every result records which
  ML model version produced it.
- **reports → report_filters**: one-to-many. A report stores the filters used
  to generate it.
- **cms_pages → cms_content_blocks**: one-to-many. A page is built from ordered
  content blocks.

## Delete behavior

- Children of an email or a scan are deleted together with the parent
  (`ON DELETE CASCADE`), e.g. deleting an email removes its headers and links.
- References that should survive a delete use `ON DELETE SET NULL`,
  e.g. `audit_logs.user_id` stays as history even if the user is removed.
