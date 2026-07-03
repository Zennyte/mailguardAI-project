# Importojme te gjitha modelet ne nje vend qe te jene te lehta per t'u perdorur
from app.models.user import User
from app.models.auth import Role, UserRole, Permission, RolePermission, RefreshToken
from app.models.audit import AuditLog
from app.models.notification import Notification
from app.models.file import File
from app.models.email import (
    EmailMessage, EmailHeader, EmailRecipient, EmailLink, EmailAttachment,
)
from app.models.scan import (
    ModelVersion, ScanRequest, ScanResult, ClassificationScore, UserFeedback,
)
from app.models.system import Setting, ImportJob, ExportJob
from app.models.report import Report, ReportFilter
from app.models.cms import CmsPage, CmsContentBlock
