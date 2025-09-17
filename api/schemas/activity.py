from typing import Optional, List
from datetime import datetime
from pydantic import validator, BaseModel


class LocationBase(BaseModel):
    id: int
    name: str
    address: str

    class Config:
        from_attributes = True


class LocationCreate(BaseModel):
    name: str
    address: str


class VisitorCategoryCreate(BaseModel):
    name: str


class VisitorCategoryBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

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
    pushkin_card: bool
    min_price: Optional[int]
    payment_url: Optional[str]
    location: LocationBase
    visitor_category: VisitorCategoryBase
    genre: GenreBase
    category: Optional[CategoryBase]

    tags: List[TagBase]

    class Config:
        from_attributes = True


class ShallowEvent(BaseModel):
    id: int
    pinned_order: Optional[int] = None
    name: str
    image_url: Optional[str]
    disabilities: bool
    date_start: datetime
    min_price: Optional[int]
    is_free: bool
    pushkin_card: bool
    location: LocationBase
    visitor_category: VisitorCategoryBase
    category: Optional[CategoryBase]

    class Config:
        from_attributes = True


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
    pushkin_card: bool
    min_price: Optional[int] = None
    location_id: Optional[int] = None
    genre_id: Optional[int] = None
    visitor_category_id: int
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
    pushkin_card: Optional[bool] = None
    min_price: Optional[int] = None
    location_id: Optional[int] = None
    genre_id: Optional[int] = None
    visitor_category_id: Optional[int] = None
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
    pushkin_card: bool
    payment_url: Optional[str]

    location: LocationBase
    visitor_category: VisitorCategoryBase
    genre: GenreBase
    category: Optional[CategoryBase]

    tags: List[TagBase]

    class Config:
        from_attributes = True


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
    pushkin_card: bool

    location: LocationBase
    visitor_category: VisitorCategoryBase
    category: Optional[CategoryBase]

    class Config:
        from_attributes = True


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
    pushkin_card: bool
    min_price: Optional[int] = None
    location_id: Optional[int] = None
    genre_id: Optional[int] = None
    visitor_category_id: int
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
    pushkin_card: Optional[bool] = None
    min_price: Optional[int] = None
    location_id: Optional[int] = None
    genre_id: Optional[int] = None
    visitor_category_id: Optional[int] = []
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
    genres: List[int]
    visitor_categories: List[int]


class ActivityPreferencesGet(BaseModel):
    events: List[ShallowEvent]
    exhibitions: List[ShallowExhibition]


class CategoryCreate(BaseModel):
    name: str
