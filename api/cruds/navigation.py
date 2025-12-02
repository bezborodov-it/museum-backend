from sqlalchemy import select, inspect, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from api.cruds.base import Base, with_model
from api.models import NavigationFloorORM, NavigationPointORM


@with_model(NavigationFloorORM)
class NavigationFloor(Base):

    @classmethod
    async def get_by_location_id(
        cls, session: AsyncSession, location_id: int
    ) -> List[NavigationFloorORM]:
        query = select(cls.model).where(cls.model.location_id == location_id)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_by_location_id_and_num(
        cls, session: AsyncSession, location_id: int, floor_num: int
    ) -> Optional[NavigationFloorORM]:
        query = select(cls.model).where(
            cls.model.location_id == location_id,
            cls.model.floor_num == floor_num,
        )

        result = await session.execute(query)
        return result.scalar_one_or_none()


@with_model(NavigationPointORM)
class NavigationPoint(Base):
    pass
