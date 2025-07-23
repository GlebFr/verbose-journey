
from telegram import ForceReply
from telegram.txt import Application, CommandHandler, ContextTypes, MessageHandler, filters

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def echo (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.replay_text(update.message.txt)


def main():
    app = Application.builder().token("TOKEN").build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


main()
    