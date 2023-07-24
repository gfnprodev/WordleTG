from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Cancel, Start
from aiogram_dialog.widgets.text import Const

from src.tgbot.dialogs import states

main_admin_window = Window(
    Const("Admin Menu"),
    Start(
        text=Const("Категории"),
        id="categories",
        state=states.CategoriesMenu.MAIN
    ),
    Cancel(text=Const("Назад")),
    state=states.AdminMenu.MAIN
)


main_admin_dialog = Dialog(
    main_admin_window,
)