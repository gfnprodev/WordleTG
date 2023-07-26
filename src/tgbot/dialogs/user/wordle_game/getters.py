from typing import TYPE_CHECKING

from aiogram_dialog import DialogManager

from src.tgbot.dialogs.user.handlers.wordle_game import GameTD

if TYPE_CHECKING:
    from src.infra.database.dao.holder import HolderDAO


async def get_categories_getter(dao: "HolderDAO", **kwargs):
    categories = await dao.category.get_all_category()
    return {"categories": categories}


async def curent_game_info_getter(dialog_manager: DialogManager, **kwargs):
    game: GameTD = dialog_manager.dialog_data['game']

    return {"word_length": len(game['word']), "not_exists_letters": ", ".join(game['nonexists_letters'])}


async def category_description_getter(dao: "HolderDAO", dialog_manager: DialogManager, **kwargs):
    cateogry_id: int = int(dialog_manager.dialog_data['category_id'])
    category = await dao.category.get_category(cateogry_id)

    return {"description": category.description}