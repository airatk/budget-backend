from sqlalchemy.ext.asyncio import AsyncSession

from core.databases.models import Category

from .utilities.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=Category,
            session=session,
        )
