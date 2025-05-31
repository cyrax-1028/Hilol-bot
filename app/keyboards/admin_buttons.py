from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_admin_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📖 Qur'on sozlash")],
            [KeyboardButton(text="🔝 Asosiy menyu")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Bo'limlardan birini tanlang"
    )


def get_admin_quran_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎧 Audio qo'shish")],
            [KeyboardButton(text="🖼️ Rasm qo'shish")],
            [KeyboardButton(text="👳‍♂️ Qori qo'shish")],
            [KeyboardButton(text="🔝 Asosiy panel")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Bo'limlardan birini tanlang"
    )
