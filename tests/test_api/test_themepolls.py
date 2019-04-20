from thupoll.models import db, ThemePoll, Role

from tests.utils import marshall
from tests.factories import Factory


def test__set_any_themes__denied_by_no_admin(client, user_headers):
    poll = Factory.poll()
    r = client.post(
        '/polls/{}/themes'.format(poll.id),
        json=[dict(theme_id=777, order_no=1)],
        headers=user_headers,
    )
    assert r.status_code == 403, r.get_json()


def test__set_two_themes__correct_if_before_no_themes(client, admin_headers):
    namespace = Factory.namespace()
    reporter = Factory.people()
    Factory.peoplenamespace(people=reporter, namespace=namespace)
    theme1 = Factory.theme(namespace=namespace, reporter=reporter)
    theme2 = Factory.theme(namespace=namespace, reporter=reporter)
    poll = Factory.poll()
    r = client.post(
        '/polls/{}/themes'.format(poll.id),
        json=[
            dict(theme_id=theme1.id, order_no=1),
            dict(theme_id=theme2.id, order_no=2),
        ],
        headers=admin_headers,
    )
    assert r.status_code == 200, r.get_json()
    assert db.session.query(ThemePoll).filter_by(poll_id=poll.id).count() == 2
    db.session.add(poll)
    db.session.refresh(poll)
    assert r.get_json() == dict(results=marshall(poll))


def test__set_two_themes_when_already_exists__change_order(
        client, admin_headers):
    namespace = Factory.namespace()
    reporter = Factory.people()
    Factory.peoplenamespace(people=reporter, namespace=namespace)
    theme1 = Factory.theme(namespace=namespace, reporter=reporter)
    theme2 = Factory.theme(namespace=namespace, reporter=reporter)

    themepoll1 = Factory.themepoll(theme=theme1)
    themepoll2 = Factory.themepoll(theme=theme2)
    poll = Factory.poll()
    r = client.post(
        '/polls/{}/themes'.format(poll.id),
        json=[
            dict(theme_id=themepoll1.theme.id, order_no=themepoll2.order_no),
            dict(theme_id=themepoll2.theme.id, order_no=themepoll1.order_no),
        ],
        headers=admin_headers,
    )
    assert r.status_code == 200, r.get_json()
    assert db.session.query(ThemePoll).filter_by(poll_id=poll.id).count() == 2


def test__set_two_theme__duplication_theme_id(client, admin_headers):
    theme = Factory.theme()
    poll = Factory.poll()
    r = client.post(
        '/polls/{}/themes'.format(poll.id),
        json=[
            dict(theme_id=theme.id, order_no=1),
            dict(theme_id=theme.id, order_no=2),
        ],
        headers=admin_headers
    )
    assert r.status_code == 422, r.get_json()
    assert r.get_json() == {'_schema': ['Duplication values of theme_id']}
    assert db.session.query(ThemePoll).filter_by(poll_id=poll.id).count() == 0


def test__set_two_theme__duplication_order_no(client, admin_headers):
    theme1 = Factory.theme()
    theme2 = Factory.theme()
    poll = Factory.poll()
    r = client.post(
        '/polls/{}/themes'.format(poll.id),
        json=[
            dict(theme_id=theme1.id, order_no=1),
            dict(theme_id=theme2.id, order_no=1),
        ],
        headers=admin_headers
    )
    assert r.status_code == 422, r.get_json()
    assert r.get_json() == {'_schema': ['Duplication values of order_no']}
    assert db.session.query(ThemePoll).filter_by(poll_id=poll.id).count() == 0


def test__invalid_theme_validation(client, admin_headers):
    poll = Factory.poll()
    r = client.post(
        '/polls/{}/themes'.format(poll.id),
        json=[dict(theme_id=1, order_no=1)],
        headers=admin_headers
    )
    assert r.status_code == 422, r.get_json()
    assert r.get_json() == {'_schema': ['Theme with id=1 does not exists']}
    assert db.session.query(ThemePoll).filter_by(poll_id=poll.id).count() == 0


def test__invalid_poll_validation(client, admin_headers):
    theme = Factory.theme()
    r = client.post(
        '/polls/{}/themes'.format(1),
        json=[dict(theme_id=theme.id, order_no=1)],
        headers=admin_headers
    )
    assert r.status_code == 422, r.get_json()
    assert r.get_json() == {'_schema': ['Poll with id=1 does not exists']}


def test__add_with_reporter_from_another_namespace(
    client, people, session_factory, headers_factory,
):
    sender_namespace = Factory.namespace()
    Factory.peoplenamespace(
        people=people, namespace=sender_namespace, role_id=Role.OCTOPUS,
    )

    reporter_namespace = Factory.namespace()
    assert sender_namespace.code != reporter_namespace.code

    reporter = Factory.people()
    Factory.peoplenamespace(people=reporter, namespace=reporter_namespace)

    theme = Factory.theme(namespace=sender_namespace, reporter=reporter)
    poll = Factory.poll(namespace=sender_namespace)

    session = session_factory(people=people)
    headers = headers_factory(session=session)
    r = client.post(
        '/polls/{}/themes'.format(poll.id),
        json=[dict(theme_id=theme.id, order_no=1)],
        headers=headers,
    )
    assert r.status_code == 422, r.get_json()
    assert r.get_json() == {
        '_schema': [
            'Reporter {} has no access to theme namespace ({})'.format(
                reporter, sender_namespace,
            )]}
