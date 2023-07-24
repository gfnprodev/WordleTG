from _operator import attrgetter

from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Start, Back, Button, Cancel
from aiogram_dialog.widgets.text import Const, Format, Jinja

from src.tgbot.dialogs import states
from src.tgbot.dialogs.admin.categories.getters import categories_getter, category_info_getter
from src.tgbot.dialogs.admin.handlers.categories.category_menu import on_click_category, on_delete_category
from src.tgbot.dialogs.admin.handlers.categories.words.add_words import on_start_add_words

main_categories_menu = Window(
    Const("Categories Menu"),
    ScrollingGroup(
        Select(
            text=Format("{item.name}"),
            id="categories_picker",
            item_id_getter=attrgetter("id"),
            items="categories",
            on_click=on_click_category,
        ),
        id="categories",
        width=1,
        height=5,
        hide_on_single_page=True
    ),
    Start(
        text=Const("➕ Добавить категорию"),
        id="add_category",
        state=states.AddCategoryMenu.INPUT_CATEGORY_NAME
    ),
    Cancel(
        text=Const("Назад")
    ),
    state=states.CategoriesMenu.MAIN,
    getter=categories_getter
)

main_category_menu = Window(
    Jinja("Категория: <b>{{ category.name }}</b>\n"
          "Количество слов: <code>{{ category.words | length }}</code>\n"),
    Button(
        text=Const("Удалить"),
        id="delete_category",
        on_click=on_delete_category,
    ),
    Button(
        text=Const("➕ Добавить слова"),
        id="add_words_in_category",
        on_click=on_start_add_words,
    ),
    Back(
        text=Const("Назад")
    ),
    getter=category_info_getter,
    state=states.CategoriesMenu.CATEGORY_MENU
)

main_categories_dialog = Dialog(
    main_categories_menu,
    main_category_menu
)
