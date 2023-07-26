from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra import dto
from src.infra.database.dao.base import BaseDAO
from src.infra.database.models import CustomWord


class CustomWordDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def add_custom_word(self, word: str) -> dto.CustomWordDTO:
        stmt = insert(CustomWord).values(word=word)

        stmt = stmt.on_conflict_do_update(
            index_elements=[CustomWord.word],
            set_=dict(word=stmt.excluded.word)
        ).returning(CustomWord)

        result = await self._session.scalars(stmt)

        word: CustomWord = result.first()

        return word.to_dto()

    async def get_custom_word_by_id(self, word_id: int) -> dto.CustomWordDTO | None:
        stmt = select(CustomWord).where(CustomWord.id == word_id)

        result = await self._session.scalars(stmt)

        word: CustomWord = result.first()
        if not word:
            return None

        return word.to_dto()
