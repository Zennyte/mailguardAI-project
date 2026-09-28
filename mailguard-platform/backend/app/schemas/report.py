from datetime import date, datetime

from pydantic import BaseModel, Field


# Te dhenat per te krijuar nje raport te ri
class ReportCreateRequest(BaseModel):
    report_name: str = Field(min_length=1, max_length=200)
    report_type: str = "scan_summary"  # scan_summary / label_distribution / phishing_activity
    date_from: date | None = None
    date_to: date | None = None
    label: str | None = None


# Nje filter i ruajtur per nje raport
class ReportFilterResponse(BaseModel):
    filter_key: str
    filter_value: str | None = None

    model_config = {"from_attributes": True}


# Raporti i ruajtur, me te dhenat e rigjeneruara
class ReportResponse(BaseModel):
    id: int
    report_name: str
    report_type: str | None = None
    created_at: datetime
    filters: list[ReportFilterResponse] = []
    data: dict | None = None

    model_config = {"from_attributes": True}


# Rezultati i nje pareje raporti (pa e ruajtur)
class ReportPreviewResponse(BaseModel):
    report_type: str
    date_from: date | None = None
    date_to: date | None = None
    label: str | None = None
    data: dict
