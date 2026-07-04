from datetime import datetime, timezone

from pymongo.errors import PyMongoError

from app.core import mongo


def save_raw_email(user_id: int, subject: str, body: str, input_type: str) -> bool:
    document = {
        "user_id": user_id,
        "subject": subject,
        "body": body,
        "input_type": input_type,
        "created_at": datetime.now(timezone.utc),
    }
    return _insert("raw_email_documents", document)


def save_scan_payload(user_id: int, scan_request_id: int, prediction: dict,
                      model_version_id) -> bool:
    document = {
        "user_id": user_id,
        "scan_request_id": scan_request_id,
        "predicted_label": prediction["predicted_label"],
        "confidence_score": prediction["confidence_score"],
        "scores": prediction["scores"],
        "model_version_id": model_version_id,
        "created_at": datetime.now(timezone.utc),
    }
    return _insert("scan_payload_logs", document)


def _insert(collection_name: str, document: dict) -> bool:
    # Nese MongoDB nuk eshte aktiv, skanimi vazhdon - humbet vetem logu
    try:
        mongo.get_mongo_db()[collection_name].insert_one(document)
        return True
    except PyMongoError:
        print(f"WARNING: MongoDB is not available, log skipped for '{collection_name}'")
        return False
