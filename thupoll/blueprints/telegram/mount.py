from thupoll.blueprints.telegram.hook import TelegramHook
from thupoll.blueprints.telegram.handler import InviteHandler
from thupoll.settings import env


def mount(hook: TelegramHook):
    """Mount handlers to hook"""
    invite_handler = InviteHandler(
        env.thupoll_url, env("TOKEN_TTL_DAYS", 10))

    hook.mount_command("invite", invite_handler.invite)
