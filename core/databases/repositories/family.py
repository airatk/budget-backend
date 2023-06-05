from sqlalchemy.ext.asyncio import AsyncSession

from core.databases.models import Family

from .utilities.base import BaseRepository


class FamilyRepository(BaseRepository[Family]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=Family,
            session=session,
        )
