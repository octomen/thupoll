from queue import Queue
from typing import Callable

from telegram import Update, ext
from telegram.ext import BaseFilter

from thupoll.telega import logger


class TelegramHook:
    def __init__(self, bot):
        self.bot = bot
        self.dispatcher = ext.Dispatcher(
            self.bot,
            Queue()
        )

    def mount_command(self, tag: str, handler: Callable):
        self.dispatcher.add_handler(
            ext.CommandHandler(tag, handler, pass_chat_data=True))

    def mount_message_handler(self, filters: BaseFilter, handler: Callable):
        self.dispatcher.add_handler(
            ext.MessageHandler(filters=filters, callback=handler))

    def handle(self, update):
        """
        Dispatch update
        :param update: update received from the telegram
            expect request.json or object after json.load
        """
        logger.info(update)
        update = Update.de_json(update, self.bot)

        self.dispatcher.process_update(update)
