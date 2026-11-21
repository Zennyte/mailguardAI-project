# Importojme te gjitha modelet ne nje vend: "from app.models import User, ScanRequest"
from app.models.user import User
from app.models.roles_and_permissions import Role, UserRole, Permission, RolePermission
from app.models.refresh_token import RefreshToken
from app.models.audit_log import AuditLog
from app.models.notification import Notification
from app.models.uploaded_file import File
from app.models.email import (
    EmailMessage, EmailHeader, EmailRecipient, EmailLink, EmailAttachment,
)
from app.models.scan import (
    ModelVersion, ScanRequest, ScanResult, ClassificationScore, UserFeedback,
)
from app.models.setting import Setting
from app.models.import_export_job import ImportJob, ExportJob
from app.models.report import Report, ReportFilter
from app.models.cms import CmsPage, CmsContentBlock
