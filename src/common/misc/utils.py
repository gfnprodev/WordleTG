import logging

import orjson
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession, create_async_engine

from .helpers import orjson_dumps


def create_session_factory(
        sqlalchemy_url: URL,
        log_level: int,
        expire_on_commit: bool = False,
        query_cache_size: int = 1200,
        pool_size: int = 100,
        max_overflow: int = 200,
) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    logger = logging.getLogger('sqlalchemy.engine')
    logger.setLevel(log_level)

    engine = create_async_engine(
        sqlalchemy_url,
        query_cache_size=query_cache_size,
        pool_size=pool_size,
        max_overflow=max_overflow,
        json_deserializer=orjson.loads,
        json_serializer=orjson_dumps,
        future=True,
    )

    session_factory = async_sessionmaker(bind=engine, expire_on_commit=expire_on_commit, class_=AsyncSession)
    return engine, session_factory
