import pytest
import telegram
from unittest.mock import Mock

from thupoll import models as md
from thupoll.blueprints.telegram.handler import InviteHandler
from thupoll.blueprints.telegram.utils import generate_invite_link


@pytest.fixture("function")
def handler(faker):
    return InviteHandler(faker.url(), faker.pyint())


def test_not_exist_user(faker, handler):
    user_id = faker.pyint()
    update, adapter, bot = Mock(), Mock(), Mock()

    adapter.exist_user.return_value = False
    update.message.from_user.id = user_id
    update.message.chat.type = telegram.Chat.PRIVATE

    handler.invite(bot, update, adapter=adapter)
    adapter.exist_user.assert_called_once_with(user_id)
    update.message.reply_text.assert_called_once_with(handler.ERROR_MESSAGE)


def test_generate_invite_link(handler, faker):

    update, adapter, bot = Mock(), Mock(), Mock()
    url = handler.url
    token = faker.uuid4()

    update.message.from_user.full_name = faker.first_name()
    update.message.chat.type = telegram.Chat.PRIVATE

    adapter.exist_user.return_value = True
    adapter.generate_token.return_value = token

    handler.invite(bot, update, adapter=adapter)
    bot.send_message.assert_called_once_with(
        chat_id=update.message.chat_id,
        text=handler.LINK_TEMPLATE.format(
            name=update.message.from_user.full_name,
            link=generate_invite_link(url, token)
        ),
        parse_mode=telegram.ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )


@pytest.mark.parametrize('chat_type', (
    telegram.Chat.CHANNEL,
    telegram.Chat.GROUP,
    telegram.Chat.SUPERGROUP,
))
def test_reject_invate_from_non_private_chat(
    handler, people, db_session, chat_type,
):
    update, bot = Mock(), Mock()

    update.message.chat.type = chat_type
    update.message.from_user.id = people.telegram_login

    handler.invite(bot, update)
    update.message.reply_text.assert_called_once_with(
        InviteHandler.GROUP_ANSWER
    )

    assert not db_session.query(md.Token).count()
