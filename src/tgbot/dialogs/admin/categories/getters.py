from aiogram_dialog import DialogManager

from src.infra.database.dao.holder import HolderDAO


async def categories_getter(dao: HolderDAO, **kwargs):
    categories = await dao.category.get_all_category()

    return {"categories": categories}


async def category_info_getter(dao: HolderDAO, dialog_manager: DialogManager, **kwargs):
    category_id = dialog_manager.dialog_data['category_id']

    category = await dao.category.get_category(category_id)

    return {"category": category}
