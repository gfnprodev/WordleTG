from aiogram import types
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from src.infra.database.dao.holder import HolderDAO


async def input_category_name(message: types.Message, message_input: MessageInput, manager: DialogManager):
    manager.dialog_data['category_name'] = message.text

    await manager.next()


async def input_category_description(message: types.Message, message_input: MessageInput, manager: DialogManager):
    manager.dialog_data['category_description'] = message.text

    await manager.next()


async def confirm_create_category(call: types.CallbackQuery, button: Button, manager: DialogManager):
    dao: HolderDAO = manager.middleware_data['dao']
    category_name = manager.dialog_data['category_name']
    category_description = manager.dialog_data['category_description']

    await dao.category.add_category(category_name, category_description)
    await dao.commit()
    await call.answer("Успешно!")
    await manager.done()
