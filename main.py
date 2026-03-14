import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# جلب البيانات من إعدادات ريندر
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))

# تعريف البوت
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 1. ميزة البحث (تعمل في المجموعة وفي الخاص)
@app.on_message(filters.text & (filters.group | filters.private))
async def search_movie(client, message):
    if message.text.startswith("/"):
        return

    query = message.text
    async for msg in client.search_messages(CHANNEL_ID, query=query, limit=1):
        if msg.video or msg.document:
            file_id = msg.video.file_id if msg.video else msg.document.file_id
            
            if message.chat.type.name == "PRIVATE":
                await client.send_chat_action(message.chat.id, "upload_video")
                try:
                    await client.send_video(chat_id=message.chat.id, video=file_id, caption=f"✅ تم العثور على: **{query}**")
                except:
                    await client.send_document(chat_id=message.chat.id, document=file_id, caption=f"✅ تم العثور على: **{query}**")
            else:
                bot_username = (await client.get_me()).username
                url = f"https://t.me/{bot_username}?start={file_id}"
                buttons = InlineKeyboardMarkup([[InlineKeyboardButton("📥 اضغط هنا لمشاهدة الفيلم", url=url)]])
                await message.reply_text(f"✅ تم العثور على: **{query}**\nاضغط على الزر لاستلامه في الخاص 👇", reply_markup=buttons)
            return

# 2. ترحيب البوت عند الضغط على /start
@app.on_message(filters.private & filters.command("start"))
async def start_command(client, message):
    if len(message.command) > 1:
        file_id = message.command[1]
        try:
            await client.send_video(chat_id=message.chat.id, video=file_id, caption="✅ مشاهدة ممتعة!")
        except:
            await client.send_document(chat_id=message.chat.id, document=file_id)
    else:
        welcome_text = (
            f"أهلاً بك يا {message.from_user.mention} 🎬\n\n"
            "أنا بوت البحث عن الأفلام. يمكنك الآن:\n"
            "1️⃣ كتابة اسم الفيلم هنا مباشرة وسأرسله لك.\n"
            "2️⃣ البحث داخل المجموعة وسأعطيك رابطاً للتحميل."
        )
        await message.reply_text(welcome_text)

# --- الطريقة الصحيحة للتشغيل في ريندر لتفادي RuntimeError ---
async def main():
    async with app:
        print("✅ البوت يعمل الآن بنجاح...")
        await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
