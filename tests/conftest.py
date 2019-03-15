import pytest
from wsgi_intercept.interceptor import RequestsInterceptor

from thupoll.app_factory import init_app
from thupoll.models import db
from thupoll.settings import env


@pytest.fixture
def app():
    app_ = init_app(db_url=env.db_url)
    db.drop_all()
    db.create_all()
    yield app_
    db.drop_all()


@pytest.fixture
def service(app):
    app.debug = app.testing = True
    with RequestsInterceptor(lambda: app) as url:
        with app.app_context():
            yield url


@pytest.fixture
def db_session(app):
    db.create_all()
    yield db.session
    db.session.close()
