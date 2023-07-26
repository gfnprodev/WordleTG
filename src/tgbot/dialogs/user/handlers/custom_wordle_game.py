from aiogram import types
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from src.tgbot.dialogs import states
from src.tgbot.dialogs.user.handlers.wordle_game import GameTD
from src.tgbot.utilities.gaming import check_guess, LetterState


async def on_game_start(data: GameTD, dialog_manager: DialogManager) -> None:
    dialog_manager.dialog_data['game'] = data
    dialog_manager.current_context().start_data = None


async def input_guess_word(message: types.Message, message_input: MessageInput, manager: DialogManager):
    data: GameTD = manager.dialog_data['game']  # Game DATA
    guess_word = message.text.lower()  # User Input guessing word

    if len(guess_word) != len(data['word']):  # If len word < 5 answer user
        return await message.answer(f"Вы ввели слово не состоящее из {len(data['word'])} букв!")

    if guess_word == data['word']:  # WIN
        manager.dialog_data['game']['win'] = True

        return await manager.switch_to(states.CustomWordleGaming.RESULT)

    for letter, state in check_guess(message.text, data['word']):
        if state is LetterState.not_present:
            if letter not in data['nonexists_letters']:
                manager.dialog_data['game']['nonexists_letters'].append(letter)

    manager.dialog_data['game']['round'] += 1  # Round += 1 ALL ROUND = 6
    manager.dialog_data['game']['guesses'].append(guess_word)

    if manager.dialog_data['game']['round'] > 6:  # IF NEXT ROUND IS 7, 8, 9 e.t.c = Loose
        manager.dialog_data['game']['win'] = False  # Loose
        await manager.switch_to(states.CustomWordleGaming.RESULT)  # Switching to Result Window
