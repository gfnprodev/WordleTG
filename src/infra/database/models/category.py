from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa

from .base import BaseModel, TimestampMixin
from src.infra import dto

if TYPE_CHECKING:
    from .words import Word
    from src.infra.dto import WordDTO


class Category(BaseModel, TimestampMixin):
    id: Mapped[int] = mapped_column(sa.INT, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.TEXT)
    words: Mapped[list["Word"]] = relationship(back_populates="category", uselist=True)

    def to_dto(self, words: list["WordDTO"] | None = None) -> dto.CategoryDTO:
        if words is None:
            words = []
        return dto.CategoryDTO(
            id=self.id,
            name=self.name,
            words=words
        )

    def to_dto_words_prefetched(self):
        return self.to_dto([word.to_dto() for word in self.words])
