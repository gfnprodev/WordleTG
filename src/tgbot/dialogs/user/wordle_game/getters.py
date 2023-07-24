from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.infra.database.dao.holder import HolderDAO


async def get_categories_getter(dao: "HolderDAO", **kwargs):
    categories = await dao.category.get_all_category()
    return {"categories": categories}


async def get_game_active_words(dao: "HolderDAO", **kwargs):
    game_history = [[["w", 1], ["o", 0], ["r", 2], ["d", 2], ["y", 1]],
                    [["w", 4], ["o", 3], ["r", 3], ["d", 1], ["y", 5]],
                    [["w", 3], ["o", 2], ["r", 3], ["d", 3], ["y", 3]]]

    return {"row1": game_history[0]}
