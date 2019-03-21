import datetime
import pytest
from freezegun import freeze_time

from thupoll.app_factory import init_app
from thupoll.models import db, freeze_tables, People, Role, Theme
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


@pytest.fixture(scope='function', autouse=True)
def truncate(db_session):
    for table in db.metadata.tables:
        if table not in freeze_tables:
            db.engine.execute('TRUNCATE TABLE {} CASCADE'.format(table))


@pytest.fixture
def db_session(app):
    db.create_all()
    yield db.session
    db.session.close()


###########
# objects #
###########


@pytest.fixture(scope='function')
def people(db_session, faker):
    people = People(
        role_id=Role.OCTOPUS,
        telegram_login=faker.name(),
    )
    db_session.add(people)
    db_session.commit()
    yield people


@pytest.fixture(scope='function')
def theme(db_session, faker, people: People):
    theme = Theme(
        title=faker.text(max_nb_chars=50),
        description=faker.text(max_nb_chars=50),
        author_id=people.id,
        reporter_id=people.id,
    )
    db_session.add(theme)
    db_session.commit()
    yield theme
