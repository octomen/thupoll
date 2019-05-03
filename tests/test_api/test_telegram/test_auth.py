import pytest

from thupoll.blueprints.telegram.auth import AuthAdapter
from thupoll import models as m


@pytest.fixture
def auth(faker, db_session):
    return AuthAdapter(db_session, faker.random.randrange(100))


@pytest.mark.filterwarnings("ignore")
def test_exist_user(auth, db_session, people):
    assert not auth.exist_user(666)
    assert auth.exist_user(people.telegram_login)


@pytest.mark.filterwarnings("ignore")
def test_generate_token(auth, db_session, people):
    token = auth.generate_token(people.telegram_login)

    assert token is not None
    assert db_session.query(m.Token).filter(
        m.Token.value == token).count() == 1
    assert db_session.query(m.Token).filter(
        m.Token.people_id == people.id).count() == 1


@pytest.mark.filterwarnings("ignore")
def test_generate_token_twice__recreate_token(auth, db_session, people):
    token1 = auth.generate_token(people.telegram_login)
    assert db_session.query(m.Token).filter(
        m.Token.people_id == people.id).one().value == token1
    token2 = auth.generate_token(people.telegram_login)
    assert db_session.query(m.Token).filter(
        m.Token.people_id == people.id).one().value == token2

    assert token1 != token2
