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
