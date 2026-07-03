-- ============================================================
-- MailGuard AI Platform - Database Schema (PostgreSQL)
-- ============================================================
-- Ky skedar do te permbaje skemen e plote relacionale.
-- Ne kete commit listohen vetem tabelat e planifikuara.
-- Definimet e plota SQL do te shtohen ne nje commit te ardhshem.
-- ============================================================

-- ------------------------------------------------------------
-- Planned tables (26 total)
-- ------------------------------------------------------------

-- Auth & users (required base tables)
--  1. users                  - platform user accounts
--  2. roles                  - user roles (admin, user, ...)
--  3. user_roles             - link between users and roles
--  4. permissions            - individual permissions
--  5. role_permissions       - link between roles and permissions
--  6. refresh_tokens         - JWT refresh tokens per user

-- System (required base tables)
--  7. audit_logs             - record of important user actions
--  8. notifications          - user notifications (also sent live via WebSocket)
--  9. settings               - application settings (key/value)
-- 10. files                  - metadata of uploaded files

-- Email data
-- 11. email_messages         - the scanned email (subject, body, ...)
-- 12. email_headers          - individual headers of an email
-- 13. email_recipients       - to/cc/bcc recipients of an email
-- 14. email_links            - links found inside an email body
-- 15. email_attachments      - attachments of an email

-- Scanning & ML
-- 16. scan_requests          - a scan request made by a user
-- 17. scan_results           - final result of a scan (label + confidence)
-- 18. classification_scores  - probability per class (safe/spam/phishing)
-- 19. model_versions         - info about the ML model version used
-- 20. user_feedback          - user feedback on a scan result

-- Import / Export
-- 21. import_jobs            - bulk email import jobs
-- 22. export_jobs            - data export jobs (CSV/JSON)

-- Reports
-- 23. reports                - generated reports
-- 24. report_filters         - filters applied to a report

-- CMS
-- 25. cms_pages              - simple CMS pages (help, tips, ...)
-- 26. cms_content_blocks     - content blocks inside a CMS page

-- ------------------------------------------------------------
-- Standards for all important tables (to apply later):
--   * primary keys
--   * foreign keys with references
--   * indexes where needed (search columns, foreign keys)
--   * created_at / updated_at timestamps
--   * created_by / updated_by where it makes sense
--   * normalized structure (3NF)
-- ------------------------------------------------------------
