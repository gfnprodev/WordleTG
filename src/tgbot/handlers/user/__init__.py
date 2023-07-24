from aiogram import Router

from src.tgbot.handlers.user import start


def setup(router: Router) -> None:
    for module in (
        start,
    ):
        router.include_router(module.router)
