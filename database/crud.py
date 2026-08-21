import uuid
import secrets
from typing import Optional, List, Tuple
from sqlalchemy import select, update, func, or_, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User, Deal, Review, PaymentRequisite, DealStatus, DealRole

# --- USER CRUD ---

async def get_or_create_user(
    session: AsyncSession,
    telegram_id: int,
    username: Optional[str] = None,
    full_name: Optional[str] = None
) -> User:
    query = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            telegram_id=telegram_id,
            username=username,
            full_name=full_name
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
    else:
        # Update username and full_name if changed
        if user.username != username or user.full_name != full_name:
            user.username = username
            user.full_name = full_name
            await session.commit()
            await session.refresh(user)
    return user


async def get_user_by_tg_id(session: AsyncSession, telegram_id: int) -> Optional[User]:
    query = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def update_user_language(session: AsyncSession, telegram_id: int, language: str) -> None:
    await session.execute(
        update(User).where(User.telegram_id == telegram_id).values(language=language)
    )
    await session.commit()


async def get_user_rating_and_stats(session: AsyncSession, telegram_id: int) -> dict:
    """Calculates user completed deals, average rating, reviews count."""
    # Completed deals count (as buyer or seller)
    deals_query = select(func.count(Deal.id)).where(
        and_(
            or_(Deal.buyer_tg_id == telegram_id, Deal.seller_tg_id == telegram_id),
            Deal.status == DealStatus.COMPLETED
        )
    )
    deals_res = await session.execute(deals_query)
    completed_deals = deals_res.scalar() or 0

    # Active deals count
    active_deals_query = select(func.count(Deal.id)).where(
        and_(
            or_(Deal.creator_tg_id == telegram_id, Deal.participant_tg_id == telegram_id),
            Deal.status.in_([
                DealStatus.PENDING_PARTNER,
                DealStatus.UNPAID,
                DealStatus.PAID_HELD,
                DealStatus.DELIVERED,
                DealStatus.DISPUTED
            ])
        )
    )
    active_res = await session.execute(active_deals_query)
    active_deals = active_res.scalar() or 0

    # Ratings
    rating_query = select(
        func.avg(Review.rating),
        func.count(Review.id)
    ).where(Review.to_tg_id == telegram_id)
    rating_res = await session.execute(rating_query)
    avg_rating, reviews_count = rating_res.first()

    return {
        "completed_deals": completed_deals,
        "active_deals": active_deals,
        "avg_rating": round(float(avg_rating), 1) if avg_rating is not None else 5.0,
        "reviews_count": reviews_count or 0
    }


async def get_user_reviews(session: AsyncSession, telegram_id: int, limit: int = 5) -> List[Review]:
    query = (
        select(Review)
        .where(Review.to_tg_id == telegram_id)
        .order_by(desc(Review.created_at))
        .limit(limit)
    )
    result = await session.execute(query)
    return list(result.scalars().all())


# --- DEAL CRUD ---

async def create_deal(
    session: AsyncSession,
    creator_tg_id: int,
    creator_role: str,
    currency: str,
    amount: float,
    title: str,
    description: Optional[str] = None
) -> Deal:
    deal_code = f"deal_{secrets.token_hex(4)}"
    buyer_tg_id = creator_tg_id if creator_role == DealRole.BUYER else None
    seller_tg_id = creator_tg_id if creator_role == DealRole.SELLER else None

    deal = Deal(
        deal_code=deal_code,
        creator_tg_id=creator_tg_id,
        creator_role=creator_role,
        buyer_tg_id=buyer_tg_id,
        seller_tg_id=seller_tg_id,
        currency=currency.upper(),
        amount=amount,
        title=title,
        description=description,
        status=DealStatus.PENDING_PARTNER
    )
    session.add(deal)
    await session.commit()
    await session.refresh(deal)
    return deal


async def get_deal_by_code(session: AsyncSession, deal_code: str) -> Optional[Deal]:
    query = select(Deal).where(Deal.deal_code == deal_code)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_deal_by_id(session: AsyncSession, deal_id: int) -> Optional[Deal]:
    query = select(Deal).where(Deal.id == deal_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def join_deal(session: AsyncSession, deal: Deal, participant_tg_id: int) -> Deal:
    """Second user joins the deal."""
    deal.participant_tg_id = participant_tg_id
    if deal.creator_role == DealRole.BUYER:
        deal.seller_tg_id = participant_tg_id
    else:
        deal.buyer_tg_id = participant_tg_id

    deal.status = DealStatus.UNPAID
    await session.commit()
    await session.refresh(deal)
    return deal


async def update_deal_status(
    session: AsyncSession,
    deal_id: int,
    new_status: str,
    dispute_reason: Optional[str] = None,
    dispute_by_tg_id: Optional[int] = None
) -> Optional[Deal]:
    deal = await get_deal_by_id(session, deal_id)
    if not deal:
        return None
    deal.status = new_status
    if dispute_reason:
        deal.dispute_reason = dispute_reason
    if dispute_by_tg_id:
        deal.dispute_by_tg_id = dispute_by_tg_id
    await session.commit()
    await session.refresh(deal)
    return deal


async def complete_deal_and_payout(session: AsyncSession, deal_id: int) -> Optional[Deal]:
    """Marks deal completed and adds money to seller's in-bot balance."""
    deal = await get_deal_by_id(session, deal_id)
    if not deal or deal.status == DealStatus.COMPLETED:
        return deal

    deal.status = DealStatus.COMPLETED

    if deal.seller_tg_id:
        seller = await get_user_by_tg_id(session, deal.seller_tg_id)
        if seller:
            if deal.currency == "RUB":
                seller.balance_rub += deal.amount
            elif deal.currency == "UAH":
                seller.balance_uah += deal.amount
            elif deal.currency == "USDT":
                seller.balance_usdt += deal.amount
            elif deal.currency == "TON":
                seller.balance_ton += deal.amount

    await session.commit()
    await session.refresh(deal)
    return deal


async def get_user_deals(
    session: AsyncSession,
    tg_id: int,
    status_filter: Optional[str] = None
) -> List[Deal]:
    query = select(Deal).where(
        or_(Deal.creator_tg_id == tg_id, Deal.participant_tg_id == tg_id)
    )
    if status_filter == "active":
        query = query.where(Deal.status.in_([
            DealStatus.PENDING_PARTNER,
            DealStatus.UNPAID,
            DealStatus.PAID_HELD,
            DealStatus.DELIVERED,
            DealStatus.DISPUTED
        ]))
    elif status_filter == "completed":
        query = query.where(Deal.status == DealStatus.COMPLETED)
    
    query = query.order_by(desc(Deal.created_at))
    result = await session.execute(query)
    return list(result.scalars().all())


# --- REVIEW CRUD ---

async def add_review(
    session: AsyncSession,
    deal_id: int,
    from_tg_id: int,
    to_tg_id: int,
    rating: int,
    comment: Optional[str] = None
) -> Review:
    review = Review(
        deal_id=deal_id,
        from_tg_id=from_tg_id,
        to_tg_id=to_tg_id,
        rating=rating,
        comment=comment
    )
    session.add(review)
    await session.commit()
    await session.refresh(review)
    return review


async def has_user_reviewed(session: AsyncSession, deal_id: int, from_tg_id: int) -> bool:
    query = select(Review).where(
        and_(Review.deal_id == deal_id, Review.from_tg_id == from_tg_id)
    )
    res = await session.execute(query)
    return res.scalar_one_or_none() is not None


# --- PAYMENT REQUISITES CRUD ---

async def get_payment_requisite(session: AsyncSession, currency: str) -> Optional[PaymentRequisite]:
    query = select(PaymentRequisite).where(
        and_(PaymentRequisite.currency == currency.upper(), PaymentRequisite.is_active == True)
    )
    res = await session.execute(query)
    return res.scalar_one_or_none()


async def get_all_requisites(session: AsyncSession) -> List[PaymentRequisite]:
    query = select(PaymentRequisite).order_by(PaymentRequisite.id)
    res = await session.execute(query)
    return list(res.scalars().all())


async def update_requisite(session: AsyncSession, currency: str, requisites_text: str, instructions: Optional[str] = None):
    req = await get_payment_requisite(session, currency)
    if req:
        req.requisites_text = requisites_text
        if instructions:
            req.instructions = instructions
    else:
        req = PaymentRequisite(currency=currency.upper(), requisites_text=requisites_text, instructions=instructions)
        session.add(req)
    await session.commit()
    await session.refresh(req)
    return req


# --- ADMIN CRUD ---

async def get_all_deals_admin(session: AsyncSession, status_filter: Optional[str] = None, limit: int = 50) -> List[Deal]:
    query = select(Deal)
    if status_filter:
        query = query.where(Deal.status == status_filter)
    query = query.order_by(desc(Deal.created_at)).limit(limit)
    res = await session.execute(query)
    return list(res.scalars().all())


async def get_admin_statistics(session: AsyncSession) -> dict:
    total_users_q = select(func.count(User.id))
    total_deals_q = select(func.count(Deal.id))
    completed_deals_q = select(func.count(Deal.id)).where(Deal.status == DealStatus.COMPLETED)
    active_deals_q = select(func.count(Deal.id)).where(Deal.status.in_([
        DealStatus.PENDING_PARTNER, DealStatus.UNPAID, DealStatus.PAID_HELD, DealStatus.DELIVERED
    ]))
    disputes_q = select(func.count(Deal.id)).where(Deal.status == DealStatus.DISPUTED)

    total_users = (await session.execute(total_users_q)).scalar() or 0
    total_deals = (await session.execute(total_deals_q)).scalar() or 0
    completed_deals = (await session.execute(completed_deals_q)).scalar() or 0
    active_deals = (await session.execute(active_deals_q)).scalar() or 0
    disputes = (await session.execute(disputes_q)).scalar() or 0

    return {
        "total_users": total_users,
        "total_deals": total_deals,
        "completed_deals": completed_deals,
        "active_deals": active_deals,
        "disputes": disputes
    }


async def get_all_user_telegram_ids(session: AsyncSession) -> List[int]:
    query = select(User.telegram_id)
    res = await session.execute(query)
    return list(res.scalars().all())
