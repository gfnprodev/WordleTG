from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Format, Const

from src.tgbot.dialogs import states

main_game_window = Window(
    Format("<b>На данный момент игра в разработке</b>"),
    Cancel(text=Const("Назад")),
    state=states.GuessHeroMenu.GAME
)


main_guess_hero_dialog = Dialog(
    main_game_window
)