import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# جلب البيانات من إعدادات ريندر
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 1. ميزة البحث (تعمل في المجموعة وفي الخاص)
@app.on_message(filters.text & (filters.group | filters.private))
async def search_movie(client, message):
    # نتخطى الأوامر مثل /start
    if message.text.startswith("/"):
        return

    query = message.text
    found = False

    # البحث في القناة المحددة
    async for msg in client.search_messages(CHANNEL_ID, query=query, limit=1):
        if msg.video or msg.document:
            found = True
            file_id = msg.video.file_id if msg.video else msg.document.file_id
            
            # إذا كان البحث من "خاص البوت" نرسل الفيلم مباشرة
            if message.chat.type == "private":
                await client.send_chat_action(message.chat.id, "upload_video")
                try:
                    await client.send_video(chat_id=message.chat.id, video=file_id, caption=f"✅ تم العثور على: **{query}**")
                except Exception:
                    await client.send_document(chat_id=message.chat.id, document=file_id, caption=f"✅ تم العثور على: **{query}**")
            
            # إذا كان البحث من "المجموعة" نرسل زر التحويل (لحماية الحقوق)
            else:
                bot_username = (await client.get_me()).username
                url = f"https://t.me/{bot_username}?start={file_id}"
                buttons = InlineKeyboardMarkup([[InlineKeyboardButton("📥 اضغط هنا لمشاهدة الفيلم", url=url)]])
                await message.reply_text(f"✅ تم العثور على: **{query}**\nاضغط على الزر لاستلامه في الخاص 👇", reply_markup=buttons)
            return

    # إذا لم يجد الفيلم في المحادثة الخاصة فقط (اختياري)
    if not found and message.chat.type == "private":
        await message.reply_text("❌ عذراً، لم أجد هذا الفيلم في القناة.")

# 2. ترحيب البوت عند الضغط على /start
@app.on_message(filters.private & filters.command("start"))
async def start_command(client, message):
    # إذا جاء من رابط (payload)
    if len(message.command) > 1:
        file_id = message.command[1]
        try:
            await client.send_video(chat_id=message.chat.id, video=file_id, caption="✅ مشاهدة ممتعة!")
        except Exception:
            await client.send_document(chat_id=message.chat.id, document=file_id)
    else:
        welcome_text = (
            f"أهلاً بك يا {message.from_user.mention} 🎬\n\n"
            "أنا بوت البحث عن الأفلام. يمكنك الآن:\n"
            "1️⃣ كتابة اسم الفيلم هنا مباشرة وسأرسله لك.\n"
            "2️⃣ البحث داخل المجموعة وسأعطيك رابطاً للتحميل."
        )
        await message.reply_text(welcome_text)

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
