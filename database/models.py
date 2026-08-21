import datetime
from sqlalchemy import (
    Column, Integer, BigInteger, String, Float, Text, Boolean, DateTime, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    username = Column(String(64), nullable=True)
    full_name = Column(String(128), nullable=True)
    language = Column(String(8), default="ru")
    
    # In-bot Balances
    balance_rub = Column(Float, default=0.0)
    balance_uah = Column(Float, default=0.0)
    balance_usdt = Column(Float, default=0.0)
    balance_ton = Column(Float, default=0.0)

    is_banned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<User {self.telegram_id} (@{self.username})>"


class DealStatus:
    PENDING_PARTNER = "pending_partner"  # Ждет второго участника
    UNPAID = "unpaid"                    # Ждет оплаты покупателем
    PAID_HELD = "paid_held"              # Оплачено (деньги в гаранте), продавец передает товар
    DELIVERED = "delivered"              # Товар передан, ждет подтверждения покупателя
    COMPLETED = "completed"              # Успешно завершена, деньги переведены продавцу
    DISPUTED = "disputed"                # Открыт спор (арбитраж)
    CANCELLED = "cancelled"              # Отменена


class DealRole:
    BUYER = "buyer"
    SELLER = "seller"


class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    deal_code = Column(String(32), unique=True, index=True, nullable=False)
    
    creator_tg_id = Column(BigInteger, ForeignKey("users.telegram_id"), nullable=False)
    participant_tg_id = Column(BigInteger, ForeignKey("users.telegram_id"), nullable=True)
    
    creator_role = Column(String(16), nullable=False)  # "buyer" or "seller"
    currency = Column(String(16), nullable=False)      # "RUB", "UAH", "USDT", "TON"
    amount = Column(Float, nullable=False)
    title = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    
    status = Column(String(32), default=DealStatus.PENDING_PARTNER, index=True)
    
    # Tracking buyer & seller specifically
    buyer_tg_id = Column(BigInteger, nullable=True)
    seller_tg_id = Column(BigInteger, nullable=True)
    
    # Dispute info
    dispute_reason = Column(Text, nullable=True)
    dispute_by_tg_id = Column(BigInteger, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    reviews = relationship("Review", back_populates="deal", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Deal #{self.id} {self.deal_code} {self.status} {self.amount} {self.currency}>"


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    deal_id = Column(Integer, ForeignKey("deals.id"), nullable=False)
    from_tg_id = Column(BigInteger, nullable=False)
    to_tg_id = Column(BigInteger, nullable=False)
    
    rating = Column(Integer, nullable=False)  # 1 to 5
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    deal = relationship("Deal", back_populates="reviews")

    def __repr__(self):
        return f"<Review {self.from_tg_id}->{self.to_tg_id} ⭐{self.rating}>"


class PaymentRequisite(Base):
    __tablename__ = "payment_requisites"

    id = Column(Integer, primary_key=True, autoincrement=True)
    currency = Column(String(16), unique=True, nullable=False)  # "RUB", "UAH", "USDT", "TON"
    requisites_text = Column(Text, nullable=False)
    instructions = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<PaymentRequisite {self.currency}: {self.requisites_text[:20]}>"
