import telegram
from telegram.ext import BaseFilter


class MemberJoinFilter(BaseFilter):
    def filter(self, message: telegram.Message):
        return bool(message.new_chat_members)


class MemberLeftFilter(BaseFilter):
    def filter(self, message: telegram.Message):
        return bool(message.left_chat_member)
