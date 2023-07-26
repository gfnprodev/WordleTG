from typing import TYPE_CHECKING

from aiogram import types
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from src.tgbot.utilities.mailing.nats_mailing import NatsMailing

if TYPE_CHECKING:
    from src.infra.database.dao.holder import HolderDAO


async def input_mailing_text(message: types.Message, message_input: MessageInput, manager: DialogManager):
    message_text = message.html_text
    manager.dialog_data['message_text'] = message_text
    await manager.next()


async def start_mailing(call: types.CallbackQuery, button: Button, manager: DialogManager):
    dao: "HolderDAO" = manager.middleware_data['dao']
    message_text = manager.dialog_data['message_text']
    nc = NatsMailing()
    await nc.connect()
    users = await dao.user.get_all_users()
    await nc.start_mailing(message_text, users)
    await nc.close()
    await manager.done()
