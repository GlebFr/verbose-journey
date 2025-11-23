
import logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
import os
CHOOSE_TYPE_HANDLER, CHOOSE_TYPE, GET_NOTIFICATION_NAME, NOTIFICATION_SEND_TIME, FINAL_MESSAGE = range(5)
load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Начнем", callback_data="1"),
            ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Привет, этот бот поможет тебе делать заметки, хочешь ли ты начать?", reply_markup=reply_markup)
    return CHOOSE_TYPE


async def choose_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)
    keyboard = [
        [
            InlineKeyboardButton("однoразавая", callback_data="2_1"),
            InlineKeyboardButton("повторна", callback_data="2_2"),
            ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("ТЫ можешь выбрать два варианта, ты можешь создать однна разовую напоминалку или многоразовую", reply_markup=reply_markup)
    return CHOOSE_TYPE_HANDLER



async def choose_type_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)
    print(query.data) # так мы получаем данные прошлого Keyboard
    if query.data == '2_1':
        await query.message.reply_text('Введите одноразовое сообщение')
        return GET_NOTIFICATION_NAME

    elif query.data == '2_2':
        await query.message.reply_text('Введите многоразовое сообщение')
        return GET_NOTIFICATION_NAME

    # keyboard = [
    #     [
    #         InlineKeyboardButton("однаразавая", callback_data="3_1"),\
    #         InlineKeyboardButton("повторна", callback_data="3_2"),
    #         ],
    # ]
    # reply_markup = InlineKeyboardMarkup(keyboard)
    # await query.message.reply_text("Введи напоминание", reply_markup=reply_markup)
    # return NOTIFICATION_SEND_TIME



async def get_notification_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['notification_text'] = update.message.text
    await update.message.reply_text(f'ваше напоминание сохранeно: {update.message.text} спасибо.\n теперь напишите время отправки напоминания в формате дд.мм.гггг')
    return NOTIFICATION_SEND_TIME


def check_data(message): # данна функция принемает обЪект message 
    try:
        user_data = datetime.strptime(message, '%d.%m.%Y').date() #  провиряет на д.м.г
        now_data = datetime.now().date() # берет время с компьютера
        if user_data > now_data: # сравнивает дату и дату компа
            return True
        else:
            return False


    
    except ValueError:
        return False


async def notifaction_send_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    notification_text = context.user_data['notification_text']
    if check_data(update.message.text):
        await update.message.reply_text(f'ваше напоминание {notification_text}, будет отправлено {update.message.text}')
    else:
        await update.message.reply_text(f'Пожалуйста введите в формате дд.мм.гггг')
        return NOTIFICATION_SEND_TIME
    keyboard = [
        [
            InlineKeyboardButton("Начнем", callback_data="1"),
            ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Привет, этот бот поможет тебе делать заметки, хочешь ли ты начать?", reply_markup=reply_markup)
    print(context.user_data)
    return CHOOSE_TYPE












def main():
    TOKEN = os.getenv('BOT_TOKEN')
    app = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSE_TYPE: [
                CallbackQueryHandler(choose_type, pattern="^" + str('1') + "$"),
            ],
            CHOOSE_TYPE_HANDLER: [
                CallbackQueryHandler(choose_type_handler, pattern="^2.*"),
            ],
            GET_NOTIFICATION_NAME:[
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_notification_name),
               ], 
            NOTIFICATION_SEND_TIME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, notifaction_send_time),
            ],
            # FINAL_MESSAGE: [
            #     CallbackQueryHandler(start_over, pattern="^" + str(ONE) + "$"),
            # ],
            },
        fallbacks=[CommandHandler("start", start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    app.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    app.run_polling(allowed_updates=Update.ALL_TYPES)






main()
    