from queue import Queue
from typing import Callable

from telegram import Bot, Update, ext
from telegram.utils.request import Request

from thupoll.blueprints.telegram import logger


class TelegramHook:
    """Telegram hook"""

    def __init__(self, token, proxy=None):

        # self.handler = Handler()

        request = None
        if proxy:
            request = Request(proxy_url=proxy)

        self.bot = Bot(
            token,
            request=request
        )
        self.dispatcher = ext.Dispatcher(
            self.bot,
            Queue()
        )

    def mount_command(self, tag: str, handler: Callable):
        """Mount command handler to telegram hook"""
        self.dispatcher.add_handler(
            ext.CommandHandler(tag, handler, pass_chat_data=True))

    def handle(self, update):
        """
        Dispatch update
        :param update: update received from the telegram
            expect request.json or object after json.load
        """
        logger.info(update)
        update = Update.de_json(update, self.bot)

        self.dispatcher.process_update(update)
