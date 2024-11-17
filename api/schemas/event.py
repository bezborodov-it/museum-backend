from typing import Optional, List
from datetime import datetime
from pydantic import validator, BaseModel
from enum import Enum

from api.models.enums import EventGenreEnum
from api.models.enums import VisitorCategoryEnum, EventGenreEnum, TagEventEnum


class GenreFilterType(str, Enum):
    excursion = "excursion"
    master_class = "master_class"
    spectacle = "spectacle"
    exhibition = "exhibition"
    interactive_lesson = "interactive_lesson"
    concert = "concert"
    genealogy = "genealogy"
    lecture = "lecture"
    creative_meeting = "creative_meeting"
    festival = "festival"
    artist_talk = "artist_talk"
    film_screening = "film_screening"


class VisitorAgeFilterType(str, Enum):
    adults = "adults"
    teenagers = "teenagers"
    kids = "kids"


class AreaFilterType(str, Enum):
    cachka_house = "cachka_house"
    metenkov_house = "metenkov_house"
    l52 = "l52"
    water_tower = "water_tower"
    makletsky_house = "makletsky_house"
    memorial_complex = "memorial_complex"


class TagEventFilterType(str, Enum):
    architecture = "architecture"
    literature = "literature"
    science = "science"
    history_of_ussr = "history_of_ussr"
    history_of_yekaterinburg = "history_of_yekaterinburg"
    poetry = "poetry"
    music = "music"
    philosophy = "philosophy"
    flora_and_fauna = "flora_and_fauna"
    handmade = "handmade"
    cinematography = "cinematography"
    cartoons = "cartoons"
    tourism = "tourism"
    genealogy = "genealogy"
    paleontology = "paleontology"
    archaeology = "archaeology"


class LocationBase(BaseModel):
    id: int
    name: str
    address: Optional[str]
    phone: Optional[str]

    class Config:
        orm_mode = True


class LocationCreate(BaseModel):
    name: str
    address: str
    phone: Optional[str]


class LocationUpdate(BaseModel):
    name: Optional[str]
    address: Optional[str]
    phone: Optional[str]


class EventVisitorCategoryCreate(BaseModel):
    name: VisitorCategoryEnum


class EventVisitorCategoryUpdate(BaseModel):
    name: Optional[VisitorCategoryEnum]


class EventVisitorCategoryBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class EventGenreCreate(BaseModel):
    name: EventGenreEnum


class EventGenreUpdate(BaseModel):
    name: Optional[EventGenreEnum]


class EventGenreBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class EventTagCreate(BaseModel):
    name: TagEventEnum


class EventTagUpdate(BaseModel):
    name: Optional[TagEventEnum]


class EventTagBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class EventBase(BaseModel):
    id: int
    name: str
    description: Optional[str]
    image_url: Optional[str]
    disabilities: bool

    location: Optional[LocationBase]
    visitor_category: List[EventVisitorCategoryBase] = []
    genre: EventGenreBase
    tag: List[EventTagBase] = []

    class Config:
        orm_mode = True


class ShallowEvent(BaseModel):
    id: int
    name: str
    image_url: Optional[str]
    disabilities: bool
    location: Optional[LocationBase]
    min_price: Optional[float] = None
    nearest_date: Optional[datetime] = None

    class Config:
        orm_mode = True


class EventFilterGet(BaseModel):
    items: List[ShallowEvent]
    total: int


class EventCreate(BaseModel):
    name: str
    description: str
    disabilities: Optional[bool]
    location_id: Optional[int]
    genre_id: Optional[int]

    visitor_category: Optional[List[int]] = []
    tag: Optional[List[int]] = []


class EventUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    disabilities: Optional[bool]
    location_id: Optional[int]
    genre_id: Optional[int]
    visitor_category: Optional[List[int]] = []
    tag: Optional[List[int]] = []


class PreferencesCreate(BaseModel):
    genres: List[int]
    tags: List[int]


class PreferencesBase(BaseModel):
    genres: List[EventTagBase]
    tags: List[EventGenreBase]

    class Config:
        orm_mode = True


class EventTicketGet(BaseModel):
    id: int
    name: str
    image_url: Optional[str]
    disabilities: bool
    location: Optional[LocationBase]

    class Config:
        orm_mode = True
