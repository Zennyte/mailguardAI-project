from datetime import datetime, timezone

from pymongo.errors import PyMongoError

from app.core import mongo

# MongoDB mban te dhenat e medha dhe fleksibile te nje skanimi:
# tekstin e plote te emailit dhe pergjigjen e plote te modelit ML.


def save_full_email_text(user_id: int, subject: str, body: str) -> bool:
    document = {
        "user_id": user_id,
        "subject": subject,
        "body": body,
        "input_type": "paste",
        "created_at": datetime.now(timezone.utc),
    }
    return insert_document("raw_email_documents", document)


def save_prediction_details(user_id: int, scan_request_id: int, prediction: dict,
                            model_version_id) -> bool:
    document = {
        "user_id": user_id,
        "scan_request_id": scan_request_id,
        "predicted_label": prediction["predicted_label"],
        "confidence_score": prediction["confidence_score"],
        "label_scores": prediction["label_scores"],
        "model_version_id": model_version_id,
        "created_at": datetime.now(timezone.utc),
    }
    return insert_document("scan_payload_logs", document)


# Nese MongoDB nuk eshte aktiv, skanimi vazhdon normalisht - humbet vetem logu
def insert_document(collection_name: str, document: dict) -> bool:
    try:
        mongo.get_mongo_database()[collection_name].insert_one(document)
        return True
    except PyMongoError:
        print(f"WARNING: MongoDB is not available, log skipped for '{collection_name}'")
        return False
