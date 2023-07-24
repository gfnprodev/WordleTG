from sqlalchemy import select, delete, Result, and_, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra import dto
from src.infra.database.dao.base import BaseDAO
from src.infra.database.models import Word


class WordDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def add_word(self, word: str, category_id: int) -> None:
        stmt = insert(Word).values(word=word, category_id=category_id)
        stmt = stmt.on_conflict_do_update(
            index_elements=[Word.word, Word.category_id],
            set_=dict(word=stmt.excluded.word, category_id=stmt.excluded.category_id)
        )
        await self._session.execute(stmt)

    async def delete_word(self, word: str, category_id: int) -> None:
        stmt = delete(Word).where(Word.word == word, Word.category_id == category_id)

        await self._session.execute(stmt)

    async def get_word_by_word_id(self, word_id: int) -> dto.WordDTO | None:
        stmt = select(Word).where(Word.id == word_id)

        result = await self._session.scalars(stmt)

        word: Word = result.first()
        if not word:
            return None

        return word.to_dto()

    async def get_random_word_by_category_id(self, category_id: int) -> dto.WordDTO | None:
        stmt = select(Word).where(Word.category_id == category_id).order_by(func.random()).limit(1)

        result = await self._session.scalars(stmt)

        word: Word = result.first()
        if not word:
            return None

        return word.to_dto()
