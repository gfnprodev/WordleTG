from typing import Sequence

from sqlalchemy import select, insert, exists, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.infra import dto
from src.infra.database.dao.base import BaseDAO
from src.infra.database.models import Category


class CategoryDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def add_category(self, category_name: str, description: str) -> dto.CategoryDTO:
        stmt = exists(Category).where(Category.name == category_name).select()

        result = await self._session.scalars(stmt)

        category: bool = result.first()

        if category:
            raise ValueError("Category exists.")

        stmt = insert(Category).values(name=category_name, description=description).returning(Category)

        return (await self._session.scalars(stmt)).first().to_dto()

    async def delete_category(self, category_id: int) -> None:
        stmt = delete(Category).where(Category.id == category_id)

        await self._session.execute(stmt)

    async def get_category(self, category_id: int) -> dto.CategoryDTO | None:
        stmt = select(Category).where(Category.id == category_id).options(
            joinedload(Category.words)
        )

        result = await self._session.scalars(stmt)

        category: Category = result.unique().first()

        if not category:
            return None

        return category.to_dto_words_prefetched()

    async def get_all_category(self) -> list[dto.CategoryDTO]:
        stmt = select(Category).options(
            joinedload(Category.words)
        )

        result = await self._session.scalars(stmt)

        categories: Sequence[Category] = result.unique().all()

        return [category.to_dto_words_prefetched() for category in categories]
