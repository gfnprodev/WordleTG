from typing import Any

from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.infra.database.dao.holder import HolderDAO
from src.tgbot.misc.helpers import HANDLER, EVENT, DATA


class DBMiddleware(BaseMiddleware):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        super().__init__()
        self._session_factory = session_factory

    async def __call__(self, handler: HANDLER, event: EVENT, data: DATA) -> Any:
        async with self._session_factory() as session:
            dao = HolderDAO(session)
            data['dao'] = dao
            result = await handler(event, data)
            del data['dao']
        return result
