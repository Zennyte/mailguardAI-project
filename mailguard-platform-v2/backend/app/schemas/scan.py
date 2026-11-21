from datetime import datetime

from pydantic import BaseModel, Field


# Emaili qe perdoruesi ngjit ne faqen Scanner
class ScanEmailRequest(BaseModel):
    subject: str = Field(default="", max_length=500)
    body: str = Field(min_length=1)


# Probabiliteti i nje etikete (nje bar ne rezultat)
class LabelScoreResponse(BaseModel):
    label: str
    score: float  # nga 0 deri ne 1


# Karta "Result" ne faqen Scanner.
# Teksti i rezultatit ("This email looks safe.") nuk vjen nga backend-i,
# por nga frontend/src/config/emailLabels.js.
class ScanResultResponse(BaseModel):
    scan_request_id: int
    predicted_label: str
    confidence_score: float
    label_scores: list[LabelScoreResponse]
    ai_explanation: str | None = None


# Nje rresht i tabeles ne faqen History
class ScanHistoryItem(BaseModel):
    scan_request_id: int
    subject: str | None = None
    predicted_label: str
    confidence_score: float
    created_at: datetime


# Numrat e kartave ne faqen Dashboard
class ScanStatsResponse(BaseModel):
    total_scans: int
    scans_per_label: dict[str, int]  # p.sh. {"safe": 5, "spam": 2, "phishing": 1}
    latest_scan_label: str | None = None
