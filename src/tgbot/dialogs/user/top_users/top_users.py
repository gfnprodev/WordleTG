from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Back
from aiogram_dialog.widgets.text import Format, Const

from src.tgbot.dialogs import states
from src.tgbot.dialogs.user.top_users.getters import get_users_top_getter

top_users = Window(
    Format("Топ пользователей по монетам:\n\n{top}"),
    Back(
        text=Const("Назад")
    ),
    state=states.Main.TOP_MONEY,
    getter=get_users_top_getter
)
