from flask import Response
from thupoll.models import Vote

from tests.factories import Factory
from tests.utils import marshall, get_past_datetime


def test__marshall(vote):
    assert marshall(vote) == dict(
        id=vote.id,
        created=vote.created_date.isoformat(),
        updated=vote.change_date.isoformat(),
        people_id=vote.people_id,
        pole_id=vote.themepoll.poll_id,
        theme_id=vote.themepoll.theme_id,
    )


def test__get_votes(db_session, client, user_headers, poll):
    themepoll = Factory.themepoll(poll=poll)
    Factory.vote(themepoll=themepoll)
    r = client.get("/polls/{}/votes".format(poll.id), headers=user_headers)
    assert r.status_code == 200, r.get_json()
    assert r.get_json() == dict(results=marshall(poll))


def _post_votes(client, poll_id, themes, headers) -> Response:
    return client.post(
        "/polls/{}/votes".format(poll_id),
        json=[dict(theme_id=theme.id) for theme in themes],
        headers=headers,
    )


def test__set_any_votes__correct(
    db_session, client, peoplenamespace, user_headers, poll,
):
    people_id = peoplenamespace.people_id
    poll_id = poll.id

    theme = Factory.themepoll(poll=poll).theme
    r = _post_votes(
        client=client, poll_id=poll_id, themes=[theme], headers=user_headers,
    )

    assert r.status_code == 200, r.get_json()
    vote = r.get_json()["results"]["votes"][0]

    assert vote["people_id"] == people_id
    assert vote["pole_id"] == poll_id
    assert vote["theme_id"] == theme.id


def test__set_any_votes__expire(
        db_session, client, peoplenamespace, user_headers,
):
    poll = Factory.poll(
        expire_date=get_past_datetime(), namespace=peoplenamespace.namespace,
    )
    theme = Factory.themepoll(poll=poll).theme
    r = _post_votes(
        client=client, poll_id=poll.id, themes=[theme], headers=user_headers,
    )

    assert r.status_code == 422, r.get_json()
    assert r.get_json() == {
        "_schema": ["Datetime {} from past".format(poll.expire_date)],
    }


def test__set_any_votes__not_themepoll(
    db_session, client, peoplenamespace, user_headers, poll,
):
    theme = Factory.themepoll().theme
    r = _post_votes(
        client=client, poll_id=poll.id, themes=[theme], headers=user_headers,
    )

    assert r.status_code == 422, r.get_json()
    assert r.get_json() == {
        "_schema": [
            "ThemePoll with poll_id={} theme_id={} does not exists".format(
                poll.id, theme.id,
            ),
        ],
    }


def test__set_any_votes__two_theme(
    db_session, client, peoplenamespace, user_headers, poll,
):
    theme1 = Factory.themepoll(poll=poll).theme
    theme2 = Factory.themepoll(poll=poll).theme
    r = _post_votes(
        client=client,
        poll_id=poll.id,
        themes=[theme1, theme2],
        headers=user_headers,
    )

    assert r.status_code == 200, r.get_json()
    assert len(r.get_json()["results"]["votes"]) == 2


def test__set_any_votes__empty_json(
    db_session, client, peoplenamespace, user_headers, poll,
):
    r = _post_votes(
        client=client,
        poll_id=poll.id,
        themes=[],
        headers=user_headers,
    )

    assert r.status_code == 422, r.get_json()
    assert r.get_json() == {"_schema": ["Sequence 'themes' is empty"]}


def test__set_any_votes__drop_old(
    db_session, client, peoplenamespace, user_headers, poll,
):
    themepoll = Factory.themepoll(poll=poll)
    Factory.vote(themepoll=themepoll, people=peoplenamespace.people)

    r = client.delete(
        "/polls/{}/votes".format(poll.id),
        headers=user_headers,
    )

    assert r.status_code == 200, r.get_json()
    assert not db_session.query(Vote).count()
