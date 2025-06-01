from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from app.core.bot import bot

SURAS_PER_PAGE = 10


async def send_audio_surah_page(chat_id: int, state: FSMContext, page: int):
    data = await state.get_data()
    audios = data.get("audios", [])
    qori_id = data.get("qori_id")

    start = page * SURAS_PER_PAGE
    end = start + SURAS_PER_PAGE
    page_audios = audios[start:end]

    buttons = [[KeyboardButton(text=audio.title)] for audio in page_audios]

    nav_buttons = []
    if page > 0:
        nav_buttons.append(KeyboardButton(text="⬅️ Orqaga"))
    nav_buttons.append(KeyboardButton(text="⬅️ Ortga"))
    if end < len(audios):
        nav_buttons.append(KeyboardButton(text="➡️ Oldinga"))

    buttons.append(nav_buttons)
    markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    await bot.send_message(chat_id, "Surani tanlang:", reply_markup=markup)

    await state.update_data(page=page)
