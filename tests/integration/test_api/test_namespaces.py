from thupoll.models import db

from tests.utils import marshall
from tests.factories import Factory


def test__marshall(peoplenamespace):
    assert marshall(peoplenamespace) == dict(
        people_id=peoplenamespace.people_id,
        namespace=peoplenamespace.namespace.marshall(),
        role=peoplenamespace.role.marshall(),
    )


def test__one__404_when_namespace_not_exists(client, user_headers):
    r = client.get('/namespaces/1', headers=user_headers)
    assert r.status_code == 404, r.get_json()


def test__one__correct(client, peoplenamespace, user_headers):
    r = client.get('/namespaces/{}'.format(
        peoplenamespace.namespace_code), headers=user_headers)
    assert r.status_code == 200, r.get_json()
    assert r.get_json() == dict(results=marshall(peoplenamespace))


def test__all__empty_when_namespaces_not_exists(client):
    people = Factory.people()
    r = client.get(
        '/namespaces',
        headers=Factory.authheader(people),
    )
    assert r.status_code == 200, r.get_json()
    assert r.get_json() == dict(results=[])


def test__all__one_theme(client, peoplenamespace, user_headers):
    r = client.get(
        '/namespaces',
        headers=user_headers,
    )
    assert r.status_code == 200, r.get_json()
    db.session.add(peoplenamespace)
    assert r.get_json() == dict(results=[marshall(peoplenamespace)])
