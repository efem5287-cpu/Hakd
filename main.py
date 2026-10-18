# language: Python, file: main.py, target: Render / Clean Bot
import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

API_ID = 35762182
API_HASH = "126917ba7359f8cddb0780ad16e0b1ba"
BOT_TOKEN = "8292808460:AAGUqckzf4LNe_01lSpsFUm7RkhTLoI5Lv4"
ADMIN_USERNAME = "@Onlywmx"

# Yasaklı kelimeler ve reklam kalıpları listesi
BAD_WORDS = ["küfür1", "küfür2", "orospu", "amk", "aq", "piç", "sik", "mal", "discord.gg/", "t.me/", "http://", "https://"]

app = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Şikayet / Destek Bildir", callback_data="complaint_info")],
        [InlineKeyboardButton("ℹ️ Bot Hakkında", callback_data="bot_info")]
    ])
    await message.reply_text(
        "👋 Merhaba! Ben grup yönetim ve şikayet asistanıyım.\n\n"
        "• Küfür ve izinsiz reklam/linkler otomatik engellenir.\n"
        "• Şikayet ve önerileriniz için aşağıdaki butonu kullanabilirsiniz.",
        reply_markup=keyboard
    )

@app.on_callback_query(filters.regex("complaint_info"))
async def complaint_info_handler(client: Client, callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Geri Dön", callback_data="back_start")]])
    await callback_query.message.edit_text(
        "📝 **Şikayet veya Öneri Göndermek İçin:**\n\n"
        "Lütfen mesajınızı `/sikayet [mesajınız]` komutuyla birlikte gönderin.\n"
        "Örnek: `/sikayet Grup hakkında bir önerim var...`",
        reply_markup=keyboard
    )

@app.on_callback_query(filters.regex("bot_info"))
async def bot_info_handler(client: Client, callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Geri Dön", callback_data="back_start")]])
    await callback_query.message.edit_text(f"Bu bot grup güvenliğini sağlamak ve şikayetleri {ADMIN_USERNAME}'e iletmek için tasarlanmıştır.", reply_markup=keyboard)

@app.on_callback_query(filters.regex("back_start"))
async def back_handler(client: Client, callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Şikayet / Destek Bildir", callback_data="complaint_info")],
        [InlineKeyboardButton("ℹ️ Bot Hakkında", callback_data="bot_info")]
    ])
    await callback_query.message.edit_text("Ana menüdesiniz. İşleminizi seçin:", reply_markup=keyboard)

@app.on_message(filters.command("sikayet"))
async def complaint_handler(client: Client, message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply_text("⚠️ Lütfen şikayetinizin detayını yazın.\nÖrnek: `/sikayet Mesaj içeriği...`")
        return
    
    await message.reply_text(f"Postanız {ADMIN_USERNAME}'e max 2 saat içinde iletilecektir.")

@app.on_message(filters.text & ~filters.command("start") & ~filters.command("sikayet"))
async def moderation_handler(client: Client, message: Message):
    if not message.text:
        return
    
    text_lower = message.text.lower()
    is_violation = any(word in text_lower for word in BAD_WORDS)
    
    if is_violation:
        try:
            await message.delete()
            warning_msg = await message.reply_text(f"⚠️ Dikkat {message.from_user.mention}, küfür veya izinsiz bağlantı/reklam paylaşmak yasaktır!")
            await asyncio.sleep(5)
            await warning_msg.delete()
        except Exception as e:
            print(f"Moderasyon hatası: {e}")

if __name__ == "__main__":
    print("-> Bot saf modda başlatılıyor...", flush=True)
    app.run()
    
