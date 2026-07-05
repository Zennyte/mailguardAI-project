from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import (
    EmailMessage, ScanRequest, ScanResult, ClassificationScore, ModelVersion,
)


def get_active_model_version_id(db: Session):
    model_version = db.query(ModelVersion).filter(ModelVersion.is_active == True).first()  # noqa: E712
    return model_version.id if model_version is not None else None


def save_scan(db: Session, user_id: int, subject: str, body: str,
              input_type: str, prediction: dict) -> ScanRequest:
    # Ruajme emailin, kerkesen, rezultatin dhe scoret ne nje transaksion
    email = EmailMessage(
        user_id=user_id,
        subject=subject[:500],
        body_preview=body[:500],
        source_type="pasted",
    )
    db.add(email)
    db.flush()  # flush na jep id-ne pa e mbyllur transaksionin

    scan_request = ScanRequest(
        user_id=user_id,
        email_message_id=email.id,
        status="completed",
        input_type=input_type,
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

    for score in prediction["scores"]:
        db.add(ClassificationScore(
            scan_result_id=scan_result.id,
            label=score["label"],
            score=score["score"],
        ))

    db.commit()
    db.refresh(scan_request)
    return scan_request


def get_scan_for_user(db: Session, scan_request_id: int, user_id: int):
    # Perdoruesi sheh vetem skanimet e veta
    return (
        db.query(ScanRequest)
        .filter(ScanRequest.id == scan_request_id, ScanRequest.user_id == user_id)
        .first()
    )


def get_history_for_user(db: Session, user_id: int, limit: int = 50):
    # Skanimet me te rejat te parat
    return (
        db.query(ScanRequest)
        .filter(ScanRequest.user_id == user_id)
        .order_by(ScanRequest.id.desc())
        .limit(limit)
        .all()
    )


def count_labels_for_user(db: Session, user_id: int) -> dict:
    # Sa skanime ka perdoruesi per cdo etikete (safe/spam/phishing)
    rows = (
        db.query(ScanResult.predicted_label, func.count(ScanResult.id))
        .join(ScanRequest, ScanRequest.id == ScanResult.scan_request_id)
        .filter(ScanRequest.user_id == user_id)
        .group_by(ScanResult.predicted_label)
        .all()
    )
    return dict(rows)
