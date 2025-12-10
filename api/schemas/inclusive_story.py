from typing import Optional, List
from pydantic import BaseModel, Field


class StoryBase(BaseModel):
    id: int
    order: int
    story_image_url: Optional[str] = None
    content: str

    class Config:
        from_attributes = True


class StoryCreate(BaseModel):
    order: int = Field(gt=0)
    content: str


class StoryUpdate(BaseModel):
    order: Optional[int] = None
    content: Optional[str] = None


class InclusiveStoryBase(BaseModel):
    id: int
    title: str

    stories: List[StoryBase] = []

    class Config:
        from_attributes = True

class InclusiveStoryCreate(BaseModel):
    title: str

class InclusiveStoryUpdate(BaseModel):
    title: str