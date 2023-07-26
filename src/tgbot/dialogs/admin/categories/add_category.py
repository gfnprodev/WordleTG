from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Row, Button
from aiogram_dialog.widgets.text import Const, Format

from src.tgbot.dialogs import states
from src.tgbot.dialogs.admin.handlers.categories.add_category import input_category_name, confirm_create_category, \
    input_category_description

input_category_name_window = Window(
    Const("Введите название категории: "),
    Cancel(
        text=Const("Назад")
    ),
    MessageInput(input_category_name),
    state=states.AddCategoryMenu.INPUT_CATEGORY_NAME,
)

input_category_description = Window(
    Const("Введите описание категории: "),
    Cancel(
        text=Const("Отмена")
    ),
    MessageInput(input_category_description),
    state=states.AddCategoryMenu.INPUT_CATEGORY_DESCRIPTION
)

confirm_category_create_window = Window(
    Format("Название новой категории: <b>{dialog_data[category_name]}</b>\n\n"
           "Вы действительно хотите создать новую категорию с таким названием?"),
    Row(
        Cancel(
            text=Const("Нет")
        ),
        Button(
            text=Const("Да"),
            id="yes_create_category",
            on_click=confirm_create_category
        )
    ),
    state=states.AddCategoryMenu.CONFIRM
)

add_category_dialog = Dialog(
    input_category_name_window,
    input_category_description,
    confirm_category_create_window
)
