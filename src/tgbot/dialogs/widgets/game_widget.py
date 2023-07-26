from abc import ABC
from typing import List

from aiogram.types import InlineKeyboardButton
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Keyboard
from aiogram_dialog.widgets.text import Const

from src.tgbot.utilities.gaming import check_guesses, LetterState
from src.tgbot.dialogs.user.handlers.wordle_game import GameTD


class GameWidget(Keyboard, ABC):
    def __init__(self, id: str):
        super().__init__(id=id)

    async def render_keyboard(
            self,
            data,
            manager: DialogManager,
    ) -> List[List[InlineKeyboardButton]]:
        if not self.is_(data, manager):
            return []
        return await self._render_keyboard(data, manager)

    async def _render_keyboard(
            self,
            data,
            manager: DialogManager,
    ) -> List[List[InlineKeyboardButton]]:
        game: GameTD = manager.dialog_data['game']
        kb = []
        if game['round'] == 1:
            row = []
            empty_text = Const("[⬛]")
            for i in range(len(game['word'])):
                button = InlineKeyboardButton(
                    text=await empty_text.render_text(data, manager),
                    callback_data=self._own_callback_data())
                row.append(button)
            kb.append(row)
        for letters_guess in check_guesses(game['word'], *game['guesses']):
            row = []
            for letter, state in letters_guess:
                if state is LetterState.correct_position:
                    prefix = "🟩"
                elif state is LetterState.incorrect_position:
                    prefix = "🟨"
                else:
                    prefix = "⬛"
                button_text = f"{prefix} {letter}"
                text = Const(button_text)
                button = InlineKeyboardButton(
                    text=await text.render_text(data, manager),
                    callback_data=self._own_callback_data())
                row.append(button)
            kb.append(row)
        return kb
