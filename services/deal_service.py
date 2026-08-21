from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Deal, DealStatus, DealRole, User
from database import crud
from keyboards.inline import get_deal_action_keyboard
from services.localization import get_text

async def format_deal_text(session: AsyncSession, deal: Deal, viewer_tg_id: int, lang: str = "ru") -> str:
    status_text_map = {
        DealStatus.PENDING_PARTNER: get_text("status_pending_partner", lang),
        DealStatus.UNPAID: get_text("status_unpaid", lang),
        DealStatus.PAID_HELD: get_text("status_paid_held", lang),
        DealStatus.DELIVERED: get_text("status_delivered", lang),
        DealStatus.COMPLETED: get_text("status_completed", lang),
        DealStatus.DISPUTED: get_text("status_disputed", lang),
        DealStatus.CANCELLED: get_text("status_cancelled", lang),
    }

    # Fetch Buyer info
    if deal.buyer_tg_id:
        buyer = await crud.get_user_by_tg_id(session, deal.buyer_tg_id)
        buyer_stats = await crud.get_user_rating_and_stats(session, deal.buyer_tg_id)
        buyer_text = (
            f"@{buyer.username or 'без_юзернейма'} (ID: <code>{buyer.telegram_id}</code> | "
            f"⭐ {buyer_stats['avg_rating']} | 🤝 {buyer_stats['completed_deals']} сделок)"
            if buyer else f"<code>{deal.buyer_tg_id}</code>"
        )
    else:
        buyer_text = "<i>(Ожидает подключения)</i>"

    # Fetch Seller info
    if deal.seller_tg_id:
        seller = await crud.get_user_by_tg_id(session, deal.seller_tg_id)
        seller_stats = await crud.get_user_rating_and_stats(session, deal.seller_tg_id)
        seller_text = (
            f"@{seller.username or 'без_юзернейма'} (ID: <code>{seller.telegram_id}</code> | "
            f"⭐ {seller_stats['avg_rating']} | 🤝 {seller_stats['completed_deals']} сделок)"
            if seller else f"<code>{deal.seller_tg_id}</code>"
        )
    else:
        seller_text = "<i>(Ожидает подключения)</i>"

    extra_info = ""
    if deal.description:
        extra_info += f"📋 <b>Описание:</b> {deal.description}\n"

    if deal.status == DealStatus.PENDING_PARTNER:
        bot_info = None  # link generated on creation
        extra_info += f"⏳ <i>Второй участник еще не присоединился по ссылке.</i>\n"

    elif deal.status == DealStatus.DISPUTED:
        extra_info += f"\n⚠️ <b>Причина спора:</b> <i>{deal.dispute_reason or 'Не указана'}</i>\n"

    return get_text(
        "deal_card",
        lang,
        deal_id=deal.id,
        deal_code=deal.deal_code,
        title=deal.title,
        amount=f"{deal.amount:g}",
        currency=deal.currency,
        status_text=status_text_map.get(deal.status, deal.status),
        buyer_text=buyer_text,
        seller_text=seller_text,
        extra_info=extra_info
    )


async def notify_deal_participants(bot: Bot, session: AsyncSession, deal: Deal, notification_text: str):
    """Sends notification to both deal participants if they are registered."""
    targets = set()
    if deal.creator_tg_id:
        targets.add(deal.creator_tg_id)
    if deal.participant_tg_id:
        targets.add(deal.participant_tg_id)

    for tg_id in targets:
        try:
            user = await crud.get_user_by_tg_id(session, tg_id)
            lang = user.language if user else "ru"
            has_reviewed = await crud.has_user_reviewed(session, deal.id, tg_id)
            deal_text = await format_deal_text(session, deal, tg_id, lang)
            
            full_msg = f"{notification_text}\n\n{deal_text}"
            kb = get_deal_action_keyboard(
                deal_id=deal.id,
                user_tg_id=tg_id,
                deal_status=deal.status,
                buyer_tg_id=deal.buyer_tg_id or 0,
                seller_tg_id=deal.seller_tg_id or 0,
                lang=lang,
                has_reviewed=has_reviewed
            )
            await bot.send_message(chat_id=tg_id, text=full_msg, reply_markup=kb, parse_mode="HTML")
        except Exception as e:
            # User might have blocked bot or other telegram exception
            print(f"Error notifying {tg_id}: {e}")
