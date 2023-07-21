import telegram
from telegram.ext import Updater, MessageHandler, Filters
from flask import Flask, request

app = Flask(__name__)

def reply(update, context):
    message = update.message.text
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text="successfully connected")

@app.route('/webhook', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('UTF-8')
    update = telegram.Update.de_json(json_string)
    dispatcher.process_update(update)
    return 'OK'

# Replace YOUR_TOKEN with your actual bot token
updater = Updater(token='6266356161:AAFnimQxhusYlKHcKH2l7YSRzp8Vgrb8tUk', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text, reply))
updater.start_polling()
