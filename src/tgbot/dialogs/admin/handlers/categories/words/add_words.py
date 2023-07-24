from typing import TYPE_CHECKING

from aiogram import types
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from src.tgbot.dialogs import states

if TYPE_CHECKING:
    from src.infra.database.dao.holder import HolderDAO


async def on_start_add_words(call: types.CallbackQuery, button: Button, manager: DialogManager):
    category_id = manager.dialog_data['category_id']
    await manager.start(state=states.AddWordsInCategory.INPUT_WORDS, data={"category_id": category_id})


async def on_input_words(message: types.Message, message_input: MessageInput, manager: DialogManager):
    messages = message.text.split("\n")
    word_list = [msg.lower() for msg in messages if 3 <= len(msg) <= 10]

    manager.dialog_data['words'] = word_list
    manager.dialog_data['len_words'] = len(word_list)
    await manager.next()


async def confirm_create_words(call: types.CallbackQuery, button: Button, manager: DialogManager):
    word_list: list[str] = manager.dialog_data['words']
    category_id = manager.start_data['category_id']
    dao: "HolderDAO" = manager.middleware_data['dao']

    for word in word_list:
        await dao.word.add_word(word, category_id)
    await dao.commit()

    await call.answer("Успешно!")
    await manager.done()
