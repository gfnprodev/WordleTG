from datetime import datetime
from re import split, Pattern, compile
from typing import Any, cast, Type, Final

from sqlalchemy import inspect, func, MetaData
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import (
    DeclarativeMeta, registry, declared_attr, has_inherited_table, declarative_mixin, Mapped, mapped_column
)

convention = {
    "ix": "ix__%(column_0_label)s",
    "uq": "uq__%(table_name)s__%(column_0_name)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "pk__%(table_name)s",
}
metadata = MetaData(naming_convention=convention)
mapper_registry = registry(metadata=metadata)

TABLE_NAME_REGEX: Pattern[str] = compile(r'(?<=[A-Z])(?=[A-Z][a-z])|(?<=[^A-Z])(?=[A-Z])')
PLURAL: Final[str] = 's'


class BaseModel(metaclass=DeclarativeMeta):
    __abstract__ = True
    __mapper_args__ = {'eager_defaults': True}

    def __init__(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    registry = mapper_registry
    metadata = mapper_registry.metadata

    @declared_attr
    def __tablename__(self) -> str | None:
        if has_inherited_table(cast(Type[BaseModel], self)):
            return None
        cls_name = cast(Type[BaseModel], self).__qualname__
        table_name_parts = split(TABLE_NAME_REGEX, cls_name)
        formatted_table_name = ''.join(
            table_name_part.lower() + '_' for i, table_name_part in enumerate(table_name_parts)
        )
        last_underscore = formatted_table_name.rfind('_')
        return formatted_table_name[:last_underscore] + PLURAL

    def _get_attributes(self) -> dict[Any, Any]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    def __str__(self) -> str:
        attrs = '|'.join(str(v) for k, v in self._get_attributes().items())
        return f'{self.__class__.__qualname__} {attrs}'

    def __repr__(self) -> str:
        table_attrs = inspect(self).attrs
        primary_keys = ' '.join(
            f'{key.name}={table_attrs[key.name].value}'
            for key in inspect(self.__class__).primary_key
        )
        return f'{self.__class__.__qualname__}->{primary_keys}'

    def as_dict(self) -> dict[Any, Any]:
        return self._get_attributes()


@declarative_mixin
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), server_default=func.now(), onupdate=func.now(),
    )


__all__ = (
    'BaseModel',
    'TimestampMixin',
)