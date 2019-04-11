from thupoll import models as md
from tests.factories import Factory


def test_connection(db_session):
    db_session.execute('SELECT 1;')


def test_sort_poll(db_session, faker):
    for _ in range(faker.random.randint(10, 20)):
        Factory.poll()

    dates = [
        (poll.expire_date, poll.meet_date)
        for poll in db_session.query(md.Poll).all()
    ]
    assert dates == sorted(dates)
