from thupoll.blueprints.telegram.hook import TelegramHook
from thupoll.blueprints.telegram.handler import (
    InviteHandler, ChatMembersHandler)
from thupoll.blueprints.telegram.filters import (
    MemberJoinFilter, MemberLeftFilter)
from thupoll.settings import env


def mount(hook: TelegramHook):
    """Mount handlers to hook"""
    invite_handler = InviteHandler(env.thupoll_url, env("TOKEN_TTL_DAYS", 10))
    hook.mount_command("invite", invite_handler.invite)
    hook.mount_command("start", invite_handler.invite)

    members_handler = ChatMembersHandler()
    hook.mount_message_handler(MemberJoinFilter(), members_handler.on_join)
    hook.mount_message_handler(MemberLeftFilter(), members_handler.on_left)
