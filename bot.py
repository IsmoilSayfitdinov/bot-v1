"""Telegram bot — telefonlar bo'yicha AI maslahatchi.

Foydalanuvchi bot bilan erkin savol-javob qiladi. Bot Claude API orqali
telefonlar katalogiga tayanib javob beradi: narx, xususiyat, tavsiya.

Ishga tushirish:
    1. .env fayliga TELEGRAM_BOT_TOKEN va ANTHROPIC_API_KEY ni yozing.
    2. pip install -r requirements.txt
    3. python bot.py
"""

import logging
import os
from collections import defaultdict, deque

from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import ai
from database import format_price, load_phones, phone_to_text

# .env fayldan muhit o'zgaruvchilarini yuklaymiz.
load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Har bir foydalanuvchi uchun oxirgi bir necha xabarni saqlaymiz (suhbat konteksti).
# Kalit — chat_id, qiymat — xabarlar navbati (max 8 ta).
_history: dict[int, deque] = defaultdict(lambda: deque(maxlen=8))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/start buyrug'iga javob."""
    text = (
        "Assalomu alaykum! 👋\n\n"
        "Men telefonlar bo'yicha AI maslahatchi botman. "
        "Menga xohlagan savolingizni yozing, masalan:\n\n"
        "• _5 million so'mgacha o'yin uchun telefon bormi?_\n"
        "• _Kamerasi eng zo'r telefon qaysi?_\n"
        "• _Samsung telefonlar narxi qancha?_\n"
        "• _Arzon va batareyasi katta telefon kerak._\n\n"
        "Buyruqlar:\n"
        "/catalog — barcha telefonlar ro'yxati\n"
        "/help — yordam"
    )
    await update.message.reply_markdown(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/help buyrug'iga javob."""
    await update.message.reply_markdown(
        "Shunchaki telefon haqida savolingizni yozing — men bazadan mos "
        "variantlarni topib beraman.\n\n"
        "/catalog — barcha mavjud telefonlar\n"
        "/start — botni qayta ishga tushirish"
    )


async def catalog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/catalog buyrug'i — barcha telefonlar qisqacha ro'yxati."""
    phones = load_phones()
    lines = ["🛍 *Mavjud telefonlar:*\n"]
    for p in phones:
        lines.append(
            f"• *{p['brand']} {p['model']}* — {format_price(p['price_uzs'])}"
        )
    lines.append("\nBatafsil ma'lumot uchun telefon nomini yozing yoki savol bering.")
    await update.message.reply_markdown("\n".join(lines))


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Oddiy matnli xabar — AI orqali javob beramiz."""
    chat_id = update.effective_chat.id
    user_text = update.message.text

    # "yozmoqda..." holatini ko'rsatamiz.
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    history = list(_history[chat_id])
    try:
        reply = ai.answer(user_text, history=history)
    except Exception as exc:  # noqa: BLE001
        logger.exception("AI javob berishda xatolik")
        await update.message.reply_text(
            "Kechirasiz, hozir javob bera olmadim. Birozdan so'ng qayta urinib ko'ring. 🙏"
        )
        return

    # Suhbat kontekstini yangilaymiz.
    _history[chat_id].append({"role": "user", "content": user_text})
    _history[chat_id].append({"role": "assistant", "content": reply})

    await update.message.reply_markdown(reply)


def main() -> None:
    if not TELEGRAM_BOT_TOKEN:
        raise SystemExit(
            "TELEGRAM_BOT_TOKEN topilmadi. .env faylini to'ldiring "
            "(.env.example dan nusxa oling)."
        )
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise SystemExit(
            "ANTHROPIC_API_KEY topilmadi. .env faylini to'ldiring "
            "(.env.example dan nusxa oling)."
        )

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("catalog", catalog))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot ishga tushdi...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
