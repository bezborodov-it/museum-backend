from typing import Optional, List
from pydantic import BaseModel

from .navigation import NavigationFloorBase


class AccessibilityBase(BaseModel):
    id: int
    name: str
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class AccessibilityCreate(BaseModel):
    name: str


class LocationBase(BaseModel):
    id: int
    name: str
    image_url: Optional[str] = None
    description: Optional[str] = None
    working_hours: Optional[str] = None
    working_days: Optional[str] = None
    address: str
    phones: Optional[str] = None
    about: Optional[str] = None
    is_active: bool

    accessibilities: List[AccessibilityBase]
    floors: List[NavigationFloorBase] = []

    class Config:
        from_attributes = True


class LocationShallow(BaseModel):
    id: int
    name: str
    address: str
    working_days: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True


class LocationCreate(BaseModel):
    name: str
    description: Optional[str] = None
    working_hours: str
    working_days: str
    address: str
    phones: Optional[str] = None
    about: Optional[str] = None
    is_active: bool

    accessibilities: List[int]


class LocationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    working_hours: Optional[str] = None
    working_days: Optional[str] = None
    address: Optional[str] = None
    phones: Optional[str] = None
    about: Optional[str] = None
    is_active: Optional[bool] = None

    accessibilities: Optional[List[int]] = []


class AboutBase(BaseModel):
    phone: str
    site_url: str
    email: str

    class Config:
        from_attributes = True


class AboutUpdate(BaseModel):
    phone: Optional[str] = None
    site_url: Optional[str] = None
    email: Optional[str] = None
