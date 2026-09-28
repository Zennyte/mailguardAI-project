from pydantic import BaseModel


# Pergjigja e nje importi: sa u importuan, sa u anashkaluan
class ImportSummary(BaseModel):
    entity: str
    imported_count: int
    skipped_count: int
    message: str
