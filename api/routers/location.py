from fastapi import (
    APIRouter,
    Depends,
    Response,
    Path,
    status,
    UploadFile,
    HTTPException,
)
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api import schemas
from api.cruds import Location, Accessibility, NavigationFloor, InclusiveStory
from api.configuration.database.db_helper import db_helper

site_router = APIRouter(tags=["location"])

response_codes = {
    200: {"description": "Success"},
    404: {"description": "Not found", "model": schemas.ErrorNotFound},
    500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
}


@site_router.get(
    "/location/{location_id}",
    response_model=schemas.LocationBase,
    tags=["admin"],
    status_code=200,
    responses=response_codes,
)
async def get_location_by_id(
    session: AsyncSession = Depends(db_helper.session_getter),
    location_id: PositiveInt = Path(..., description="The identifier of location"),
) -> Response:
    location = await Location.get_by_id(session, location_id)
    return location


@site_router.get(
    "/location/{location_id}",
    response_model=schemas.LocationBase,
    tags=["admin"],
    status_code=200,
    responses=response_codes,
)
async def get_location_by_id(
    session: AsyncSession = Depends(db_helper.session_getter),
    location_id: PositiveInt = Path(..., description="The identifier of location"),
) -> Response:
    location = await Location.get_by_id(session, location_id)
    return location


@site_router.get(
    "/location/{location_id}/navigation-floors",
    response_model=List[schemas.NavigationFloorBase],
    tags=["navigation"],
    status_code=200,
)
async def get_navigation_floors(
    location_id: PositiveInt = Path(..., description="The identifier of location"),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> List[schemas.NavigationFloorBase]:
    await Location.get_by_id(session, location_id)

    floors = await NavigationFloor.get_by_location_id(session, location_id)
    return floors

@site_router.get(
    "/location/{location_id}/inclusive-stories",
    response_model=List[schemas.InclusiveStoryBase],
    tags=["inclusive"],
    status_code=200,
)
async def get_inclusive_stories(
    location_id: PositiveInt = Path(..., description="The identifier of location"),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> List[schemas.NavigationFloorBase]:
    await Location.get_by_id(session, location_id)

    inclusive_stories = await InclusiveStory.get_by_location_id(session, location_id)
    return inclusive_stories


@site_router.get(
    "/locations",
    response_model=List[schemas.LocationShallow],
    tags=["location", "admin"],
    status_code=200,
    responses=response_codes,
)
async def get_location_list(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    return await Location.get_all(session)


@site_router.get(
    "/accessibilities",
    tags=["accessibility", "admin"],
    response_model=List[schemas.AccessibilityBase],
    status_code=200,
    responses=response_codes,
)
async def get_accessibility_list(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    return await Accessibility.get_all(session)
