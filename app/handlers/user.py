from aiogram import Router, types, F
from app.keyboards.default import get_main_menu, get_quran_menu, get_dua_menu, get_namoz_times_menu
from app.services.user_service import save_user_if_not_exists
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from app.services.ai_service import ask_bahromjon_ai
from app.services.help_menu import HELP_TEXT, CONECT_TO_ADMIN
from app.database.database import async_session
from app.database.models import Qori, Audio, Surah
from app.handlers.states import UserAudioState
from app.services.audio_service import send_audio_surah_page, SURAS_PER_PAGE
from app.core.bot import bot


router = Router()


@router.message(F.text == "/start")
async def start_handler(message: types.Message):
    await save_user_if_not_exists(message.from_user)
    await message.answer("Assalomu alaykum!", reply_markup=get_main_menu())


@router.message(F.text == "📖 Qur'on")
async def quran_menu_handler(message: Message):
    await message.answer("Qur'on bo‘limi:", reply_markup=get_quran_menu())


@router.message(F.text == "🙏 Duo va zikr")
async def dua_menu_handler(message: Message):
    await message.answer("Duo bo'limi:", reply_markup=get_dua_menu())


@router.message(F.text == "🕋 Namoz vaqtlari")
async def namoz_menu_handler(message: Message):
    await message.answer("Hududlardan birini tanlang:", reply_markup=get_namoz_times_menu())


class AIState(StatesGroup):
    waiting_for_question = State()


@router.message(F.text == "📄 Eslatma")
async def disklaymer_handler(message: Message):
    await message.answer(
        "📄 Eslatma: \n\n"
        "Ushbu botdagi barcha ma’lumotlar rasmiy saytlardan olingan va "
        "ruxsat asosida foydalanilmoqda.\n\n"
        "Bot hech qanday tijoriy maqsadda ishlatilmaydi. "
        "Agar xatolik yoki noto‘g‘ri ma’lumot ko‘rsangiz, iltimos, [admin](https://t.me/QuestionUZ_Robot?start=acdd3a6f02ed4c) bilan bog‘laning.\n\n"
        "📚 Manbalar:\n"
        "==> https://muslim.uz\n"
        "==> https://islom.uz/\n",
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )


@router.message(F.text == "🤖 AI bo'limi")
async def enter_ai_mode(message: Message, state: FSMContext):
    await message.answer(
        "Salom! AI bo'limiga xush kelibsiz !\n",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="🔝 Asosiy menyu")]],
            resize_keyboard=True
        )
    )
    await state.set_state(AIState.waiting_for_question)


@router.message(AIState.waiting_for_question)
async def ai_response_handler(message: Message, state: FSMContext):
    user_text = message.text

    if user_text == "🔝 Asosiy menyu":
        await state.clear()
        await message.answer("Asosiy menyuga qaytdingiz.", reply_markup=get_main_menu())
        return

    response = await ask_bahromjon_ai(user_text)
    await message.answer(response)


@router.message(F.text == "ℹ️ Yordam")
async def help_handler(message: types.Message):
    await message.answer(HELP_TEXT)
    await message.answer(CONECT_TO_ADMIN, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


@router.message(F.text == "🔝 Asosiy menyu")
async def back_to_main_menu(message: Message):
    await message.answer("Asosiy menyuga qaytdingiz:", reply_markup=get_main_menu())


@router.message(F.text == "🎧 Audio")
async def open_audio_section(message: Message, state: FSMContext):
    async with async_session() as session:
        qorilar = await session.execute(Qori.__table__.select())
        qorilar = qorilar.fetchall()

    buttons = [[KeyboardButton(text=q.name)] for q in qorilar]
    buttons.append([KeyboardButton(text="⬅️ Ortga")])
    markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    await message.answer("Qorini tanlang:", reply_markup=markup)
    await state.set_state(UserAudioState.choosing_qori)


@router.message(UserAudioState.choosing_qori)
async def qori_tanlandi(message: Message, state: FSMContext):
    qori_name = message.text

    if qori_name == "⬅️ Ortga":
        await message.answer("Ortga qaytdingiz.", reply_markup=get_quran_menu())
        await state.clear()
        return

    async with async_session() as session:
        qori = await session.execute(Qori.__table__.select().where(Qori.name == qori_name))
        qori = qori.scalar_one_or_none()
        if not qori:
            await message.answer("Bunday qori topilmadi. Iltimos, qaytadan tanlang.")
            return

        audios = await session.execute(
            Audio.__table__.select().where(Audio.qori_id == qori)
        )
        audios = audios.fetchall()

    if not audios:
        await message.answer("Bu qoriga tegishli audio topilmadi.")
        return

    await state.update_data(qori_id=qori, page=0, audios=[a for a in audios])

    await send_audio_surah_page(message.chat.id, state, 0)
    await state.set_state(UserAudioState.choosing_sura)


@router.message(UserAudioState.choosing_sura)
async def sura_yoki_navi(message: Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    page = data.get("page", 0)
    audios = data.get("audios", [])

    if text == "⬅️ Ortga":
        await message.answer("Asosiy panelga qaytdingiz.", reply_markup=get_quran_menu())
        await state.clear()
        return

    if text == "⬅️ Orqaga":
        new_page = max(0, page - 1)
        await send_audio_surah_page(message.chat.id, state, new_page)
        return

    if text == "➡️ Oldinga":
        max_page = (len(audios) - 1) // SURAS_PER_PAGE
        new_page = min(max_page, page + 1)
        await send_audio_surah_page(message.chat.id, state, new_page)
        return

    for audio in audios:
        if audio.title == text:
            await bot.send_audio(chat_id=message.chat.id, audio=audio.file_id)
            return

    await message.answer("Iltimos, menyudan surani tanlang yoki navigatsiya tugmalarini ishlating.")
