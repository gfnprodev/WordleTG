from operator import itemgetter

from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import SwitchTo, Cancel, Select, ScrollingGroup, Back, Start
from aiogram_dialog.widgets.text import Const, Format

from src.tgbot.dialogs import states
from src.tgbot.dialogs.user.wordle_game.getters import get_categories_getter
from src.tgbot.dialogs.user.handlers.wordle_game import play_choose_category

main_window = Window(
    Const("Описание игры"),
    SwitchTo(
        text=Const("Classic Wordle"),
        id="choose_category",
        state=states.WordleGameMenu.CHOOSE_CATEGORY
    ),
    Start(
        text=Const("Угадай Героя"),
        id="guess_dota_2_hero",
        state=states.GuessHeroMenu.GAME
    ),
    Cancel(
        text=Const("Назад")
    ),
    state=states.WordleGameMenu.MAIN
)

categorys_dialog = Window(
    Const("Выберите категорию: "),
    ScrollingGroup(
        Select(
            text=Format("{item.name}"),
            id="get_category",
            item_id_getter=lambda item: item.id,
            items="categories",
            on_click=play_choose_category
        ),
        width=1,
        height=5,
        id="get_categories",
        hide_on_single_page=True
    ),
    Back(Const("Назад")),
    getter=get_categories_getter,
    state=states.WordleGameMenu.CHOOSE_CATEGORY
)


main_gaming_dialog = Dialog(
    main_window,
    categorys_dialog
)
