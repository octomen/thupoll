from telegram import Bot
from telegram.utils.request import Request

from thupoll.settings import env
from thupoll.telega.mount import mount
from thupoll.telega.hook import TelegramHook
from thupoll.utils import di


def _telegram_bot_factory():
    token = env.bot_telegram_token
    request = None
    if env.proxy_url:
        request = Request(proxy_url=env.proxy_url)
    return Bot(token, request=request)


class Components(di.Container):
    telegram_bot = di.Singleton(_telegram_bot_factory)
    telegram_hook = di.Singleton(
        lambda: mount(TelegramHook(bot=Components.telegram_bot())),
        bot=telegram_bot
    )
