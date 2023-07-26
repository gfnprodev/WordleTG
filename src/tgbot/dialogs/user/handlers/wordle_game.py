from typing import Any, TYPE_CHECKING, TypedDict

from aiogram import types
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from src.tgbot.dialogs import states
from src.tgbot.utilities.gaming import check_guess, LetterState
from src.tgbot.utilities.other import plural_form

if TYPE_CHECKING:
    from src.infra.database.dao.holder import HolderDAO


class GameTD(TypedDict):
    word: str
    round: int
    guesses: list[str]
    win: bool
    word_id: int
    nonexists_letters: list


async def on_click_play_choosed_category(call: types.CallbackQuery, button: Button, manager: DialogManager):
    holder: "HolderDAO" = manager.middleware_data.get("dao")
    category_id: int = int(manager.dialog_data['category_id'])
    word = await holder.word.get_random_word_by_category_id(category_id)

    if not word:
        return await call.answer("Слов в категории нет!")
    await manager.start(states.WordleGaming.GAME,
                        data={"word": word.word, "round": 1, "guesses": [], "win": False, "word_id": word.id,
                              "nonexists_letters": []})


async def play_choose_category(call: types.CallbackQuery, widget: Any, manager: DialogManager, selected_item: str):
    category_id: int = int(selected_item)
    manager.dialog_data['category_id'] = category_id

    await manager.switch_to(states.WordleGameMenu.CATEGORY_INFO)


async def on_game_start(data: GameTD, dialog_manager: DialogManager) -> None:
    dialog_manager.dialog_data['game'] = data
    dialog_manager.current_context().start_data = None


async def input_guess_word(message: types.Message, message_input: MessageInput, manager: DialogManager):
    data: GameTD = manager.dialog_data['game']  # Game DATA
    guess_word = message.text.lower()  # User Input guessing word
    dao: HolderDAO = manager.middleware_data['dao']

    if len(guess_word) != len(data['word']):  # If len word < 5 answer user
        return await message.answer(f"Вы ввели слово не состоящее из {len(data['word'])} букв!")

    if guess_word == data['word']:  # WIN
        manager.dialog_data['game']['win'] = True

        length_bonus = 10
        prize = round(30 / data['round']) + round(((length_bonus * len(data['word'])) / data['round']))
        prize_text = f"{prize} {plural_form(prize)}"

        length_rating_bonus = 2
        rating = round(50 / data['round']) + round((length_rating_bonus * len(data['word']) / data['round']))

        await dao.user.add_user_balance(message.from_user.id, prize)
        await dao.user.edit_user_rating(message.from_user.id, rating)
        await dao.commit()

        manager.dialog_data['prize'] = prize_text
        return await manager.switch_to(states.WordleGaming.RESULT)

    for letter, state in check_guess(message.text, data['word']):
        if state is LetterState.not_present:
            if letter not in data['nonexists_letters']:
                manager.dialog_data['game']['nonexists_letters'].append(letter)

    manager.dialog_data['game']['round'] += 1  # Round += 1 ALL ROUND = 6
    manager.dialog_data['game']['guesses'].append(guess_word)

    if manager.dialog_data['game']['round'] > 6:  # IF NEXT ROUND IS 7, 8, 9 e.t.c = Loose
        manager.dialog_data['game']['win'] = False  # Loose

        length_rating_bonus = 2
        rating = round(50 / data['round']) + round((length_rating_bonus * len(data['word']) / data['round']))
        user = await dao.user.get_user(message.from_user.id)
        if user.rating - rating >= 0:
            await dao.user.edit_user_rating(message.from_user.id, -rating)
            await dao.commit()

        await manager.switch_to(states.WordleGaming.RESULT)  # Switching to Result Window
