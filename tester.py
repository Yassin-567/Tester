import telegram
from telegram.ext import Updater, MessageHandler, Filters

def reply(update, context):
    message = update.message.text
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text="successfully connected")

# Replace YOUR_TOKEN with your actual bot token
updater = Updater(token='6386130136:AAEsVZqx0eRWUE3x9HlXxM8WzutfeJD_SoA', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text, reply))
updater.start_polling()