from aiogram import F
from aiogram.types import User
from aiogram_dialog import (
    Dialog, Window, LaunchMode,
)
from aiogram_dialog.widgets.kbd import Start, SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from src.common.config.bot import BotConfig
from src.infra.database.dao.holder import HolderDAO
from . import states
from .user.top_users.top_users import top_users
from ..utilities.other import plural_form

admins = BotConfig.compose().admins


async def get_user_data(dao: HolderDAO, event_from_user: User, **kwargs):
    user = await dao.user.get_user(event_from_user.id)
    if not user:
        user = await dao.user.add_user(event_from_user.id, "@" + event_from_user.username if event_from_user.username else event_from_user.first_name)
        await dao.commit()

    return {"user_id": user.id, "balance": f"{user.balance} {plural_form(user.balance)}"}


main_dialog = Dialog(
    Window(
        Format("Добро пожаловать в Wordle! Для начала игры нажмите кнопку ниже.\n\nВаш баланс: {balance}"),
        Start(
            text=Const("Играть"),
            id="play_game",
            state=states.WordleGameMenu.MAIN
        ),
        SwitchTo(
            text=Const("Топ пользователей"),
            id="top_users",
            state=states.Main.TOP_MONEY
        ),
        Start(
            text=Const('Админ-Меню'),
            id="admin_menu",
            when=F['user_id'].in_(admins),
            state=states.AdminMenu.MAIN
        ),
        state=states.Main.MAIN,
        getter=get_user_data
    ),
    top_users,
    launch_mode=LaunchMode.ROOT
)
