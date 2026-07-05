from datetime import date, datetime

from pydantic import BaseModel, Field


class ReportCreateRequest(BaseModel):
    report_name: str = Field(min_length=1, max_length=200)
    report_type: str = "scan_summary"  # scan_summary / label_distribution / phishing_activity
    date_from: date | None = None
    date_to: date | None = None
    label: str | None = None


class ReportFilterResponse(BaseModel):
    filter_key: str
    filter_value: str | None = None

    model_config = {"from_attributes": True}


class ReportResponse(BaseModel):
    id: int
    report_name: str
    report_type: str | None = None
    created_at: datetime
    filters: list[ReportFilterResponse] = []
    data: dict | None = None

    model_config = {"from_attributes": True}


class ReportPreviewResponse(BaseModel):
    report_type: str
    date_from: date | None = None
    date_to: date | None = None
    label: str | None = None
    data: dict
