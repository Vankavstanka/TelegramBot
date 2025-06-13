from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Iterable

def delete_keyboard(tasks: Iterable[dict]) -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    for t in tasks:
        kb.button(text=f"Удалить {t['id']}", callback_data=f"del:{t['id']}")
    kb.adjust(2)
    return kb
