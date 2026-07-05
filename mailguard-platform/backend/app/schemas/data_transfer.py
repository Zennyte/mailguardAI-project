from pydantic import BaseModel


class ImportSummary(BaseModel):
    entity: str
    imported_count: int
    skipped_count: int
    message: str
