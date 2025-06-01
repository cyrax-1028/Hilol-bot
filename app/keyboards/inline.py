from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_info_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Batafsil", url="https://example.com")]
        ]
    )


def get_qorilar_inline_keyboard(qorilar):
    buttons = []
    for qori in qorilar:
        btns = [
            InlineKeyboardButton(text=f"{qori.name}", callback_data=f"qori_detail:{qori.id}"),
            InlineKeyboardButton(text="✏️", callback_data=f"edit_qori:{qori.id}"),
            InlineKeyboardButton(text="🗑", callback_data=f"delete_qori:{qori.id}")
        ]
        buttons.append(btns)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_cancel_inline():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel")]
    ])
