import random
from thupoll.models import db, Poll

from tests.utils import marshall, get_future_datetime
from tests.factories import Factory, date_between


def test__marshall():
    themepoll = Factory.themepoll()
    vote = Factory.vote(themepoll=themepoll)
    poll = themepoll.poll
    assert marshall(poll) == dict(
        id=poll.id,
        expire_date=poll.expire_date.isoformat(),
        meet_date=poll.meet_date.isoformat(),
        created=poll.created_date.isoformat(),
        updated=poll.change_date.isoformat(),
        themes=[marshall(themepoll.theme)],
        votes=[marshall(vote)],
    )


def test__update__403_denied_for_simple_user(
        poll, client, user_headers, namespace):
    r = client.patch(
        '/polls/{}'.format(poll.id),
        json={'namespace_code': namespace.code},
        headers=user_headers)
    assert r.status_code == 403, r.get_json()


def test__delete__403_denied_for_simple_user(client):
    peoplenamespace = Factory.peoplenamespace()
    poll = Factory.poll(namespace=peoplenamespace.namespace)
    r = client.delete(
        '/polls/{}'.format(poll.id),
        json={'namespace_code': peoplenamespace.namespace.code},
        headers=Factory.authheader(peoplenamespace.people),
    )
    assert r.status_code == 403, r.get_json()


def test__one__404_when_not_exists(client, namespace, user_headers):
    r = client.get(
        '/polls/1',
        json={'namespace_code': namespace.code},
        headers=user_headers,
    )
    assert r.status_code == 404, r.get_json()


def test__one__correct(client, poll, user_headers):
    r = client.get(
        '/polls/{}'.format(poll.id),
        json={'namespace_code': poll.namespace_code},
        headers=user_headers,
    )
    assert r.status_code == 200, r.get_json()
    db.session.add(poll)
    assert r.get_json() == dict(results=marshall(poll))


def test__one__with_sort(client, poll, admin_headers):
    objects_num = 50

    order_nos = list(range(objects_num))
    random.shuffle(order_nos)

    themespolls = {}
    for order_no in order_nos:
        themepoll = Factory.themepoll(poll=poll, order_no=order_no)
        themespolls[order_no] = themepoll.theme_id

    r = client.get(
        '/polls/{}'.format(poll.id),
        json={'namespace_code': poll.namespace_code},
        headers=admin_headers,
    )
    assert r.status_code == 200, r.get_json()

    themes = [theme['id'] for theme in r.get_json()['results']['themes']]
    for idx in range(objects_num):
        assert themes[idx] == themespolls[idx]


def test__all__empty_when_not_exists(client):
    peoplenamespace = Factory.peoplenamespace()
    r = client.get(
        '/polls',
        json={'namespace_code': peoplenamespace.namespace.code},
        headers=Factory.authheader(peoplenamespace.people),
    )
    assert r.status_code == 200, r.get_json()
    assert r.get_json() == dict(results=[])


def test__all__one(client, poll, user_headers):
    r = client.get(
        '/polls',
        json={'namespace_code': poll.namespace_code},
        headers=user_headers,
    )
    assert r.status_code == 200, r.get_json()
    db.session.add(poll)
    assert r.get_json() == dict(results=[marshall(poll)])


def test__all__with_sort(client, namespace, admin_headers):
    for _ in range(50):
        Factory.poll(
            namespace=namespace,
            expire_date=date_between('+1d', '+50d'))

    r = client.get(
        '/polls',
        json={'namespace_code': namespace.code},
        headers=admin_headers,
    )
    assert r.status_code == 200, r.get_json()
    dates = [
        (poll['expire_date'], poll['meet_date'])
        for poll in r.get_json()['results']
    ]
    assert dates == sorted(dates)


def test__create__admin_correct(client, admin_headers, namespace):
    r = client.post('/polls', json=dict(
        expire_date=get_future_datetime(),
        meet_date=get_future_datetime(),
        namespace_code=namespace.code,
    ), headers=admin_headers)
    created = r.get_json()
    assert r.status_code == 201, created
    getted = client.get('/polls/{}'.format(
        created['results']['id']), headers=admin_headers).get_json()
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


def test__get_all__denied_by_no_auth(client, user_headers, namespace):
    r = client.get(
        '/polls',
        json={'namespace_code': namespace.code},
        headers=user_headers,
    )
    assert r.status_code == 403, r.get_json()


def test__get_one__denied_by_no_auth(client):
    poll = Factory.poll()
    r = client.get(
        '/polls/{}'.format(poll.id),
        json={'namespace_code': poll.namespace.code},
    )
    assert r.status_code == 401, r.get_json()


def test__delete__denied_by_user(client, user_headers):
    poll = Factory.poll()
    assert db.session.query(Poll).count() == 1
    r = client.delete(
        '/polls/{}'.format(poll.id),
        json={'namespace_code': poll.namespace.code},
        headers=user_headers,
    )
    assert r.status_code == 403, r.get_json()
    assert db.session.query(Poll).count() == 1


def test__delete__correct_by_admin(client, admin_headers):
    poll = Factory.poll()
    assert db.session.query(Poll).count() == 1
    r = client.delete(
        '/polls/{}'.format(poll.id),
        json={'namespace_code': poll.namespace.code},
        headers=admin_headers,
    )
    assert r.status_code == 200, r.get_json()
    assert db.session.query(Poll).count() == 0
