from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import AsyncSessionLocal
from database import crud
from keyboards.inline import get_language_keyboard
from keyboards.reply import get_main_menu_keyboard
from services.localization import get_text

router = Router()

@router.message(F.text.in_([
    "🌐 Смена языка", "🌐 Зміна мови", "🌐 Change Language", "/language"
]))
async def cmd_language(message: Message):
    async with AsyncSessionLocal() as session:
        user = await crud.get_user_by_tg_id(session, message.from_user.id)
        lang = user.language if user else "ru"

    await message.answer(
        get_text("choose_language", lang),
        reply_markup=get_language_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("set_lang:"))
async def callback_set_lang(callback: CallbackQuery):
    new_lang = callback.data.split(":")[1]
    async with AsyncSessionLocal() as session:
        await crud.update_user_language(session, callback.from_user.id, new_lang)

    confirm_text = get_text("language_changed", new_lang)
    await callback.message.edit_text(confirm_text, parse_mode="HTML")
    await callback.message.answer(
        get_text("welcome", new_lang),
        reply_markup=get_main_menu_keyboard(new_lang),
        parse_mode="HTML"
    )
    await callback.answer()
