import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    try:
        response = model.generate_content(user_msg)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("မေးခွန်းထပ်ပို့ပါ၊ ပြဿနာတစ်ခုဖြစ်သွားသည်။")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
app.run_polling()