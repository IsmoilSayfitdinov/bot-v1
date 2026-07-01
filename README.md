# 📱 Telefon Maslahatchi — Telegram Bot (AI)

Telefonlar bazasidan foydalanib, foydalanuvchi bilan **savol-javob** qiladigan
Telegram bot. Foydalanuvchi erkin savol yozadi (masalan _"5 million so'mgacha
o'yin uchun telefon bormi?"_), bot esa **Claude AI** yordamida katalogdagi
telefonlar asosida narx va xususiyatlar bilan javob beradi.

## ✨ Imkoniyatlar

- 🤖 Erkin matnli savol-javob (AI, o'zbek tilida)
- 💰 Narx, RAM, xotira, kamera, batareya bo'yicha tavsiya
- 🛍 `/catalog` — barcha telefonlar ro'yxati
- 🧠 Suhbat kontekstini eslab qoladi (oxirgi bir necha xabar)
- 📄 Telefonlar bazasi oddiy `data/phones.json` faylida — oson tahrirlanadi

## 🗂 Loyiha tuzilishi

```
phone-bot/
├── bot.py              # Telegram bot (asosiy fayl)
├── ai.py               # Claude API bilan javob berish logikasi
├── database.py         # phones.json bilan ishlash
├── data/
│   └── phones.json     # Telefonlar bazasi (bu yerni tahrirlab telefon qo'shing)
├── requirements.txt    # Kutubxonalar
├── .env.example        # Muhit o'zgaruvchilari namunasi
└── README.md
```

## 🚀 O'rnatish va ishga tushirish

### 1. Kerakli narsalar

- Python 3.10+
- Telegram bot tokeni — [@BotFather](https://t.me/BotFather) dan `/newbot` orqali oling
- Claude API kaliti — [console.anthropic.com](https://console.anthropic.com) dan oling

### 2. Loyihani yuklab oling

```bash
git clone https://github.com/FOYDALANUVCHI/phone-bot.git
cd phone-bot
```

### 3. Kutubxonalarni o'rnating

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Kalitlarni sozlang

`.env.example` faylidan nusxa oling va to'ldiring:

```bash
cp .env.example .env
```

`.env` fayl ichida:

```
TELEGRAM_BOT_TOKEN=123456:AbCdEf...
ANTHROPIC_API_KEY=sk-ant-...
```

> ⚠️ `.env` faylni hech qachon GitHub'ga yuklamang — u `.gitignore` da bloklangan.

### 5. Ishga tushiring

```bash
python bot.py
```

Endi Telegram'da botingizga `/start` yozing! 🎉

## 📝 Telefon qo'shish / o'zgartirish

`data/phones.json` faylini tahrirlang. Har bir telefon quyidagi ko'rinishda:

```json
{
  "id": 13,
  "brand": "Xiaomi",
  "model": "Redmi Note 14",
  "price_uzs": 4200000,
  "ram_gb": 8,
  "storage_gb": 256,
  "display": "6.67\" AMOLED 120Hz",
  "battery_mah": 5500,
  "main_camera_mp": 108,
  "chipset": "MediaTek Dimensity 7025",
  "release_year": 2024,
  "os": "Android",
  "tags": ["o'rta", "kamera", "batareya"]
}
```

Botni qayta ishga tushirish shart emas emas — keyingi savolda yangi baza o'qiladi.

## 🤔 Botdan namunaviy savollar

- _5 million so'mgacha o'yin uchun telefon bormi?_
- _Kamerasi eng zo'r telefon qaysi?_
- _Samsung telefonlar narxini ayting_
- _Arzon va batareyasi katta telefon kerak_
- _iPhone 15 Pro Max xususiyatlari qanday?_

## 🛠 Texnologiyalar

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [Anthropic Claude API](https://docs.anthropic.com/)

## 📄 Litsenziya

MIT
