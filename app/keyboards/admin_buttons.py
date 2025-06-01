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
            [KeyboardButton(text="👳 Qorilar")],
            [KeyboardButton(text="🔝 Asosiy panel")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Bo'limlardan birini tanlang"
    )

def get_admin_qorilar_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👳 Qori qo'shish")],
            [KeyboardButton(text="📋 Qorilar ro'yxati")],
            [KeyboardButton(text="🔝 Asosiy panel")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Bo'limlardan birini tanlang"
    )

cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
    resize_keyboard=True
)
