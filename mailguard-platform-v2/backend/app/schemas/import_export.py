from pydantic import BaseModel


# Mesazhi i gjelber pas nje importi: sa rreshta u importuan dhe sa u anashkaluan
class ImportSummary(BaseModel):
    list_name: str
    imported_count: int
    skipped_count: int
    message: str
