from pydantic import BaseModel


class SearchResponse(BaseModel):
    entity: str
    count: int
    results: list[dict]
