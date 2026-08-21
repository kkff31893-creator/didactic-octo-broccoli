from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import DealStatus, DealRole
from services.localization import get_text

def get_role_choice_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text=get_text("role_buyer", lang), callback_data="create_role:buyer"),
            InlineKeyboardButton(text=get_text("role_seller", lang), callback_data="create_role:seller")
        ],
        [
            InlineKeyboardButton(text=get_text("btn_cancel", lang), callback_data="cancel_action")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_currency_choice_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="🇷🇺 RUB (Рубли)", callback_data="create_curr:RUB"),
            InlineKeyboardButton(text="🇺🇦 UAH (Гривны)", callback_data="create_curr:UAH")
        ],
        [
            InlineKeyboardButton(text="💎 USDT (TRC20)", callback_data="create_curr:USDT"),
            InlineKeyboardButton(text="💎 TON", callback_data="create_curr:TON")
        ],
        [
            InlineKeyboardButton(text=get_text("btn_cancel", lang), callback_data="cancel_action")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_cancel_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text=get_text("btn_cancel", lang), callback_data="cancel_action")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_deal_action_keyboard(
    deal_id: int,
    user_tg_id: int,
    deal_status: str,
    buyer_tg_id: int,
    seller_tg_id: int,
    lang: str = "ru",
    has_reviewed: bool = False
) -> InlineKeyboardMarkup:
    kb = []
    is_buyer = (user_tg_id == buyer_tg_id)
    is_seller = (user_tg_id == seller_tg_id)

    if deal_status == DealStatus.PENDING_PARTNER:
        kb.append([
            InlineKeyboardButton(text="🔄 Обновить статус", callback_data=f"deal_refresh:{deal_id}"),
            InlineKeyboardButton(text="❌ Отменить сделку", callback_data=f"deal_cancel:{deal_id}")
        ])

    elif deal_status == DealStatus.UNPAID:
        if is_buyer:
            kb.append([
                InlineKeyboardButton(text="💳 Оплатить в гарант", callback_data=f"deal_pay:{deal_id}")
            ])
            kb.append([
                InlineKeyboardButton(text="❌ Отменить сделку", callback_data=f"deal_cancel:{deal_id}"),
                InlineKeyboardButton(text="🔄 Обновить", callback_data=f"deal_refresh:{deal_id}")
            ])
        else:
            kb.append([
                InlineKeyboardButton(text="⏳ Ожидание оплаты покупателем", callback_data="noop"),
            ])
            kb.append([
                InlineKeyboardButton(text="❌ Отменить сделку", callback_data=f"deal_cancel:{deal_id}"),
                InlineKeyboardButton(text="🔄 Обновить", callback_data=f"deal_refresh:{deal_id}")
            ])

    elif deal_status == DealStatus.PAID_HELD:
        if is_seller:
            kb.append([
                InlineKeyboardButton(text="📦 Товар передан покупателю", callback_data=f"deal_deliver:{deal_id}")
            ])
            kb.append([
                InlineKeyboardButton(text="⚠️ Открыть спор", callback_data=f"deal_dispute:{deal_id}"),
                InlineKeyboardButton(text="🔄 Обновить", callback_data=f"deal_refresh:{deal_id}")
            ])
        else:
            kb.append([
                InlineKeyboardButton(text="🔒 Оплата в гаранте. Ожидайте товар", callback_data="noop")
            ])
            kb.append([
                InlineKeyboardButton(text="⚠️ Открыть спор", callback_data=f"deal_dispute:{deal_id}"),
                InlineKeyboardButton(text="🔄 Обновить", callback_data=f"deal_refresh:{deal_id}")
            ])

    elif deal_status == DealStatus.DELIVERED:
        if is_buyer:
            kb.append([
                InlineKeyboardButton(text="✅ Подтвердить получение и выплату", callback_data=f"deal_confirm_rec:{deal_id}")
            ])
            kb.append([
                InlineKeyboardButton(text="⚠️ Открыть спор", callback_data=f"deal_dispute:{deal_id}"),
                InlineKeyboardButton(text="🔄 Обновить", callback_data=f"deal_refresh:{deal_id}")
            ])
        else:
            kb.append([
                InlineKeyboardButton(text="⏳ Ожидание подтверждения покупателя", callback_data="noop")
            ])
            kb.append([
                InlineKeyboardButton(text="⚠️ Открыть спор", callback_data=f"deal_dispute:{deal_id}"),
                InlineKeyboardButton(text="🔄 Обновить", callback_data=f"deal_refresh:{deal_id}")
            ])

    elif deal_status == DealStatus.COMPLETED:
        row = []
        if not has_reviewed:
            row.append(InlineKeyboardButton(text="⭐ Оставить отзыв", callback_data=f"deal_review:{deal_id}"))
        row.append(InlineKeyboardButton(text="🔄 Обновить", callback_data=f"deal_refresh:{deal_id}"))
        kb.append(row)

    elif deal_status == DealStatus.DISPUTED:
        kb.append([
            InlineKeyboardButton(text="⚠️ Спор на рассмотрении у админа", callback_data="noop")
        ])
        kb.append([
            InlineKeyboardButton(text="🔄 Обновить", callback_data=f"deal_refresh:{deal_id}")
        ])

    elif deal_status == DealStatus.CANCELLED:
        kb.append([
            InlineKeyboardButton(text="❌ Сделка отменена", callback_data="noop")
        ])

    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_payment_details_keyboard(deal_id: int, lang: str = "ru") -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="✅ Я оплатил", callback_data=f"deal_paid_confirm:{deal_id}")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад к сделке", callback_data=f"deal_refresh:{deal_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_rating_keyboard(deal_id: int) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="⭐ 1", callback_data=f"rate:{deal_id}:1"),
            InlineKeyboardButton(text="⭐ 2", callback_data=f"rate:{deal_id}:2"),
            InlineKeyboardButton(text="⭐ 3", callback_data=f"rate:{deal_id}:3"),
            InlineKeyboardButton(text="⭐ 4", callback_data=f"rate:{deal_id}:4"),
            InlineKeyboardButton(text="⭐ 5", callback_data=f"rate:{deal_id}:5"),
        ],
        [
            InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_action")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_skip_review_text_keyboard(deal_id: int, rating: int, lang: str = "ru") -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text=get_text("btn_skip_review_text", lang), callback_data=f"rateskip:{deal_id}:{rating}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_language_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang:ru"),
            InlineKeyboardButton(text="🇺🇦 Українська", callback_data="set_lang:ua"),
        ],
        [
            InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang:en"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_my_deals_filter_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="⏳ Активные сделки", callback_data="deals_list:active"),
            InlineKeyboardButton(text="✅ Завершенные", callback_data="deals_list:completed")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


# --- ADMIN KEYBOARDS ---

def get_admin_main_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"),
            InlineKeyboardButton(text="💼 Все сделки", callback_data="admin_deals:all")
        ],
        [
            InlineKeyboardButton(text="⚠️ Сделки в споре", callback_data="admin_deals:disputed"),
            InlineKeyboardButton(text="💳 Реквизиты оплаты", callback_data="admin_requisites")
        ],
        [
            InlineKeyboardButton(text="📢 Рассылка", callback_data="admin_broadcast"),
            InlineKeyboardButton(text="👥 Найти сделку по ID", callback_data="admin_search_deal")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_admin_deal_actions_keyboard(deal_id: int) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="✅ Завершить (Выплатить продавцу)", callback_data=f"adm_deal_complete:{deal_id}"),
        ],
        [
            InlineKeyboardButton(text="❌ Отменить сделку (Возврат)", callback_data=f"adm_deal_cancel:{deal_id}"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад в админку", callback_data="admin_menu")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_admin_requisites_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="🇷🇺 Изменить RUB", callback_data="adm_req_edit:RUB"),
            InlineKeyboardButton(text="🇺🇦 Изменить UAH", callback_data="adm_req_edit:UAH"),
        ],
        [
            InlineKeyboardButton(text="💎 Изменить USDT", callback_data="adm_req_edit:USDT"),
            InlineKeyboardButton(text="💎 Изменить TON", callback_data="adm_req_edit:TON"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад в админку", callback_data="admin_menu")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
