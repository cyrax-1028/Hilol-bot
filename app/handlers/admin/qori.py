from sqlalchemy import select
from app.database.models import Qori
from app.database.database import async_session
from aiogram.fsm.context import FSMContext
from app.handlers.states import AddQoriState, EditQoriState
from app.keyboards.admin_buttons import get_admin_quran_menu, cancel_keyboard
from aiogram import Router, types, F
from app.services.qori_service import *
from app.keyboards.inline import get_qorilar_inline_keyboard, get_cancel_inline
from app.handlers.admin.admin import is_admin

admin_router = Router()

@admin_router.message(lambda msg: msg.text == "👳 Qori qo'shish")
async def ask_qori_name(message: types.Message, state: FSMContext):
    if await is_admin(message.from_user.id):
        await message.answer("👳‍♂️ Iltimos, qori ismini kiriting:", reply_markup=cancel_keyboard)

        await state.set_state(AddQoriState.name)


@admin_router.message(AddQoriState.name)
async def save_qori_name(message: types.Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await message.answer("❌ Qori qo‘shish bekor qilindi.", reply_markup=get_admin_quran_menu())
        await state.clear()
        return

    qori_name = message.text.strip()

    async with async_session() as session:
        existing_qori = await session.execute(
            select(Qori).where(Qori.name == qori_name)
        )
        existing_qori = existing_qori.scalar_one_or_none()

        if existing_qori:
            await message.answer(
                f"⚠️ Qori '{qori_name}' allaqachon mavjud. Iltimos, boshqa ism kiriting yoki ❌ Bekor qiling.")
            return

        new_qori = Qori(name=qori_name)
        session.add(new_qori)
        await session.commit()

    await message.answer(f"✅ Qori '{qori_name}' muvaffaqiyatli qo‘shildi.", reply_markup=get_admin_quran_menu())
    await state.clear()


@admin_router.message(F.text == "📋 Qorilar ro'yxati")
async def list_qorilar(message: types.Message):
    qorilar = await get_all_qorilar()
    if qorilar:
        await message.answer("Qorilar ro'yxati:", reply_markup=get_qorilar_inline_keyboard(qorilar))
    else:
        await message.answer("Hech qanday qori mavjud emas.")


@admin_router.callback_query(F.data.startswith("edit_qori:"))
async def start_edit_qori(call: types.CallbackQuery, state: FSMContext):
    qori_id = int(call.data.split(":")[1])
    qori = await get_qori_by_id(qori_id)
    if qori:
        await state.set_state(EditQoriState.waiting_for_new_name)
        await state.update_data(qori_id=qori_id)
        await call.message.answer(f"✏️ Yangi nomni kiriting (hozirgi: {qori.name}):", reply_markup=get_cancel_inline())
    await call.answer()


@admin_router.message(EditQoriState.waiting_for_new_name)
async def save_new_qori_name(message: types.Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await message.answer("❌ O‘zgartirish bekor qilindi.")
        await state.clear()
        return

    data = await state.get_data()
    qori_id = data["qori_id"]
    success = await update_qori(qori_id, message.text.strip())

    if success:
        await message.answer("✅ Qori nomi muvaffaqiyatli o‘zgartirildi.")
    else:
        await message.answer("❌ Xatolik yuz berdi.")

    await state.clear()


@admin_router.callback_query(F.data.startswith("delete_qori:"))
async def delete_qori_handler(call: types.CallbackQuery):
    qori_id = int(call.data.split(":")[1])
    success = await delete_qori(qori_id)

    if success:
        await call.message.edit_text("🗑 Qori o‘chirildi.")
    else:
        await call.message.edit_text("❌ Qori topilmadi yoki o‘chirib bo‘lmadi.")
    await call.answer()
