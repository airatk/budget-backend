from sqlalchemy.ext.asyncio import AsyncSession

from core.databases.models import Budget

from .utilities.base import BaseRepository


class BudgetRepository(BaseRepository[Budget]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=Budget,
            session=session,
        )
