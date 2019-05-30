from thupoll.models import db, Vote, ThemePoll


def delete_votes(poll_id, people_id):
    sq = db.session.query(Vote.id).join(ThemePoll).filter(
        ThemePoll.poll_id == poll_id,
        Vote.people_id == people_id,
    ).subquery()

    db.session.query(Vote).filter(
        Vote.id.in_(sq),
    ).delete(synchronize_session=False)
