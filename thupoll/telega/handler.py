import telegram  # noqa: F401
from telegram.chat import Chat

from thupoll import validators
from thupoll.fronturl import FrontUrl
from thupoll.models import db
from thupoll.telega import logger
from thupoll.telega.auth import AuthAdapter, RegistrationAdapter


class InviteHandler:
    """Handler for generate token and link to "thupoll"."""

    GROUP_ANSWER = "Для получения приглашения напишите боту личное сообщение."
    ERROR_MESSAGE = (
        "Вы не являетесь зарегистрированным пользователем."
        "Обратитесь к администратору."
    )
    LINK_TEMPLATE = "Привет, {name}! Твоя [ссылка]({link})"

    def __init__(self, token_ttl_days):
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
                link=FrontUrl.root(token),
            ),
            parse_mode=telegram.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )


class ChatMembersHandler:
    WELCOME = ('Welcome! Send me private message for getting access '
               'to our beautiful poll service.')
    GOODBYE = 'Goodbye, {name}!'

    def on_join(self, bot, update, adapter=None):
        adapter = adapter or RegistrationAdapter(db.session)
        message = update.message  # type: telegram.Message

        logger.info(
            '%s joined to %s', message.new_chat_members, message.chat_id)

        try:
            namespace = validators.namespace_chat_id(
                chat_id=message.chat_id, must_exists=True,
            )
        except validators.ValidationError:
            return

        peoplenamespace_gen = (
            adapter.bind_inhabitant(
                name=user.username, telegram_login=user.id,
                namespace=namespace,
            )
            for user in message.new_chat_members
            if not user.is_bot
        )
        new_peoplenamespace = tuple(pn for pn in peoplenamespace_gen if pn)
        if not new_peoplenamespace:
            return

        db.session.commit()
        bot.send_message(
            chat_id=message.chat_id,
            text=self.WELCOME,
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_to_message_id=message.message_id,
        )
        logger.info(
            'added %s members to %s', len(new_peoplenamespace), namespace.code)

    def on_left(self, bot, update, adapter=None):
        adapter = adapter or RegistrationAdapter(db.session)
        message = update.message  # type: telegram.Message

        try:
            namespace = validators.namespace_chat_id(
                chat_id=message.chat_id, must_exists=True,
            )
        except validators.ValidationError:
            return

        user = message.left_chat_member  # type: telegram.User

        if adapter.unbind_people(namespace=namespace, telegram_login=user.id):
            bot.send_message(
                chat_id=message.chat_id,
                text=self.GOODBYE.format(name=user.first_name),
                parse_mode=telegram.ParseMode.MARKDOWN,
            )
            db.session.commit()
            logger.info('remove %s from %s', user.username, namespace.code)
