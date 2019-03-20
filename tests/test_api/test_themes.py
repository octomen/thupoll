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


def test__delete__404_when_theme_not_exists(client):
    r = client.delete('/themes/1')
    assert r.status_code == 404, r.get_json()


def test__one__404_when_theme_not_exists(client):
    r = client.get('/themes/1')
    assert r.status_code == 404, r.get_json()


def test__one__correct(client, theme, now):
    r = client.get('/themes/{}'.format(theme.id))
    assert r.status_code == 200, r.get_json()
    assert r.get_json() == marshall(theme)


def test__all__empty_when_themes_not_exists(client):
    r = client.get('/themes')
    assert r.status_code == 200, r.get_json()
    assert r.get_json() == []


def test__all__one_theme(client, theme):
    r = client.get('/themes')
    assert r.status_code == 200, r.get_json()
    assert r.get_json() == [marshall(theme)]


def test__create__correct(client, people):
    title = 'title'
    description = 'description'
    r = client.post('/themes', json=dict(
        title=title,
        description=description,
        author_id=people.id,
    ))
    assert r.status_code == 200, r.get_json()
    assert r.get_json() == client.get(
        '/themes/{}'.format(r.get_json()['id'])).get_json()


def test__delete__correct(client, theme):
    assert db.session.query(Theme).count() == 1
    r = client.delete('/themes/{}'.format(theme.id))
    assert r.status_code == 200, r.get_json()
    assert db.session.query(Theme).count() == 0
