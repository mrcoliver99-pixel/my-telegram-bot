import logging
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# إعدادات تسجيل الأخطاء لضمان أعلى مستوى من الاستقرار
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ==========================================================
# ⚙️ [ قسم الإعدادات والرسائل - اكتب بياناتك هنا ] ⚙️
# ==========================================================
BOT_TOKEN = "8721360021:AAGW_ZRnONtURyf9HUjhQsZRhQuSyriAbHA"
ADMIN_CHAT_ID = "6506150207" 
# 1️⃣ اكتب رسالتك الترحيبية الطويلة جداً هنا (التي تظهر بعد ضغط Start):
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

# 2️⃣ اكتب هنا الرسالة التي تظهر للمستخدم بعد أن يرسل سؤاله:
THANK_YOU_MESSAGE = """
شكراً على اهتمامك بالفريق، نقدر وقتك الثمين، وسيتم الرد عليك من قبل رئيس الفريق بأسرع وقت ممكن، شاكرين تفهمك.🪻
"""
# ==========================================================

# 🌐 نظام السيرفر المصغر المتوافق 100% مع السيرفرات الخارجية ومنع النوم
app = Flask('')

@app.route('/')
def home():
    return "Bot is Alive and Flying! 🚀"

def run_flask():
    from werkzeug.serving import run_simple
    # تشغيل السيرفر بأعلى كفاءة تدعم الرفع أونلاين
    run_simple('0.0.0.0', 8080, app, use_reloader=False, use_debugger=False, threaded=True)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)

async def handle_incoming_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    # 👤 نظام الرد المباشر والنظيف للأدمن (بدون عناوين)
    if str(user_id) == str(ADMIN_CHAT_ID):
        if update.message.reply_to_message:
            try:
                reply_markup = update.message.reply_to_message.reply_markup
                button_url = reply_markup.inline_keyboard[0][0].url
                original_user_id = button_url.split('id=')[1]
                
                await context.bot.send_message(chat_id=original_user_id, text=update.message.text)
                await update.message.reply_text("✅ تم إرسال ردك بنجاح.")
            except Exception:
                await update.message.reply_text("❌ عذراً، لا يمكن الرد على هذه الرسالة.")
        return

    # 📥 نظام استقبال رسائل المستخدمين وتحويلها للأدمن
    user_name = user.first_name
    username = f"@{user.username}" if user.username else "لا يوجد يوزرنيم"
    message_text = update.message.text

    admin_notification_text = (
        f"📩 رسالة جديدة وصلت للبوت!**\n\n"
        f"👤 **الاسم: {user_name}\n"
        f"🆔 الآيدي: `{user_id}`\n"
        f"🏷 اليوزرنيم: {username}\n"
        f"✍️ **الرسالة:**\n{message_text}"
    )

    keyboard = [[InlineKeyboardButton(text=f"👤 فتح حساب: {user_name}", url=f"tg://user?id={user_id}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_notification_text, reply_markup=reply_markup)
    await update.message.reply_text(THANK_YOU_MESSAGE)

def main():
    # تشغيل خيط الويب (Thread) بشكل منفصل تماماً لمنع أي تعليق
    threading.Thread(target=run_flask, daemon=True).start()
    
    print("🤖 البوت يعمل الآن بنجاح استقراطي تام وجاهز للكمبيوتر أو الرفع...")
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_incoming_messages))
    application.run_polling()

if __name__ == '__main__':
