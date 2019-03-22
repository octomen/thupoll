import logging
from flask import Blueprint, jsonify, abort, g
from webargs import fields
from webargs.flaskparser import use_args

from thupoll import validators
from thupoll.models import db, Theme, ThemeStatus
from thupoll.utils import for_auth


blueprint = Blueprint('themes', __name__)
logger = logging.getLogger(__name__)

# TODO check auth & check roles


@blueprint.route('/', strict_slashes=False)
def get_all():
    logger.info('Themes. Get info all')
    return jsonify(
        [theme.marshall() for theme in db.session.query(Theme).all()])


@blueprint.route('/<int:theme_id>')
def get_one(theme_id: int):
    logger.info('Themes. Get info %s', theme_id)
    theme = db.session.query(Theme).get(theme_id)
    if not theme:
        abort(404)
    return jsonify(theme.marshall())


@blueprint.route('/', methods=['POST'], strict_slashes=False)
@for_auth
@use_args({
    'title': fields.Str(required=True),
    'description': fields.Str(),
    'reporter_id': fields.Int(),
    'status_id': fields.Int(),
})
def create(args):
    title = args.get('title')
    desc = args.get('description')
    reporter_id = args.get('reporter_id')
    author_id = g.people.id
    status_id = args.get('status_id') or ThemeStatus.NEW
    logger.info(
        'Themes. Creating new (title %s, desc %s, reporter %s, status %s',
        title, desc, reporter_id, status_id)

    reporter = validators.people_id(reporter_id, must_exists=True)
    author = validators.people_id(author_id, must_exists=True)
    status = validators.theme_status_id(status_id, must_exists=True)

    theme = Theme(
        title=title,
        description=desc,
        author_id=author_id,
        reporter_id=reporter_id,
        status_id=status_id,
        status=status,
        reporter=reporter,  # fill relation for marshall
        author=author,  # fill relation for marshall
    )
    db.session.add(theme)
    # TODO remove. Now needed for tests (when happens auto-commit?)
    db.session.commit()

    logger.info('Themes. Created %s', theme.id)

    return jsonify(theme.marshall())


@blueprint.route('/<int:theme_id>', methods=['DELETE'])
@for_auth
def delete(theme_id):
    logger.info('Themes. Delete %s', theme_id)

    theme = db.session.query(Theme).get(theme_id)

    if not theme:
        abort(404)

    if not (g.people.is_admin() or g.people.id == theme.author_id):
        abort(403)

    db.session.delete(theme)

    logger.info('Themes. Deleted %s', theme.id)

    return jsonify(dict(id=theme_id))
