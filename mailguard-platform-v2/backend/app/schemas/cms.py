from datetime import datetime

from pydantic import BaseModel, Field


# Forma "New page" dhe "Edit page" ne faqen CMS
class CmsPageSaveRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=1, max_length=200)
    is_published: bool = False


# Forma e nje blloku permbajtjeje (krijim dhe ndryshim)
class CmsBlockSaveRequest(BaseModel):
    block_type: str = "text"  # text / image / list
    content: str | None = None
    sort_order: int = 0


# Nje bllok permbajtjeje ne pergjigjen e API
class CmsBlockResponse(BaseModel):
    id: int
    block_type: str
    content: str | None = None
    sort_order: int

    model_config = {"from_attributes": True}


# Nje faqe CMS bashke me blloqet e saj
class CmsPageResponse(BaseModel):
    id: int
    title: str
    slug: str
    is_published: bool
    created_at: datetime
    blocks: list[CmsBlockResponse] = []

    model_config = {"from_attributes": True}
