import logging
import json
import copy
from datetime import datetime
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, ConversationHandler, filters
)
from bot.states import States
from bot.keyboards import choice_keyboard, image_keyboard, type_keyboard
from config.settings import (
    TELEGRAM_BOT_TOKEN, EXTERNAL_API_SAVE_URL, EXTERNAL_API_CREATE_URL
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NEWS_TYPES = [
    {'label': 'MARKET MOVES', 'key': 'type_market_moves'},
    {'label': 'FOCUS', 'key': 'type_focus'},
    {'label': 'INFO', 'key': 'type_info'},
    {'label': 'WEEK AHEAD', 'key': 'type_week_ahead'}
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отправьте сообщение для обработки.")

async def incoming_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # context.user_data['message'] = update.effective_message.to_dict()
    context.user_data['message'] = json.loads(update.message.to_json())
    await update.message.reply_text(
        "Выберите действие:", reply_markup=choice_keyboard()
    )
    return States.WAITING_CHOICE

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    await update.callback_query.answer()
    if data == 'cancel':
        await update.callback_query.edit_message_text("Отменено.")
        return ConversationHandler.END
    if data == 'save':
        payload = context.user_data['message']
        requests.post(EXTERNAL_API_SAVE_URL, json=payload)
        await update.callback_query.edit_message_text("Сохранено в базу.")
        return ConversationHandler.END
    # create news
    await update.callback_query.edit_message_text(
        "Использовать картинку?", reply_markup=image_keyboard()
    )
    return States.WAITING_IMAGE_CHOICE

async def handle_image_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    await update.callback_query.answer()
    if data == 'cancel':
        await update.callback_query.edit_message_text("Отменено.")
        return ConversationHandler.END
    context.user_data['use_image'] = (data == 'use_image')
    await update.callback_query.edit_message_text(
        "Выберите тип новости:", reply_markup=type_keyboard(NEWS_TYPES)
    )
    return States.WAITING_NEWS_TYPE

async def handle_type_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    await update.callback_query.answer()
    if data == 'cancel':
        await update.callback_query.edit_message_text("Отменено.")
        return ConversationHandler.END
    # message = context.user_data['message']
    message = context.user_data.get('message', {})
    payload = copy.deepcopy(message)
    # payload = {
    #     'message_id': message.get('message_id'),
    #     'text': message.get('text') or message.get('caption'),
    #     'use_image': context.user_data['use_image'],
    #     'news_type': data,
    #     'timestamp': message.get('date')
    # }
    payload.update({
        'use_image': context.user_data.get('use_image', False),
        'news_type': data,
        'timestamp': datetime.utcnow().isoformat()
    })

    requests.post(EXTERNAL_API_CREATE_URL, json=payload)
    await update.callback_query.edit_message_text("Новость отправлена на создание.")
    return ConversationHandler.END

def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[MessageHandler(filters.ALL, incoming_message)],
        states={
            States.WAITING_CHOICE: [
                CallbackQueryHandler(handle_choice)
            ],
            States.WAITING_IMAGE_CHOICE: [
                CallbackQueryHandler(handle_image_choice)
            ],
            States.WAITING_NEWS_TYPE: [
                CallbackQueryHandler(handle_type_choice)
            ],
        },
        fallbacks=[CommandHandler('cancel', lambda u,c: u.message.reply_text("Отменено.") or ConversationHandler.END)]
    )

    app.add_handler(CommandHandler('start', start))
    app.add_handler(conv)

    app.run_polling()
