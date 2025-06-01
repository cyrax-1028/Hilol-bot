from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.future import select
from app.database.models import Audio, Qori, Surah, User
from app.database.database import async_session
from app.keyboards.admin_buttons import get_admin_menu, get_admin_quran_menu, cancel_keyboard, get_admin_qorilar_menu
from app.handlers.states import AddQoriState

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


@admin_router.message(F.text == "👳 Qorilar")
async def qorilar_menu_handler(message: Message):
    if await is_admin(message.from_user.id):
        await message.answer("Qorilar bo'limi", reply_markup=get_admin_qorilar_menu())


@admin_router.message(F.text == "❌ Bekor qilish")
async def cancel_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Amal bekor qilindi ✅", reply_markup=get_admin_menu())
