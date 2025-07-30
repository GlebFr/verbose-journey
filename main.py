from telegram import Update
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import os

load_dotenv()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text('hi my')


async def echo (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)


def main():
    app = Application.builder().token(os.getenv('BOT_TOKEN')).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


main()
    