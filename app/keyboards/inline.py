from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_info_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Batafsil", url="https://example.com")]
        ]
    )
