import os
import asyncio
import logging
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# إعدادات تسجيل الأخطاء لضمان أعلى مستوى من الاستقرار في Render
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ==========================================================
# ⚙️ [ قسم الإعدادات والرسائل - اكتب بياناتك هنا ] ⚙️
# ==========================================================

# 1️⃣ ضع توكن البوت الخاص بك هنا بين علامات التنصيص:
BOT_TOKEN = "8721360021:AAGW_ZRnONtURyf9HUjhQsZRhQuSyriAbHA"

# 2️⃣ ضع معرف حسابك (Chat ID) كأدمن هنا بين علامات التنصيص (رقم فقط):
ADMIN_CHAT_ID = "6506150207"

# 3️⃣ رسالتك الترحيبية الطويلة جداً (تظهر بعد ضغط Start):
WELCOME_MESSAGE = """

فريق أثر الخالدين | رؤية نحو المستقبل

​نعيش اليوم مرحلة تتطلب مهارات تتجاوز المقاعد الدراسية. من قلب ثانوية المتفوقين الثانية، انطلقنا لنكون البيئة التي تحتضن العلماء والأطباء والأدباء القادمين؛ لتخريج جيل منافس عالمياً يمثل مدرستنا ووطننا في أرقى المحافل والجامعات العالمية.

​📋 أقسام الفريق:

🔬 البحث العلمي الشامل: كتابة البحوث العلمية والإنسانية بمهنية عالية (بعيداً عن المواضيع السياسية والدينية).

🎨 الفن والأدب والمسرح: لكل المبدعين في الفنون بجميع أنواعها والباحثين في الأدب.

💻 التكنولوجيا والذكاء الاصطناعي: الاهتمام بالبرمجة والتقنيات الحديثة.

📸 الإعلام والتصميم: تصميم البحوث، التدقيق اللغوي، وتصوير الفعاليات.

⚽️ النشاطات والرياضة: المساعدة في تنظيم الحملات التطوعية والفعاليات الرياضية.

​📄 للمزيد من المعلومات:

لمعرفة تفاصيل أكثر حول رؤية الفريق ونظامه الداخلي وقواعد الانضمام، يمكنكم الاطلاع على الملف التعريفي المرفق في الرابط أدناه.

​https://www.canva.com/design/DAHMZe1VjH0/HI7p552O9TrJgmMMRXc0HQ/view?utm_content=DAHMZe1VjH0&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hee20c388a2

​🎫 لطلب كود التقديم:

يرجى إرسال (الاسم الثلاثي + المرحلة الدراسية والشعبة) هنا. 

⚠️ ملاحظة: في حال كان الاسم وهمياً، لن يصلك كود الدخول للاستمارة إلكترونية.

​⏳ تنبيه: يغلق التقديم يوم الجمعة القادم تمام الساعة 6:00 مساءً.



​رئيس مجلس إدارة الفريق

[يوسف محمد عبدالرضا]

"""

# 4️⃣ رسالة الشكر والرد التلقائي (تظهر للمستخدم فور إرسال رسالته):
THANK_YOU_MESSAGE = """
شكراً على اهتمامك بالفريق، نقدر وقتك الثمين، وسيتم الرد عليك من قبل رئيس الفريق بأسرع وقت ممكن،  شاكرين تفهمك.🪻
"""

# ==========================================================

# 🌐 نظام السيرفر المدمج المتوافق 100% مع بيئة Render ومنع النوم
app = Flask('')

@app.route('/')
def home():
    return "Athar Bot Core Engine is Active and Flying! 🚀"

def run_flask():
    # جلب المنفذ تلقائياً ليتوافق مع نظام Render (الافتراضي 10000 أو المنفذ المحدد سحابياً)
    port = int(os.environ.get("PORT", 10000))
    print(f"[INFO] Web Server listening on port {port}...", flush=True)
    app.run(host='0.0.0.0', port=port)

# 🚀 دالة معالجة أمر /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)

# 📩 دالة استقبال وتحويل الرسائل ونظام الرد الذكي
async def handle_incoming_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    # 👤 أولاً: نظام الرد المباشر للأدمن عند عمل Reply على رسالة البوت
    if str(user_id) == str(ADMIN_CHAT_ID):
        if update.message.reply_to_message:
            try:
                reply_markup = update.message.reply_to_message.reply_markup
                button_url = reply_markup.inline_keyboard[0][0].url
                original_user_id = button_url.split('id=')[1]
                
                await context.bot.send_message(chat_id=int(original_user_id), text=update.message.text)
                await update.message.reply_text("✅ تم إرسال ردك بنجاح.")
            except Exception:
                await update.message.reply_text("❌ عذراً، لا يمكن الرد على هذه الرسالة.")
        return

    # 📥 ثانياً: نظام استقبال رسائل المستخدمين وتحويلها للأدمن بسرعة البرق
    user_name = user.first_name
    username = f"@{user.username}" if user.username else "لا يوجد يوزرنيم"
    message_text = update.message.text

    admin_notification_text = (
        f"📩 رسالة جديدة وصلت للبوت!\n\n"
        f"👤 الاسم: {user_name}\n"
        f"🆔 الآيدي: `{user_id}`\n"
        f"🏷 اليوزرنيم: {username}\n"
        f"✍️ الرسالة:\n{message_text}"
    )

    # زر مدمج ذكي للانتقال المباشر لحساب الشخص المرسل
    keyboard = [[InlineKeyboardButton(text=f"👤 فتح حساب: {user_name}", url=f"tg://user?id={user_id}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # إرسال الرسالة للأدمن فوراً وإرسال رسالة الشكر التلقائية للمستخدم
    await context.bot.send_message(chat_id=int(ADMIN_CHAT_ID), text=admin_notification_text, reply_markup=reply_markup)
    await update.message.reply_text(THANK_YOU_MESSAGE)

# الدالة الأساسية لتشغيل محرك البوت
async def main_bot():
    print("🤖 البوت يعمل الآن بنجاح واستقرار تام على سيرفرات Render...", flush=True)
    
    # بناء التطبيق وربط الدوال البرمجية بالأوامر والرسائل
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_incoming_messages))
    
    # تشغيل الاستماع المستمر المتوافق مع البيئة السحابية لـ Render
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    # حلقة مستمرة لضمان عدم توقف البوت نهائياً عن العمل
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    def start_all():
    # 1. تشغيل سيرفر الويب الخفيف في الخلفية لمنع ريندر من الإغلاق
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # 2. إنشاء وتجهيز محرك البوت مع كل خاصياتك وأزرارك
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    BOT_TOKEN = "YOUR_BOT_TOKEN_HERE" # ⚠️ امسح هذا واكتب توكن بوتك الحقيقي هنا
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # ربط دالاتك الخاصة بالردود والأوامر داخل المحرك الجديد
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_incoming_messages))
    
    # 3. إطلاق البوت والبدء في استقبال الرسائل فوراً
    logger.info("[SYSTEM] Starting bot polling with all handlers...")
    
    loop.run_until_complete(application.initialize())
    loop.run_until_complete(application.start())
    loop.run_until_complete(application.updater.start_polling())
    
    # إبقاء البوت مستيقظاً بشكل دائم
    while True:
        loop.run_until_complete(asyncio.sleep(3600))

# السطر الأخير لتشغيل المنظومة كاملة فوراً
start_all()
