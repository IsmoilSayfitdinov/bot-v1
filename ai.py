"""Claude API yordamida foydalanuvchi savoliga javob beruvchi qism.

Bot foydalanuvchi yozgan erkin savolni (masalan "5 million so'mgacha o'yin
uchun telefon bormi?") oladi va telefonlar katalogiga tayangan holda javob
beradi. Model faqat bazadagi telefonlar asosida javob berishi uchun katalog
tizim promptiga (system prompt) qo'shib beriladi.
"""

import os

from anthropic import Anthropic

from database import phones_as_catalog_text

# Model nomi. Opus 4.8 — kuchli va aniq javob beradi.
# Arzonroq/tezroq variant uchun "claude-haiku-4-5-20251001" ni ishlatishingiz mumkin.
MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-4-8")

# API kaliti muhit o'zgaruvchisidan olinadi.
_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def _build_system_prompt() -> str:
    """Model uchun tizim prompti — katalog va qoidalar."""
    catalog = phones_as_catalog_text()
    return (
        "Sen telefon do'konining yordamchi chatbotisan. Foydalanuvchilarga "
        "o'zbek tilida, samimiy va qisqa javob berasan. Faqat quyidagi "
        "katalogdagi telefonlar asosida maslahat berasan — katalogda yo'q "
        "telefonni taklif qilma va narx/xususiyatlarni o'zingdan to'qib "
        "chiqarma.\n\n"
        "Agar foydalanuvchi byudjet, brend yoki maqsad (o'yin, kamera, "
        "batareya, arzon) aytsa — shunga mos 1-3 ta telefonni tavsiya qil, "
        "har birining narxi va asosiy afzalligini yoz. Agar mos telefon "
        "bo'lmasa, buni ochiq ayt va eng yaqin variantni taklif qil.\n\n"
        "Narxlarni doim 'so'm'da ko'rsat. Javobni juda uzun qilma.\n\n"
        "=== TELEFONLAR KATALOGI ===\n"
        f"{catalog}\n"
        "=== KATALOG TUGADI ==="
    )


def answer(user_message: str, history: list[dict] | None = None) -> str:
    """Foydalanuvchi savoliga Claude yordamida javob qaytaradi.

    history — oldingi xabarlar ro'yxati (ixtiyoriy), suhbat kontekstini
    saqlash uchun. Har biri {"role": "user"|"assistant", "content": str}.
    """
    messages = list(history or [])
    messages.append({"role": "user", "content": user_message})

    response = _client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=_build_system_prompt(),
        messages=messages,
    )
    # Javob matnini yig'ib qaytaramiz.
    return "".join(block.text for block in response.content if block.type == "text")
