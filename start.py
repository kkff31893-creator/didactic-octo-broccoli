from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import AsyncSessionLocal
from database import crud
from database.models import Deal
from keyboards.inline import get_rating_keyboard, get_skip_review_text_keyboard
from services.localization import get_text

router = Router()

class ReviewStates(StatesGroup):
    entering_text = State()


@router.callback_query(F.data.startswith("deal_review:"))
async def start_deal_review(callback: CallbackQuery):
    deal_id = int(callback.data.split(":")[1])
    async with AsyncSessionLocal() as session:
        deal = await crud.get_deal_by_id(session, deal_id)
        if not deal:
            await callback.answer("Сделка не найдена", show_alert=True)
            return

        has_rev = await crud.has_user_reviewed(session, deal_id, callback.from_user.id)
        if has_rev:
            await callback.answer("Вы уже оставили отзыв по этой сделке!", show_alert=True)
            return

        await callback.message.answer(
            f"⭐ <b>Оцените работу партнера по сделке #{deal.id}:</b>",
            reply_markup=get_rating_keyboard(deal.id),
            parse_mode="HTML"
        )
        await callback.answer()


@router.callback_query(F.data.startswith("rate:"))
async def process_star_rating(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split(":")
    deal_id = int(parts[1])
    rating = int(parts[2])

    await state.update_data(review_deal_id=deal_id, review_rating=rating)
    await state.set_state(ReviewStates.entering_text)

    async with AsyncSessionLocal() as session:
        user = await crud.get_user_by_tg_id(session, callback.from_user.id)
        lang = user.language if user else "ru"

    await callback.message.edit_text(
        f"⭐ Вы выбрали оценку: <b>{'⭐' * rating}</b> ({rating}/5)\n\n"
        f"✍️ <b>Напишите текстовый отзыв о сделке</b> или нажмите кнопку ниже, чтобы пропустить:",
        reply_markup=get_skip_review_text_keyboard(deal_id, rating, lang),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("rateskip:"))
async def process_skip_review_text(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split(":")
    deal_id = int(parts[1])
    rating = int(parts[2])
    await state.clear()

    async with AsyncSessionLocal() as session:
        deal = await crud.get_deal_by_id(session, deal_id)
        if not deal:
            await callback.answer("Сделка не найдена", show_alert=True)
            return

        to_tg_id = deal.seller_tg_id if callback.from_user.id == deal.buyer_tg_id else deal.buyer_tg_id
        if to_tg_id:
            await crud.add_review(
                session=session,
                deal_id=deal_id,
                from_tg_id=callback.from_user.id,
                to_tg_id=to_tg_id,
                rating=rating,
                comment=None
            )

    await callback.message.edit_text("✅ <b>Оценка успешно сохранена! Спасибо за ваш отзыв.</b>", parse_mode="HTML")
    await callback.answer()


@router.message(ReviewStates.entering_text)
async def process_review_comment(message: Message, state: FSMContext):
    data = await state.get_data()
    deal_id = data.get("review_deal_id")
    rating = data.get("review_rating", 5)
    await state.clear()

    async with AsyncSessionLocal() as session:
        deal = await crud.get_deal_by_id(session, deal_id)
        if not deal:
            await message.answer("Сделка не найдена.")
            return

        to_tg_id = deal.seller_tg_id if message.from_user.id == deal.buyer_tg_id else deal.buyer_tg_id
        if to_tg_id:
            await crud.add_review(
                session=session,
                deal_id=deal_id,
                from_tg_id=message.from_user.id,
                to_tg_id=to_tg_id,
                rating=rating,
                comment=message.text.strip()
            )

    await message.answer("✅ <b>Ваш отзыв успешно опубликован! Спасибо за обратную связь.</b>", parse_mode="HTML")
