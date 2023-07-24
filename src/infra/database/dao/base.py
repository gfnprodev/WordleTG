from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO(ABC):
    @abstractmethod
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()
