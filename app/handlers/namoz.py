from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.services.pray_times import get_prayer_times
from app.keyboards.default import regions

router = Router()

@router.message(F.text.in_(regions))
async def show_prayer_times(message: Message, state: FSMContext):
    region = message.text
    prayer_times = get_prayer_times(region)
    if prayer_times:
        msg = f"📍 {region} uchun namoz vaqtlari:\n\n"
        msg += "\n".join([f"{key}: {value}" for key, value in prayer_times.items()])
        await message.answer(msg)
    else:
        await message.answer("❌ Namoz vaqtlarini olishda xatolik yuz berdi.")
