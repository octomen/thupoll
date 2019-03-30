import datetime
from thupoll.models import db, Poll
from tests.utils import marshall


def get_future_datetime(delta=30):
    return datetime.datetime.now() + datetime.timedelta(days=delta)


def get_past_datetime(delta=30):
    return datetime.datetime.now() - datetime.timedelta(days=delta)


def test__marshall(poll):
    assert marshall(poll) == dict(
        id=poll.id,
        expire_date=poll.expire_date.isoformat(),
        meet_date=poll.meet_date.isoformat(),
        created=poll.created_date.isoformat(),
        updated=poll.change_date.isoformat()
    )


def test__update__403_denied_for_user(poll, client, user_headers):
    r = client.patch('/polls/{}'.format(poll.id), headers=user_headers)
    assert r.status_code == 403, r.get_json()


def test__delete__403_denied_when_not_exists(client, user_headers):
    r = client.delete('/polls/1', headers=user_headers)
    assert r.status_code == 403, r.get_json()


def test__one__404_when_not_exists(client):
    r = client.get('/polls/1')
    assert r.status_code == 404, r.get_json()


def test__one__correct(client, poll):
    r = client.get('/polls/{}'.format(poll.id))
    assert r.status_code == 200, r.get_json()
    assert r.get_json() == dict(results=marshall(poll))


def test__all__empty_when_not_exists(client):
    r = client.get('/polls')
    assert r.status_code == 200, r.get_json()
    assert r.get_json() == dict(results=[])


def test__all__one(client, poll):
    r = client.get('/polls')
    assert r.status_code == 200, r.get_json()
    assert r.get_json() == dict(results=[marshall(poll)])


def test__create__admin_correct(client, admin_headers):
    r = client.post('/polls', json=dict(
        expire_date=get_future_datetime(),
        meet_date=get_future_datetime(),
    ), headers=admin_headers)
    created = r.get_json()
    assert r.status_code == 200, created
    getted = client.get('/polls/{}'.format(
        created['results']['id'])).get_json()
    assert created == getted


def test__update__admin_correct_all_params(poll, client, admin_headers):
    new_expire_date = get_future_datetime(delta=10)
    new_meet_date = get_future_datetime(delta=14)
    r = client.patch('/polls/{}'.format(poll.id), json=dict(
        expire_date=new_expire_date,
        meet_date=new_meet_date,
    ), headers=admin_headers)
    updated = r.get_json()
    assert r.status_code == 200, updated
    assert updated['results']['expire_date'] == new_expire_date.isoformat()
    assert updated['results']['meet_date'] == new_meet_date.isoformat()


def test__update__admin_correct_one_param(poll, client, admin_headers):
    new_expire_date = get_future_datetime(delta=10)
    r = client.patch('/polls/{}'.format(poll.id), json=dict(
        expire_date=new_expire_date,
    ), headers=admin_headers)
    updated = r.get_json()
    assert r.status_code == 200, updated
    assert updated['results']['expire_date'] == new_expire_date.isoformat()


def test__update__error_on_send_none(poll, client, admin_headers):
    r = client.patch('/polls/{}'.format(poll.id), json=dict(
        expire_date=None,
    ), headers=admin_headers)
    assert r.status_code == 422, r.get_json()
    assert r.get_json() == {
        'errors': {'expire_date': ['Field may not be null.']}}


def test__delete__denied_by_user(client, poll, user_headers):
    assert db.session.query(Poll).count() == 1
    r = client.delete('/polls/{}'.format(poll.id), headers=user_headers)
    assert r.status_code == 403, r.get_json()
    assert db.session.query(Poll).count() == 1


def test__delete__correct_by_admin(client, poll, admin_headers):
    assert db.session.query(Poll).count() == 1
    r = client.delete('/polls/{}'.format(poll.id), headers=admin_headers)
    assert r.status_code == 200, r.get_json()
    assert db.session.query(Poll).count() == 0
