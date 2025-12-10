from api.cruds.base import Base, with_model, select
from api.models import InclusiveStoryORM, StoryORM
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

@with_model(InclusiveStoryORM)
class InclusiveStory(Base):
    @classmethod
    async def get_by_location_id(
            cls, session: AsyncSession, location_id: int
    ) -> List[InclusiveStoryORM]:
        query = select(cls.model).where(cls.model.location_id == location_id)
        result = await session.execute(query)
        return result.scalars().all()


@with_model(StoryORM)
class Story(Base):
    pass
