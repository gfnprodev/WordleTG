from aiogram import types, Bot
from aiogram.utils.deep_linking import create_start_link
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from src.infra.database.dao.holder import HolderDAO
from src.tgbot.dialogs import states


async def input_custom_word(message: types.Message, message_input: MessageInput, manager: DialogManager):
    if len(message.text) < 3 or len(message.text) > 8:
        await message.answer("Слово должно иметь не менее 3 и не более 8 символов.")
        return await manager.done()

    manager.dialog_data['word'] = message.text
    await manager.next()


async def on_create_custom_word(call: types.CallbackQuery, button: Button, manager: DialogManager):
    dao: HolderDAO = manager.middleware_data['dao']

    word = await dao.custom_words.add_custom_word(manager.dialog_data['word'])
    await dao.commit()
    bot: Bot = manager.middleware_data['bot']

    start_link = await create_start_link(bot, f"custom_{word.id}")

    manager.dialog_data['word_link'] = start_link
    await manager.switch_to(states.CreateCustomWord.RESULT)

