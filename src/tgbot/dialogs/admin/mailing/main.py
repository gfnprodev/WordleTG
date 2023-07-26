from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Button
from aiogram_dialog.widgets.text import Const, Format

from src.tgbot.dialogs import states
from src.tgbot.dialogs.admin.handlers.mailing.mailing import input_mailing_text, start_mailing

input_mailing_text_window = Window(
    Const("Отправьте текст рассылки: "),
    MessageInput(input_mailing_text),
    Cancel(
        text=Const("Назад")
    ),
    state=states.MailingMenu.INPUT_MAILING_TEXT
)


confirm_mailing = Window(
    Format("Вы действительно хотите сделать рассылку с таким текстом:\n\n{dialog_data[message_text]}"),
    Button(
        text=Const("Отправить"),
        id="start_mailing",
        on_click=start_mailing
    ),
    Cancel(
        text=Const("Отмена")
    ),
    state=states.MailingMenu.CONFIRM
)


mailing_dialog = Dialog(
    input_mailing_text_window,
    confirm_mailing
)