from datetime import date

from pydantic import BaseModel


# Filtrat e formes ne faqen Search (te gjithe opsionale)
class SearchFilters(BaseModel):
    search_text: str | None = None
    label: str | None = None  # vlen vetem per listen "scans"
    date_from: date | None = None
    date_to: date | None = None
    newest_first: bool = True
    limit: int = 50


# Pergjigja e kerkimit: rreshtat e tabeles se rezultateve
class SearchResponse(BaseModel):
    list_name: str
    count: int
    rows: list[dict]
