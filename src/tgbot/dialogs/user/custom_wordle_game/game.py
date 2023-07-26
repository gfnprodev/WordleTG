from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Format, Case, Const

from src.tgbot.dialogs import states
from src.tgbot.dialogs.user.custom_wordle_game.getters import curent_game_info_getter
from src.tgbot.dialogs.user.handlers.custom_wordle_game import on_game_start
from src.tgbot.dialogs.user.handlers.custom_wordle_game import input_guess_word
from src.tgbot.dialogs.widgets.game_widget import GameWidget

main_game_window = Window(
    Format("Раунд: {dialog_data[game][round]}\n"
           "Количество букв в слове: {word_length}\n"
           "Нет букв: {not_exists_letters}\n\n"
           "Введите слово: "),
    GameWidget(id="custom_gaming"),
    MessageInput(input_guess_word),
    getter=curent_game_info_getter,
    state=states.CustomWordleGaming.GAME,
)


finish_window = Window(
    Case(
        {
            False: Format("<b>Вы не угадали загаданное слово!</b>\n\n"
                          "Слово: <code>{dialog_data[game][word]}</code>\n\n"
                          "Хотите сыграть снова?"),
            True: Format("<b>Вы угадали загаданное слово!</b>\n\n"
                         "Слово: <code>{dialog_data[game][word]}</code>\n"
                         "Количество раундов: <code>{dialog_data[game][round]}</code>\n"
                         "<b>Хотите сыграть снова?</b>")
        },
        selector=lambda data, _, dm: data["dialog_data"]["game"]["win"]
    ),
    Start(text=Const("Сыграть снова"), id="play_again", state=states.WordleGameMenu.MAIN),
    Start(text=Const("В меню"), id="go_to_menu", state=states.Main.MAIN),
    state=states.CustomWordleGaming.RESULT
)


main_custom_game_dialog = Dialog(
    main_game_window,
    finish_window,
    on_start=on_game_start,
)