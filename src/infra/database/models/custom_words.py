import sqlalchemy as sa
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.infra import dto
from .base import BaseModel, TimestampMixin


class CustomWord(BaseModel, TimestampMixin):
    id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(sa.VARCHAR(7))

    __table_args__ = (UniqueConstraint('word'),)

    def to_dto(self) -> dto.CustomWordDTO:
        return dto.CustomWordDTO(
            id=self.id,
            word=self.word
        )
