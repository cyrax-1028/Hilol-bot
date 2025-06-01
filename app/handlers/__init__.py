from aiogram import Dispatcher
from .user import router as user_router
from.namoz import router as namoz_router
from app.handlers.admin.qori import admin_router as qori_router
from app.handlers.admin.admin import admin_router as admin_router
from app.handlers.admin.audio import admin_router as audio_router

def register_all_handlers(dp: Dispatcher):
    dp.include_router(user_router)
    dp.include_router(namoz_router)
    dp.include_router(admin_router)
    dp.include_router(audio_router)
    dp.include_router(qori_router)
