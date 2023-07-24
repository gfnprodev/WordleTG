import logging

from aiogram import types, Router, Bot
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram_dialog import DialogManager, StartMode

from src.infra.database.dao.holder import HolderDAO
from src.tgbot.dialogs import states

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart(deep_link=True))
async def on_referral_start(message: types.Message, command: CommandObject, dialog_manager: DialogManager, dao: HolderDAO,
                            bot: Bot):
    user = await dao.user.get_user(message.from_user.id)
    if not user:
        await dao.user.add_user(message.from_user.id, "@" + message.from_user.username if message.from_user.username else message.from_user.first_name)
        await dao.commit()
    else:
        return await dialog_manager.start(states.Main.MAIN, mode=StartMode.RESET_STACK)
    args = command.args
    try:
        args = args.split("_")
        inviter = int(args[1])
        word_id = int(args[0])
    except Exception as e:
        logger.exception(e)
        return await dialog_manager.start(states.Main.MAIN, mode=StartMode.RESET_STACK)
    word = await dao.word.get_word_by_word_id(word_id)
    await dao.user.add_user_balance(inviter, 50)
    try:
        await bot.send_message(inviter, "<b>Вы пригласили нового пользователя и получили 50 монет!</b>")
    except Exception as e:
        logger.exception(e)
    if not word:
        return await dialog_manager.start(states.Main.MAIN, mode=StartMode.RESET_STACK)
    await dialog_manager.start(states.WordleGaming.GAME, data={"word": word.word, "round": 1, "guesses": [], "win": False,
                                                               "word_id": word_id})


@router.message(CommandStart())
async def cmd_start(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(states.Main.MAIN, mode=StartMode.RESET_STACK)
