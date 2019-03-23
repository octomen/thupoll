import pytest
from unittest.mock import Mock

from thupoll.blueprints.telegram.handler import InviteHandler
from thupoll.blueprints.telegram.utils import generate_invite_link


@pytest.fixture("function")
def handler(faker):
    return InviteHandler(faker.url(), faker.pyint())


def test_not_exist_user(faker, handler):
    user_id = faker.pyint()
    update, adapter = Mock(), Mock()

    adapter.exist_user.return_value = False
    update.message.from_user.id = user_id

    handler.invite(None, update, adapter=adapter)
    adapter.exist_user.assert_called_once_with(user_id)
    update.message.reply_text.assert_called_once_with(handler.ERROR_MESSAGE)


def test_generate_invite_link(handler, faker):

    update, adapter = Mock(), Mock()
    url = handler.url
    token = faker.uuid4()

    update.message.from_user.full_name = faker.first_name()

    adapter.exist_user.return_value = True
    adapter.generate_token.return_value = token

    handler.invite(None, update, adapter=adapter)
    update.message.reply_text.assert_called_once_with(
        handler.LINK_TEMPLATE.format(
            name=update.message.from_user.full_name,
            link=generate_invite_link(url, token)
        ))