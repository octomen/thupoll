import datetime
import pytest
from freezegun import freeze_time
from unittest.mock import Mock

from thupoll.app_factory import init_app
from thupoll.components import Components
from thupoll.settings import env
from thupoll.utils import di


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


##############
# components #
##############


@Components.override
class TestComponents(di.Container):
    telegram_bot = di.Singleton(Mock)


@pytest.fixture
def telegram_bot():
    return Components.telegram_bot()
