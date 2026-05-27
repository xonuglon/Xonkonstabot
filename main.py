import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Tokenni Render saytidan xavfsiz oladi (bunga tegmang)
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # Rasmda ko'rsatilgan pastki asosiy tugmalar
    kb = [
        [types.KeyboardButton(text="➕ Bot yaratish"), types.KeyboardButton(text="🤖 Botlarim")],
        [types.KeyboardButton(text="👤 Shaxsiy kabinet"), types.KeyboardButton(text="💳 Hisob to'ldirish")],
        [types.KeyboardButton(text="🔗 Referal"), types.KeyboardButton(text="📚 Qo'llanma")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    
    await message.answer(
        "👋 Salom! Bot yaratish platformasiga xush kelibsiz!\n\n"
        "O'zingizga kerakli menyuni tanlang:",
        reply_markup=keyboard
    )

@dp.message(lambda message: message.text == "➕ Bot yaratish")
async def create_bot_handler(message: types.Message):
    # Rasmda ko'rsatilgan ichki tugmalar (Bot turlari)
    kb = [
        [types.InlineKeyboardButton(text="🎬 Kino Bot", callback_data="type_kino"),
         types.InlineKeyboardButton(text="💎 ProKino Bot 💎", callback_data="type_prokino")],
        [types.InlineKeyboardButton(text="🔄 Tarjimon Bot", callback_data="type_tarjimon"),
         types.InlineKeyboardButton(text="🛍️ Mahsulot Bot", callback_data="type_mahsulot")],
        [types.InlineKeyboardButton(text="🚀 Smm Bot", callback_data="type_smm"),
         types.InlineKeyboardButton(text="📞 Aloqa Bot", callback_data="type_aloqa")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer("🤖 Quyidagi bot turlaridan birini tanlang:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith('type_'))
async def process_bot_type(callback_query: types.CallbackQuery):
    bot_type = callback_query.data.split('_')[1]
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        f"🎯 Siz **{bot_type.upper()}** turini tanladingiz.\n\n"
        f"Endi ushbu botni faollashtirish uchun @BotFather'dan olingan **Tokenni** shu yerga yuboring."
    )

async def main():
    print("Builder Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
           
