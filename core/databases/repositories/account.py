from sqlalchemy.ext.asyncio import AsyncSession

from core.databases.models import Account

from .utilities.base import BaseRepository


class AccountRepository(BaseRepository[Account]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=Account,
            session=session,
        )
