from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📖 Qur'on")],
            [KeyboardButton(text="🕋 Namoz vaqtlari")],
            [KeyboardButton(text="🙏 Duo")],
            [KeyboardButton(text="🤖 AI bo'limi")],
            [KeyboardButton(text="📄 Eslatma")],
            # [KeyboardButton(text="📘 O‘rganish")],
            [KeyboardButton(text="ℹ️ Yordam")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Bo'limlardan birini tanlang"
    )


def get_quran_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎧 Audio")],
            [KeyboardButton(text="🖼️ Rasm")],
            [KeyboardButton(text="🔝 Asosiy menyu")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Bo'limlardan birini tanlang"
    )


def get_dua_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎧 Audio")],
            [KeyboardButton(text="🖼️ Rasm")],
            [KeyboardButton(text="🔝 Asosiy menyu")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Bo'limlardan birini tanlang"
    )


regions = [
    "Tashkent", "Samarkand", "Bukhara", "Khiva",
    "Andijan", "Namangan", "Fergana", "Navoi",
    "Qarshi", "Termez", "Sirdarya",
    "Jizzakh", "Nukus"
]


def get_namoz_times_menu():
    keyboard = [
        [KeyboardButton(text=region) for region in regions[i:i + 3]]
        for i in range(0, len(regions), 3)
    ]
    keyboard.append([KeyboardButton(text="🔝 Asosiy menyu")])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Hududingizni tanlang"
    )
