import os
import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# إعداد السجلات لمراقبة أداء البوت
logging.basicConfig(level=logging.INFO)

# جلب التوكن من إعدادات Render (Environment Variables)
API_TOKEN = os.getenv("BOT_TOKEN") 

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- بيانات المطور (تم التحديث) ---
DEV_NAME = "Abood"
DEV_USER = "TQTTP" # يوزرك الجديد

# --- دالة إنشاء القائمة الرئيسية ---
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    # زر البحث الفوري
    search_btn = InlineKeyboardButton("🔍 البحث في البوت", switch_inline_query_current_chat="")
    
    # توزيع الأزرار حسب التصميم الذي طلبته
    btn_marvel = InlineKeyboardButton("مارفل", callback_data="cat_marvel")
    btn_series = InlineKeyboardButton("المسلسلات", callback_data="cat_series")
    btn_movies = InlineKeyboardButton("الافلام", callback_data="cat_movies")
    btn_arabic = InlineKeyboardButton("افلام عربية", callback_data="cat_arabic")
    
    btn_dev = InlineKeyboardButton("👨‍💻 المطور", callback_data="dev_section")
    btn_quotes = InlineKeyboardButton("قناة اقتباسات", url="https://t.me/your_channel") # ضع رابط قناتك هنا
    btn_featured = InlineKeyboardButton("🎬 أفلام مختارة", callback_data="cat_featured")

    keyboard.add(search_btn)
    keyboard.row(btn_marvel, btn_series)
    keyboard.row(btn_movies, btn_arabic)
    keyboard.row(btn_dev, btn_quotes)
    keyboard.add(btn_featured)
    
    return keyboard

# --- الرد على أمر /start ---
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    text = (
        f"🎬 **مرحباً بك في بوت الأفلام والمسلسلات**\n\n"
        f"بإشراف المطور: **{DEV_NAME}**\n"
        "استخدم القائمة أدناه للبحث أو اختيار القسم المناسب."
    )
    await message.reply(text, reply_markup=get_main_keyboard(), parse_mode="Markdown")

# --- عرض معلومات المطور عند الضغط على الزر ---
@dp.callback_query_handler(text="dev_section")
async def show_dev(call: types.CallbackQuery):
    dev_text = (
        f"👨‍💻 **معلومات مطور البوت**\n\n"
        f"• الاسم: {DEV_NAME}\n"
        f"• المعرف: @{DEV_USER}\n"
        f"• التخصص: مختبرات طبية - جامعة تعز"
    )
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("💬 مراسلة المطور مباشرة", url=f"https://t.me/{DEV_USER}"))
    
    await bot.send_message(call.from_user.id, dev_text, reply_markup=kb, parse_mode="Markdown")
    await call.answer()

# --- محرك البحث (Inline) لنتائج سريعة ---
@dp.inline_handler()
async def search_movies(inline_query: types.InlineQuery):
    query = inline_query.query.lower()
    
    # قائمة تجريبية للأفلام (يمكنك التوسع فيها لاحقاً)
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
