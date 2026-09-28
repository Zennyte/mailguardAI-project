from datetime import datetime

from pydantic import BaseModel, Field


# Te dhenat e emailit per t'u skanuar
class ScanEmailRequest(BaseModel):
    subject: str = Field(default="", max_length=500)
    body: str = Field(min_length=1)
    input_type: str = "manual"


# Probabiliteti per nje klase (safe/spam/phishing)
class ClassificationScoreResponse(BaseModel):
    label: str
    score: float


# Rezultati i plote i nje skanimi
class ScanResultResponse(BaseModel):
    scan_request_id: int
    predicted_label: str
    confidence_score: float
    scores: list[ClassificationScoreResponse]
    message: str
    ai_explanation: str | None = None


# Nje rresht i historikut te skanimeve
class ScanHistoryItem(BaseModel):
    scan_request_id: int
    subject: str | None = None
    predicted_label: str
    confidence_score: float
    created_at: datetime


# Statistika te permbledhura per dashboard
class ScanStatsResponse(BaseModel):
    total_scans: int
    safe_count: int
    spam_count: int
    phishing_count: int
    latest_scan_label: str | None = None
