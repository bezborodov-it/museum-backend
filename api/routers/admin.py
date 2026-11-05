from fastapi import (
    APIRouter,
    Depends,
    status,
    Response,
    Path,
    UploadFile,
    Query,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import PositiveInt
from typing import Optional, List

from api import schemas
from api.cruds import (
    Event,
    Exhibition,
    Location,
    Accessibility,
    About,
    NavigationFloor,
    NavigationPoint,
    InclusiveStory,
    Story
)
from api.configuration.database.db_helper import db_helper
from api.dependencies import get_basic_user, get_image_with
from api.models import UserORM
from api.utils.image import save_image
from api.models.enum import ActivityVisibilityEnum

site_router = APIRouter(prefix="/admin", tags=["admin"])

response_codes = {
    200: {"description": "Success"},
    404: {"description": "Not found", "model": schemas.ErrorNotFound},
    500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
}


@site_router.get(
    "/events",
    tags=["event"],
    status_code=200,
    response_model=schemas.EventsAdminGet,
    responses={
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def get_admin_events(
        search: Optional[str] = Query(None, description="Search string"),
        status: Optional[ActivityVisibilityEnum] = Query(
            None, description="Filter by visibility status"
        ),
        offset: int = Query(0, ge=0, description="Offset"),
        limit: int = Query(10, gt=0, le=100, description="Limit"),
        current_user: UserORM = Depends(get_basic_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    events, total_count = await Event.get_admin_list(
        session,
        search,
        status,
        offset,
        limit,
    )
    return schemas.EventsAdminGet(items=events, total=total_count)


@site_router.post(
    "/event",
    tags=["event"],
    response_model=schemas.EventBase,
    status_code=201,
    responses={
        201: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def create_event(
        payload: schemas.EventCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
        current_user: UserORM = Depends(get_basic_user),
) -> Response:
    event = await Event.create(session, payload.model_dump())
    return event


@site_router.patch(
    "/event/{event_id}",
    response_model=schemas.EventBase,
    tags=["event"],
    status_code=200,
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def update_event_by_id(
        payload: schemas.EventUpdate,
        event_id: PositiveInt = Path(..., description="The identifier of event"),
        current_user: UserORM = Depends(get_basic_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    event = await Event.update(session, event_id, payload.model_dump())
    return event


@site_router.delete(
    "/event/{event_id}",
    status_code=204,
    tags=["event"],
    responses={
        200: {"description": "Success"},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def delete_event_by_id(
        event_id: PositiveInt = Path(..., description="The identifier of event"),
        current_user: UserORM = Depends(get_basic_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    await Event.delete(session, event_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@site_router.post(
    "/event/{event_id}/upload_logo",
    status_code=200,
    response_model=schemas.EventBase,
    tags=["event"],
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def upload_logo_by_event_id(
        event_id: PositiveInt = Path(..., description="The identifier of event"),
        file: UploadFile = Depends(get_image_with),
        current_user: UserORM = Depends(get_basic_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    image_url = save_image(file)
    event = await Event.update_image_url(session, event_id, image_url)
    return event


@site_router.post(
    "/exhibition",
    tags=["exhibition"],
    response_model=schemas.ExhibitionBase,
    status_code=201,
    responses={
        201: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def create_exhibition(
        payload: schemas.ExhibitionCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
        current_user: UserORM = Depends(get_basic_user),
) -> Response:
    exhibition = await Exhibition.create(session, payload.model_dump())
    return schemas.ExhibitionBase.model_validate(exhibition)


@site_router.get(
    "/exhibitions",
    tags=["exhibition"],
    status_code=200,
    response_model=schemas.ExhibitionsAdminGet,
    responses={
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def get_admin_exhibitions(
        search: Optional[str] = Query(None, description="Search string"),
        status: Optional[ActivityVisibilityEnum] = Query(None, description="Filter by status"),
        offset: int = Query(0, ge=0, description="Offset"),
        limit: int = Query(10, gt=0, le=100, description="Limit"),
        current_user: UserORM = Depends(get_basic_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    exhibitions, total_count = await Exhibition.get_admin_list(
        session,
        search,
        status,
        offset,
        limit,
    )
    return schemas.ExhibitionsAdminGet(items=exhibitions, total=total_count)


@site_router.patch(
    "/exhibition/{exhibition_id}",
    response_model=schemas.ExhibitionBase,
    tags=["exhibition"],
    status_code=200,
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def update_exhibition_by_id(
        pyload: schemas.ExhibitionUpdate,
        exhibition_id: PositiveInt = Path(..., description="The identifier of exhibition"),
        current_user: UserORM = Depends(get_basic_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    exhibition = await Exhibition.update(session, exhibition_id, pyload.model_dump())
    return exhibition


@site_router.delete(
    "/exhibition/{exhibition_id}",
    tags=["exhibition"],
    status_code=204,
    responses={
        200: {"description": "Success"},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def delete_exhibition_by_id(
        exhibition_id: PositiveInt = Path(..., description="The identifier of event"),
        current_user: UserORM = Depends(get_basic_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    await Exhibition.delete(session, exhibition_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@site_router.post(
    "/exhibition/{exhibition_id}/upload_logo",
    status_code=200,
    tags=["exhibition"],
    response_model=schemas.ExhibitionBase,
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def upload_logo_by_exhibition_id(
        exhibition_id: PositiveInt = Path(..., description="The identifier of exhibition"),
        file: UploadFile = Depends(get_image_with),
        current_user: UserORM = Depends(get_basic_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    image_url = save_image(file)
    exhibition = await Exhibition.update_image_url(session, exhibition_id, image_url)
    return exhibition


@site_router.post(
    "/location",
    tags=["location"],
    response_model=schemas.LocationBase,
    status_code=201,
    responses={
        201: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def create_location(
        payload: schemas.LocationCreate,
        current_user: UserORM = Depends(get_basic_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    location = await Location.create(session, payload.model_dump())
    return location


@site_router.post(
    "/location/{location_id}/floor",
    response_model=schemas.NavigationFloorBase,
    tags=["navigation"],
    status_code=200,
    responses=response_codes,
)
async def create_navigation_floor(
        payload: schemas.NavigationFloorCreate,
        current_user: UserORM = Depends(get_basic_user),
        location_id: PositiveInt = Path(..., description="The identifier of location"),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    await Location.get_by_id(session, location_id)
    existing_floor = await NavigationFloor.get_by_location_id_and_num(
        session, location_id, payload.floor_num
    )
    if existing_floor:
        raise HTTPException(
            status_code=409,
            detail=f"Floor with floor_num={payload.floor_num} already exists for this location",
        )

    floor_data = {
        "location_id": location_id,
        "floor_num": payload.floor_num,
    }
    navigation_floor = await NavigationFloor.create(session, floor_data)
    return navigation_floor


@site_router.patch(
    "/navigation-floor/{navigation_floor_id}",
    response_model=schemas.NavigationFloorBase,
    tags=["navigation"],
    status_code=200,
    responses=response_codes,
)
async def update_navigation_floor_plan(
        payload: schemas.NavigationFloorUpdate,
        navigation_floor_id: PositiveInt = Path(
            ..., description="The identifier of navigation floor"
        ),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    navigation_floor = await NavigationFloor.get_by_id(session, navigation_floor_id)

    if payload.floor_num != navigation_floor.floor_num:
        existing_floor = await NavigationFloor.get_by_location_id_and_num(
            session, navigation_floor.location_id, payload.floor_num
        )
        if existing_floor:
            raise HTTPException(
                status_code=409,
                detail=f"Floor with floor_num={payload.floor_num} already exists for this location",
            )

    navigation_floor = await NavigationFloor.update(
        session, navigation_floor_id, payload.model_dump(exclude_unset=True)
    )
    return navigation_floor


@site_router.delete(
    "/navigation-floor/{navigation_floor_id}",
    status_code=204,
    tags=["navigation"],
)
async def delete_navigation_floor(
        navigation_floor_id: PositiveInt = Path(
            ..., description="The identifier of navigation floor"
        ),
        session: AsyncSession = Depends(db_helper.session_getter),
        current_user: UserORM = Depends(get_basic_user),
):
    await NavigationFloor.delete(session, navigation_floor_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@site_router.post(
    "/navigation-floor/{navigation_floor_id}/upload-plan",
    response_model=schemas.NavigationFloorBase,
    tags=["navigation"],
    status_code=200,
    responses=response_codes,
)
async def upload_navigation_floor_plan(
        file: UploadFile = Depends(get_image_with),
        navigation_floor_id: PositiveInt = Path(
            ..., description="The identifier of navigation floor"
        ),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    image_url = save_image(file)
    navigation_floor = await NavigationFloor.update(
        session, navigation_floor_id, {"plan_image_url": image_url}
    )
    return navigation_floor


@site_router.post(
    "/navigation-floor/{navigation_floor_id}/point",
    response_model=schemas.NavigationPointBase,
    tags=["navigation"],
    status_code=201,
)
async def create_navigation_point(
        payload: schemas.NavigationPointCreate,
        current_user: UserORM = Depends(get_basic_user),
        navigation_floor_id: PositiveInt = Path(
            ..., description="The identifier of navigation floor"
        ),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    await NavigationFloor.get_by_id(session, navigation_floor_id)
    point_data = {
        "floor_id": navigation_floor_id,
        "title": payload.title,
        "number": payload.number,
        "x": payload.x,
        "y": payload.y,
    }
    navigation_point = await NavigationPoint.create(session, point_data)
    return navigation_point


@site_router.patch(
    "/navigation-point/{navigation_point_id}",
    response_model=schemas.NavigationPointBase,
    tags=["navigation"],
    status_code=200,
)
async def update_navigation_point(
        payload: schemas.NavigationPointUpdate,
        current_user: UserORM = Depends(get_basic_user),
        navigation_point_id: PositiveInt = Path(..., description="The identifier of navigation point"),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    navigation_point = await NavigationPoint.update(
        session, navigation_point_id, payload.model_dump(exclude_unset=True)
    )
    return navigation_point


@site_router.delete(
    "/navigation-point/{navigation_point_id}",
    tags=["navigation"],
    status_code=204,
)
async def delete_navigation_point(
        current_user: UserORM = Depends(get_basic_user),
        navigation_point_id: PositiveInt = Path(..., description="The identifier of navigation point"),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    await NavigationPoint.delete(session, navigation_point_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@site_router.post(
    "/location/{location_id}/inclusive-story",
    response_model=schemas.InclusiveStoryBase,
    tags=["inclusive"],
    status_code=200,
    responses=response_codes,
)
async def create_inclusive_story(
        payload: schemas.InclusiveStoryCreate,
        current_user: UserORM = Depends(get_basic_user),
        location_id: PositiveInt = Path(..., description="The identifier of location"),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    await Location.get_by_id(session, location_id)

    inclusive_story_data = {
        "location_id": location_id,
        "title": payload.title,
    }
    inclusive_story = await InclusiveStory.create(session, inclusive_story_data)
    return inclusive_story


@site_router.patch(
    "/inclusive-story/{inclusive_story_id}",
    response_model=schemas.InclusiveStoryBase,
    tags=["inclusive"],
    status_code=200,
    responses=response_codes,
)
async def update_inclusive_story(
        payload: schemas.InclusiveStoryUpdate,
        inclusive_story_id: PositiveInt = Path(..., description="The identifier of inclusive story"),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    inclusive_story = await InclusiveStory.update(
        session, inclusive_story_id, payload.model_dump(exclude_unset=True)
    )
    return inclusive_story


@site_router.delete(
    "/inclusive-story/{inclusive_story_id}",
    status_code=204,
    tags=["inclusive"],
)
async def delete_inclusive_story(
        inclusive_story_id: PositiveInt = Path(..., description="The identifier of inclusive story"),
        session: AsyncSession = Depends(db_helper.session_getter),
        current_user: UserORM = Depends(get_basic_user),
):
    await InclusiveStory.delete(session, inclusive_story_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@site_router.post(
    "/inclusive-story/{inclusive_story_id}/story",
    response_model=schemas.StoryBase,
    tags=["inclusive"],
    status_code=201,
)
async def create_story(
        payload: schemas.StoryCreate,
        current_user: UserORM = Depends(get_basic_user),
        inclusive_story_id: PositiveInt = Path(..., description="The identifier of inclusive story"),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    await InclusiveStory.get_by_id(session, inclusive_story_id)
    story_data = {
        "inclusive_story_id": inclusive_story_id,
        "order": payload.order,
        "content": payload.content,
    }
    story = await Story.create(session, story_data)
    return story


@site_router.post(
    "/story/{story_id}",
    response_model=schemas.StoryBase,
    tags=["inclusive"],
    status_code=200,
    responses=response_codes,
)
async def upload_story_image(
        file: UploadFile = Depends(get_image_with),
        story_id: PositiveInt = Path(..., description="The identifier of story"),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    image_url = save_image(file)
    story = await Story.update(
        session, story_id, {"story_image_url": image_url}
    )
    return story


@site_router.patch(
    "/story/{story_id}",
    response_model=schemas.StoryBase,
    tags=["inclusive"],
    status_code=200,
)
async def update_story(
        payload: schemas.StoryUpdate,
        current_user: UserORM = Depends(get_basic_user),
        story_id: PositiveInt = Path(..., description="The identifier of story"),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    story = await Story.update(
        session, story_id, payload.model_dump(exclude_unset=True)
    )
    return story


@site_router.delete(
    "/story/{story_id}",
    tags=["inclusive"],
    status_code=204,
)
async def delete_story(
        current_user: UserORM = Depends(get_basic_user),
        story_id: PositiveInt = Path(..., description="The identifier of story"),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    await Story.delete(session, story_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@site_router.post(
    "/accessibility",
    tags=["accessibility"],
    response_model=schemas.AccessibilityBase,
    status_code=201,
    responses={
        201: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def create_accessibility(
        payload: schemas.AccessibilityCreate,
        current_user: UserORM = Depends(get_basic_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    accessibility = await Accessibility.create(session, payload.model_dump())
    return accessibility


@site_router.get(
    "/accessibility/{accessibility_id}",
    response_model=schemas.AccessibilityBase,
    tags=["accessibility"],
    status_code=200,
    responses={
        200: {"description": "Success"},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def get_accessibility_by_id(
        accessibility_id: PositiveInt = Path(
            ..., description="The identifier of accessibility"
        ),
        current_user: UserORM = Depends(get_basic_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    accessibility = await Accessibility.get_by_id(session, accessibility_id)
    return accessibility


@site_router.delete(
    "/accessibility/{accessibility_id}",
    tags=["accessibility"],
    status_code=204,
    responses={
        200: {"description": "Success"},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def delete_accessibility_by_id(
        accessibility_id: PositiveInt = Path(
            ..., description="The identifier of accessibility"
        ),
        current_user: UserORM = Depends(get_basic_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    await Accessibility.delete(session, accessibility_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@site_router.post(
    "/accessibility/{accessibility_id}/upload-logo",
    status_code=200,
    tags=["accessibility"],
    response_model=schemas.AccessibilityBase,
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def upload_logo_by_accessibility_id(
        accessibility_id: PositiveInt = Path(
            ..., description="The identifier of accessibility"
        ),
        file: UploadFile = Depends(get_image_with),
        current_user: UserORM = Depends(get_basic_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    image_url = save_image(file)
    accessibility = await Accessibility.update(
        session, accessibility_id, {"image_url": image_url}
    )
    return accessibility


@site_router.patch(
    "/location/{location_id}",
    response_model=schemas.LocationBase,
    tags=["location"],
    status_code=200,
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def update_location_by_id(
        pyload: schemas.LocationUpdate,
        location_id: PositiveInt = Path(..., description="The identifier of location"),
        current_user: UserORM = Depends(get_basic_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    location = await Location.update(
        session, location_id, pyload.model_dump(exclude_unset=True)
    )
    return location


@site_router.delete(
    "/location/{location_id}",
    tags=["location"],
    status_code=204,
    responses={
        200: {"description": "Success"},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def delete_location_by_id(
        location_id: PositiveInt = Path(..., description="The identifier of location"),
        current_user: UserORM = Depends(get_basic_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    await Location.delete(session, location_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@site_router.post(
    "/location/{location_id}/upload-image",
    status_code=200,
    tags=["location"],
    response_model=schemas.LocationBase,
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def upload_image_by_location_id(
        location_id: PositiveInt = Path(..., description="The identifier of location"),
        file: UploadFile = Depends(get_image_with),
        current_user: UserORM = Depends(get_basic_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    image_url = save_image(file)
    location = await Location.update(session, location_id, {"image_url": image_url})
    return location


@site_router.patch(
    "/about",
    tags=["about"],
    response_model=schemas.AboutBase,
    status_code=200,
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def update_about(
        payload: schemas.AboutUpdate,
        current_user: UserORM = Depends(get_basic_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    about = await About.update_one(session, payload.model_dump(exclude_unset=True))
    return about
