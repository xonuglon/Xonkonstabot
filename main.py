import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    kb = [
        [types.KeyboardButton(text="➕ Bot yaratish"), types.KeyboardButton(text="🤖 Botlarim")],
        [types.KeyboardButton(text="👤 Shaxsiy kabinet"), types.KeyboardButton(text="💳 Hisob to'ldirish")],
        [types.KeyboardButton(text="🔗 Referal"), types.KeyboardButton(text="📚 Qo'llanma")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(
        f"👋 Salom! **Xonkonstabot** platformasiga xush kelibsiz!\n\n"
        f"Menyuni tanlang:", 
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@dp.message(lambda message: message.text == "➕ Bot yaratish")
async def create_bot_handler(message: types.Message):
    kb = [
        [types.InlineKeyboardButton(text="🎬 Kino Bot", callback_data="type_kino"),
         types.InlineKeyboardButton(text="💎 ProKino Bot 💎", callback_data="type_prokino")],
        [types.InlineKeyboardButton(text="🔄 Tarjimon Bot", callback_data="type_tarjimon"),
         types.InlineKeyboardButton(text="🛍️ Mahsulot Bot", callback_data="type_mahsulot")],
        [types.InlineKeyboardButton(text="🚀 Smm Bot", callback_data="type_smm"),
         types.InlineKeyboardButton(text="📞 Aloqa Bot", callback_data="type_aloqa")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer("🤖 Qaysi turdagi botni yaratmoqchisiz? Tanlang:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith('type_'))
async def process_bot_type(callback_query: types.CallbackQuery):
    bot_type = callback_query.data.split('_')[1]
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id, 
        f"🎯 Siz **{bot_type.upper()} BOT** turini tanladingiz.\n\n"
        f"Endi us'hbu botni ishga tushirish uchun @BotFather'dan olingan **Tokenni** shu yerga yuboring."
    )

async def handle_root(request):
    return web.Response(text="Xonkonstabot is running successfully!")

async def main():
    app = web.Application()
    app.router.add_get("/", handle_root)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.getenv("PORT", 10000)))
    await site.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
