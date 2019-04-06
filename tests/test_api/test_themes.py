import pytest

from thupoll.models import db, Theme, ThemeStatus

from tests.utils import marshall
from tests.factories import Factory


def test__marshall(theme):
    assert marshall(theme) == dict(
        id=theme.id,
        title=theme.title,
        description=theme.description,
        created=theme.created_date.isoformat(),
        updated=theme.change_date.isoformat(),
        author=marshall(theme.author),
        reporter=marshall(theme.reporter),
        status=marshall(theme.status),
    )


def test__delete__404_when_theme_not_exists(client, user_headers):
    r = client.delete('/themes/1', headers=user_headers)
    assert r.status_code == 404, r.get_json()


def test__one__404_when_theme_not_exists(client, user_headers):
    r = client.get('/themes/1', headers=user_headers)
    assert r.status_code == 404, r.get_json()


def test__one__correct(client, theme, user_headers):
    r = client.get('/themes/{}'.format(theme.id), headers=user_headers)
    assert r.status_code == 200, r.get_json()
    assert r.get_json() == dict(results=marshall(theme))


def test__all__empty_when_themes_not_exists(client):
    peoplenamespace = Factory.peoplenamespace()
    r = client.get(
        '/themes',
        json={'namespace_code': peoplenamespace.namespace.code},
        headers=Factory.authheader(peoplenamespace.people),
    )
    assert r.status_code == 200, r.get_json()
    assert r.get_json() == dict(results=[])


def test__all__one_theme(client, theme, user_headers):
    r = client.get(
        '/themes',
        json={'namespace_code': theme.namespace_code},
        headers=user_headers,
    )
    assert r.status_code == 200, r.get_json()
    db.session.add(theme)
    assert r.get_json() == dict(results=[marshall(theme)])


def test__create__correct(client):
    poeplenamespace = Factory.peoplenamespace()
    people, namespace = poeplenamespace.people, poeplenamespace.namespace
    expected_author_id = people.id
    title = 'title'
    description = 'description'
    r = client.post('/themes', json=dict(
        title=title,
        description=description,
        namespace_code=namespace.code,
    ), headers=Factory.authheader(people))
    created_theme = r.get_json()
    assert r.status_code == 201, created_theme
    getted_theme = client.get(
        '/themes/{}'.format(created_theme['results']['id']),
        headers=Factory.authheader(people)
    ).get_json()
    assert created_theme == getted_theme
    # check binding to user which doing request
    assert created_theme['results']['author']['id'] == expected_author_id


def test__delete__correct_by_author(client, theme, user_headers):
    assert db.session.query(Theme).count() == 1
    r = client.delete('/themes/{}'.format(theme.id), headers=user_headers)
    assert r.status_code == 200, r.get_json()
    assert db.session.query(Theme).count() == 0


def test__delete__correct_by_admin(client, theme, admin_headers):
    assert db.session.query(Theme).count() == 1
    r = client.delete('/themes/{}'.format(theme.id), headers=admin_headers)
    assert r.status_code == 200, r.get_json()
    assert db.session.query(Theme).count() == 0


def test__patch__all_correct(
    client, theme, faker, db_session, session_factory, headers_factory,
):
    assert db.session.query(Theme).count() == 1

    new_description = faker.text(max_nb_chars=500)
    new_title = faker.text(max_nb_chars=20)

    new_people = Factory.peoplenamespace(namespace=theme.namespace).people
    _session = session_factory(people=new_people)
    headers = headers_factory(_session)

    new_status = db.session.query(ThemeStatus).filter(
        ThemeStatus.id != ThemeStatus.NEW,
    ).first()
    assert new_status

    r = client.patch('/themes/{}'.format(theme.id), json=dict(
        title=new_title,
        description=new_description,
        reporter_id=new_people.id,
        status_id=new_status.id,
    ), headers=headers)

    response = r.get_json()
    assert r.status_code == 200, response
    assert response
    assert response.keys() == {'results'}

    theme = db.session.query(Theme).one()  # type: Theme
    assert response['results'] == marshall(theme)

    assert theme.title == new_title
    assert theme.description == new_description
    assert theme.reporter_id == new_people.id
    assert theme.status_id == new_status.id


@pytest.mark.parametrize('changed', (
    'reporter_id', 'status_id', 'title', 'description'))
def test__patch__one_correct(
    client, theme, faker, db_session, people_factory, admin_headers,
    changed,
):
    assert db.session.query(Theme).count() == 1

    new_description = faker.text(max_nb_chars=500)
    new_title = faker.text(max_nb_chars=20)
    new_people = people_factory()
    new_status = db.session.query(ThemeStatus).filter(
        ThemeStatus.id != ThemeStatus.NEW,
    ).first()
    assert new_status

    full_params = {
        'title': new_title,
        'description': new_description,
        'reporter_id': new_people.id,
        'status_id': new_status.id,
    }
    one_param = {k: v for k, v in full_params.items() if k == changed}
    assert one_param

    r = client.patch(
        '/themes/{}'.format(theme.id), json=one_param, headers=admin_headers)

    response = r.get_json()
    assert response
    assert r.status_code == 200, response
    assert response.keys() == {'results'}

    theme = db.session.query(Theme).one()  # type: Theme
    marshalled = marshall(theme)
    assert response['results'] == marshalled

    assert theme.title == marshalled['title']
    assert theme.description == marshalled['description']
    assert theme.reporter_id == marshalled['reporter']['id']
    assert theme.status_id == marshalled['status']['id']


def test__patch__set_description_none(
    client, theme, faker, db_session, people_factory, admin_headers,
):
    assert db.session.query(Theme).count() == 1

    r = client.patch(
        '/themes/{}'.format(theme.id),
        json={'description': None},
        headers=admin_headers)

    response = r.get_json()
    assert response
    assert r.status_code == 200, response

    theme = db.session.query(Theme).one()  # type: Theme
    assert theme.description is None


def test__patch__404(
    client, theme, faker, db_session, people_factory,
    session_factory, headers_factory,
):
    assert db.session.query(Theme).count() == 1

    new_description = faker.text(max_nb_chars=500)
    new_title = faker.text(max_nb_chars=20)

    new_status = db.session.query(ThemeStatus).filter(
        ThemeStatus.id != ThemeStatus.NEW,
    ).first()
    assert new_status

    new_people = people_factory()
    _session = session_factory(people=new_people)
    headers = headers_factory(_session)

    r = client.patch('/themes/{}'.format(theme.id + 1), json=dict(
        title=new_title,
        description=new_description,
        reporter_id=new_people.id,
        status_id=new_status.id,
    ), headers=headers)

    assert r.status_code == 404, r.get_json()
