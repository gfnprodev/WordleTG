from aiogram import F
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Start, SwitchInlineQuery
from aiogram_dialog.widgets.text import Const, Format, Case

from src.tgbot.dialogs import states
from src.tgbot.dialogs.user.handlers.wordle_game import on_game_start, input_guess_word
from src.tgbot.dialogs.widgets.game_widget import GameWidget
from src.tgbot.dialogs.widgets.referral_widget import ReferralWidget

main_game_window = Window(
    Const("Новое слово загадано! Начните вводить его."),
    GameWidget(id="gaming"),
    MessageInput(input_guess_word),
    state=states.WordleGaming.GAME,
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
                         "Приз: <code>{dialog_data[prize]}</code>\n\n"
                         "<b>Хотите сыграть снова?</b>")
        },
        selector=lambda data, _, dm: data["dialog_data"]["game"]["win"]
    ),
    Start(text=Const("Сыграть снова"), id="play_again", state=states.WordleGameMenu.CHOOSE_CATEGORY),
    ReferralWidget(id='referral_button', text=Const("Загадать слово другу"), word_id=F['dialog_data']['game']['word_id'], user_id=F['middleware_data']['event_from_user'].id),
    Start(text=Const("В меню"), id="go_to_menu", state=states.Main.MAIN),
    state=states.WordleGaming.RESULT
)

main_game_dialog = Dialog(
    main_game_window,
    finish_window,
    on_start=on_game_start,
)