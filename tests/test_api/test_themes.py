from thupoll.models import db, Theme

from tests.utils import marshall


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


def test__one__404_when_theme_not_exists(client):
    r = client.get('/themes/1')
    assert r.status_code == 404, r.get_json()


def test__one__correct(client, theme, now):
    r = client.get('/themes/{}'.format(theme.id))
    assert r.status_code == 200, r.get_json()
    assert r.get_json() == dict(results=marshall(theme))


def test__all__empty_when_themes_not_exists(client):
    r = client.get('/themes')
    assert r.status_code == 200, r.get_json()
    assert r.get_json() == dict(results=[])


def test__all__one_theme(client, theme):
    r = client.get('/themes')
    assert r.status_code == 200, r.get_json()
    assert r.get_json() == dict(results=[marshall(theme)])


def test__create__correct(client, people, user_headers):
    expected_author_id = people.id
    title = 'title'
    description = 'description'
    r = client.post('/themes', json=dict(
        title=title,
        description=description,
    ), headers=user_headers)
    created_theme = r.get_json()
    assert r.status_code == 200, created_theme
    getted_theme = client.get('/themes/{}'.format(
        created_theme['results']['id'])).get_json()
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
