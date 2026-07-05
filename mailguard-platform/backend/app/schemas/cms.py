from datetime import datetime

from pydantic import BaseModel, Field


class CmsPageCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=1, max_length=200)
    is_published: bool = False


class CmsPageUpdateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=1, max_length=200)
    is_published: bool = False


class CmsBlockCreateRequest(BaseModel):
    block_type: str = "text"  # text / image / list
    content: str | None = None
    sort_order: int = 0


class CmsBlockResponse(BaseModel):
    id: int
    block_type: str
    content: str | None = None
    sort_order: int

    model_config = {"from_attributes": True}


class CmsPageResponse(BaseModel):
    id: int
    title: str
    slug: str
    is_published: bool
    created_at: datetime
    blocks: list[CmsBlockResponse] = []

    model_config = {"from_attributes": True}
