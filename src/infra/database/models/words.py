from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa

from .base import BaseModel, TimestampMixin
from src.infra import dto

if TYPE_CHECKING:
    from .category import Category


class Word(BaseModel, TimestampMixin):
    id: Mapped[int] = mapped_column(sa.BIGINT, autoincrement=True, primary_key=True)
    word: Mapped[str] = mapped_column(sa.VARCHAR(11))
    category_id: Mapped[int] = mapped_column(sa.INT, sa.ForeignKey("categorys.id", ondelete="CASCADE"))
    category: Mapped["Category"] = relationship(back_populates="words", uselist=False)

    __table_args__ = (UniqueConstraint('word', 'category_id'),)

    def to_dto(self) -> dto.WordDTO:
        return dto.WordDTO(
            id=self.id,
            word=self.word,
            category_id=self.category_id
        )
