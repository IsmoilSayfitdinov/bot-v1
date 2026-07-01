"""Telefonlar bazasi bilan ishlash uchun yordamchi funksiyalar."""

import json
from pathlib import Path

# phones.json fayl yo'li (shu fayl joylashgan papkaga nisbatan)
DATA_PATH = Path(__file__).parent / "data" / "phones.json"


def load_phones() -> list[dict]:
    """phones.json faylidan barcha telefonlarni o'qib qaytaradi."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def format_price(price_uzs: int) -> str:
    """Narxni o'qishga qulay ko'rinishga keltiradi: 16500000 -> '16 500 000 so'm'."""
    return f"{price_uzs:,}".replace(",", " ") + " so'm"


def phone_to_text(phone: dict) -> str:
    """Bitta telefonni chiroyli matn ko'rinishida qaytaradi."""
    return (
        f"📱 *{phone['brand']} {phone['model']}*\n"
        f"💰 Narxi: {format_price(phone['price_uzs'])}\n"
        f"🧠 RAM / Xotira: {phone['ram_gb']} GB / {phone['storage_gb']} GB\n"
        f"🖥 Ekran: {phone['display']}\n"
        f"🔋 Batareya: {phone['battery_mah']} mAh\n"
        f"📷 Asosiy kamera: {phone['main_camera_mp']} MP\n"
        f"⚙️ Protsessor: {phone['chipset']}\n"
        f"📅 Chiqarilgan yili: {phone['release_year']}"
    )


def phones_as_catalog_text() -> str:
    """AI modelga uzatish uchun butun katalogni ixcham matn qiladi."""
    phones = load_phones()
    lines = []
    for p in phones:
        lines.append(
            f"- {p['brand']} {p['model']}: narxi {format_price(p['price_uzs'])}, "
            f"RAM {p['ram_gb']}GB, xotira {p['storage_gb']}GB, ekran {p['display']}, "
            f"batareya {p['battery_mah']}mAh, kamera {p['main_camera_mp']}MP, "
            f"protsessor {p['chipset']}, yil {p['release_year']}, "
            f"OS {p['os']}, teglar: {', '.join(p['tags'])}"
        )
    return "\n".join(lines)


def get_brands() -> list[str]:
    """Bazadagi noyob brendlar ro'yxati."""
    phones = load_phones()
    return sorted({p["brand"] for p in phones})
