from sqlalchemy.orm import Session

from app.core.constants import EMAIL_LABELS
from app.repositories import scan_repository, scan_log_repository
from app.schemas.scan import (
    ScanEmailRequest, ScanResultResponse, ScanHistoryItem, ScanStatsResponse,
)
from app.services import ml_model_service, notification_service, ai_explanation_service


# Rrjedha kryesore e aplikacionit (butoni "Scan Email" ne faqen Scanner)
async def scan_email(db: Session, user_id: int, email: ScanEmailRequest) -> ScanResultResponse:
    # 1. Modeli ML parashikon etiketen
    prediction = ml_model_service.predict_email(email.subject, email.body)

    # 2. Rezultati ruhet ne PostgreSQL
    scan_request = scan_repository.save_completed_scan(
        db, user_id, email.subject, email.body, prediction,
    )

    # 3. Emaili i plote dhe detajet e parashikimit ruhen ne MongoDB
    scan_log_repository.save_full_email_text(user_id, email.subject, email.body)
    scan_log_repository.save_prediction_details(
        user_id, scan_request.id, prediction, scan_request.result.model_version_id,
    )

    # 4. Perdoruesi merr nje njoftim live
    await notification_service.notify_scan_completed(
        db, user_id, prediction["predicted_label"], prediction["confidence_score"],
    )

    # 5. Shpjegimi AI (opsional - None nese nuk eshte konfiguruar)
    ai_explanation = await ai_explanation_service.explain_scan_result(
        email.subject, email.body, prediction["predicted_label"], prediction["confidence_score"],
    )

    # "prediction" ka tashme fushat predicted_label, confidence_score dhe label_scores
    return ScanResultResponse(
        scan_request_id=scan_request.id,
        ai_explanation=ai_explanation,
        **prediction,
    )


# Rreshtat e tabeles ne faqen History
def get_scan_history(db: Session, user_id: int) -> list:
    history_items = []
    for scan_request in scan_repository.get_latest_scans_of_user(db, user_id):
        if scan_request.result is None:
            continue
        history_items.append(ScanHistoryItem(
            scan_request_id=scan_request.id,
            subject=scan_request.email_message.subject if scan_request.email_message else None,
            predicted_label=scan_request.result.predicted_label,
            confidence_score=float(scan_request.result.confidence_score),
            created_at=scan_request.created_at,
        ))
    return history_items


# Numrat e kartave ne faqen Dashboard
def get_scan_stats(db: Session, user_id: int) -> ScanStatsResponse:
    counts_from_database = scan_repository.count_scans_per_label(db, user_id)

    # Etiketat pa skanime marrin 0, qe frontend-i te mos duhet ta kontrolloje
    scans_per_label = {label: counts_from_database.get(label, 0) for label in EMAIL_LABELS}

    latest_scan_label = None
    latest_scans = scan_repository.get_latest_scans_of_user(db, user_id, limit=1)
    if latest_scans and latest_scans[0].result is not None:
        latest_scan_label = latest_scans[0].result.predicted_label

    return ScanStatsResponse(
        total_scans=sum(scans_per_label.values()),
        scans_per_label=scans_per_label,
        latest_scan_label=latest_scan_label,
    )
