from thupoll.models import db, Vote
from tests.utils import marshall


def test__marshall(vote):
    assert marshall(vote) == dict(
        id=vote.id,
        created=vote.created_date.isoformat(),
        updated=vote.change_date.isoformat(),
        themepoll_id=vote.themepoll_id,
        people_id=vote.people_id,
        themepoll=marshall(vote.themepoll),
        people=marshall(vote.people),
    )



