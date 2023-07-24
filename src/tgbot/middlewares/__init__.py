from typing import Any

from aiogram import Router
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .db_middleware import DBMiddleware
from .config_middleware import ConfigMiddleware


def setup(router: Router, **kwargs: Any) -> None:
    session_factory: async_sessionmaker[AsyncSession] = kwargs['session_factory']
    for middleware in (
        DBMiddleware(session_factory),
        ConfigMiddleware(kwargs['config']),
    ):
        router.message.outer_middleware(middleware)
        router.callback_query.outer_middleware(middleware)
