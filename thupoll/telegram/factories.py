from telegram import Bot
from telegram.utils.request import Request

from thupoll.settings import env
from thupoll.telegram.mount import mount
from thupoll.telegram.hook import TelegramHook


def telegram_bot_factory():
    token = env.bot_telegram_token
    request = None
    if env.bot_proxy_url:
        request = Request(proxy_url=env.bot_proxy_url)
    return Bot(token, request=request)


def telegram_hook_factory(bot):
    return mount(TelegramHook(bot=bot))
