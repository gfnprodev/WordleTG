from typing import Any, TYPE_CHECKING

from aiogram import types
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from src.tgbot.dialogs import states

if TYPE_CHECKING:
    from src.infra.database.dao.holder import HolderDAO


async def on_click_category(call: types.CallbackQuery, widget: Any, manager: DialogManager, selected_item: str):
    manager.dialog_data['category_id'] = int(selected_item)

    await manager.switch_to(state=states.CategoriesMenu.CATEGORY_MENU)


async def on_delete_category(call: types.CallbackQuery, button: Button, manager: DialogManager):
    category_id = manager.dialog_data['category_id']
    dao: "HolderDAO" = manager.middleware_data['dao']

    await dao.category.delete_category(category_id)
    await dao.commit()
    await call.answer("Успешно!")
    await manager.switch_to(state=states.CategoriesMenu.MAIN)
