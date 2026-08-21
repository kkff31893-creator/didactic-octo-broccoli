# Multi-language dictionary and helper functions

TEXTS = {
    "ru": {
        "welcome": (
            "👋 <b>Добро пожаловать в сервис безопасных сделок Garant Bot!</b>\n\n"
            "🛡️ <i>Я обеспечу полную безопасность вашей сделки между покупателем и продавцом. "
            "Деньги хранятся в гаранте до момента успешного получения товара или услуги.</i>\n\n"
            "👇 <b>Выберите действие в меню ниже:</b>"
        ),
        "btn_create_deal": "🤝 Создать сделку",
        "btn_profile": "👤 Мой профиль",
        "btn_my_deals": "📋 Мои сделки",
        "btn_language": "🌐 Смена языка",
        "btn_support": "💬 Поддержка",
        "btn_back": "⬅️ Назад в меню",
        "btn_cancel": "❌ Отмена",

        # Profile
        "profile_card": (
            "👤 <b>Ваш профиль:</b>\n\n"
            "🆔 <b>Telegram ID:</b> <code>{telegram_id}</code>\n"
            "👤 <b>Юзернейм:</b> @{username}\n"
            "⭐ <b>Рейтинг:</b> {rating} / 5.0 (Отзывов: {reviews_count})\n"
            "🤝 <b>Успешных сделок:</b> {completed_deals}\n"
            "⏳ <b>Активных сделок:</b> {active_deals}\n\n"
            "💰 <b>Ваш баланс:</b>\n"
            "├ 🇷🇺 <b>RUB:</b> <code>{balance_rub:.2f} ₽</code>\n"
            "├ 🇺🇦 <b>UAH:</b> <code>{balance_uah:.2f} ₴</code>\n"
            "├ 💎 <b>USDT:</b> <code>{balance_usdt:.2f} $</code>\n"
            "└ 💎 <b>TON:</b> <code>{balance_ton:.2f} TON</code>"
        ),
        "btn_view_reviews": "💬 Посмотреть отзывы ({count})",
        "btn_withdraw": "💸 Вывод средств",

        # Partner Profile in Deal
        "partner_profile_card": (
            "👤 <b>Профиль второго участника:</b>\n"
            "🆔 <b>ID:</b> <code>{telegram_id}</code>\n"
            "👤 <b>Юзернейм:</b> @{username}\n"
            "⭐ <b>Рейтинг:</b> {rating} / 5.0 ({reviews_count} отз.)\n"
            "🤝 <b>Завершенных сделок:</b> {completed_deals}"
        ),

        # Deal Creation
        "create_deal_step_role": "🤝 <b>Создание новой сделки:</b>\n\nВыберите вашу роль в сделке:",
        "role_buyer": "🛒 Я Покупатель",
        "role_seller": "📦 Я Продавец",
        "create_deal_step_currency": "💱 <b>Выберите валюту сделки:</b>",
        "create_deal_step_amount": "💵 <b>Введите сумму сделки</b> (числом, например: <code>1500</code> или <code>25.5</code>):",
        "invalid_amount": "⚠️ <i>Пожалуйста, введите корректное положительное число!</i>",
        "create_deal_step_title": "📝 <b>Введите краткое название или описание товара/услуги:</b>\n<i>(Например: Покупка Telegram канала / Дизайн сайта)</i>",
        "deal_created_success": (
            "✅ <b>Сделка #{deal_id} успешно создана!</b>\n\n"
            "📌 <b>Название:</b> {title}\n"
            "💰 <b>Сумма:</b> {amount} {currency}\n"
            "🎭 <b>Ваша роль:</b> {role_text}\n"
            "📊 <b>Статус:</b> ⏳ Ожидание второго участника\n\n"
            "🔗 <b>Отправьте эту ссылку второму участнику:</b>\n"
            "<code>{invite_link}</code>\n\n"
            "<i>Как только участник перейдет по ссылке, сделка начнется!</i>"
        ),

        # Deal View Card
        "deal_card": (
            "🤝 <b>Сделка #{deal_id}</b> [<code>{deal_code}</code>]\n\n"
            "📌 <b>Товар/Услуга:</b> {title}\n"
            "💰 <b>Сумма:</b> <code>{amount} {currency}</code>\n"
            "📊 <b>Статус:</b> {status_text}\n\n"
            "🛒 <b>Покупатель:</b> {buyer_text}\n"
            "📦 <b>Продавец:</b> {seller_text}\n\n"
            "{extra_info}"
        ),

        # Statuses
        "status_pending_partner": "⏳ Ожидает второго участника",
        "status_unpaid": "💳 Не оплачено (Ожидает оплаты покупателем)",
        "status_paid_held": "🔒 Оплачено (Деньги в гаранте, передайте товар)",
        "status_delivered": "📦 Товар передан (Ожидает подтверждения покупателя)",
        "status_completed": "✅ Успешно завершена (Выплата произведена)",
        "status_disputed": "⚠️ Открыт спор (Ожидает арбитража)",
        "status_cancelled": "❌ Отменена",

        # Deal Action Buttons
        "btn_pay_deal": "💳 Оплатить сделку",
        "btn_confirm_paid": "✅ Я оплатил",
        "btn_deliver_goods": "📦 Товар передан",
        "btn_confirm_received": "✅ Подтвердить получение и выплату",
        "btn_open_dispute": "⚠️ Открыть спор",
        "btn_cancel_deal": "❌ Отменить сделку",
        "btn_refresh_deal": "🔄 Обновить статус",
        "btn_leave_review": "⭐ Оставить отзыв",

        # Deal Notifications
        "notify_partner_joined": (
            "🔔 <b>Второй участник присоединился к сделке #{deal_id}!</b>\n\n"
            "{partner_profile}\n\n"
            "👉 Теперь покупатель должен внести оплату в гарант-сервис."
        ),
        "notify_payment_held": (
            "🔔 <b>Оплата по сделке #{deal_id} успешно получена гарантом!</b>\n\n"
            "📦 <b>Продавец, можете передавать товар/услугу покупателю.</b>\n"
            "<i>После передачи нажмите кнопку «📦 Товар передан».</i>"
        ),
        "notify_goods_delivered": (
            "🔔 <b>Продавец сообщил о передаче товара по сделке #{deal_id}!</b>\n\n"
            "🛒 <b>Покупатель, проверьте товар/услугу.</b>\n"
            "<i>Если всё в порядке, нажмите «✅ Подтвердить получение и выплату». Если возникли проблемы — нажмите «⚠️ Открыть спор».</i>"
        ),
        "notify_deal_completed": (
            "🎉 <b>Сделка #{deal_id} успешно завершена!</b>\n\n"
            "💰 <b>{amount} {currency}</b> зачислены на баланс продавца.\n"
            "⭐ Пожалуйста, оставьте отзыв друг о друге!"
        ),
        "notify_deal_cancelled": "❌ <b>Сделка #{deal_id} была отменена.</b>",
        "notify_dispute_opened": (
            "⚠️ <b>По сделке #{deal_id} открыт спор!</b>\n\n"
            "Причина: <i>{reason}</i>\n"
            "Администратор сервиса уведомлен и подключится к разрешению ситуации."
        ),

        # Reviews
        "review_prompt_rating": "⭐ <b>Оцените работу участника по сделке #{deal_id}:</b>",
        "review_prompt_text": "✍️ <b>Напишите ваш комментарий / отзыв:</b>\n<i>(Или нажмите «Пропустить», чтобы оставить только оценку)</i>",
        "btn_skip_review_text": "⏩ Пропустить комментарий",
        "review_saved_success": "✅ <b>Спасибо! Ваш отзыв успешно сохранен.</b>",

        # Language
        "choose_language": "🌐 <b>Выберите язык интерфейса / Select language:</b>",
        "language_changed": "✅ <b>Язык успешно изменен на Русский!</b>",

        # Support
        "support_text": (
            "💬 <b>Служба поддержки Garant Bot</b>\n\n"
            "Если у вас возникли вопросы по сделке, проблемы с оплатой или предложения:\n\n"
            "👨‍💻 <b>Контакт оператора:</b> {support_username}\n"
            "⏰ <b>Время ответа:</b> 5-15 минут"
        ),
    },

    "ua": {
        "welcome": (
            "👋 <b>Ласкаво просимо до сервісу безпечних угод Garant Bot!</b>\n\n"
            "🛡️ <i>Я забезпечу повну безпеку вашої угоди між покупцем та продавцем. "
            "Гроші зберігаються в гаранті до моменту успішного отримання товару чи послуги.</i>\n\n"
            "👇 <b>Оберіть дію в меню нижче:</b>"
        ),
        "btn_create_deal": "🤝 Створити угоду",
        "btn_profile": "👤 Мій профіль",
        "btn_my_deals": "📋 Мої угоди",
        "btn_language": "🌐 Зміна мови",
        "btn_support": "💬 Підтримка",
        "btn_back": "⬅️ Назад в меню",
        "btn_cancel": "❌ Скасувати",

        # Profile
        "profile_card": (
            "👤 <b>Ваш профіль:</b>\n\n"
            "🆔 <b>Telegram ID:</b> <code>{telegram_id}</code>\n"
            "👤 <b>Юзернейм:</b> @{username}\n"
            "⭐ <b>Рейтинг:</b> {rating} / 5.0 (Відгуків: {reviews_count})\n"
            "🤝 <b>Успішних угод:</b> {completed_deals}\n"
            "⏳ <b>Активних угод:</b> {active_deals}\n\n"
            "💰 <b>Ваш баланс:</b>\n"
            "├ 🇷🇺 <b>RUB:</b> <code>{balance_rub:.2f} ₽</code>\n"
            "├ 🇺🇦 <b>UAH:</b> <code>{balance_uah:.2f} ₴</code>\n"
            "├ 💎 <b>USDT:</b> <code>{balance_usdt:.2f} $</code>\n"
            "└ 💎 <b>TON:</b> <code>{balance_ton:.2f} TON</code>"
        ),
        "btn_view_reviews": "💬 Переглянути відгуки ({count})",
        "btn_withdraw": "💸 Виведення коштів",

        # Partner Profile
        "partner_profile_card": (
            "👤 <b>Профіль другого учасника:</b>\n"
            "🆔 <b>ID:</b> <code>{telegram_id}</code>\n"
            "👤 <b>Юзернейм:</b> @{username}\n"
            "⭐ <b>Рейтинг:</b> {rating} / 5.0 ({reviews_count} відгуків)\n"
            "🤝 <b>Завершених угод:</b> {completed_deals}"
        ),

        # Deal Creation
        "create_deal_step_role": "🤝 <b>Створення нової угоди:</b>\n\nОберіть вашу роль в угоді:",
        "role_buyer": "🛒 Я Покупець",
        "role_seller": "📦 Я Продавець",
        "create_deal_step_currency": "💱 <b>Оберіть валюту угоди:</b>",
        "create_deal_step_amount": "💵 <b>Введіть суму угоди</b> (числом, наприклад: <code>1500</code> або <code>25.5</code>):",
        "invalid_amount": "⚠️ <i>Будь ласка, введіть коректне додатне число!</i>",
        "create_deal_step_title": "📝 <b>Введіть короткий опис товару/послуги:</b>",
        "deal_created_success": (
            "✅ <b>Угода #{deal_id} успішно створена!</b>\n\n"
            "📌 <b>Назва:</b> {title}\n"
            "💰 <b>Сума:</b> {amount} {currency}\n"
            "🎭 <b>Ваша роль:</b> {role_text}\n"
            "📊 <b>Статус:</b> ⏳ Очікування другого учасника\n\n"
            "🔗 <b>Надішліть це посилання другому учаснику:</b>\n"
            "<code>{invite_link}</code>"
        ),

        # Deal View Card
        "deal_card": (
            "🤝 <b>Угода #{deal_id}</b> [<code>{deal_code}</code>]\n\n"
            "📌 <b>Товар/Послуга:</b> {title}\n"
            "💰 <b>Сума:</b> <code>{amount} {currency}</code>\n"
            "📊 <b>Статус:</b> {status_text}\n\n"
            "🛒 <b>Покупець:</b> {buyer_text}\n"
            "📦 <b>Продавець:</b> {seller_text}\n\n"
            "{extra_info}"
        ),

        # Statuses
        "status_pending_partner": "⏳ Очікує другого учасника",
        "status_unpaid": "💳 Не оплачено (Очікує оплати покупцем)",
        "status_paid_held": "🔒 Оплачено (Гроші в гаранті, передайте товар)",
        "status_delivered": "📦 Товар передано (Очікує підтвердження)",
        "status_completed": "✅ Успішно завершено (Виплата проведена)",
        "status_disputed": "⚠️ Відкрито суперечку (Очікує арбітражу)",
        "status_cancelled": "❌ Скасовано",

        "btn_pay_deal": "💳 Оплатити угоду",
        "btn_confirm_paid": "✅ Я оплатив",
        "btn_deliver_goods": "📦 Товар передано",
        "btn_confirm_received": "✅ Підтвердити отримання та виплату",
        "btn_open_dispute": "⚠️ Відкрити суперечку",
        "btn_cancel_deal": "❌ Скасувати угоду",
        "btn_refresh_deal": "🔄 Оновити статус",
        "btn_leave_review": "⭐ Залишити відгук",

        "notify_partner_joined": (
            "🔔 <b>Другий учасник приєднався до угоди #{deal_id}!</b>\n\n"
            "{partner_profile}\n\n"
            "👉 Тепер покупець повинен внести оплату в гарант-сервіс."
        ),
        "notify_payment_held": (
            "🔔 <b>Оплата за угодою #{deal_id} успішно отримана гарантом!</b>\n\n"
            "📦 <b>Продавець, можете передавати товар/послугу покупцю.</b>"
        ),
        "notify_goods_delivered": (
            "🔔 <b>Продавець повідомив про передачу товару за угодою #{deal_id}!</b>\n\n"
            "🛒 <b>Покупець, перевірте товар/послугу.</b>"
        ),
        "notify_deal_completed": (
            "🎉 <b>Угода #{deal_id} успішно завершена!</b>\n\n"
            "💰 <b>{amount} {currency}</b> зараховано на баланс продавця."
        ),
        "notify_deal_cancelled": "❌ <b>Угода #{deal_id} була скасована.</b>",
        "notify_dispute_opened": "⚠️ <b>За угодою #{deal_id} відкрито суперечку!</b>",

        "review_prompt_rating": "⭐ <b>Оцініть роботу учасника за угодою #{deal_id}:</b>",
        "review_prompt_text": "✍️ <b>Напишіть ваш відгук:</b>",
        "btn_skip_review_text": "⏩ Пропустити коментар",
        "review_saved_success": "✅ <b>Дякуємо! Ваш відгук успішно збережено.</b>",
        "choose_language": "🌐 <b>Оберіть мову інтерфейсу:</b>",
        "language_changed": "✅ <b>Мову успішно змінено на Українську!</b>",
        "support_text": "💬 <b>Служба підтримки Garant Bot</b>\n\n👨‍💻 <b>Контакт:</b> {support_username}",
    },

    "en": {
        "welcome": (
            "👋 <b>Welcome to Garant Bot Escrow Service!</b>\n\n"
            "🛡️ <i>I provide full protection for deals between buyers and sellers. "
            "Funds are safely held in escrow until the product or service is confirmed.</i>\n\n"
            "👇 <b>Select an action in the menu below:</b>"
        ),
        "btn_create_deal": "🤝 Create Deal",
        "btn_profile": "👤 My Profile",
        "btn_my_deals": "📋 My Deals",
        "btn_language": "🌐 Change Language",
        "btn_support": "💬 Support",
        "btn_back": "⬅️ Back to Menu",
        "btn_cancel": "❌ Cancel",

        # Profile
        "profile_card": (
            "👤 <b>Your Profile:</b>\n\n"
            "🆔 <b>Telegram ID:</b> <code>{telegram_id}</code>\n"
            "👤 <b>Username:</b> @{username}\n"
            "⭐ <b>Rating:</b> {rating} / 5.0 ({reviews_count} reviews)\n"
            "🤝 <b>Completed Deals:</b> {completed_deals}\n"
            "⏳ <b>Active Deals:</b> {active_deals}\n\n"
            "💰 <b>Your Balance:</b>\n"
            "├ 🇷🇺 <b>RUB:</b> <code>{balance_rub:.2f} ₽</code>\n"
            "├ 🇺🇦 <b>UAH:</b> <code>{balance_uah:.2f} ₴</code>\n"
            "├ 💎 <b>USDT:</b> <code>{balance_usdt:.2f} $</code>\n"
            "└ 💎 <b>TON:</b> <code>{balance_ton:.2f} TON</code>"
        ),
        "btn_view_reviews": "💬 View Reviews ({count})",
        "btn_withdraw": "💸 Withdraw Funds",

        # Partner Profile
        "partner_profile_card": (
            "👤 <b>Partner Profile:</b>\n"
            "🆔 <b>ID:</b> <code>{telegram_id}</code>\n"
            "👤 <b>Username:</b> @{username}\n"
            "⭐ <b>Rating:</b> {rating} / 5.0 ({reviews_count} reviews)\n"
            "🤝 <b>Completed Deals:</b> {completed_deals}"
        ),

        # Deal Creation
        "create_deal_step_role": "🤝 <b>Create a new deal:</b>\n\nSelect your role in the deal:",
        "role_buyer": "🛒 I am Buyer",
        "role_seller": "📦 I am Seller",
        "create_deal_step_currency": "💱 <b>Select deal currency:</b>",
        "create_deal_step_amount": "💵 <b>Enter deal amount</b> (number, e.g. <code>1500</code> or <code>25.5</code>):",
        "invalid_amount": "⚠️ <i>Please enter a valid positive number!</i>",
        "create_deal_step_title": "📝 <b>Enter product/service title:</b>",
        "deal_created_success": (
            "✅ <b>Deal #{deal_id} created successfully!</b>\n\n"
            "📌 <b>Title:</b> {title}\n"
            "💰 <b>Amount:</b> {amount} {currency}\n"
            "🎭 <b>Your Role:</b> {role_text}\n"
            "📊 <b>Status:</b> ⏳ Waiting for partner\n\n"
            "🔗 <b>Send this invite link to your partner:</b>\n"
            "<code>{invite_link}</code>"
        ),

        # Deal View Card
        "deal_card": (
            "🤝 <b>Deal #{deal_id}</b> [<code>{deal_code}</code>]\n\n"
            "📌 <b>Item/Service:</b> {title}\n"
            "💰 <b>Amount:</b> <code>{amount} {currency}</code>\n"
            "📊 <b>Status:</b> {status_text}\n\n"
            "🛒 <b>Buyer:</b> {buyer_text}\n"
            "📦 <b>Seller:</b> {seller_text}\n\n"
            "{extra_info}"
        ),

        # Statuses
        "status_pending_partner": "⏳ Waiting for partner to join",
        "status_unpaid": "💳 Unpaid (Waiting for buyer payment)",
        "status_paid_held": "🔒 Paid (Funds in escrow, seller can deliver)",
        "status_delivered": "📦 Delivered (Waiting for buyer confirmation)",
        "status_completed": "✅ Completed (Payout processed)",
        "status_disputed": "⚠️ Disputed (Waiting for arbitration)",
        "status_cancelled": "❌ Cancelled",

        "btn_pay_deal": "💳 Pay Deal",
        "btn_confirm_paid": "✅ I have Paid",
        "btn_deliver_goods": "📦 Goods Delivered",
        "btn_confirm_received": "✅ Confirm Receipt & Payout",
        "btn_open_dispute": "⚠️ Open Dispute",
        "btn_cancel_deal": "❌ Cancel Deal",
        "btn_refresh_deal": "🔄 Refresh Status",
        "btn_leave_review": "⭐ Leave Review",

        "notify_partner_joined": (
            "🔔 <b>Partner joined deal #{deal_id}!</b>\n\n"
            "{partner_profile}\n\n"
            "👉 Buyer should now make payment to the escrow service."
        ),
        "notify_payment_held": (
            "🔔 <b>Payment for deal #{deal_id} held in escrow!</b>\n\n"
            "📦 <b>Seller, you can now transfer the goods/service to the buyer.</b>"
        ),
        "notify_goods_delivered": (
            "🔔 <b>Seller delivered goods for deal #{deal_id}!</b>\n\n"
            "🛒 <b>Buyer, please check the goods and confirm receipt.</b>"
        ),
        "notify_deal_completed": (
            "🎉 <b>Deal #{deal_id} completed successfully!</b>\n\n"
            "💰 <b>{amount} {currency}</b> credited to seller's balance."
        ),
        "notify_deal_cancelled": "❌ <b>Deal #{deal_id} was cancelled.</b>",
        "notify_dispute_opened": "⚠️ <b>Dispute opened for deal #{deal_id}!</b>",

        "review_prompt_rating": "⭐ <b>Rate the partner for deal #{deal_id}:</b>",
        "review_prompt_text": "✍️ <b>Write your review comment:</b>",
        "btn_skip_review_text": "⏩ Skip Comment",
        "review_saved_success": "✅ <b>Thank you! Your review has been saved.</b>",
        "choose_language": "🌐 <b>Select language:</b>",
        "language_changed": "✅ <b>Language set to English!</b>",
        "support_text": "💬 <b>Garant Bot Support</b>\n\n👨‍💻 <b>Contact:</b> {support_username}",
    }
}

def get_text(key: str, lang: str = "ru", **kwargs) -> str:
    lang_dict = TEXTS.get(lang, TEXTS["ru"])
    raw_text = lang_dict.get(key, TEXTS["ru"].get(key, f"[{key}]"))
    if kwargs:
        return raw_text.format(**kwargs)
    return raw_text
