from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDAO
from .category import CategoryDAO
from .user import UserDAO
from .word import WordDAO


class HolderDAO(BaseDAO):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.user = UserDAO(session)
        self.word = WordDAO(session)
        self.category = CategoryDAO(session)

    async def commit(self) -> None:
        await self._session.commit()
