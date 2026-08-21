from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from services.localization import get_text

def get_main_menu_keyboard(lang: str = "ru") -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text=get_text("btn_create_deal", lang)),
        ],
        [
            KeyboardButton(text=get_text("btn_profile", lang)),
            KeyboardButton(text=get_text("btn_my_deals", lang)),
        ],
        [
            KeyboardButton(text=get_text("btn_language", lang)),
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        is_persistent=True
    )
