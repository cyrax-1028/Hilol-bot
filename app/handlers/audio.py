from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from app.database.models import Qori, Surah, Audio
from app.database.database import async_session
from app.handlers.states import AddAudioState
from app.handlers.admin import is_admin
from app.keyboards.admin_buttons import get_admin_quran_menu

admin_router = Router()


@admin_router.message(F.text == "🎧 Audio qo'shish")
async def start_adding_audio(message: Message, state: FSMContext):
    if await is_admin(message.from_user.id):
        async with async_session() as session:
            qorilar = await session.execute(Qori.__table__.select())
            qorilar = qorilar.fetchall()

            buttons = [[KeyboardButton(text=q.name)] for q in qorilar]
            buttons.append([KeyboardButton(text="🔝 Asosiy panel")])
            markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

            await message.answer("Qorini tanlang:", reply_markup=markup)
            await state.set_state(AddAudioState.choosing_qori)


@admin_router.message(AddAudioState.choosing_qori)
async def choose_qori(message: Message, state: FSMContext):
    qori_name = message.text
    async with async_session() as session:
        qori = await session.scalar(Qori.__table__.select().where(Qori.name == qori_name))

        if not qori:
            return await message.answer("❌ Qori topilmadi. Qaytadan tanlang.")

        await state.update_data(qori_id=qori)

        surahlar = await session.execute(Surah.__table__.select())
        surahlar = surahlar.fetchall()
        buttons = [[KeyboardButton(text=s.name)] for s in surahlar]
        buttons.append([KeyboardButton(text="📖 Qur'on sozlash")])
        buttons.append([KeyboardButton(text="🔝 Asosiy panel")])
        markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

        await message.answer("Endi surani tanlang:", reply_markup=markup)
        await state.set_state(AddAudioState.choosing_surah)


@admin_router.message(AddAudioState.choosing_surah)
async def choose_surah(message: Message, state: FSMContext):
    surah_name = message.text
    async with async_session() as session:
        surah = await session.scalar(Surah.__table__.select().where(Surah.name == surah_name))

        if not surah:
            return await message.answer("❌ Sura topilmadi. Qaytadan tanlang.")

        await state.update_data(surah_id=surah)

        await message.answer("Endi audio faylni yuboring:")
        await state.set_state(AddAudioState.sending_audio)


@admin_router.message(AddAudioState.sending_audio, F.audio)
async def save_audio(message: Message, state: FSMContext):
    data = await state.get_data()
    file_id = message.audio.file_id

    async with async_session() as session:
        new_audio = Audio(
            title=message.audio.title or "Noma'lum",
            file_id=file_id,
            surah_id=data["surah_id"],
            qori_id=data["qori_id"]
        )
        session.add(new_audio)
        await session.commit()

    await message.answer("✅ Audio muvaffaqiyatli qo‘shildi.")
    await message.answer("Qur'on bo‘limi:", reply_markup=get_admin_quran_menu())
    await state.clear()
