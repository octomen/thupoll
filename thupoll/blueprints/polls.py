import logging
from flask import Blueprint, jsonify, abort, g
from marshmallow import Schema
from webargs import fields
from webargs.flaskparser import use_kwargs, use_args

from thupoll import validators
from thupoll.models import db, Poll, ThemePoll, Vote
from thupoll.utils import for_auth


blueprint = Blueprint('polls', __name__)
logger = logging.getLogger(__name__)


@blueprint.route('/', strict_slashes=False)
@for_auth
@use_kwargs({
    'namespace_code': fields.Str(required=True),
})
def get_all(namespace_code):
    logger.info('Polls. Get info all')
    validators.namespace_access(namespace_code)
    q = db.session.query(Poll)
    if not namespace_code and not g.people.is_admin():
        abort(403)  # TODO return all accessed objects
    elif namespace_code:
        q = q.filter_by(namespace_code=namespace_code)
    return jsonify(dict(results=[obj.marshall() for obj in q]))


@blueprint.route('/<int:poll_id>')
@for_auth
def get_one(poll_id: int):
    logger.info('Poll. Get info %s', poll_id)
    obj = db.session.query(Poll).get_or_404(poll_id)  # type: Poll
    validators.namespace_access(obj.namespace_code)
    return jsonify(dict(results=obj.marshall()))


@blueprint.route('/', methods=['POST'], strict_slashes=False)
@for_auth
@use_kwargs({
    'expire_date': fields.DateTime(required=True),
    'meet_date': fields.DateTime(required=True),
    'namespace_code': fields.Str(required=True),
})
def create(expire_date, meet_date, namespace_code):
    logger.info(
        'Poll. Creating new (expire_date %s, meet_date %s) in %s',
        expire_date, meet_date, namespace_code)

    validators.future_datetime_validator(expire_date)
    validators.future_datetime_validator(meet_date)
    validators.namespace_access(namespace_code, admin=True)

    poll = Poll(
        expire_date=expire_date,
        meet_date=meet_date,
        namespace_code=namespace_code,
    )
    db.session.add(poll)
    # TODO remove. Now needed for tests (when happens auto-commit?)
    db.session.commit()

    logger.info('Poll. Created %s', poll.id)

    return jsonify(dict(results=poll.marshall())), 201


@blueprint.route('/<int:poll_id>', methods=['DELETE'])
@for_auth
def delete(poll_id):
    logger.info('Poll. Delete %s', poll_id)

    poll = db.session.query(Poll).get_or_404(poll_id)

    validators.namespace_access(poll.namespace_code, admin=True)

    db.session.delete(poll)
    db.session.commit()

    logger.info('Poll. Deleted %s', poll.id)

    return jsonify(dict(results=dict(id=poll_id)))


@blueprint.route('/<int:poll_id>', methods=['PATCH'])
@for_auth
@use_kwargs({
    'meet_date': fields.DateTime(allow_none=False),
    'expire_date': fields.DateTime(allow_none=False),
})
def update(poll_id, meet_date=None, expire_date=None):
    logger.info('Poll. Update %s %s %s', poll_id, expire_date, meet_date)

    poll = db.session.query(Poll).get_or_404(poll_id)

    validators.namespace_access(poll.namespace_code, admin=True)

    if expire_date:
        poll.expire_date = expire_date
    if meet_date:
        poll.meet_date = meet_date

    db.session.commit()

    return jsonify(dict(results=poll.marshall()))


class ThemeToPoll(Schema):
    theme_id = fields.Int(required=True)
    order_no = fields.Int(required=True)


@blueprint.route('/<int:poll_id>/themes', methods=['POST'])
@for_auth
@use_args(ThemeToPoll(many=True))
def set_themes(themes, poll_id):
    logger.info('Poll %s. Set themes %s', poll_id, themes)

    poll = validators.poll_id(poll_id, must_exists=True)
    validators.namespace_access(poll.namespace_code, admin=True)
    validators.distinct(
        themes, name='theme_id', fetcher=lambda x: x['theme_id'])
    validators.distinct(
        themes, name='order_no', fetcher=lambda x: x['order_no'])

    for theme in themes:
        validators.theme_id(theme['theme_id'], must_exists=True)

    # delete previous state of themes
    db.session.query(ThemePoll).filter_by(poll_id=poll_id).delete()
    # create new state of themes
    for theme in themes:
        db.session.add(ThemePoll(
            theme_id=theme['theme_id'],
            poll_id=poll_id,
            order_no=theme['order_no'],
        ))
    db.session.commit()

    logger.info(
        'Poll %s. %s themes was set (%s)',
        poll_id, len(themes), themes)

    return get_one(poll_id=poll_id)


class ThemeArg(Schema):
    theme_id = fields.Int(required=True)


@blueprint.route('/<int:poll_id>/votes', methods=['GET'])
@for_auth
def get_votes(poll_id):
    logger.info('Votes for poll %s', poll_id)

    poll: Poll = validators.poll_id(poll_id, must_exists=True)
    validators.namespace_access(poll.namespace_code)

    votes = db.session.query(Vote).join(
        ThemePoll
    ).filter(
        ThemePoll.poll == poll,
    )
    return jsonify(dict(results=[obj.marshall() for obj in votes]))


@blueprint.route('/<int:poll_id>/votes', methods=['POST'])
@for_auth
@use_args(ThemeArg(many=True))
def set_votes(themes, poll_id):
    logger.info('Poll %s. Votes for themes %s', poll_id, themes)

    poll: Poll = validators.poll_id(poll_id, must_exists=True)

    validators.future_datetime_validator(poll.expire_date)
    validators.namespace_access(poll.namespace_code)
    validators.distinct(
        themes, name='theme_id', fetcher=lambda x: x['theme_id'])

    themepolls = []
    for theme in themes:
        themepolls.append(
            validators.themepoll(
                theme_id=theme['theme_id'],
                poll_id=poll_id
            )
        )

    # delete previous state of votes
    db.session.query(Vote).filter(
        ThemePoll.id == Vote.themepoll_id,
        ThemePoll.poll_id == poll_id,
        Vote.people_id == g.people.id,
    ).delete(synchronize_session=False)

    # create new state of themes
    for themepoll in themepolls:
        db.session.add(Vote(
            themepoll_id=themepoll.id,
            people_id=g.people.id,
        ))
    db.session.commit()

    logger.info(
        'Poll %s. %s votes was set (for themes %s)',
        poll_id, len(themes), themes)

    return get_votes(poll_id=poll_id)
