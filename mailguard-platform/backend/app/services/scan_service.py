from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import scan_repository, mongo_log_repository
from app.schemas.scan import ScanEmailRequest, ScanResultResponse, ClassificationScoreResponse
from app.services import ml_service, notification_service

RESULT_MESSAGES = {
    "safe": "This email looks safe.",
    "spam": "This email looks like spam.",
    "phishing": "Warning: this email looks like a phishing attempt!",
}


async def analyze_email(db: Session, user_id: int, data: ScanEmailRequest) -> ScanResultResponse:
    prediction = ml_service.predict_email(data.subject, data.body)

    # Ruajme rezultatin e skanimit ne PostgreSQL
    scan_request = scan_repository.save_scan(
        db, user_id, data.subject, data.body, data.input_type, prediction,
    )

    # Ne MongoDB ruhet emaili i plote dhe payload-i i parashikimit
    mongo_log_repository.save_raw_email(user_id, data.subject, data.body, data.input_type)
    mongo_log_repository.save_scan_payload(
        user_id, scan_request.id, prediction, scan_request.result.model_version_id,
    )

    # Njoftimi ruhet ne databaze dhe dergohet live me WebSocket
    await notification_service.notify_scan_completed(
        db, user_id, prediction["predicted_label"], prediction["confidence_score"],
    )

    return ScanResultResponse(
        scan_request_id=scan_request.id,
        predicted_label=prediction["predicted_label"],
        confidence_score=prediction["confidence_score"],
        scores=[ClassificationScoreResponse(**score) for score in prediction["scores"]],
        message=RESULT_MESSAGES.get(prediction["predicted_label"], "Scan completed."),
    )


def get_scan(db: Session, user_id: int, scan_request_id: int) -> ScanResultResponse:
    scan_request = scan_repository.get_scan_for_user(db, scan_request_id, user_id)
    if scan_request is None or scan_request.result is None:
        raise HTTPException(status_code=404, detail="Scan not found")

    result = scan_request.result
    return ScanResultResponse(
        scan_request_id=scan_request.id,
        predicted_label=result.predicted_label,
        confidence_score=float(result.confidence_score),
        scores=[
            ClassificationScoreResponse(label=s.label, score=float(s.score))
            for s in result.scores
        ],
        message=RESULT_MESSAGES.get(result.predicted_label, "Scan completed."),
    )
