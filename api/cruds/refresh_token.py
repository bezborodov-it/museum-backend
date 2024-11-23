from sqlalchemy import select

from api.cruds.base import Base, with_model
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import RefreshTokenORM


@with_model(RefreshTokenORM)
class RefreshToken(Base):
    @classmethod
    async def get_by_token(cls, session: AsyncSession, refresh_token: str) -> str:
        query = select(RefreshTokenORM).where(RefreshTokenORM.token == refresh_token)
        result = await session.execute(query)
        return result.scalars().first()
