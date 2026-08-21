from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import AsyncSessionLocal
from database import crud
from services.localization import get_text
from config import settings

router = Router()

@router.message(F.text.in_([
    "💬 Поддержка", "💬 Підтримка", "💬 Support", "/support"
]))
async def show_support(message: Message):
    async with AsyncSessionLocal() as session:
        user = await crud.get_user_by_tg_id(session, message.from_user.id)
        lang = user.language if user else "ru"

    text = get_text("support_text", lang, support_username=settings.SUPPORT_USERNAME)
    await message.answer(text, parse_mode="HTML")


@router.callback_query(F.data == "support_contact")
async def callback_support_contact(callback: CallbackQuery):
    async with AsyncSessionLocal() as session:
        user = await crud.get_user_by_tg_id(session, callback.from_user.id)
        lang = user.language if user else "ru"

    text = get_text("support_text", lang, support_username=settings.SUPPORT_USERNAME)
    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()
