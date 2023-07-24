from typing import Any, Callable, Awaitable

from aiogram import Bot
from aiogram.types import CallbackQuery, Message

EVENT = CallbackQuery | Message
DATA = dict[str, Any]
HANDLER = Callable[[EVENT, DATA], Awaitable[Any]]


def get_bot_instance(token: str) -> Bot:
    return Bot(token=token,
               parse_mode='HTML')
