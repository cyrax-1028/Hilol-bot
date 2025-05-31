from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.future import select
from app.database.models import Audio, Qori, Surah, User
from app.database.database import async_session
from app.keyboards.admin_buttons import get_admin_menu, get_admin_quran_menu
from app.handlers.states import AddQoriState
from app.services.add_qori_service import add_qori_to_db

admin_router = Router()


async def is_admin(user_id: int) -> bool:
    async with async_session() as session:
        result = await session.execute(select(User).filter_by(user_id=user_id))
        user = result.scalars().first()
        return user.is_admin if user else False


@admin_router.message(F.text == "🔝 Asosiy panel")
async def back_to_main_menu(message: Message):
    if await is_admin(message.from_user.id):
        await message.answer("Asosiy menyuga qaytdingiz:", reply_markup=get_admin_menu())


@admin_router.message(Command("admin"))
async def admin_panel(message: Message):
    if await is_admin(message.from_user.id):
        await message.answer("Admin panel", reply_markup=get_admin_menu())


@admin_router.message(F.text == "📖 Qur'on sozlash")
async def quran_menu_handler(message: Message):
    if await is_admin(message.from_user.id):
        await message.answer("Qur'on bo‘limi:", reply_markup=get_admin_quran_menu())


@admin_router.message(lambda msg: msg.text == "👳‍♂️ Qori qo'shish")
async def ask_qori_name(message: types.Message, state: FSMContext):
    if await is_admin(message.from_user.id):
        async with async_session() as session:
            qorilar_result = await session.execute(select(Qori))
            qorilar = qorilar_result.scalars().all()

        if qorilar:
            qorilar_names = "\n".join(f"- {q.name}" for q in qorilar)
            await message.answer(f"Hozirgi mavjud qorilar:\n{qorilar_names}")
        else:
            await message.answer("Hozircha qorilar mavjud emas.")

        await message.answer("👳‍♂️ Iltimos, qori ismini kiriting:")
        await state.set_state(AddQoriState.name)


@admin_router.message(AddQoriState.name)
async def save_qori_name(message: types.Message, state: FSMContext):
    qori_name = message.text.strip()
    await add_qori_to_db(qori_name)
    await message.answer(f"✅ Qori '{qori_name}' muvaffaqiyatli qo‘shildi.", reply_markup=get_admin_quran_menu())
    await state.clear()
