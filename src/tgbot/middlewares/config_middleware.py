from typing import Any

from aiogram import BaseMiddleware

from src.common.config import Config
from src.tgbot.misc.helpers import HANDLER, EVENT, DATA


class ConfigMiddleware(BaseMiddleware):
    def __init__(self, config: Config):
        super().__init__()
        self.config = config

    async def __call__(self, handler: HANDLER, event: EVENT, data: DATA) -> Any:
        data['config'] = self.config
        result = await handler(event, data)
        del data['config']
        return result
