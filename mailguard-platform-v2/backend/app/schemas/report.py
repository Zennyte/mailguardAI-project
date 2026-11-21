from datetime import date, datetime

from pydantic import BaseModel, Field


# Butoni "Save Report": emri + lloji + filtrat e zgjedhur
class ReportCreateRequest(BaseModel):
    report_name: str = Field(min_length=1, max_length=200)
    report_type: str = "scan_summary"  # scan_summary / label_distribution / phishing_activity
    date_from: date | None = None
    date_to: date | None = None
    label: str | None = None


# Nje filter i ruajtur bashke me raportin (p.sh. date_from = 2026-01-01)
class ReportFilterResponse(BaseModel):
    filter_key: str
    filter_value: str | None = None

    model_config = {"from_attributes": True}


# Nje raport i ruajtur (lista "Saved reports"); report_data plotesohet kur hapet
class ReportResponse(BaseModel):
    id: int
    report_name: str
    report_type: str | None = None
    created_at: datetime
    filters: list[ReportFilterResponse] = []
    report_data: dict | None = None

    model_config = {"from_attributes": True}


# Butoni "Preview": te dhenat e raportit pa e ruajtur
class ReportPreviewResponse(BaseModel):
    report_type: str
    date_from: date | None = None
    date_to: date | None = None
    label: str | None = None
    report_data: dict
