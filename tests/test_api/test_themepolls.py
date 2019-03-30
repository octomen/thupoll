from thupoll.models import db, ThemePoll


def __count_themepolls(poll_id, theme_id):
    return db.session.query(ThemePoll).filter_by(
        poll_id=poll_id).filter_by(theme_id=theme_id).count()


def test__add_theme__correct(client, poll, theme, admin_headers):
    r = client.post('/polls/{}/themes/{}'.format(poll.id, theme.id),
                    headers=admin_headers)
    assert r.status_code == 200
    assert __count_themepolls(poll.id, theme.id) == 1


def test__add_theme__error_when_already_exists(
        client, themepoll, admin_headers):
    r = client.post('/polls/{}/themes/{}'.format(
        themepoll.poll_id, themepoll.theme_id), headers=admin_headers)
    assert r.status_code == 422


def test__delete_theme__correct(client, themepoll, admin_headers):
    r = client.delete('/polls/{}/themes/{}'.format(
        themepoll.poll_id, themepoll.theme_id), headers=admin_headers)
    assert r.status_code == 200
    assert __count_themepolls(themepoll.poll_id, themepoll.theme_id) == 0


def test__delete_theme__error_when_not_exists(
        client, poll, theme, admin_headers):
    r = client.delete('/polls/{}/themes/{}'.format(poll.id, theme.id),
                      headers=admin_headers)
    assert r.status_code == 422
