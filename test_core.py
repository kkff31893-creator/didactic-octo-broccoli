import asyncio
from database.db import init_db, AsyncSessionLocal
from database import crud
from database.models import DealStatus, DealRole

async def test_bot_core():
    print("Testing DB initialization...")
    await init_db()
    print("DB initialized successfully.")

    async with AsyncSessionLocal() as session:
        print("Testing User creation...")
        user1 = await crud.get_or_create_user(session, telegram_id=353890607, username="timir_buyer", full_name="Buyer Timir")
        user2 = await crud.get_or_create_user(session, telegram_id=8689976952, username="seller_user", full_name="Seller User")
        print(f"Created/Found users: {user1.telegram_id}, {user2.telegram_id}")

        print("Testing Deal creation...")
        deal = await crud.create_deal(
            session=session,
            creator_tg_id=user1.telegram_id,
            creator_role=DealRole.BUYER,
            currency="USDT",
            amount=100.0,
            title="Тестовая покупка канала",
            description="Проверка передачи прав владельца"
        )
        print(f"Deal created: #{deal.id}, code: {deal.deal_code}, status: {deal.status}")

        print("Testing Partner joining deal...")
        deal = await crud.join_deal(session, deal, participant_tg_id=user2.telegram_id)
        print(f"Joined deal #{deal.id}, status: {deal.status}, buyer: {deal.buyer_tg_id}, seller: {deal.seller_tg_id}")

        print("Testing status changes: UNPAID -> PAID_HELD -> DELIVERED...")
        deal = await crud.update_deal_status(session, deal.id, DealStatus.PAID_HELD)
        assert deal.status == DealStatus.PAID_HELD

        deal = await crud.update_deal_status(session, deal.id, DealStatus.DELIVERED)
        assert deal.status == DealStatus.DELIVERED

        print("Testing Complete deal & payout...")
        deal = await crud.complete_deal_and_payout(session, deal.id)
        assert deal.status == DealStatus.COMPLETED

        # Check seller balance
        seller_updated = await crud.get_user_by_tg_id(session, user2.telegram_id)
        print(f"Seller USDT balance: {seller_updated.balance_usdt}")
        assert seller_updated.balance_usdt >= 100.0

        print("Testing Review & Rating system...")
        review = await crud.add_review(
            session=session,
            deal_id=deal.id,
            from_tg_id=user1.telegram_id,
            to_tg_id=user2.telegram_id,
            rating=5,
            comment="Отличный продавец! Всё быстро передал."
        )
        print(f"Review added: {review.rating} stars")

        stats = await crud.get_user_rating_and_stats(session, user2.telegram_id)
        print(f"Seller stats: {stats}")
        assert stats["completed_deals"] >= 1
        assert stats["avg_rating"] == 5.0
        assert stats["reviews_count"] >= 1

        print("Testing Admin stats...")
        admin_stats = await crud.get_admin_statistics(session)
        print(f"Admin stats: {admin_stats}")

    print("\nALL CORE LOGIC TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(test_bot_core())
