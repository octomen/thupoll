import telegram  # noqa: F401
from telegram.chat import Chat

from thupoll.blueprints.telegram import logger
from thupoll.blueprints.telegram.auth import AuthAdapter
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

        adapter = adapter or AuthAdapter(db.session, self.token_ttl_days)
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
