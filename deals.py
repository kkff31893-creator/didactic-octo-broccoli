import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import AsyncSessionLocal
from database import crud
from database.models import DealStatus, DealRole
from keyboards.inline import (
    get_admin_main_keyboard,
    get_admin_deal_actions_keyboard,
    get_admin_requisites_keyboard
)
from services.deal_service import format_deal_text, notify_deal_participants
from config import settings

router = Router()

class AdminStates(StatesGroup):
    search_deal_id = State()
    edit_requisite_curr = State()
    edit_requisite_text = State()
    broadcast_message = State()


def is_admin(user_id: int) -> bool:
    return user_id in settings.admin_id_list


# --- MAIN ADMIN MENU ---

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ <b>У вас нет прав доступа к панели администратора.</b>", parse_mode="HTML")
        return

    await message.answer(
        "🛡️ <b>Панель администратора Garant Bot</b>\n\n"
        "Выберите раздел для управления сервисом:",
        reply_markup=get_admin_main_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "admin_menu")
async def callback_admin_menu(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещен", show_alert=True)
        return
    await state.clear()
    await callback.message.edit_text(
        "🛡️ <b>Панель администратора Garant Bot</b>\n\n"
        "Выберите раздел для управления сервисом:",
        reply_markup=get_admin_main_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


# --- STATISTICS ---

@router.callback_query(F.data == "admin_stats")
async def callback_admin_stats(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return

    async with AsyncSessionLocal() as session:
        stats = await crud.get_admin_statistics(session)

    text = (
        "📊 <b>Статистика сервиса:</b>\n\n"
        f"👥 <b>Всего пользователей:</b> <code>{stats['total_users']}</code>\n"
        f"🤝 <b>Всего сделок:</b> <code>{stats['total_deals']}</code>\n"
        f"├ ✅ <b>Завершенных:</b> <code>{stats['completed_deals']}</code>\n"
        f"├ ⏳ <b>Активных:</b> <code>{stats['active_deals']}</code>\n"
        f"└ ⚠️ <b>В споре (арбитраж):</b> <code>{stats['disputes']}</code>"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад в админку", callback_data="admin_menu")]
    ])

    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()


# --- DEALS LIST & MODERATION ---

@router.callback_query(F.data.startswith("admin_deals:"))
async def callback_admin_deals_list(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return

    filter_type = callback.data.split(":")[1]
    status_filter = DealStatus.DISPUTED if filter_type == "disputed" else None

    async with AsyncSessionLocal() as session:
        deals = await crud.get_all_deals_admin(session, status_filter=status_filter, limit=15)

    if not deals:
        await callback.message.edit_text(
            f"💼 <b>Сделок по запросу ({filter_type}) не найдено.</b>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Назад в админку", callback_data="admin_menu")]
            ]),
            parse_mode="HTML"
        )
        await callback.answer()
        return

    kb_rows = []
    for d in deals:
        status_icon = "⚠️" if d.status == DealStatus.DISPUTED else "✅" if d.status == DealStatus.COMPLETED else "⏳"
        btn_text = f"{status_icon} #{d.id} | {d.amount:g} {d.currency} | {d.title[:15]}"
        kb_rows.append([InlineKeyboardButton(text=btn_text, callback_data=f"adm_view_deal:{d.id}")])

    kb_rows.append([InlineKeyboardButton(text="⬅️ Назад в админку", callback_data="admin_menu")])

    title = "⚠️ <b>Сделки, требующие арбитража:</b>" if filter_type == "disputed" else "💼 <b>Список последних сделок:</b>"
    await callback.message.edit_text(
        f"{title}\n<i>Нажмите на сделку для управления:</i>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=kb_rows),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("adm_view_deal:"))
async def callback_admin_view_deal(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return

    deal_id = int(callback.data.split(":")[1])
    async with AsyncSessionLocal() as session:
        deal = await crud.get_deal_by_id(session, deal_id)
        if not deal:
            await callback.answer("Сделка не найдена", show_alert=True)
            return

        deal_text = await format_deal_text(session, deal, callback.from_user.id, "ru")
        admin_card = (
            f"🛡️ <b>Управление сделкой (Админ)</b>\n\n"
            f"{deal_text}\n\n"
            f"🛒 Покупатель ID: <code>{deal.buyer_tg_id}</code>\n"
            f"📦 Продавец ID: <code>{deal.seller_tg_id}</code>"
        )

        await callback.message.edit_text(
            admin_card,
            reply_markup=get_admin_deal_actions_keyboard(deal.id, deal.status),
            parse_mode="HTML"
        )
        await callback.answer()


@router.callback_query(F.data.startswith("adm_deal_hold:"))
async def callback_admin_hold_payment(callback: CallbackQuery, bot: Bot):
    if not is_admin(callback.from_user.id):
        return

    deal_id = int(callback.data.split(":")[1])
    async with AsyncSessionLocal() as session:
        deal = await crud.update_deal_status(session, deal_id, DealStatus.PAID_HELD)
        if not deal:
            await callback.answer("Сделка не найдена", show_alert=True)
            return

        await callback.answer("🔒 Оплата подтверждена! Средства заморожены в гаранте.", show_alert=True)
        notify_msg = (
            f"🔒 <b>Оплата по сделке #{deal.id} подтверждена администратором!</b>\n"
            f"💰 Средства в размере <code>{deal.amount:g} {deal.currency}</code> зачислены на баланс гаранта.\n\n"
            f"📦 <b>Продавец</b>, теперь вы можете безопасно передать товар/услугу покупателю.\n"
            f"После передачи нажмите кнопку «📦 Товар передан покупателю»."
        )
        await notify_deal_participants(bot, session, deal, notify_msg)

        await callback.message.edit_text(
            f"🔒 <b>Оплата по сделке #{deal.id} успешно подтверждена!</b>\n\n"
            f"💰 Средства заморожены в гаранте (на балансе сделки).\n"
            f"📦 Продавец уведомлен о необходимости передачи товара.\n"
            f"✅ Выплата продавцу произойдет только после того, как покупатель подтвердит получение товара.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Назад в админку", callback_data="admin_menu")]
            ]),
            parse_mode="HTML"
        )


@router.callback_query(F.data.startswith("adm_deal_complete:"))
async def callback_admin_force_complete(callback: CallbackQuery, bot: Bot):
    if not is_admin(callback.from_user.id):
        return

    deal_id = int(callback.data.split(":")[1])
    async with AsyncSessionLocal() as session:
        deal = await crud.complete_deal_and_payout(session, deal_id)
        if not deal:
            await callback.answer("Ошибка при завершении", show_alert=True)
            return

        await callback.answer("✅ Сделка принудительно завершена, средства переведены продавцу!", show_alert=True)
        notify_msg = f"⚖️ <b>Администратор завершил сделку #{deal.id} в пользу продавца!</b>\n💰 Средства зачислены на баланс продавца."
        await notify_deal_participants(bot, session, deal, notify_msg)

        await callback.message.edit_text(
            f"✅ <b>Сделка #{deal.id} завершена в пользу продавца.</b>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Назад в админку", callback_data="admin_menu")]
            ]),
            parse_mode="HTML"
        )


@router.callback_query(F.data.startswith("adm_deal_cancel:"))
async def callback_admin_force_cancel(callback: CallbackQuery, bot: Bot):
    if not is_admin(callback.from_user.id):
        return

    deal_id = int(callback.data.split(":")[1])
    async with AsyncSessionLocal() as session:
        deal = await crud.update_deal_status(session, deal_id, DealStatus.CANCELLED)
        if not deal:
            await callback.answer("Ошибка при отмене", show_alert=True)
            return

        await callback.answer("❌ Сделка отменена администратором (Возврат покупателю)", show_alert=True)
        notify_msg = f"⚖️ <b>Администратор отменил сделку #{deal.id}!</b> Средства возвращены покупателю."
        await notify_deal_participants(bot, session, deal, notify_msg)

        await callback.message.edit_text(
            f"❌ <b>Сделка #{deal.id} отменена администратором.</b>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Назад в админку", callback_data="admin_menu")]
            ]),
            parse_mode="HTML"
        )


# --- SEARCH DEAL BY ID ---

@router.callback_query(F.data == "admin_search_deal")
async def callback_admin_search(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return

    await state.set_state(AdminStates.search_deal_id)
    await callback.message.edit_text(
        "🔍 <b>Введите ID сделки</b> (число, например <code>1</code> или <code>42</code>):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="admin_menu")]
        ]),
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(AdminStates.search_deal_id)
async def process_search_deal_input(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    raw = message.text.strip()
    if not raw.isdigit():
        await message.answer("⚠️ Введите корректный числовой ID сделки.")
        return

    deal_id = int(raw)
    await state.clear()

    async with AsyncSessionLocal() as session:
        deal = await crud.get_deal_by_id(session, deal_id)
        if not deal:
            await message.answer(
                f"❌ Сделка с ID #{deal_id} не найдена.",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="⬅️ В админку", callback_data="admin_menu")]
                ]),
                parse_mode="HTML"
            )
            return

        deal_text = await format_deal_text(session, deal, message.from_user.id, "ru")
        admin_card = (
            f"🛡️ <b>Управление сделкой #{deal.id} (Админ)</b>\n\n"
            f"{deal_text}\n\n"
            f"🛒 Покупатель ID: <code>{deal.buyer_tg_id}</code>\n"
            f"📦 Продавец ID: <code>{deal.seller_tg_id}</code>"
        )

        await message.answer(
            admin_card,
            reply_markup=get_admin_deal_actions_keyboard(deal.id, deal.status),
            parse_mode="HTML"
        )


# --- PAYMENT REQUISITES MANAGEMENT ---

@router.callback_query(F.data == "admin_requisites")
async def callback_admin_requisites(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return

    async with AsyncSessionLocal() as session:
        reqs = await crud.get_all_requisites(session)

    text = "💳 <b>Текущие платежные реквизиты:</b>\n\n"
    for r in reqs:
        text += f"🔹 <b>{r.currency}:</b>\n<code>{r.requisites_text}</code>\n<i>{r.instructions or ''}</i>\n\n"

    text += "<i>Нажмите кнопку ниже, чтобы изменить реквизиты для выбранной валюты:</i>"

    await callback.message.edit_text(
        text,
        reply_markup=get_admin_requisites_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("adm_req_edit:"))
async def callback_admin_req_edit(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return

    currency = callback.data.split(":")[1]
    await state.update_data(edit_curr=currency)
    await state.set_state(AdminStates.edit_requisite_text)

    await callback.message.edit_text(
        f"📝 <b>Введите новые реквизиты для валюты {currency}:</b>\n"
        f"<i>(Например: номер карты, кошелек USDT TRC20, номер телефона СБП)</i>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="admin_requisites")]
        ]),
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(AdminStates.edit_requisite_text)
async def process_new_requisite_text(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()
    currency = data.get("edit_curr")
    new_text = message.text.strip()
    await state.clear()

    async with AsyncSessionLocal() as session:
        await crud.update_requisite(session, currency, new_text)

    await message.answer(
        f"✅ <b>Реквизиты для {currency} успешно обновлены!</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ К реквизитам", callback_data="admin_requisites")]
        ]),
        parse_mode="HTML"
    )


# --- BROADCAST SYSTEM ---

@router.callback_query(F.data == "admin_broadcast")
async def callback_admin_broadcast(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return

    await state.set_state(AdminStates.broadcast_message)
    await callback.message.edit_text(
        "📢 <b>Рассылка сообщений:</b>\n\n"
        "Отправьте текст сообщения (поддерживается HTML форматирование), которое будет доставлено всем пользователям бота:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="admin_menu")]
        ]),
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(AdminStates.broadcast_message)
async def process_broadcast_message(message: Message, state: FSMContext, bot: Bot):
    if not is_admin(message.from_user.id):
        return

    text = message.text
    await state.clear()

    async with AsyncSessionLocal() as session:
        user_ids = await crud.get_all_user_telegram_ids(session)

    status_msg = await message.answer(f"⏳ Начинаю рассылку для <b>{len(user_ids)}</b> пользователей...", parse_mode="HTML")

    success_count = 0
    fail_count = 0

    for uid in user_ids:
        try:
            await bot.send_message(chat_id=uid, text=text, parse_mode="HTML")
            success_count += 1
            await asyncio.sleep(0.05)  # Avoid rate limits
        except Exception:
            fail_count += 1

    await status_msg.edit_text(
        f"✅ <b>Рассылка завершена!</b>\n\n"
        f"Успешно доставлено: <b>{success_count}</b>\n"
        f"Ошибок / заблокировали: <b>{fail_count}</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ В админку", callback_data="admin_menu")]
        ]),
        parse_mode="HTML"
    )
