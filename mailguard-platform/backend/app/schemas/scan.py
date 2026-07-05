from datetime import datetime

from pydantic import BaseModel, Field


class ScanEmailRequest(BaseModel):
    subject: str = Field(default="", max_length=500)
    body: str = Field(min_length=1)
    input_type: str = "manual"


class ClassificationScoreResponse(BaseModel):
    label: str
    score: float


class ScanResultResponse(BaseModel):
    scan_request_id: int
    predicted_label: str
    confidence_score: float
    scores: list[ClassificationScoreResponse]
    message: str


class ScanHistoryItem(BaseModel):
    scan_request_id: int
    subject: str | None = None
    predicted_label: str
    confidence_score: float
    created_at: datetime


class ScanStatsResponse(BaseModel):
    total_scans: int
    safe_count: int
    spam_count: int
    phishing_count: int
    latest_scan_label: str | None = None
