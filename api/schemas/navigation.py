from typing import Optional, List
from pydantic import BaseModel


class NavigationPointBase(BaseModel):
    id: int
    name: str
    x: float
    y: float

    class Config:
        from_attributes = True


class NavigationPointCreate(BaseModel):
    name: str
    x: float
    y: float


class NavigationPointUpdate(BaseModel):
    name: Optional[str] = None
    x: Optional[float] = None
    y: Optional[float] = None


class NavigationFloorBase(BaseModel):
    id: int
    floor_num: int
    plan_image_url: Optional[str] = None

    points: Optional[List[NavigationPointBase]] = []

    class Config:
        from_attributes = True


class NavigationFloorCreate(BaseModel):
    floor_num: int


class NavigationFloorUpdate(BaseModel):
    floor_num: int
