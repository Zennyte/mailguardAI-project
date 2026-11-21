from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import (
    EmailMessage, ScanRequest, ScanResult, ClassificationScore, ModelVersion,
)


def get_active_model_version_id(db: Session):
    active_model_version = db.query(ModelVersion).filter(ModelVersion.is_active == True).first()  # noqa: E712
    return active_model_version.id if active_model_version is not None else None


# Ruan nje skanim te perfunduar ne 4 tabela, brenda nje transaksioni:
# email_messages -> scan_requests -> scan_results -> classification_scores
def save_completed_scan(db: Session, user_id: int, subject: str, body: str,
                        prediction: dict) -> ScanRequest:
    email_message = EmailMessage(
        user_id=user_id,
        subject=subject[:500],
        body_preview=body[:500],
        source_type="pasted",
    )
    db.add(email_message)
    db.flush()  # flush na jep id-ne e emailit pa e mbyllur transaksionin

    scan_request = ScanRequest(
        user_id=user_id,
        email_message_id=email_message.id,
        status="completed",
        input_type="paste",
    )
    db.add(scan_request)
    db.flush()

    scan_result = ScanResult(
        scan_request_id=scan_request.id,
        predicted_label=prediction["predicted_label"],
        confidence_score=prediction["confidence_score"],
        model_version_id=get_active_model_version_id(db),
    )
    db.add(scan_result)
    db.flush()

    for label_score in prediction["label_scores"]:
        db.add(ClassificationScore(
            scan_result_id=scan_result.id,
            label=label_score["label"],
            score=label_score["score"],
        ))

    db.commit()
    db.refresh(scan_request)
    return scan_request


# Skanimet e perdoruesit, me te rejat te parat
def get_latest_scans_of_user(db: Session, user_id: int, limit: int = 50):
    return (
        db.query(ScanRequest)
        .filter(ScanRequest.user_id == user_id)
        .order_by(ScanRequest.id.desc())
        .limit(limit)
        .all()
    )


# Sa skanime ka perdoruesi per cdo etikete, p.sh. {"safe": 5, "spam": 2}
def count_scans_per_label(db: Session, user_id: int) -> dict:
    rows = (
        db.query(ScanResult.predicted_label, func.count(ScanResult.id))
        .join(ScanRequest, ScanRequest.id == ScanResult.scan_request_id)
        .filter(ScanRequest.user_id == user_id)
        .group_by(ScanResult.predicted_label)
        .all()
    )
    return dict(rows)
