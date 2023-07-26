from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Button, SwitchInlineQuery
from aiogram_dialog.widgets.text import Const, Format

from src.tgbot.dialogs import states
from src.tgbot.dialogs.common import MAIN_MENU_BUTTON
from src.tgbot.dialogs.user.handlers.create_custom_word import input_custom_word, on_create_custom_word

input_word_window = Window(
    Const("Введите слово:\n\n"
          "Слово должно быть не менее 3 и не более 8 символов."),
    MessageInput(input_custom_word),
    Cancel(
        text=Const("Назад")
    ),
    state=states.CreateCustomWord.INPUT_WORD
)

confirm_input_word = Window(
    Format("Вы ввели слово: {dialog_data[word]}\n\n"
           "Вы уверены что хотите его создать?"),
    Button(
        text=Const("Создать"),
        id="yes_create_custom_word",
        on_click=on_create_custom_word
    ),
    Cancel(
        text=Const("Отмена")
    ),
    state=states.CreateCustomWord.CONFIRM
)

result_window = Window(
    Format("<b>Вы успешно загадали слово, скорее делись им с друзьями!</b>"),
    SwitchInlineQuery(
        text=Const("Поделиться"),
        switch_inline_query=Format("Я загадал тебе слово в Wordle!\n\n"
                                   "Попробуй его угадать: {dialog_data[word_link]}")
    ),
    MAIN_MENU_BUTTON,
    state=states.CreateCustomWord.RESULT
)


create_custom_word_dialog = Dialog(
    input_word_window,
    confirm_input_word,
    result_window
)