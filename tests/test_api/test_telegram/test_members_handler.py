from functools import partial

import pytest
import telegram
from unittest.mock import Mock

from thupoll import models as md
from thupoll.blueprints.telegram.auth import RegistrationAdapter
from thupoll.blueprints.telegram.handler import ChatMembersHandler


@pytest.fixture
def handler(faker) -> ChatMembersHandler:
    return ChatMembersHandler()


@pytest.fixture
def adapter(db_session):
    return RegistrationAdapter(session=db_session)


@pytest.fixture
def bot():
    return Mock()


def _new_chat_member(faker, username=None, user_id=None, is_bot=False):
    member = Mock()
    member.id = user_id or faker.pyint()
    member.first_name = faker.name()
    member.is_bot = is_bot
    member.username = username or faker.first_name()
    return member


@pytest.fixture
def new_chat_member(faker):
    return partial(_new_chat_member, faker)


def _join_update(faker, member_or_members, chat_id):
    if not isinstance(member_or_members, list):
        member_or_members = [member_or_members]
    update = Mock()
    update.message.message_id = faker.pyint()
    update.message.chat_id = chat_id
    update.message.new_chat_members = member_or_members
    return update


@pytest.fixture
def join_update(faker):
    return partial(_join_update, faker)


def _left_update(faker, member, chat_id):
    update = Mock()
    update.message.message_id = faker.pyint()
    update.message.chat_id = chat_id
    update.message.left_chat_member = member
    return update


@pytest.fixture
def left_update(faker):
    return partial(_left_update, faker)


def test__do_nothing__when__bot_join_moitored_chat(
    db_session, faker, adapter, handler, new_chat_member, bot, join_update,
    namespace,
):
    assert not db_session.query(md.People).count()

    member = new_chat_member(is_bot=True)
    update = join_update(member, chat_id=namespace.telegram_chat_id)

    handler.on_join(bot, update, adapter=adapter)

    bot.send_message.assert_not_called()
    assert not db_session.query(md.People).count()


def test__create__when__unknown_user__join__monitored_chat(
    db_session, faker, adapter, handler, new_chat_member, bot, join_update,
    namespace,
):
    assert not db_session.query(md.People).count()

    member = new_chat_member()
    update = join_update(member, chat_id=namespace.telegram_chat_id)

    handler.on_join(bot, update, adapter=adapter)

    bot.send_message.assert_called_once_with(
        chat_id=update.message.chat_id,
        text=handler.WELCOME,
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_to_message_id=update.message.message_id,
    )
    people = db_session.query(md.People).one()
    assert people.role_id == md.Role.INHABITANT
    assert people.name == member.username
    assert people.telegram_login == str(member.id)

    people_namespace = db_session.query(md.PeopleNamespace).one()
    assert people_namespace.namespace_code == namespace.code
    assert people_namespace.people_id == people.id


def test__do_nothing__when__unknown_user__join__not_monitored_chat(
    db_session, faker, adapter, handler, new_chat_member, bot, join_update,
    namespace,
):
    assert not db_session.query(md.People).count()

    member = new_chat_member()
    chat_id = faker.random.randrange(10 ** 6, 10 ** 7) * (-1)
    update = join_update(member, chat_id=chat_id)

    handler.on_join(bot, update, adapter=adapter)

    bot.send_message.assert_not_called()
    assert not db_session.query(md.People).count()


def test__add_to_namespace__when__exists_user__join__monitored_chat(
    db_session, faker, adapter, handler, people, new_chat_member, bot,
    join_update, namespace,
):
    assert db_session.query(md.People).count() == 1
    assert not db_session.query(md.PeopleNamespace).count()

    member = new_chat_member(user_id=people.telegram_login)
    update = join_update(member, chat_id=namespace.telegram_chat_id)

    handler.on_join(bot, update, adapter=adapter)

    bot.send_message.assert_called_once_with(
        chat_id=update.message.chat_id,
        text=handler.WELCOME,
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_to_message_id=update.message.message_id,
    )
    assert db_session.query(md.People).count() == 1

    people_namespace = db_session.query(md.PeopleNamespace).one()
    assert people_namespace.namespace_code == namespace.code
    assert people_namespace.people_id == people.id


def test__do_nothing__when__registered_user__join__monitored_chat(
    db_session, faker, adapter, handler, new_chat_member, bot,
    join_update, peoplenamespace,
):
    assert db_session.query(md.People).count() == 1
    assert db_session.query(md.PeopleNamespace).count() == 1

    member = new_chat_member(user_id=peoplenamespace.people.telegram_login)
    update = join_update(
        member, chat_id=peoplenamespace.namespace.telegram_chat_id)

    handler.on_join(bot, update, adapter=adapter)

    bot.send_message.assert_not_called()
    assert db_session.query(md.People).count() == 1
    assert db_session.query(md.PeopleNamespace).count() == 1


def test__do_nothing__when__exists_user__join__not_monitored_chat(
    db_session, faker, adapter, handler, people, new_chat_member, bot,
    join_update, namespace,
):
    assert db_session.query(md.People).count() == 1
    assert not db_session.query(md.PeopleNamespace).count()

    member = new_chat_member(user_id=people.telegram_login)
    chat_id = faker.random.randrange(10 ** 6, 10 ** 7) * (-1)
    update = join_update(member, chat_id=chat_id)

    handler.on_join(bot, update, adapter=adapter)

    bot.send_message.assert_not_called()
    assert db_session.query(md.People).count() == 1
    assert not db_session.query(md.PeopleNamespace).count()


def test__welcome_once__when__two_users__join(
    db_session, faker, adapter, handler, new_chat_member, bot, join_update,
    namespace,
):
    assert not db_session.query(md.People).count()
    assert not db_session.query(md.PeopleNamespace).count()

    update = join_update(
        [new_chat_member(), new_chat_member()],
        chat_id=namespace.telegram_chat_id,
    )

    handler.on_join(bot, update, adapter=adapter)

    bot.send_message.assert_called_once_with(
        chat_id=update.message.chat_id,
        text=handler.WELCOME,
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_to_message_id=update.message.message_id,
    )
    assert db_session.query(md.People).count() == 2
    assert db_session.query(md.PeopleNamespace).count() == 2


def test__do_nothing__when__unknown_user__left__monitored_chat(
    db_session, faker, adapter, handler, new_chat_member, bot, left_update,
    namespace,
):
    member = new_chat_member()
    update = left_update(member, chat_id=namespace.telegram_chat_id)

    handler.on_left(bot, update, adapter=adapter)

    bot.send_message.assert_not_called()


def test__do_nothing__when__unknown_user__left__not_monitored_chat(
    db_session, faker, adapter, handler, new_chat_member, bot, left_update,
    namespace,
):
    member = new_chat_member()
    chat_id = faker.random.randrange(10 ** 6, 10 ** 7) * (-1)
    update = left_update(member, chat_id=chat_id)

    handler.on_left(bot, update, adapter=adapter)

    bot.send_message.assert_not_called()


def test__rm_peoplenamespace__when__registered_user__left__monitored_chat(
    db_session, faker, adapter, handler, new_chat_member, bot,
    left_update, peoplenamespace,
):
    assert db_session.query(md.PeopleNamespace).count() == 1

    member = new_chat_member(user_id=peoplenamespace.people.telegram_login)
    update = left_update(
        member, chat_id=peoplenamespace.namespace.telegram_chat_id)

    handler.on_left(bot, update, adapter=adapter)

    bot.send_message.assert_called_once_with(
        chat_id=update.message.chat_id,
        text=handler.GOODBYE.format(name=member.first_name),
        parse_mode=telegram.ParseMode.MARKDOWN,
    )
    assert db_session.query(md.People).count() == 1
    assert not db_session.query(md.PeopleNamespace).count()


def test__do_nothing__when_exists_user__left__not_monitored_chat(
    db_session, faker, adapter, handler, new_chat_member, bot,
    left_update, peoplenamespace,
):
    member = new_chat_member(user_id=peoplenamespace.people.telegram_login)
    chat_id = faker.random.randrange(10 ** 6, 10 ** 7) * (-1)
    update = left_update(member, chat_id=chat_id)

    handler.on_left(bot, update, adapter=adapter)

    bot.send_message.assert_not_called()
    assert db_session.query(md.PeopleNamespace).count() == 1
