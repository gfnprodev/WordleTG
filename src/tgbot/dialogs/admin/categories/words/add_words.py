from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Row, Button
from aiogram_dialog.widgets.text import Const, Jinja, Format

from src.tgbot.dialogs import states
from src.tgbot.dialogs.admin.handlers.categories.words.add_words import confirm_create_words, on_input_words

input_words_window = Window(
    Const("Введите слова через строку. Пример:\n\n"
          "столб\n"
          "лампа\n"
          "мороз\n"
          "лента\n"
          "плита"),
    Cancel(
        text=Const("Назад")
    ),
    MessageInput(on_input_words),
    state=states.AddWordsInCategory.INPUT_WORDS
)

confirm_new_words_window = Window(
    Format("Слов на добавление: <code>{dialog_data[len_words]}</code>\n\n"
           "Вы действительно хотите их добавить?"),
    Row(
        Cancel(
            text=Const("Нет")
        ),
        Button(
            text=Const("Да"),
            id="yes_create_category",
            on_click=confirm_create_words
        )
    ),
    state=states.AddWordsInCategory.CONFIRM
)

add_words_dialog = Dialog(
    input_words_window,
    confirm_new_words_window
)
