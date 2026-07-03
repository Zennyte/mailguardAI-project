-- ============================================================
-- MailGuard AI Platform - Seed Data (PostgreSQL)
-- ============================================================
-- Te dhenat fillestare: rolet, lejet, konfigurimet dhe modeli ML.
-- Ekzekutohet pas schema.sql:
--   psql -U postgres -d mailguard_platform -f database/seed.sql
--
-- Perdoruesit real (me fjalekalime te hash-uara) krijohen ne
-- commitin e autentikimit, jo ketu.
-- ============================================================

-- Rolet baze
INSERT INTO roles (name, description) VALUES
    ('Admin',   'Full access to the whole platform'),
    ('Manager', 'Can scan, view reports and manage imports/exports'),
    ('User',    'Can scan emails and view own history')
ON CONFLICT (name) DO NOTHING;

-- Lejet baze
INSERT INTO permissions (name, description) VALUES
    ('scan_email',        'Scan an email with the ML model'),
    ('view_scan_history', 'View own scan history'),
    ('manage_users',      'Create, edit and deactivate users'),
    ('view_reports',      'View and generate reports'),
    ('manage_cms',        'Create and edit CMS pages'),
    ('import_data',       'Import emails in bulk'),
    ('export_data',       'Export scan data (CSV/JSON)')
ON CONFLICT (name) DO NOTHING;

-- Lidhja rol -> leje
-- Admin i merr te gjitha lejet
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r, permissions p
WHERE r.name = 'Admin'
ON CONFLICT (role_id, permission_id) DO NOTHING;

INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r, permissions p
WHERE r.name = 'Manager'
  AND p.name IN ('scan_email', 'view_scan_history', 'view_reports',
                 'import_data', 'export_data')
ON CONFLICT (role_id, permission_id) DO NOTHING;

INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r, permissions p
WHERE r.name = 'User'
  AND p.name IN ('scan_email', 'view_scan_history', 'export_data')
ON CONFLICT (role_id, permission_id) DO NOTHING;

-- Konfigurimet baze
INSERT INTO settings (setting_key, setting_value, description) VALUES
    ('app_name',              'MailGuard AI Platform', 'Application display name'),
    ('maintenance_mode',      'false',                 'When true, the app shows a maintenance message'),
    ('max_upload_size_mb',    '5',                     'Maximum upload size for email files (MB)'),
    ('notifications_enabled', 'true',                  'Enable real-time notifications'),
    ('default_page_size',     '10',                    'Default page size for lists')
ON CONFLICT (setting_key) DO NOTHING;

-- Modeli ML i eksportuar nga projekti mailguard-ml
INSERT INTO model_versions (model_name, version, file_path, is_active) VALUES
    ('MailGuard Logistic Regression', '1.0', 'app/ml/mail_detection_pipeline.joblib', TRUE)
ON CONFLICT (model_name, version) DO NOTHING;
