from typing import Callable, TypeVar, Type, Any, Dict, List, Generic
from sqlalchemy import select, inspect, func
from sqlalchemy.ext.asyncio import AsyncSession

from api.exceptions.cruds import NotFoundError
from api.models import BaseORM

T = TypeVar("T", bound=BaseORM)


class Base(Generic[T]):
    model: Type[T]

    @classmethod
    async def create(cls, session: AsyncSession, data: Dict[str, Any]) -> T:
        obj_data = {
            key: value for key, value in data.items() if not isinstance(value, list)
        }
        obj = cls.model(**obj_data)

        await cls._update_related_fields(session, obj, data)

        session.add(obj)
        await session.commit()
        await session.refresh(obj)

        return obj

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id_: int) -> T:
        primary_key_column = inspect(cls.model).primary_key[0]
        query = select(cls.model).where(primary_key_column == id_)
        result = await session.execute(query)
        obj = result.scalar_one_or_none()
        if obj is None:
            raise NotFoundError(cls.model.__tablename__, "id", id_)
        return obj

    @classmethod
    async def update(cls, session: AsyncSession, id_: int, data: Dict[str, Any]) -> T:
        obj = await cls.get_by_id(session, id_)
        for key, value in data.items():
            if value is not None and not isinstance(value, list):
                setattr(obj, key, value)

        await cls._update_related_fields(session, obj, data)
        await session.commit()
        await session.refresh(obj)
        return obj

    @classmethod
    async def _update_related_fields(
        cls, session: AsyncSession, obj: BaseORM, data: Dict[str, Any]
    ):
        for field, related_ids in data.items():
            if isinstance(related_ids, list):
                related_model = getattr(cls.model, field).property.mapper.class_

                related_objs = await session.execute(
                    select(related_model).where(related_model.id.in_(related_ids))
                )
                related_objs = related_objs.scalars().all()

                setattr(obj, field, related_objs)

    @classmethod
    async def delete(cls, session: AsyncSession, id_: int) -> None:
        obj = await cls.get_by_id(session, id_)
        await session.delete(obj)
        await session.commit()

    @classmethod
    async def get_admin_list(
        cls,
        session: AsyncSession,
        search: str,
        offset: int = 0,
        limit: int = 10,
    ) -> tuple[List[T], int]:
        query = select(cls.model)

        if search:
            query = query.where(cls.model.name.ilike(f"%{search}%"))

        total_count = await session.scalar(
            select(func.count()).select_from(query.subquery())
        )

        query = query.offset(offset).limit(limit)
        result = await session.execute(query)

        items = result.scalars().all()

        return items, total_count

    @classmethod
    async def get_all(cls, session: AsyncSession) -> List[T]:
        query = select(cls.model)
        result = await session.execute(query)
        return result.scalars().all()


_BaseCRUDT = TypeVar("_BaseCRUDT", bound=Base)


def with_model(model: Type[BaseORM]) -> Callable[[_BaseCRUDT], _BaseCRUDT]:
    def wrapper(crud_class: _BaseCRUDT) -> _BaseCRUDT:
        crud_class.model = model
        return crud_class

    return wrapper
