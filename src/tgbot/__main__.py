import asyncio
import logging

import betterlogging as bl
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from redis.asyncio.client import Redis

from src.common.config import Config
from src.common.misc.utils import create_session_factory
from src.tgbot.dialogs import register_dialogs
from src.tgbot.handlers import register_events
from src.tgbot.misc.helpers import get_bot_instance

log = logging.getLogger(__name__)


async def main():
    config = Config.from_env()
    bl.basic_colorized_config(level=config.misc.log_level)
    log.info("Starting...")

    db_engine, session_factory = create_session_factory(config.db.sqlalchemy_uri, config.misc.log_level)
    if config.misc.use_redis:
        redis = Redis(host=config.redis.host, port=config.redis.port, db=5)
        storage = RedisStorage(redis, key_builder=DefaultKeyBuilder(with_destiny=True))
    else:
        storage = MemoryStorage()
    workflow_data = dict(
        config=config,
    )
    bot = get_bot_instance(config.bot.bot_token)
    dp = Dispatcher(storage=storage, **workflow_data)
    register_events(dp, session_factory=session_factory, config=config)
    register_dialogs(dp)
    setup_dialogs(dp)
    # dp.errors.register(on_unknown_intent,
    #                    ExceptionTypeFilter(UnknownIntent))
    try:
        log.info("Everything is ready to launch")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await db_engine.dispose()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.info("Exiting...")
