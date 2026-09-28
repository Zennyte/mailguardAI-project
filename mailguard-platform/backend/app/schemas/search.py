from pydantic import BaseModel


# Pergjigja e kerkimit: lista + numri i rezultateve
class SearchResponse(BaseModel):
    entity: str
    count: int
    results: list[dict]
