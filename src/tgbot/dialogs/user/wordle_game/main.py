from operator import itemgetter

from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import SwitchTo, Cancel, Select, ScrollingGroup, Back, Start, Button
from aiogram_dialog.widgets.text import Const, Format

from src.tgbot.dialogs import states
from src.tgbot.dialogs.common import MAIN_MENU_BUTTON
from src.tgbot.dialogs.user.wordle_game.getters import get_categories_getter, category_description_getter
from src.tgbot.dialogs.user.handlers.wordle_game import play_choose_category, on_click_play_choosed_category

main_window = Window(
    Const("<b>Выберите подходящую для вас игру: </b>\n\n"
          "Classic Worlde - Классический Wordle."),
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


WORDLE_CLASSIC_BUTTON = SwitchTo(
    text=Const("Назад"), id="back", state=states.WordleGameMenu.CHOOSE_CATEGORY,
)

category_info = Window(
    Format("{description}"),
    Button(
        text=Const("Начать играть"),
        id="get_category_info",
        on_click=on_click_play_choosed_category,
    ),
    WORDLE_CLASSIC_BUTTON,
    getter=category_description_getter,
    state=states.WordleGameMenu.CATEGORY_INFO
)

categorys_dialog = Window(
    Const("<b>Добро пожаловать в игру Wordle!</b>\n\n"
          "<i>Целью игры Wordle является угадывание загаданного слова за ограниченное количество попыток.</i>\n\n"
          "<code>1. Введите загаданное слово, количество букв у вас отображенно на клавиатуре под сообщением. (6 клавиш - 6 букв)\n"
          "2. Количество раундов - 6.\n"
          "3. Если буква отмечена чёрным - его нет в слове\n"
          "4. Если буква отмечена зелёным - она на своей позиции в слове\n"
          "5. Если буква отмеченая жёлтым - она есть в слове, но не на своей позиции\n"
          "6. Количество заработанных монет зависит от количества букв в слове и количестве раундов, за которое угадано слово.</code>\n\n\n"
          "<b>Выберите подходящую для вас категорию:</b>"),
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
    MAIN_MENU_BUTTON,
    getter=get_categories_getter,
    state=states.WordleGameMenu.CHOOSE_CATEGORY
)


main_gaming_dialog = Dialog(
    main_window,
    category_info,
    categorys_dialog
)
