from fastapi import APIRouter, Depends, Response, Path, status
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api import schemas
from api.cruds import Genre, Tag, VisitorCategory, Location, Category
from api.configuration.database.db_helper import db_helper
from api.models import UserORM
from api.dependencies import get_basic_user

site_router = APIRouter(prefix="/reference", tags=["reference"])

response_codes = {
    200: {"description": "Success"},
    404: {"description": "Not found", "model": schemas.ErrorNotFound},
    500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
}


@site_router.get(
    "/visitor_categories",
    response_model=List[schemas.VisitorCategoryBase],
    status_code=200,
    responses=response_codes,
)
async def get_visitor_category_list(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    return await VisitorCategory.get_all(session)


@site_router.post(
    "/visitor_category",
    tags=["admin"],
    response_model=schemas.VisitorCategoryBase,
    status_code=201,
    responses={
        201: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def create_visitor_category(
    payload: schemas.VisitorCategoryCreate,
    current_user: UserORM = Depends(get_basic_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    visitor_category = await VisitorCategory.create(session, payload.model_dump())
    return visitor_category


@site_router.delete(
    "/visitor_category/{visitor_category_id}",
    tags=["admin"],
    status_code=204,
    responses={
        200: {"description": "Success"},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def delete_visitor_category_by_id(
    visitor_category_id: PositiveInt = Path(
        ..., description="The identifier of visitor category"
    ),
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: UserORM = Depends(get_basic_user),
) -> Response:
    await VisitorCategory.delete(session, visitor_category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@site_router.post(
    "/location",
    tags=["admin"],
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


@site_router.get(
    "/locations",
    response_model=List[schemas.LocationBase],
    status_code=200,
    responses=response_codes,
)
async def get_location_list(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    return await Location.get_all(session)


@site_router.delete(
    "/location/{location_id}",
    tags=["admin"],
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
    "/genre",
    tags=["admin"],
    response_model=schemas.GenreBase,
    status_code=201,
    responses={
        201: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def create_genre(
    payload: schemas.GenreCreate,
    current_user: UserORM = Depends(get_basic_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    genre = await Genre.create(session, payload.model_dump())
    return genre


@site_router.get(
    "/genres",
    response_model=List[schemas.GenreBase],
    status_code=200,
    responses=response_codes,
)
async def get_genre_list(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    return await Genre.get_all(session)


@site_router.delete(
    "/genre/{genre_id}",
    tags=["admin"],
    status_code=204,
    responses={
        200: {"description": "Success"},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def delete_genre_by_id(
    genre_id: PositiveInt = Path(..., description="The identifier of genre"),
    current_user: UserORM = Depends(get_basic_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    await Genre.delete(session, genre_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@site_router.post(
    "/tag",
    tags=["admin"],
    response_model=schemas.TagBase,
    status_code=201,
    responses={
        201: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def create_tag(
    payload: schemas.TagCreate,
    current_user: UserORM = Depends(get_basic_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    tag = await Tag.create(session, payload.model_dump())
    return tag


@site_router.get(
    "/tags",
    response_model=List[schemas.TagBase],
    status_code=200,
    responses=response_codes,
)
async def get_tag_list(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    return await Tag.get_all(session)


@site_router.delete(
    "/tag/{tag_id}",
    tags=["admin"],
    status_code=204,
    responses={
        200: {"description": "Success"},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def delete_tag_by_id(
    tag_id: PositiveInt = Path(..., description="The identifier of tag"),
    current_user: UserORM = Depends(get_basic_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    await Tag.delete(session, tag_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@site_router.post(
    "/category",
    tags=["admin"],
    response_model=schemas.CategoryBase,
    status_code=201,
    responses={
        201: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def create_category(
    payload: schemas.CategoryCreate,
    current_user: UserORM = Depends(get_basic_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    category = await Category.create(session, payload.model_dump())
    return category


@site_router.get(
    "/categories",
    response_model=List[schemas.CategoryBase],
    status_code=200,
    responses=response_codes,
)
async def get_category_list(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    return await Category.get_all(session)


@site_router.delete(
    "/category/{category_id}",
    tags=["admin"],
    status_code=204,
    responses={
        200: {"description": "Success"},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def delete_category_by_id(
    category_id: PositiveInt = Path(..., description="The identifier of category"),
    current_user: UserORM = Depends(get_basic_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    await Category.delete(session, category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
