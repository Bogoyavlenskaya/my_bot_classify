from model import ClassPredictor
from telegram_token import token
import torch
import numpy as np
from PIL import Image
from io import BytesIO
import telebot
from telegram.ext import CommandHandler


model = ClassPredictor()

def start(bot, update):
    #приветственное сообщение
    bot.sendMessage(chat_id=update.message.chat_id, text="Hi! I am a bot that will help you identify a flower =^_^=\n \
If you have questions write: /help")

def help(bot, update):
    #руководство по боту
    bot.sendMessage(chat_id=update.message.chat_id, text="Just send me a photo of a flower)\n \
I know the following flowers: \n daisy \n dandelion \n rose \n sunflower \n tulip")


def send_prediction_on_photo(bot, update):
    chat_id = update.message.chat_id
    print("Got image from {}".format(chat_id))

    # получаем информацию о картинке
    image_info = update.message.photo[-1]
    image_file = bot.get_file(image_info)
    image_stream = BytesIO()
    image_file.download(out=image_stream)

    class_ = model.predict(image_stream)

    # теперь отправим результат
    update.message.reply_text("I know this flower. This is a {}!".format(class_))
    print("Sent Answer to user, predicted: {}".format(class_))


if __name__ == '__main__':
    from telegram.ext import Updater, MessageHandler, Filters
    import logging

    # Включим самый базовый логгинг, чтобы видеть сообщения об ошибках
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    # используем прокси, так как без него у меня ничего не работало(
    REQUEST_KWARGS={
    'proxy_url': 'http://51.79.31.19:8080'
    }
    updater = Updater(token=token, request_kwargs=REQUEST_KWARGS)
    start_handler = CommandHandler('start', start)
    updater.dispatcher.add_handler(start_handler)
    help_handler = CommandHandler('help', help)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, send_prediction_on_photo))
    updater.start_polling()
