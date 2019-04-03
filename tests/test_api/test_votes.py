from tests.factories import Factory
from tests.utils import marshall


def test__marshall(vote):
    assert marshall(vote) == dict(
        id=vote.id,
        created=vote.created_date.isoformat(),
        updated=vote.change_date.isoformat(),
        people_id=vote.people_id,
        pole_id=vote.themepoll.poll_id,
        theme_id=vote.themepoll.theme_id,
    )


def test__set_any_votes__correct(client, user_headers):
    poll = Factory.poll()
    theme1 = Factory.themepoll(poll=poll).theme
    theme2 = Factory.themepoll(poll=poll).theme
    r = client.post(
        '/polls/{}/votes'.format(poll.id),
        json=[
            dict(theme_id=theme1.id),
            dict(theme_id=theme2.id),
        ],
        headers=user_headers,
    )
    print(r.get_json())
    assert r.status_code == 200, r.get_json()


def test__set_any_votes__incorrect_after_expire_poll(): ...


def test__set_any_votes__incorrect_for_namespace_denied(): ...


def test__set_any_votes__incorrect_duplication(): ...


def test__invalid_themepoll_validation(): ...


def test__invalid_theme_validation(): ...


def test__invalid_poll_validation(): ...
