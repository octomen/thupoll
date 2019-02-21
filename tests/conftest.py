import pytest
from server.app_factory import init_app


@pytest.fixture
def initialize():
    init_app()
