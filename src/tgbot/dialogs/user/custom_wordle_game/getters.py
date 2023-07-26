from aiogram_dialog import DialogManager

from src.tgbot.dialogs.user.handlers.wordle_game import GameTD


async def curent_game_info_getter(dialog_manager: DialogManager, **kwargs):
    game: GameTD = dialog_manager.dialog_data['game']

    return {"word_length": len(game['word']), "not_exists_letters": ", ".join(game['nonexists_letters'])}