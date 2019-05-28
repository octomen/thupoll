import datetime
import pytest
import random
from functools import partial
from freezegun import freeze_time

from thupoll.app_factory import init_app
from thupoll.components import Components
from thupoll.models import (
    db, freeze_tables, People, Role, Theme, Session, Token, Poll,
    ThemePoll, Namespace, PeopleNamespace,
)
from thupoll.settings import env


@pytest.fixture(scope='session', autouse=True)
def now():
    _now = datetime.datetime.now()
    with freeze_time(_now):
        yield _now


@pytest.fixture
def app():
    app_ = init_app(db_url=env.db_url)
    app_.debug = app_.testing = True
    with app_.app_context():
        yield app_


@pytest.fixture
def client(app):
    yield app.test_client()


def _headers(session):
    return {'Authentication': session.value}


@pytest.fixture
def user_headers(user_session):
    return _headers(user_session)


@pytest.fixture
def admin_headers(admin_session):
    return _headers(admin_session)


@pytest.fixture
def headers_factory():
    return _headers


@pytest.fixture(scope='function', autouse=True)
def truncate(db_session):
    for table in db.metadata.tables:
        if table not in freeze_tables:
            db.engine.execute('TRUNCATE TABLE {} CASCADE'.format(table))


@pytest.fixture
def db_session(app):
    yield db.session
    db.session.close()


##############
# components #
##############


# @containers.override(Components)
# class TestComponents(containers.DeclarativeContainer):
#     telegram_bot = providers.Singleton(Mock)


@pytest.fixture
def telegram_bot():
    return Components.telegram_bot()


###########
# objects #
###########


def _create_people(session, faker):
    people = People(
        role_id=Role.INHABITANT,
        telegram_login=random.randint(10000, 99999),
        name=faker.name(),
    )
    session.add(people)
    session.commit()
    return people


@pytest.fixture(scope='function')
def people(db_session, faker):
    return _create_people(db_session, faker)


@pytest.fixture(scope='function')
def people_factory(db_session, faker):
    return partial(_create_people, session=db_session, faker=faker)


@pytest.fixture(scope='function')
def admin(db_session, faker):
    people = People(
        role_id=Role.OCTOPUS,
        telegram_login=random.randint(10000, 99999),
        name=faker.name(),
    )
    db_session.add(people)
    db_session.commit()
    yield people


@pytest.fixture
def token(db_session, people: People):
    token = Token(
        people=people,
        people_id=people.id,
        expire=datetime.datetime.now() + datetime.timedelta(days=1),
    )
    db_session.add(token)
    db_session.commit()
    yield token


def _session(db_session, people: People):
    session = Session(people=people, people_id=people.id)
    db_session.add(session)
    db_session.commit()
    return session


@pytest.fixture(scope='function')
def session_factory(db_session):
    return partial(_session, db_session=db_session)


@pytest.fixture(scope='function')
def user_session(db_session, people: People):
    return _session(db_session, people=people)


@pytest.fixture(scope='function')
def admin_session(db_session, admin: People):
    return _session(db_session, people=admin)


@pytest.fixture(scope='function')
def theme(db_session, faker, peoplenamespace):
    theme = Theme(
        title=faker.text(max_nb_chars=50),
        description=faker.text(max_nb_chars=50),
        author_id=peoplenamespace.people_id,
        reporter_id=peoplenamespace.people_id,
        namespace_code=peoplenamespace.namespace_code,
    )
    db_session.add(theme)
    db_session.commit()
    yield theme


@pytest.fixture(scope='function')
def namespace(db_session, faker) -> Namespace:
    obj = Namespace(
        code=faker.text(max_nb_chars=50),
        name=faker.text(max_nb_chars=50),
        telegram_chat_id=random.randint(-10000, 0),
    )
    db_session.add(obj)
    db_session.commit()
    yield obj


@pytest.fixture(scope='function')
def peoplenamespace(db_session, people, namespace) -> PeopleNamespace:
    obj = PeopleNamespace(
        people_id=people.id,
        namespace_code=namespace.code,
    )
    db_session.add(obj)
    db_session.commit()
    yield obj


@pytest.fixture(scope='function')
def poll(db_session, peoplenamespace):
    obj = Poll(
        expire_date=datetime.datetime.now() + datetime.timedelta(days=20),
        meet_date=datetime.datetime.now() + datetime.timedelta(days=20),
        namespace_code=peoplenamespace.namespace_code,
    )
    db_session.add(obj)
    db_session.commit()
    yield obj


@pytest.fixture(scope='function')
def themepoll(db_session, theme, poll):
    obj = ThemePoll(
        theme_id=theme.id, poll_id=poll.id, order_no=random.randint(1, 100))
    db_session.add(obj)
    db_session.commit()
    yield obj
