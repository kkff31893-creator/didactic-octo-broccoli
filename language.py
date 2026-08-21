from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import AsyncSessionLocal
from database import crud
from database.models import DealStatus, DealRole
from keyboards.reply import get_main_menu_keyboard
from keyboards.inline import (
    get_role_choice_keyboard,
    get_currency_choice_keyboard,
    get_cancel_keyboard,
    get_deal_action_keyboard,
    get_payment_details_keyboard,
    get_my_deals_filter_keyboard
)
from services.localization import get_text
from services.deal_service import format_deal_text, notify_deal_participants
from config import settings

router = Router()

class DealCreationStates(StatesGroup):
    choosing_role = State()
    choosing_currency = State()
    entering_amount = State()
    entering_title = State()


class DisputeStates(StatesGroup):
    entering_reason = State()


# --- DEAL CREATION FSM ---

@router.message(F.text.in_([
    "🤝 Создать сделку", "🤝 Створити угоду", "🤝 Create Deal", "/create_deal"
]))
async def start_deal_creation(message: Message, state: FSMContext):
    await state.clear()
    async with AsyncSessionLocal() as session:
        user = await crud.get_or_create_user(session, message.from_user.id, message.from_user.username, message.from_user.full_name)
        lang = user.language or "ru"
    
    await state.set_state(DealCreationStates.choosing_role)
    await message.answer(
        get_text("create_deal_step_role", lang),
        reply_markup=get_role_choice_keyboard(lang),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("create_role:"))
async def process_role_choice(callback: CallbackQuery, state: FSMContext):
    role = callback.data.split(":")[1]
    await state.update_data(role=role)
    
    async with AsyncSessionLocal() as session:
        user = await crud.get_user_by_tg_id(session, callback.from_user.id)
        lang = user.language if user else "ru"

    await state.set_state(DealCreationStates.choosing_currency)
    await callback.message.edit_text(
        get_text("create_deal_step_currency", lang),
        reply_markup=get_currency_choice_keyboard(lang),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("create_curr:"))
async def process_currency_choice(callback: CallbackQuery, state: FSMContext):
    currency = callback.data.split(":")[1]
    await state.update_data(currency=currency)

    async with AsyncSessionLocal() as session:
        user = await crud.get_user_by_tg_id(session, callback.from_user.id)
        lang = user.language if user else "ru"

    await state.set_state(DealCreationStates.entering_amount)
    await callback.message.edit_text(
        get_text("create_deal_step_amount", lang),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(DealCreationStates.entering_amount)
async def process_amount_input(message: Message, state: FSMContext):
    async with AsyncSessionLocal() as session:
        user = await crud.get_user_by_tg_id(session, message.from_user.id)
        lang = user.language if user else "ru"

    raw_text = message.text.replace(",", ".").strip()
    try:
        amount = float(raw_text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer(
            get_text("invalid_amount", lang),
            reply_markup=get_cancel_keyboard(lang),
            parse_mode="HTML"
        )
        return

    await state.update_data(amount=amount)
    await state.set_state(DealCreationStates.entering_title)
    await message.answer(
        get_text("create_deal_step_title", lang),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML"
    )


@router.message(DealCreationStates.entering_title)
async def process_title_input(message: Message, state: FSMContext, bot: Bot):
    async with AsyncSessionLocal() as session:
        user = await crud.get_user_by_tg_id(session, message.from_user.id)
        lang = user.language if user else "ru"

        data = await state.get_data()
        await state.clear()

        deal = await crud.create_deal(
            session=session,
            creator_tg_id=message.from_user.id,
            creator_role=data["role"],
            currency=data["currency"],
            amount=data["amount"],
            title=message.text.strip(),
            description=None
        )

        bot_user = await bot.get_me()
        invite_link = f"https://t.me/{bot_user.username}?start={deal.deal_code}"
        role_text = get_text("role_buyer", lang) if deal.creator_role == DealRole.BUYER else get_text("role_seller", lang)

        success_text = get_text(
            "deal_created_success",
            lang,
            deal_id=deal.id,
            title=deal.title,
            amount=f"{deal.amount:g}",
            currency=deal.currency,
            role_text=role_text,
            invite_link=invite_link
        )

        kb = get_deal_action_keyboard(
            deal_id=deal.id,
            user_tg_id=message.from_user.id,
            deal_status=deal.status,
            buyer_tg_id=deal.buyer_tg_id or 0,
            seller_tg_id=deal.seller_tg_id or 0,
            lang=lang
        )

        await message.answer(
            success_text,
            reply_markup=kb,
            parse_mode="HTML"
        )


@router.callback_query(F.data == "cancel_action")
async def cancel_action_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    async with AsyncSessionLocal() as session:
        user = await crud.get_user_by_tg_id(session, callback.from_user.id)
        lang = user.language if user else "ru"
    
    await callback.message.edit_text("❌ <b>Действие отменено.</b>", parse_mode="HTML")
    await callback.answer()


# --- DEAL LIFECYCLE HANDLERS ---

@router.callback_query(F.data.startswith("deal_refresh:"))
async def callback_deal_refresh(callback: CallbackQuery):
    deal_id = int(callback.data.split(":")[1])
    async with AsyncSessionLocal() as session:
        user = await crud.get_user_by_tg_id(session, callback.from_user.id)
        lang = user.language if user else "ru"
        deal = await crud.get_deal_by_id(session, deal_id)

        if not deal:
            await callback.answer("Сделка не найдена", show_alert=True)
            return

        has_reviewed = await crud.has_user_reviewed(session, deal.id, callback.from_user.id)
        deal_text = await format_deal_text(session, deal, callback.from_user.id, lang)
        kb = get_deal_action_keyboard(
            deal_id=deal.id,
            user_tg_id=callback.from_user.id,
            deal_status=deal.status,
            buyer_tg_id=deal.buyer_tg_id or 0,
            seller_tg_id=deal.seller_tg_id or 0,
            lang=lang,
            has_reviewed=has_reviewed
        )

        try:
            await callback.message.edit_text(deal_text, reply_markup=kb, parse_mode="HTML")
        except Exception:
            pass
        await callback.answer("🔄 Данные обновлены")


@router.callback_query(F.data.startswith("deal_pay:"))
async def callback_deal_pay(callback: CallbackQuery):
    deal_id = int(callback.data.split(":")[1])
    async with AsyncSessionLocal() as session:
        user = await crud.get_user_by_tg_id(session, callback.from_user.id)
        lang = user.language if user else "ru"
        deal = await crud.get_deal_by_id(session, deal_id)

        if not deal or deal.status != DealStatus.UNPAID:
            await callback.answer("Сделка недоступна для оплаты", show_alert=True)
            return

        # Fetch payment requisites for this currency
        req = await crud.get_payment_requisite(session, deal.currency)
        req_text = req.requisites_text if req else "Реквизиты уточняйте у поддержки"
        instructions = req.instructions if req and req.instructions else "Переведите точную сумму и нажмите «Я оплатил»"

        pay_msg = (
            f"💳 <b>Оплата по сделке #{deal.id}</b>\n\n"
            f"💰 <b>К оплате:</b> <code>{deal.amount:g} {deal.currency}</code>\n\n"
            f"📌 <b>Реквизиты для оплаты:</b>\n"
            f"<code>{req_text}</code>\n\n"
            f"ℹ️ <b>Инструкция:</b>\n{instructions}\n\n"
            f"<i>После завершения перевода нажмите кнопку «✅ Я оплатил» ниже:</i>"
        )

        await callback.message.edit_text(
            pay_msg,
            reply_markup=get_payment_details_keyboard(deal.id, lang),
            parse_mode="HTML"
        )
        await callback.answer()


@router.callback_query(F.data.startswith("deal_paid_confirm:"))
async def callback_deal_paid_confirm(callback: CallbackQuery, bot: Bot):
    deal_id = int(callback.data.split(":")[1])
    async with AsyncSessionLocal() as session:
        deal = await crud.get_deal_by_id(session, deal_id)
        if not deal:
            await callback.answer("Сделка не найдена", show_alert=True)
            return

        await callback.answer("✅ Уведомление об оплате отправлено администратору!", show_alert=True)

        # Notify buyer
        await callback.message.edit_text(
            f"⏳ <b>Уведомление об оплате сделки #{deal.id} передано администратору.</b>\n\n"
            f"💰 Сумма: <code>{deal.amount:g} {deal.currency}</code>\n\n"
            f"<i>После проверки поступления средств статус сделки изменится на «🔒 В гаранте», и продавец получит сигнал передавать товар.</i>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔄 Обновить статус", callback_data=f"deal_refresh:{deal.id}")]
            ]),
            parse_mode="HTML"
        )

        # Notify admins
        admin_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"🔒 Подтвердить оплату #{deal.id} (В гарант)", callback_data=f"adm_deal_hold:{deal.id}")],
            [InlineKeyboardButton(text=f"🔍 Открыть сделку #{deal.id}", callback_data=f"adm_view_deal:{deal.id}")]
        ])

        for admin_id in settings.admin_id_list:
            try:
                await bot.send_message(
                    chat_id=admin_id,
                    text=(
                        f"💳 <b>Покупатель нажал «Я оплатил» по сделке #{deal.id}!</b>\n\n"
                        f"📌 <b>Название:</b> {deal.title}\n"
                        f"💰 <b>Сумма:</b> <code>{deal.amount:g} {deal.currency}</code>\n"
                        f"👤 <b>Покупатель:</b> @{callback.from_user.username or 'нет'} (ID: <code>{deal.buyer_tg_id}</code>)\n"
                        f"📦 <b>Продавец ID:</b> <code>{deal.seller_tg_id}</code>\n\n"
                        f"<i>Проверьте поступление на ваши реквизиты и подтвердите зачисление в гарант:</i>"
                    ),
                    reply_markup=admin_kb,
                    parse_mode="HTML"
                )
            except Exception as e:
                print(f"Error notifying admin {admin_id}: {e}")


@router.callback_query(F.data.startswith("deal_deliver:"))
async def callback_deal_deliver(callback: CallbackQuery, bot: Bot):
    deal_id = int(callback.data.split(":")[1])
    async with AsyncSessionLocal() as session:
        deal = await crud.get_deal_by_id(session, deal_id)
        if not deal or deal.status != DealStatus.PAID_HELD:
            await callback.answer("Невозможно изменить статус", show_alert=True)
            return

        if callback.from_user.id != deal.seller_tg_id:
            await callback.answer("Только продавец может подтвердить передачу товара", show_alert=True)
            return

        deal = await crud.update_deal_status(session, deal_id, DealStatus.DELIVERED)
        await callback.answer("📦 Статус обновлен: Товар передан", show_alert=True)

        notify_msg = "📦 <b>Продавец передал товар/услугу покупателю!</b>"
        await notify_deal_participants(bot, session, deal, notify_msg)


@router.callback_query(F.data.startswith("deal_confirm_rec:"))
async def callback_deal_confirm_received(callback: CallbackQuery, bot: Bot):
    deal_id = int(callback.data.split(":")[1])
    async with AsyncSessionLocal() as session:
        deal = await crud.get_deal_by_id(session, deal_id)
        if not deal or deal.status != DealStatus.DELIVERED:
            await callback.answer("Невозможно подтвердить сделку", show_alert=True)
            return

        if callback.from_user.id != deal.buyer_tg_id:
            await callback.answer("Только покупатель может подтвердить получение товара", show_alert=True)
            return

        deal = await crud.complete_deal_and_payout(session, deal_id)
        await callback.answer("🎉 Сделка успешно завершена! Средства выплачены продавцу.", show_alert=True)

        notify_msg = f"🎉 <b>Сделка #{deal.id} успешно завершена!</b>\n💰 <b>{deal.amount:g} {deal.currency}</b> переведены на баланс продавца."
        await notify_deal_participants(bot, session, deal, notify_msg)


@router.callback_query(F.data.startswith("deal_cancel:"))
async def callback_deal_cancel(callback: CallbackQuery, bot: Bot):
    deal_id = int(callback.data.split(":")[1])
    async with AsyncSessionLocal() as session:
        deal = await crud.get_deal_by_id(session, deal_id)
        if not deal:
            await callback.answer("Сделка не найдена", show_alert=True)
            return

        # Can only cancel if pending partner or unpaid
        if deal.status not in [DealStatus.PENDING_PARTNER, DealStatus.UNPAID]:
            await callback.answer("Сделку нельзя отменить на этом этапе. Откройте спор.", show_alert=True)
            return

        deal = await crud.update_deal_status(session, deal_id, DealStatus.CANCELLED)
        await callback.answer("❌ Сделка отменена", show_alert=True)
        await notify_deal_participants(bot, session, deal, "❌ <b>Сделка была отменена.</b>")


# --- DISPUTE HANDLER ---

@router.callback_query(F.data.startswith("deal_dispute:"))
async def callback_start_dispute(callback: CallbackQuery, state: FSMContext):
    deal_id = int(callback.data.split(":")[1])
    await state.update_data(dispute_deal_id=deal_id)
    await state.set_state(DisputeStates.entering_reason)

    await callback.message.answer(
        "⚠️ <b>Открытие спора по сделке:</b>\n\n"
        "Пожалуйста, подробно опишите причину спора и возникшую проблему:\n"
        "<i>(Администратор сервиса получит ваше обращение и подключится)</i>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_action")]
        ]),
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(DisputeStates.entering_reason)
async def process_dispute_reason(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    deal_id = data.get("dispute_deal_id")
    await state.clear()

    async with AsyncSessionLocal() as session:
        deal = await crud.update_deal_status(
            session=session,
            deal_id=deal_id,
            new_status=DealStatus.DISPUTED,
            dispute_reason=message.text.strip(),
            dispute_by_tg_id=message.from_user.id
        )

        if not deal:
            await message.answer("Ошибка: сделка не найдена.")
            return

        notify_msg = f"⚠️ <b>По сделке #{deal.id} открыт спор!</b>\nПричина: <i>{deal.dispute_reason}</i>\nОжидайте ответа администратора."
        await notify_deal_participants(bot, session, deal, notify_msg)

        # Notify admins about dispute
        for admin_id in settings.admin_id_list:
            try:
                await bot.send_message(
                    chat_id=admin_id,
                    text=(
                        f"🚨 <b>ВНИМАНИЕ: Открыт спор по сделке #{deal.id}!</b>\n\n"
                        f"📌 <b>Сделка:</b> {deal.title} (<code>{deal.amount:g} {deal.currency}</code>)\n"
                        f"👤 <b>Инициатор спора:</b> @{message.from_user.username or 'нет'} (ID: <code>{message.from_user.id}</code>)\n"
                        f"📝 <b>Причина:</b> {deal.dispute_reason}\n\n"
                        f"👉 Перейдите в /admin для решения спора."
                    ),
                    parse_mode="HTML"
                )
            except Exception as e:
                print(f"Error notifying admin {admin_id}: {e}")

        await message.answer(
            "✅ <b>Спор успешно зарегистрирован!</b> Администраторы оповещены.",
            parse_mode="HTML"
        )


# --- MY DEALS LIST ---

@router.message(F.text.in_([
    "📋 Мои сделки", "📋 Мої угоди", "📋 My Deals", "/my_deals"
]))
async def cmd_my_deals(message: Message):
    async with AsyncSessionLocal() as session:
        user = await crud.get_user_by_tg_id(session, message.from_user.id)
        lang = user.language if user else "ru"
        deals = await crud.get_user_deals(session, message.from_user.id)

    if not deals:
        await message.answer(
            "📋 <b>У вас пока нет активных или завершенных сделок.</b>\n"
            "Вы можете создать первую сделку кнопкой «🤝 Создать сделку».",
            reply_markup=get_main_menu_keyboard(lang),
            parse_mode="HTML"
        )
        return

    kb_rows = []
    for d in deals[:10]:
        status_icon = "⏳" if d.status in [DealStatus.PENDING_PARTNER, DealStatus.UNPAID] else "🔒" if d.status == DealStatus.PAID_HELD else "📦" if d.status == DealStatus.DELIVERED else "✅" if d.status == DealStatus.COMPLETED else "⚠️"
        btn_text = f"{status_icon} #{d.id} {d.title[:18]} - {d.amount:g} {d.currency}"
        kb_rows.append([InlineKeyboardButton(text=btn_text, callback_data=f"deal_refresh:{d.id}")])

    await message.answer(
        "📋 <b>Ваши последние сделки:</b>\n<i>Нажмите на сделку, чтобы открыть её карточку:</i>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=kb_rows),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "noop")
async def noop_callback(callback: CallbackQuery):
    await callback.answer()
