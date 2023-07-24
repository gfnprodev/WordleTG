from abc import ABC
from typing import List

from aiogram import Bot
from magic_filter import MagicFilter
from aiogram.types import InlineKeyboardButton
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Keyboard
from aiogram_dialog.widgets.text import Text
from aiogram.utils.deep_linking import create_start_link


class ReferralWidget(Keyboard, ABC):
    def __init__(self, id: str, text: Text, word_id: MagicFilter, user_id: MagicFilter):
        super().__init__(id=id)
        self.word_id = word_id
        self.text = text
        self.user_id = user_id

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

        bot: Bot = data['middleware_data']['bot']
        user_id = self.user_id.resolve(data)
        word_id = self.word_id.resolve(data)
        start_link = await create_start_link(bot, f"{word_id}_{user_id}")
        invite_text = "Я загадал тебе слово с доты, попробуй его угадать 😉\n\n" \
                      f"{start_link}"
        kb = [
            [
                InlineKeyboardButton(text=await self.text.render_text(data, manager), switch_inline_query=invite_text)
            ]
        ]
        return kb
