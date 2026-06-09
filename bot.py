import os
import asyncio
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

client = genai.Client(api_key=GEMINI_KEY)

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_msg
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("မေးခွန်းထပ်ပို့ပါ၊ ပြဿနာတစ်ခုဖြစ်သွားသည်။")

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    async with app:
        await app.start()
        await app.updater.start_polling()
        await asyncio.sleep(float("inf"))
        await app.updater.stop()
        await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
