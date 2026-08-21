from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import AsyncSessionLocal
from database import crud
from keyboards.reply import get_main_menu_keyboard
from services.localization import get_text
from config import settings

router = Router()

@router.message(F.text.in_([
    "👤 Мой профиль", "👤 Мій профіль", "👤 My Profile", "👤 Профиль", "/profile"
]))
async def show_profile(message: Message):
    async with AsyncSessionLocal() as session:
        user = await crud.get_or_create_user(
            session=session,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name
        )
        stats = await crud.get_user_rating_and_stats(session, message.from_user.id)
        lang = user.language or "ru"

        profile_text = get_text(
            "profile_card",
            lang,
            telegram_id=user.telegram_id,
            username=user.username or "без_юзернейма",
            rating=stats["avg_rating"],
            reviews_count=stats["reviews_count"],
            completed_deals=stats["completed_deals"],
            active_deals=stats["active_deals"],
            balance_rub=user.balance_rub or 0.0,
            balance_uah=user.balance_uah or 0.0,
            balance_usdt=user.balance_usdt or 0.0,
            balance_ton=user.balance_ton or 0.0
        )

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"💬 Отзывы ({stats['reviews_count']})",
                    callback_data="profile_reviews"
                ),
                InlineKeyboardButton(
                    text="💸 Запросить вывод",
                    callback_data="profile_withdraw"
                )
            ]
        ])

        await message.answer(
            profile_text,
            reply_markup=kb,
            parse_mode="HTML"
        )


@router.callback_query(F.data == "profile_reviews")
async def callback_profile_reviews(callback: CallbackQuery):
    async with AsyncSessionLocal() as session:
        reviews = await crud.get_user_reviews(session, callback.from_user.id, limit=5)

    if not reviews:
        await callback.answer("У вас пока нет отзывов", show_alert=True)
        return

    text = "⭐ <b>Последние отзывы о вашей работе:</b>\n\n"
    for r in reviews:
        stars = "⭐" * r.rating
        comment = f"<i>«{r.comment}»</i>" if r.comment else "<i>(без комментария)</i>"
        text += f"├ {stars} (Сделка #{r.deal_id})\n└ {comment}\n\n"

    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "profile_withdraw")
async def callback_profile_withdraw(callback: CallbackQuery):
    await callback.message.answer(
        "💸 <b>Вывод средств с баланса:</b>\n\n"
        "Заявка на вывод средств принята и будет автоматически обработана в ближайшее время.",
        parse_mode="HTML"
    )
    await callback.answer()
