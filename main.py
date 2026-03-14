import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# جلب البيانات من إعدادات ريندر (Environment Variables)
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID")) # آيدي القناة التي بها الأفلام

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 1. البحث عند كتابة اسم الفيلم في المجموعة
@app.on_message(filters.group & filters.text)
async def search_in_channel(client, message):
    query = message.text
    # البحث في القناة المحددة
    async for msg in client.search_messages(CHANNEL_ID, query=query, limit=1):
        # التأكد أن الرسالة تحتوي على فيديو أو ملف
        if msg.video or msg.document:
            file_id = msg.video.file_id if msg.video else msg.document.file_id
            
            # إنشاء رابط يحول المستخدم للبوت مع كود الفيلم
            bot_username = (await client.get_me()).username
            url = f"https://t.me/{bot_username}?start={file_id}"
            
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("📥 اضغط هنا لمشاهدة الفيلم", url=url)]
            ])
            
            await message.reply_text(
                f"✅ تم العثور على: **{query}**\n\nاضغط على الزر بالأسفل لاستلام الفيلم في الخاص 👇",
                reply_markup=buttons
            )
            return

# 2. استقبال المستخدم في الخاص وإرسال الفيلم له
@app.on_message(filters.private & filters.command("start"))
async def send_file_private(client, message):
    # إذا كان الرابط يحتوي على كود الفيلم (payload)
    if len(message.command) > 1:
        file_id = message.command[1]
        try:
            await client.send_video(
                chat_id=message.chat.id, 
                video=file_id, 
                caption="✅ إليك الفيلم الذي طلبته، مشاهدة ممتعة!"
            )
        except Exception:
            # في حال كان الملف "Document" وليس "Video"
            await client.send_document(chat_id=message.chat.id, document=file_id)
    else:
        await message.reply_text("أهلاً بك! أنا بوت البحث عن الأفلام. ابحث عن أي فيلم داخل المجموعة وسأرسله لك هنا.")

print("البوت يعمل الآن...")
app.run()
