from datetime import datetime

from pydantic import BaseModel, Field


# Te dhenat per te krijuar nje faqe CMS
class CmsPageCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=1, max_length=200)
    is_published: bool = False


# Te dhenat per te perditesuar nje faqe CMS
class CmsPageUpdateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=1, max_length=200)
    is_published: bool = False


# Te dhenat per te krijuar/perditesuar nje bllok permbajtjeje
class CmsBlockCreateRequest(BaseModel):
    block_type: str = "text"  # text / image / list
    content: str | None = None
    sort_order: int = 0


# Forma e nje blloku ne pergjigjen e API
class CmsBlockResponse(BaseModel):
    id: int
    block_type: str
    content: str | None = None
    sort_order: int

    model_config = {"from_attributes": True}


# Forma e nje faqeje CMS (me blloqet e saj) ne pergjigjen e API
class CmsPageResponse(BaseModel):
    id: int
    title: str
    slug: str
    is_published: bool
    created_at: datetime
    blocks: list[CmsBlockResponse] = []

    model_config = {"from_attributes": True}
