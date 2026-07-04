-- ============================================================
-- MailGuard AI Platform - Database Schema (PostgreSQL)
-- ============================================================
-- Skema e plote relacionale me 26 tabela.
--
-- Si te ekzekutohet:
--   psql -U postgres -d mailguard_platform -f database/schema.sql
-- Ose me scriptin Python (perdor modelet SQLAlchemy):
--   cd backend && python -m app.create_tables
--
-- Standardet e perdorura:
--   * BIGSERIAL primary key me emrin "id" ne cdo tabele
--   * foreign keys me REFERENCES
--   * created_at / updated_at ne cdo tabele
--   * created_by / updated_by vetem ne tabelat qe menaxhohen
--     nga administratori (roles, permissions, settings, model_versions,
--     cms_pages) - tabelat e tjera e kane pronarin te user_id
--   * indekse ne kolonat qe kerkohen shpesh
--   * struktura e normalizuar (3NF)
-- ============================================================


-- ------------------------------------------------------------
-- AUTH & USERS
-- ------------------------------------------------------------

-- 1. users - llogarite e perdoruesve
CREATE TABLE users (
    id            BIGSERIAL PRIMARY KEY,
    first_name    VARCHAR(50)  NOT NULL,
    last_name     VARCHAR(50)  NOT NULL,
    email         VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active     BOOLEAN   NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 2. roles - rolet e perdoruesve (Admin, User, Manager)
CREATE TABLE roles (
    id          BIGSERIAL PRIMARY KEY,
    name        VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255),
    created_by  BIGINT REFERENCES users(id),
    updated_by  BIGINT REFERENCES users(id),
    created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 3. user_roles - lidhja many-to-many mes users dhe roles
CREATE TABLE user_roles (
    id         BIGSERIAL PRIMARY KEY,
    user_id    BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_id    BIGINT NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, role_id)
);
CREATE INDEX idx_user_roles_user_id ON user_roles(user_id);

-- 4. permissions - lejet individuale
CREATE TABLE permissions (
    id          BIGSERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255),
    created_by  BIGINT REFERENCES users(id),
    updated_by  BIGINT REFERENCES users(id),
    created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 5. role_permissions - lidhja many-to-many mes roles dhe permissions
CREATE TABLE role_permissions (
    id            BIGSERIAL PRIMARY KEY,
    role_id       BIGINT NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    permission_id BIGINT NOT NULL REFERENCES permissions(id) ON DELETE CASCADE,
    created_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (role_id, permission_id)
);
CREATE INDEX idx_role_permissions_role_id ON role_permissions(role_id);

-- 6. refresh_tokens - tokenat JWT refresh per cdo perdorues
CREATE TABLE refresh_tokens (
    id         BIGSERIAL PRIMARY KEY,
    user_id    BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token      VARCHAR(500) NOT NULL UNIQUE,
    expires_at TIMESTAMP NOT NULL,
    is_revoked BOOLEAN   NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);


-- ------------------------------------------------------------
-- SYSTEM
-- ------------------------------------------------------------

-- 7. audit_logs - regjistri i veprimeve te rendesishme
CREATE TABLE audit_logs (
    id         BIGSERIAL PRIMARY KEY,
    user_id    BIGINT REFERENCES users(id) ON DELETE SET NULL,
    action     VARCHAR(100) NOT NULL,
    entity     VARCHAR(100),
    entity_id  BIGINT,
    details    TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);

-- 8. notifications - njoftimet e perdoruesit (dergohen edhe live me WebSocket)
CREATE TABLE notifications (
    id                BIGSERIAL PRIMARY KEY,
    user_id           BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title             VARCHAR(200) NOT NULL,
    message           TEXT,
    notification_type VARCHAR(50),
    is_read           BOOLEAN   NOT NULL DEFAULT FALSE,
    created_at        TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_notifications_user_id ON notifications(user_id);

-- 9. settings - konfigurime globale key/value
CREATE TABLE settings (
    id            BIGSERIAL PRIMARY KEY,
    setting_key   VARCHAR(100) NOT NULL UNIQUE,
    setting_value TEXT,
    description   VARCHAR(255),
    created_by    BIGINT REFERENCES users(id),
    updated_by    BIGINT REFERENCES users(id),
    created_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 10. files - metadata e skedareve te ngarkuar
CREATE TABLE files (
    id            BIGSERIAL PRIMARY KEY,
    original_name VARCHAR(255) NOT NULL,
    stored_name   VARCHAR(255) NOT NULL,
    mime_type     VARCHAR(100),
    file_size     BIGINT,
    file_path     VARCHAR(500),
    uploaded_by   BIGINT REFERENCES users(id) ON DELETE SET NULL,
    created_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_files_uploaded_by ON files(uploaded_by);


-- ------------------------------------------------------------
-- EMAIL DATA
-- ------------------------------------------------------------

-- 11. email_messages - emaili qe do te skanohet
CREATE TABLE email_messages (
    id           BIGSERIAL PRIMARY KEY,
    user_id      BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subject      VARCHAR(500),
    body_preview TEXT,
    source_type  VARCHAR(20) NOT NULL DEFAULT 'pasted', -- pasted / uploaded / imported
    created_at   TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_email_messages_user_id ON email_messages(user_id);

-- 12. email_headers - headerat e nje emaili
CREATE TABLE email_headers (
    id               BIGSERIAL PRIMARY KEY,
    email_message_id BIGINT NOT NULL REFERENCES email_messages(id) ON DELETE CASCADE,
    header_name      VARCHAR(100) NOT NULL,
    header_value     TEXT,
    created_at       TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_email_headers_message_id ON email_headers(email_message_id);

-- 13. email_recipients - marresit e nje emaili (to/cc/bcc)
CREATE TABLE email_recipients (
    id               BIGSERIAL PRIMARY KEY,
    email_message_id BIGINT NOT NULL REFERENCES email_messages(id) ON DELETE CASCADE,
    recipient_email  VARCHAR(255) NOT NULL,
    recipient_type   VARCHAR(10) NOT NULL DEFAULT 'to', -- to / cc / bcc
    created_at       TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_email_recipients_message_id ON email_recipients(email_message_id);

-- 14. email_links - linqet e gjetura brenda trupit te emailit
CREATE TABLE email_links (
    id               BIGSERIAL PRIMARY KEY,
    email_message_id BIGINT NOT NULL REFERENCES email_messages(id) ON DELETE CASCADE,
    url              TEXT NOT NULL,
    domain           VARCHAR(255),
    is_suspicious    BOOLEAN   NOT NULL DEFAULT FALSE,
    created_at       TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_email_links_message_id ON email_links(email_message_id);

-- 15. email_attachments - bashkengjitjet e nje emaili
CREATE TABLE email_attachments (
    id               BIGSERIAL PRIMARY KEY,
    email_message_id BIGINT NOT NULL REFERENCES email_messages(id) ON DELETE CASCADE,
    filename         VARCHAR(255),
    mime_type        VARCHAR(100),
    file_size        BIGINT,
    created_at       TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_email_attachments_message_id ON email_attachments(email_message_id);


-- ------------------------------------------------------------
-- SCANNING & ML
-- ------------------------------------------------------------

-- 19. model_versions - versionet e modelit ML
-- (krijohet para scan_results sepse scan_results e referencon)
CREATE TABLE model_versions (
    id         BIGSERIAL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    version    VARCHAR(20)  NOT NULL,
    file_path  VARCHAR(500),
    is_active  BOOLEAN   NOT NULL DEFAULT FALSE,
    created_by BIGINT REFERENCES users(id),
    updated_by BIGINT REFERENCES users(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (model_name, version)
);

-- 16. scan_requests - kerkesa e nje perdoruesi per skanim
CREATE TABLE scan_requests (
    id               BIGSERIAL PRIMARY KEY,
    user_id          BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    email_message_id BIGINT REFERENCES email_messages(id) ON DELETE SET NULL,
    status           VARCHAR(20) NOT NULL DEFAULT 'pending', -- pending / completed / failed
    input_type       VARCHAR(20) NOT NULL DEFAULT 'paste',   -- paste / upload
    created_at       TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_scan_requests_user_id ON scan_requests(user_id);
CREATE INDEX idx_scan_requests_status ON scan_requests(status);

-- 17. scan_results - rezultati final i nje skanimi
CREATE TABLE scan_results (
    id               BIGSERIAL PRIMARY KEY,
    scan_request_id  BIGINT NOT NULL UNIQUE REFERENCES scan_requests(id) ON DELETE CASCADE,
    predicted_label  VARCHAR(20) NOT NULL, -- safe / spam / phishing
    confidence_score NUMERIC(5, 4),
    model_version_id BIGINT REFERENCES model_versions(id),
    created_at       TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_scan_results_label ON scan_results(predicted_label);

-- 18. classification_scores - probabiliteti per cdo klase
CREATE TABLE classification_scores (
    id             BIGSERIAL PRIMARY KEY,
    scan_result_id BIGINT NOT NULL REFERENCES scan_results(id) ON DELETE CASCADE,
    label          VARCHAR(20) NOT NULL,
    score          NUMERIC(5, 4) NOT NULL,
    created_at     TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at     TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_classification_scores_result_id ON classification_scores(scan_result_id);

-- 20. user_feedback - feedback i perdoruesit per nje rezultat skanimi
CREATE TABLE user_feedback (
    id             BIGSERIAL PRIMARY KEY,
    scan_result_id BIGINT NOT NULL REFERENCES scan_results(id) ON DELETE CASCADE,
    user_id        BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    correct_label  VARCHAR(20),
    comment        TEXT,
    created_at     TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at     TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_user_feedback_user_id ON user_feedback(user_id);


-- ------------------------------------------------------------
-- IMPORT / EXPORT
-- ------------------------------------------------------------

-- 21. import_jobs - importimi masiv i emaileve
CREATE TABLE import_jobs (
    id             BIGSERIAL PRIMARY KEY,
    user_id        BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    file_id        BIGINT REFERENCES files(id) ON DELETE SET NULL,
    status         VARCHAR(20) NOT NULL DEFAULT 'pending', -- pending / processing / completed / failed
    total_rows     INTEGER NOT NULL DEFAULT 0,
    processed_rows INTEGER NOT NULL DEFAULT 0,
    created_at     TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at     TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_import_jobs_user_id ON import_jobs(user_id);

-- 22. export_jobs - eksportimi i te dhenave (CSV/JSON)
CREATE TABLE export_jobs (
    id          BIGSERIAL PRIMARY KEY,
    user_id     BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    export_type VARCHAR(20) NOT NULL DEFAULT 'csv', -- csv / json
    file_id     BIGINT REFERENCES files(id) ON DELETE SET NULL,
    status      VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_export_jobs_user_id ON export_jobs(user_id);


-- ------------------------------------------------------------
-- REPORTS
-- ------------------------------------------------------------

-- 23. reports - raportet e gjeneruara
CREATE TABLE reports (
    id          BIGSERIAL PRIMARY KEY,
    user_id     BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    report_name VARCHAR(200) NOT NULL,
    report_type VARCHAR(50), -- p.sh. scan_summary / label_distribution
    created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_reports_user_id ON reports(user_id);

-- 24. report_filters - filtrat e aplikuar ne nje raport
CREATE TABLE report_filters (
    id           BIGSERIAL PRIMARY KEY,
    report_id    BIGINT NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
    filter_key   VARCHAR(100) NOT NULL,
    filter_value VARCHAR(255),
    created_at   TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_report_filters_report_id ON report_filters(report_id);


-- ------------------------------------------------------------
-- CMS
-- ------------------------------------------------------------

-- 25. cms_pages - faqet e thjeshta CMS (ndihma, keshilla, ...)
CREATE TABLE cms_pages (
    id           BIGSERIAL PRIMARY KEY,
    title        VARCHAR(200) NOT NULL,
    slug         VARCHAR(200) NOT NULL UNIQUE,
    is_published BOOLEAN   NOT NULL DEFAULT FALSE,
    created_by   BIGINT REFERENCES users(id),
    updated_by   BIGINT REFERENCES users(id),
    created_at   TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 26. cms_content_blocks - blloqet e permbajtjes brenda nje faqeje CMS
CREATE TABLE cms_content_blocks (
    id          BIGSERIAL PRIMARY KEY,
    cms_page_id BIGINT NOT NULL REFERENCES cms_pages(id) ON DELETE CASCADE,
    block_type  VARCHAR(50) NOT NULL DEFAULT 'text', -- text / image / list
    content     TEXT,
    sort_order  INTEGER NOT NULL DEFAULT 0,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_cms_blocks_page_id ON cms_content_blocks(cms_page_id);
