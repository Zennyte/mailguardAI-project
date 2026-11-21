import os

import joblib
from fastapi import HTTPException

# Modeli i eksportuar nga projekti mailguard-ml (TF-IDF + Logistic Regression)
MODEL_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "ml", "mail_detection_pipeline.joblib")

_loaded_model = None


# Modeli ngarkohet nga disku vetem njehere dhe pastaj mbahet ne memorie
def get_model():
    global _loaded_model
    if _loaded_model is None:
        if not os.path.isfile(MODEL_FILE_PATH):
            raise HTTPException(
                status_code=503,
                detail="ML model is not available. Copy mail_detection_pipeline.joblib "
                       "from the ML project into backend/app/ml/.",
            )
        _loaded_model = joblib.load(MODEL_FILE_PATH)
    return _loaded_model


# Kthen parashikimin e modelit per nje email, p.sh.:
# {
#   "predicted_label": "phishing",
#   "confidence_score": 0.94,
#   "label_scores": [{"label": "phishing", "score": 0.94}, {"label": "safe", ...}, ...]
# }
def predict_email(subject: str, body: str) -> dict:
    model = get_model()

    # Njesoj si ne trajnim: subjekti dhe trupi bashkohen ne nje tekst te vetem
    email_text = f"{subject} {body}".strip()

    predicted_label = model.predict([email_text])[0]
    probabilities = model.predict_proba([email_text])[0]

    label_scores = []
    for label, probability in zip(model.classes_, probabilities):
        label_scores.append({"label": str(label), "score": round(float(probability), 4)})

    return {
        "predicted_label": str(predicted_label),
        "confidence_score": round(float(max(probabilities)), 4),
        "label_scores": label_scores,
    }
