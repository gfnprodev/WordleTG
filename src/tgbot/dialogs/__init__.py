from aiogram import Router, Dispatcher

from src.tgbot.dialogs.admin.categories.add_category import add_category_dialog
from src.tgbot.dialogs.admin.categories.main import main_categories_dialog
from src.tgbot.dialogs.admin.categories.words.add_words import add_words_dialog
from src.tgbot.dialogs.admin.mailing.main import mailing_dialog
from src.tgbot.dialogs.admin.main import main_admin_dialog
from src.tgbot.dialogs.main import main_dialog
from src.tgbot.dialogs.user.create_custom_words.main import create_custom_word_dialog
from src.tgbot.dialogs.user.custom_wordle_game.game import main_custom_game_dialog
from src.tgbot.dialogs.user.guess_hero.game import main_guess_hero_dialog
from src.tgbot.dialogs.user.wordle_game.game import main_game_dialog
from src.tgbot.dialogs.user.wordle_game.main import main_gaming_dialog


def register_dialogs(dp: Dispatcher):
    dialog_router = Router()
    dialog_router.include_routers(
        main_dialog,
        main_gaming_dialog,
        main_game_dialog,
        main_guess_hero_dialog,
        main_admin_dialog,
        main_categories_dialog,
        add_category_dialog,
        add_words_dialog,
        mailing_dialog,
        main_custom_game_dialog,
        create_custom_word_dialog
    )
    dp.include_router(dialog_router)
