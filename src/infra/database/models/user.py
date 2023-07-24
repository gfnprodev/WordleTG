from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa

from .base import BaseModel, TimestampMixin
from src.infra import dto


class User(BaseModel, TimestampMixin):
    id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True)
    username: Mapped[str] = mapped_column(sa.VARCHAR(33))
    balance: Mapped[int] = mapped_column(sa.BIGINT)

    def to_dto(self) -> dto.UserDTO:
        return dto.UserDTO(
            id=self.id,
            username=self.username,
            balance=self.balance,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
