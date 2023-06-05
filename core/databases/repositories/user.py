from sqlalchemy.ext.asyncio import AsyncSession

from core.databases.models import User

from .utilities.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=User,
            session=session,
        )

    async def get_by_username(self, username: str) -> User | None:
        return await self.get(
            User.username == username,
        )
