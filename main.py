import os
import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# إعداد السجلات
logging.basicConfig(level=logging.INFO)

# التوكن من إعدادات ريندر
API_TOKEN = os.getenv("BOT_TOKEN") 

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- معلومات المطور (تعديلك هنا) ---
DEVELOPER_NAME = "Ali Samir"
DEVELOPER_USERNAME = "TQTTP"  # ضع يوزرك هنا بدون @

# --- قائمة الأزرار الرئيسية ---
def main_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    # زر البحث
    search_btn = InlineKeyboardButton("🔍 البحث في البوت", switch_inline_query_current_chat="")
    
    # أزرار الأقسام
    btn_marvel = InlineKeyboardButton("مارفل", callback_data="marvel")
    btn_series = InlineKeyboardButton("المسلسلات", callback_data="series")
    btn_movies = InlineKeyboardButton("الافلام", callback_data="movies")
    btn_arabic = InlineKeyboardButton("افلام عربية", callback_data="arabic")
    
    # زر المطور وقناة الاقتباسات
    btn_dev = InlineKeyboardButton("👨‍💻 المطور", callback_data="dev_info")
    btn_quotes = InlineKeyboardButton("قناة اقتباسات", url="https://t.me/your_channel")

    keyboard.add(search_btn)
    keyboard.row(btn_marvel, btn_series)
    keyboard.row(btn_movies, btn_arabic)
    keyboard.row(btn_dev, btn_quotes)
    
    return keyboard

# --- الرد على /start ---
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_text = (
        f"🎬 **أهلاً بك في بوت الأفلام!**\n\n"
        f"البوت بإشراف المطور: **{DEVELOPER_NAME}**\n"
        "استخدم الأزرار أدناه للتنقل."
    )
    await message.reply(welcome_text, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

# --- معالجة زر المطور ---
@dp.callback_query_handler(text="dev_info")
async def dev_info(callback_query: types.CallbackQuery):
    dev_text = (
        f"👤 **معلومات المطور**\n\n"
        f"📝 الاسم: {DEVELOPER_NAME}\n"
        f"🆔 اليوزر: @{DEVELOPER_USERNAME}\n"
        f"🎓 التخصص: Medical Laboratory"
    )
    keyboard = InlineKeyboardMarkup()
    btn_contact = InlineKeyboardButton("💬 مراسلة المطور", url=f"https://t.me/{DEVELOPER_USERNAME}")
    keyboard.add(btn_contact)
    
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, dev_text, reply_markup=keyboard, parse_mode="Markdown")

# --- محرك البحث (Inline Query) ---
@dp.inline_handler()
async def search_movies(inline_query: types.InlineQuery):
    query = inline_query.query.lower()
    
    # مثال لقاعدة بيانات (أضف أفلامك هنا)
    movies_db = [
        {"id": "1", "title": "Inception", "link": "https://t.me/share/1"},
        {"id": "2", "title": "Interstellar", "link": "https://t.me/share/2"},
    ]

    results = []
    for movie in movies_db:
        if query in movie['title'].lower():
            results.append(
                types.InlineQueryResultArticle(
                    id=movie['id'],
                    title=movie['title'],
                    input_message_content=types.InputTextMessageContent(
                        f"🎬 **الفيلم:** {movie['title']}\n🔗 **الرابط:** {movie['link']}",
                        parse_mode="Markdown"
                    )
                )
            )
    await bot.answer_inline_query(inline_query.id, results=results, cache_time=1)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
