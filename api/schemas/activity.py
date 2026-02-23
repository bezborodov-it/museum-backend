from typing import Optional, List, Union
from datetime import datetime
from pydantic import BaseModel, field_serializer

from .location import LocationShallow
from ..models.enum import AgeEnum, ActivityTypeEnum


class CategoryBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class GenreCreate(BaseModel):
    name: str


class GenreBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class TagCreate(BaseModel):
    name: str


class TagBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class EventBase(BaseModel):
    id: int
    pinned_order: Optional[int]
    name: str
    description: str
    disabilities: bool
    image_url: Optional[str]
    date_start: datetime
    is_free: bool
    require_registration: bool
    privilege_ticket: bool
    pushkin_card: bool
    min_price: Optional[int]
    duration: Optional[int]
    payment_url: Optional[str]
    location: LocationShallow
    age: AgeEnum
    genre: GenreBase
    category: Optional[CategoryBase]

    tags: List[TagBase]

    class Config:
        from_attributes = True

    @field_serializer("age")
    def serialize_age(self, age: AgeEnum):
        return age.display_name


class ShallowEvent(BaseModel):
    id: int
    pinned_order: Optional[int] = None
    name: str
    image_url: Optional[str]
    disabilities: bool
    date_start: datetime
    min_price: Optional[int]
    is_free: bool
    privilege_ticket: bool
    pushkin_card: bool
    location: LocationShallow
    age: AgeEnum
    category: Optional[CategoryBase]

    class Config:
        from_attributes = True

    @field_serializer("age")
    def serialize_age(self, age: AgeEnum):
        return age.display_name


class ShallowAdminEvent(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class EventFilterGet(BaseModel):
    items: List[ShallowEvent]
    total: int


class EventCreate(BaseModel):
    name: str
    pinned_order: Optional[int] = None
    description: str
    disabilities: bool
    date_start: datetime
    payment_url: Optional[str] = None
    is_free: bool
    privilege_ticket: bool
    require_registration: bool
    pushkin_card: bool
    min_price: Optional[int] = None
    duration: Optional[int] = None
    location_id: Optional[int] = None
    genre_id: Optional[int] = None
    age: AgeEnum
    category_id: Optional[int] = None

    tags: List[int]


class EventUpdate(BaseModel):
    name: Optional[str] = None
    pinned_order: Optional[int] = None
    description: Optional[str] = None
    disabilities: Optional[bool] = None
    date_start: Optional[datetime] = None
    payment_url: Optional[str] = None
    is_free: Optional[bool] = None
    require_registration: Optional[bool] = None
    privilege_ticket: Optional[bool] = None
    pushkin_card: Optional[bool] = None
    min_price: Optional[int] = None
    duration: Optional[int] = None
    location_id: Optional[int] = None
    genre_id: Optional[int] = None
    age: Optional[AgeEnum] = None
    category_id: Optional[int] = None

    tags: Optional[List[int]] = []


class PreferencesCreate(BaseModel):
    genres: List[int]
    tags: List[int]


class PreferencesBase(BaseModel):
    genres: List[TagBase]
    tags: List[GenreBase]

    class Config:
        from_attributes = True


class EventsAdminGet(BaseModel):
    items: List[ShallowAdminEvent]
    total: int


class EventAdminGet(BaseModel):
    event: EventBase


class ExhibitionBase(BaseModel):
    id: int
    pinned_order: Optional[int]
    name: str
    description: str
    disabilities: bool
    image_url: Optional[str]
    date_start: datetime
    date_end: datetime
    min_price: Optional[int]
    is_free: bool
    require_registration: bool
    audio_guide: bool
    privilege_ticket: bool
    pushkin_card: bool
    payment_url: Optional[str]

    location: LocationShallow
    age: AgeEnum
    category: Optional[CategoryBase]

    tags: List[TagBase]

    class Config:
        from_attributes = True

    @field_serializer("age")
    def serialize_age(self, age: AgeEnum):
        return age.display_name


class ShallowExhibition(BaseModel):
    id: int
    pinned_order: Optional[int] = None
    name: str
    image_url: Optional[str]
    disabilities: bool
    date_start: datetime
    date_end: datetime
    min_price: Optional[int]
    is_free: bool
    audio_guide: bool
    privilege_ticket: bool
    pushkin_card: bool

    location: LocationShallow
    age: AgeEnum
    category: Optional[CategoryBase]

    class Config:
        from_attributes = True

    @field_serializer("age")
    def serialize_age(self, age: AgeEnum):
        return age.display_name


class ExhibitionFilterGet(BaseModel):
    items: List[ShallowExhibition]
    total: int


class ExhibitionCreate(BaseModel):
    name: str
    pinned_order: Optional[int]
    description: str
    disabilities: bool
    date_start: datetime
    date_end: datetime
    payment_url: Optional[str] = None
    is_free: bool
    require_registration: bool
    audio_guide: bool
    privilege_ticket: bool
    pushkin_card: bool
    min_price: Optional[int] = None
    location_id: Optional[int] = None
    age: AgeEnum
    category_id: Optional[int] = None

    tags: List[int]


class ExhibitionUpdate(BaseModel):
    name: Optional[str] = None
    pinned_order: Optional[int] = None
    description: Optional[str] = None
    disabilities: Optional[bool] = None
    date_start: Optional[datetime] = None
    date_end: Optional[datetime] = None
    payment_url: Optional[str] = None
    is_free: Optional[bool] = None
    require_registration: Optional[bool] = None
    audio_guide: Optional[bool] = None
    privilege_ticket: Optional[bool] = None
    pushkin_card: Optional[bool] = None
    min_price: Optional[int] = None
    location_id: Optional[int] = None
    age: Optional[AgeEnum] = None
    category_id: Optional[int] = None

    tags: Optional[List[int]] = []


class ShallowAdminExhibition(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ExhibitionsAdminGet(BaseModel):
    items: List[ShallowAdminExhibition]
    total: int


class ActivityPreferencesCreate(BaseModel):
    push_token: str
    tags: List[int]
    activity_types: List[ActivityTypeEnum]
    genres: List[int] = []
    ages: List[AgeEnum]


class ActivityPreferencesGet(BaseModel):
    items: List[Union[ShallowExhibition, ShallowEvent]]
    total: int


class CategoryCreate(BaseModel):
    name: str
