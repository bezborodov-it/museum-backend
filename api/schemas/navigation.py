from typing import Optional, List
from pydantic import BaseModel


class NavigationPointBase(BaseModel):
    id: int
    number: float
    title: str
    x: float
    y: float

    class Config:
        from_attributes = True


class NavigationPointCreate(BaseModel):
    number: float
    title: str
    x: float
    y: float


class NavigationPointUpdate(BaseModel):
    number: Optional[float] = None
    title: Optional[str] = None
    x: Optional[float] = None
    y: Optional[float] = None


class NavigationFloorBase(BaseModel):
    id: int
    floor_num: int
    plan_image_url: Optional[str] = None

    points: List[NavigationPointBase] = []

    class Config:
        from_attributes = True


class NavigationFloorCreate(BaseModel):
    floor_num: int


class NavigationFloorUpdate(BaseModel):
    floor_num: int
