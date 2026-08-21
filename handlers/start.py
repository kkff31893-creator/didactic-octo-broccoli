from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, CommandObject
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import AsyncSessionLocal
from database import crud
from database.models import DealStatus, DealRole
from keyboards.reply import get_main_menu_keyboard
from keyboards.inline import get_deal_action_keyboard
from services.localization import get_text
from services.deal_service import format_deal_text, notify_deal_participants

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject, bot: Bot):
    async with AsyncSessionLocal() as session:
        user = await crud.get_or_create_user(
            session=session,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name
        )
        lang = user.language or "ru"

        # Check for deep link (e.g. /start deal_abc123)
        args = command.args
        if args and args.startswith("deal_"):
            deal_code = args
            deal = await crud.get_deal_by_code(session, deal_code)
            
            if not deal:
                await message.answer(
                    "❌ <b>Сделка не найдена или была удалена.</b>",
                    reply_markup=get_main_menu_keyboard(lang),
                    parse_mode="HTML"
                )
                return

            # Check if this user is already in the deal
            if deal.creator_tg_id == message.from_user.id or deal.participant_tg_id == message.from_user.id:
                has_reviewed = await crud.has_user_reviewed(session, deal.id, message.from_user.id)
                deal_text = await format_deal_text(session, deal, message.from_user.id, lang)
                kb = get_deal_action_keyboard(
                    deal_id=deal.id,
                    user_tg_id=message.from_user.id,
                    deal_status=deal.status,
                    buyer_tg_id=deal.buyer_tg_id or 0,
                    seller_tg_id=deal.seller_tg_id or 0,
                    lang=lang,
                    has_reviewed=has_reviewed
                )
                await message.answer(
                    deal_text,
                    reply_markup=kb,
                    parse_mode="HTML"
                )
                return

            # If deal is waiting for a partner, join it!
            if deal.status == DealStatus.PENDING_PARTNER and not deal.participant_tg_id:
                deal = await crud.join_deal(session, deal, message.from_user.id)

                # Get joining user stats
                joiner_stats = await crud.get_user_rating_and_stats(session, message.from_user.id)
                creator = await crud.get_user_by_tg_id(session, deal.creator_tg_id)
                creator_lang = creator.language if creator else "ru"

                joiner_card = get_text(
                    "partner_profile_card",
                    creator_lang,
                    telegram_id=message.from_user.id,
                    username=message.from_user.username or "без_юзернейма",
                    rating=joiner_stats["avg_rating"],
                    reviews_count=joiner_stats["reviews_count"],
                    completed_deals=joiner_stats["completed_deals"]
                )

                notify_text = get_text(
                    "notify_partner_joined",
                    creator_lang,
                    deal_id=deal.id,
                    partner_profile=joiner_card
                )

                # Notify creator
                try:
                    creator_deal_text = await format_deal_text(session, deal, deal.creator_tg_id, creator_lang)
                    creator_kb = get_deal_action_keyboard(
                        deal_id=deal.id,
                        user_tg_id=deal.creator_tg_id,
                        deal_status=deal.status,
                        buyer_tg_id=deal.buyer_tg_id or 0,
                        seller_tg_id=deal.seller_tg_id or 0,
                        lang=creator_lang
                    )
                    await bot.send_message(
                        chat_id=deal.creator_tg_id,
                        text=f"{notify_text}\n\n{creator_deal_text}",
                        reply_markup=creator_kb,
                        parse_mode="HTML"
                    )
                except Exception as e:
                    print(f"Error notifying creator: {e}")

                # Send response to joiner
                creator_stats = await crud.get_user_rating_and_stats(session, deal.creator_tg_id)
                creator_card = get_text(
                    "partner_profile_card",
                    lang,
                    telegram_id=deal.creator_tg_id,
                    username=creator.username or "без_юзернейма" if creator else "неизвестно",
                    rating=creator_stats["avg_rating"],
                    reviews_count=creator_stats["reviews_count"],
                    completed_deals=creator_stats["completed_deals"]
                )

                joiner_deal_text = await format_deal_text(session, deal, message.from_user.id, lang)
                joiner_kb = get_deal_action_keyboard(
                    deal_id=deal.id,
                    user_tg_id=message.from_user.id,
                    deal_status=deal.status,
                    buyer_tg_id=deal.buyer_tg_id or 0,
                    seller_tg_id=deal.seller_tg_id or 0,
                    lang=lang
                )

                await message.answer(
                    f"🤝 <b>Вы успешно присоединились к сделке #{deal.id}!</b>\n\n"
                    f"{creator_card}\n\n"
                    f"{joiner_deal_text}",
                    reply_markup=joiner_kb,
                    parse_mode="HTML"
                )
                return

            else:
                await message.answer(
                    "⚠️ <b>В этой сделке уже участвуют два пользователя или она недоступна.</b>",
                    reply_markup=get_main_menu_keyboard(lang),
                    parse_mode="HTML"
                )
                return

        # Regular /start
        welcome_text = get_text("welcome", lang)
        await message.answer(
            welcome_text,
            reply_markup=get_main_menu_keyboard(lang),
            parse_mode="HTML"
        )
