import logging
from flask import Blueprint, jsonify, abort
from marshmallow import Schema
from webargs import fields
from webargs.flaskparser import use_args, use_kwargs

from thupoll import validators
from thupoll.models import db, Poll, ThemePoll
from thupoll.utils import for_admins


blueprint = Blueprint('polls', __name__)
logger = logging.getLogger(__name__)


@blueprint.route('/', strict_slashes=False)
def get_all():
    logger.info('Polls. Get info all')
    return jsonify(dict(results=[
        obj.marshall() for obj in db.session.query(Poll).all()
    ]))


@blueprint.route('/<int:poll_id>')
def get_one(poll_id: int):
    logger.info('Poll. Get info %s', poll_id)
    obj = db.session.query(Poll).get(poll_id)
    if not obj:
        abort(404)
    return jsonify(dict(results=obj.marshall()))


@blueprint.route('/', methods=['POST'], strict_slashes=False)
@for_admins
@use_args({
    'expire_date': fields.DateTime(),
    'meet_date': fields.DateTime(),
})
def create(args):
    expire_date = args.get('expire_date')
    meet_date = args.get('meet_date')
    logger.info(
        'Poll. Creating new (expire_date %s, meet_date %s)',
        expire_date, meet_date)

    validators.future_datetime_validator(expire_date)
    validators.future_datetime_validator(meet_date)

    poll = Poll(expire_date=expire_date, meet_date=meet_date)
    db.session.add(poll)
    # TODO remove. Now needed for tests (when happens auto-commit?)
    db.session.commit()

    logger.info('Poll. Created %s', poll.id)

    return jsonify(dict(results=poll.marshall()))


@blueprint.route('/<int:poll_id>', methods=['DELETE'])
@for_admins
def delete(poll_id):
    logger.info('Poll. Delete %s', poll_id)

    poll = db.session.query(Poll).get(poll_id)

    if not poll:
        abort(404)

    db.session.delete(poll)
    db.session.commit()

    logger.info('Poll. Deleted %s', poll.id)

    return jsonify(dict(results=dict(id=poll_id)))


@blueprint.route('/<int:poll_id>', methods=['PATCH'])
@for_admins
@use_kwargs({
    'meet_date': fields.DateTime(allow_none=False),
    'expire_date': fields.DateTime(allow_none=False),
})
def update(poll_id, meet_date=None, expire_date=None):
    logger.info('Poll. Update %s %s %s', poll_id, expire_date, meet_date)

    poll = db.session.query(Poll).get(poll_id)

    if not poll:
        abort(404)

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
@for_admins
@use_args(ThemeToPoll(many=True))
def set_themes(themes, poll_id):
    logger.info('Poll %s. Set themes %s', poll_id, themes)

    validators.poll_id(poll_id, must_exists=True)
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
