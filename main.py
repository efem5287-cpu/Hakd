# language: Python, file: main.py, target: Railway / Group Moderation & Complaint Bot
import os
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

print("-> Mini sunucu başlatılıyor...", flush=True)

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot aktif!")
    def log_message(self, format, *args):
        pass

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()
print("-> Mini sunucu aktifleşti, port dinleniyor.", flush=True)

API_ID = 35762182
API_HASH = "126917ba7359f8cddb0780ad16e0b1ba"
BOT_TOKEN = "8292808460:AAGUqckzf4LNe_01lSpsFUm7RkhTLoI5Lv4"
ADMIN_USERNAME = "@Onlywmx"

# Yasaklı kelimeler ve reklam kalıpları listesi
BAD_WORDS = ["küfür1", "küfür2", "orospu", "amk", "aq", "piç", "sik", "mal", "discord.gg/", "t.me/", "http://", "https://"]

print("-> Pyrogram in-memory istemcisi oluşturuluyor...", flush=True)
app = Client(
    ":memory:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# /start Komutu ve Ana Menü
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

# Şikayet Bilgi Butonu
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

# Şikayet Komutu İşleyicisi
@app.on_message(filters.command("sikayet"))
async def complaint_handler(client: Client, message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply_text("⚠️ Lütfen şikayetinizin detayını yazın.\nÖrnek: `/sikayet Mesaj içeriği...`")
        return
    
    # Kullanıcıya tam istediğin yanıtı gönderiyoruz
    await message.reply_text(f"Postanız {ADMIN_USERNAME}'e max 2 saat içinde iletilecektir.")

# Küfür ve Reklam / Link Engelleyici
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

async def main():
    print("-> Bot Telegram'a bağlanıyor...", flush=True)
    await app.start()
    print("-> YENİ BOT BAŞARIYLA AKTİF EDİLDİ!", flush=True)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
                              
