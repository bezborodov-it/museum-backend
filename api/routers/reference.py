from fastapi import APIRouter, Depends, Response, Path, status
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api import schemas
from api.cruds import Genre, Tag, Category, About
from api.configuration.database.db_helper import db_helper
from api.models import UserORM
from api.dependencies import get_basic_user
from api.models.enum import AgeEnum

site_router = APIRouter(prefix="/reference", tags=["reference"])

response_codes = {
    200: {"description": "Success"},
    404: {"description": "Not found", "model": schemas.ErrorNotFound},
    500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
}


@site_router.get("/age", response_model=dict[str, str])
async def get_age_list():
    return {age.name: age.display_name for age in AgeEnum}


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


@site_router.get(
    "/about",
    tags=["admin", "about"],
    response_model=schemas.AboutBase,
    status_code=200,
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def get_about(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    about = await About.get_one(session)
    return about


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
