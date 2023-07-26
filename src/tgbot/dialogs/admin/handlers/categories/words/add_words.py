import io
from typing import TYPE_CHECKING

from aiogram import types, Bot
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
    if message.document:
        bot: Bot = manager.middleware_data['bot']
        file = await bot.get_file(message.document.file_id)
        result: io.BytesIO | None = await bot.download_file(file_path=file.file_path)
        messages = result.read().decode("UTF-8").split("\n")
        word_list = [msg.lower() for msg in messages if 5 <= len(msg) <= 7 and msg.isalpha()]
    else:
        messages = message.text.split("\n")
        word_list = [msg.lower() for msg in messages if 3 <= len(msg) <= 7 and msg.isalpha()]

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


async def on_delete_words_in_category(call: types.CallbackQuery, button: Button, manager: DialogManager):
    dao: "HolderDAO" = manager.middleware_data['dao']
    category_id: int = manager.dialog_data['category_id']

    await dao.word.delete_words_by_category_id(category_id)
    await dao.commit()
    await call.answer("Успешно!")
