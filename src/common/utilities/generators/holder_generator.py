import logging
from typing import AsyncIterator, Callable

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.infra.database.dao.holder import HolderDAO

log = logging.getLogger(__name__)


def session_dependency(session_factory: async_sessionmaker[AsyncSession]) -> Callable[[], AsyncIterator[AsyncSession]]:
    async def dao_holder_generator() -> AsyncIterator[AsyncSession]:
        session = session_factory()
        try:
            yield HolderDAO(session)
        except Exception as e:
            log.exception(e)
            await session.rollback()
        finally:
            await session.close()
    return dao_holder_generator
