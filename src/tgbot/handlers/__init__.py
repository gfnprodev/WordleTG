from typing import Any

from aiogram import Dispatcher
from . import user

from src.tgbot import middlewares


def register_events(dp: Dispatcher, **middleware_kwargs: Any) -> None:
    middlewares.setup(dp, **middleware_kwargs)
    user.setup(dp)
    # admin.setup(dp)
