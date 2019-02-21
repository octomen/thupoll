import pytest
from server.app_factory import init_app
from server.models import db


@pytest.fixture
def initialize():
    init_app()
    db.drop_all()  # TODO пофиксить это дерьмо
    db.create_all()
