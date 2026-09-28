from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import scan_repository, mongo_log_repository
from app.schemas.scan import (
    ScanEmailRequest, ScanResultResponse, ClassificationScoreResponse,
    ScanHistoryItem, ScanStatsResponse,
)
from app.services import ml_service, notification_service, ai_explanation_service

RESULT_MESSAGES = {
    "safe": "This email looks safe.",
    "spam": "This email looks like spam.",
    "phishing": "Warning: this email looks like a phishing attempt!",
}


# Skanon nje email: ML + ruajtje DB/Mongo + njoftim + shpjegim AI
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

    # Shpjegim opsional nga Groq - nese s'ka API key ose deshton, kthehet None
    ai_explanation = await ai_explanation_service.get_explanation(
        data.subject, data.body, prediction["predicted_label"], prediction["confidence_score"],
    )

    return ScanResultResponse(
        scan_request_id=scan_request.id,
        predicted_label=prediction["predicted_label"],
        confidence_score=prediction["confidence_score"],
        scores=[ClassificationScoreResponse(**score) for score in prediction["scores"]],
        message=RESULT_MESSAGES.get(prediction["predicted_label"], "Scan completed."),
        ai_explanation=ai_explanation,
    )


# Historiku i skanimeve te perdoruesit, i formatuar per pergjigje
def get_history(db: Session, user_id: int) -> list:
    items = []
    for scan_request in scan_repository.get_history_for_user(db, user_id):
        if scan_request.result is None:
            continue
        items.append(ScanHistoryItem(
            scan_request_id=scan_request.id,
            subject=scan_request.email_message.subject if scan_request.email_message else None,
            predicted_label=scan_request.result.predicted_label,
            confidence_score=float(scan_request.result.confidence_score),
            created_at=scan_request.created_at,
        ))
    return items


# Statistika te permbledhura per dashboard (total + sipas etiketes)
def get_stats(db: Session, user_id: int) -> ScanStatsResponse:
    counts = scan_repository.count_labels_for_user(db, user_id)
    history = scan_repository.get_history_for_user(db, user_id, limit=1)
    latest_label = None
    if history and history[0].result is not None:
        latest_label = history[0].result.predicted_label

    return ScanStatsResponse(
        total_scans=sum(counts.values()),
        safe_count=counts.get("safe", 0),
        spam_count=counts.get("spam", 0),
        phishing_count=counts.get("phishing", 0),
        latest_scan_label=latest_label,
    )


# Detajet e nje skanimi specifik te perdoruesit
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
