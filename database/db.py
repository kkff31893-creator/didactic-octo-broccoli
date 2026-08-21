from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def init_db():
    from database.models import User, Deal, Review, PaymentRequisite
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Initialize default payment requisites if empty
    async with AsyncSessionLocal() as session:
        from database.models import PaymentRequisite
        from sqlalchemy import select
        res = await session.execute(select(PaymentRequisite))
        if not res.scalars().first():
            default_reqs = [
                PaymentRequisite(currency="USDT", requisites_text="TRC20: TYDzsxdq4H... (Замените в админке)", instructions="Переведите точную сумму на указанный TRC20 кошелек"),
                PaymentRequisite(currency="TON", requisites_text="EQB... (Замените в админке)", instructions="Переведите точную сумму на указанный TON кошелек"),
                PaymentRequisite(currency="RUB", requisites_text="Сбербанк / СБП: +7 999 000-00-00 (Замените в админке)", instructions="Переведите точную сумму по СБП и прикрепите чек"),
                PaymentRequisite(currency="UAH", requisites_text="Monobank / ПриватБанк: 4441 0000 0000 0000 (Замените в админке)", instructions="Переведіть точну суму на картку"),
            ]
            session.add_all(default_reqs)
            await session.commit()
