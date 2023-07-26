from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDAO
from .category import CategoryDAO
from .custom_words import CustomWordDAO
from .user import UserDAO
from .word import WordDAO


class HolderDAO(BaseDAO):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.user = UserDAO(session)
        self.word = WordDAO(session)
        self.category = CategoryDAO(session)
        self.custom_words = CustomWordDAO(session)

    async def commit(self) -> None:
        await self._session.commit()
