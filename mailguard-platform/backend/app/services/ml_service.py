import os

import joblib
from fastapi import HTTPException

# Modeli i eksportuar nga projekti mailguard-ml
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml", "mail_detection_pipeline.joblib")

_model = None


# Ngarkon modelin .joblib nje here dhe e mban ne memorie
def get_model():
    # Modeli ngarkohet vetem njehere dhe mbahet ne memorie
    global _model
    if _model is None:
        if not os.path.isfile(MODEL_PATH):
            raise HTTPException(
                status_code=503,
                detail="ML model is not available. Copy mail_detection_pipeline.joblib "
                       "from the ML project into backend/app/ml/.",
            )
        _model = joblib.load(MODEL_PATH)
    return _model


# Bashkon subject+body dhe kerkon parashikimin nga modeli ML
def predict_email(subject: str, body: str) -> dict:
    model = get_model()

    # Njesoj si ne trajnim: subjekti dhe trupi bashkohen ne nje tekst
    text = f"{subject} {body}".strip()

    predicted_label = model.predict([text])[0]
    probabilities = model.predict_proba([text])[0]

    scores = [
        {"label": str(label), "score": round(float(prob), 4)}
        for label, prob in zip(model.classes_, probabilities)
    ]

    return {
        "predicted_label": str(predicted_label),
        "confidence_score": round(float(max(probabilities)), 4),
        "scores": scores,
    }
