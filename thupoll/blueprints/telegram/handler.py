import telegram  # noqa: F401
from telegram.chat import Chat
from telegram.ext import BaseFilter

from thupoll.blueprints.telegram import logger
from thupoll.blueprints.telegram.auth import AuthAdapter, TokenAdapter
from thupoll.blueprints.telegram.utils import generate_invite_link
from thupoll.models import db


class InviteHandler:
    """Handler for generate token and link to "thupoll"."""

    GROUP_ANSWER = "Для получения приглашения напишите боту личное сообщение."
    ERROR_MESSAGE = (
        "Вы не являетесь зарегистрированным пользователем."
        "Обратитесь к администратору."
    )
    LINK_TEMPLATE = "Привет, {name}! Твоя [ссылка]({link})"

    def __init__(self, url, token_ttl_days):
        self.url = url
        self.token_ttl_days = token_ttl_days

    def invite(self, bot, update, adapter=None, **kw):
        """
        Generate link if user is registered else send error massage
        :param bot: for support interface of library "telegram"
        :param update: telegram.Update
        :param adapter: over
        """

        adapter = adapter or TokenAdapter(db.session, self.token_ttl_days)
        message = update.message  # type: telegram.Message
        user = message.from_user  # type: telegram.User

        if message.chat.type != Chat.PRIVATE:
            logger.info("Message from channel or group %s", message.chat_id)
            message.reply_text(self.GROUP_ANSWER)
            return

        if not adapter.exist_user(user.id):
            logger.info("Unregistered user %s", user.id)
            message.reply_text(self.ERROR_MESSAGE)
            return

        token = adapter.generate_token(user.id)
        db.session.commit()

        logger.info("Generate link for user %s (%s)", user.id, user.full_name)
        bot.send_message(
            chat_id=message.chat_id,
            text=self.LINK_TEMPLATE.format(
                name=user.full_name,
                link=generate_invite_link(self.url, token),
            ),
            parse_mode=telegram.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )


class ChatMembersHandler:
    WELCOME = ('Welcome, {name}! Send me private message for getting access '
               'to our beautiful poll service.')
    GOODBYE = 'Goodbye, {name}!'

    def __init__(self, chats):
        self.chats = chats

    def on_join(self, bot, update, adapter=None):
        adapter = adapter or AuthAdapter(db.session)
        message = update.message  # type: telegram.Message
        if message.chat_id not in self.chats:
            return

        for user in message.new_chat_members:
            if not adapter.exist_user(user.username):
                bot.send_message(
                    chat_id=message.chat_id,
                    text=self.WELCOME.format(name=user.full_name),
                    parse_mode=telegram.ParseMode.MARKDOWN,
                )

    def on_left(self, bot, update, adapter=None):
        adapter = adapter or AuthAdapter(db.session)
        message = update.message  # type: telegram.Message
        if message.chat_id not in self.chats:
            return

        user = message.left_chat_member

        if adapter.exist_user(user.username):
            bot.send_message(
                chat_id=message.chat_id,
                text=self.GOODBYE.format(name=user.full_name),
                parse_mode=telegram.ParseMode.MARKDOWN,
            )


class MemberJoinFilter(BaseFilter):
    def filter(self, message: telegram.Message):
        return bool(message.new_chat_members)


class MemberLeftFilter(BaseFilter):
    def filter(self, message: telegram.Message):
        return bool(message.left_chat_member)


join_filter = MemberJoinFilter()
left_filter = MemberJoinFilter()
