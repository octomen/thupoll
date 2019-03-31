import logging
from flask import Blueprint, jsonify, abort, g
from webargs import fields
from webargs.flaskparser import use_args

from thupoll import validators
from thupoll.models import db, Theme, ThemeStatus
from thupoll.utils import for_auth


blueprint = Blueprint('themes', __name__)
logger = logging.getLogger(__name__)


@blueprint.route('/', strict_slashes=False)
def get_all():
    logger.info('Themes. Get info all')
    return jsonify(dict(results=[
        theme.marshall() for theme in db.session.query(Theme).all()
    ]))


@blueprint.route('/<int:theme_id>')
def get_one(theme_id: int):
    logger.info('Themes. Get info %s', theme_id)
    theme = db.session.query(Theme).get_or_404(theme_id)
    return jsonify(dict(results=theme.marshall()))


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

    return jsonify(dict(results=theme.marshall()))


@blueprint.route('/<int:theme_id>', methods=['DELETE'])
@for_auth
def delete(theme_id):
    logger.info('Themes. Delete %s', theme_id)

    theme = db.session.query(Theme).get_or_404(theme_id)

    if not (g.people.is_admin() or g.people.id == theme.author_id):
        abort(403)

    db.session.delete(theme)
    db.session.commit()

    logger.info('Themes. Deleted %s', theme.id)

    return jsonify(dict(results=dict(id=theme_id)))


@blueprint.route('/<int:theme_id>', methods=['PATCH'])
@for_auth
@use_args({
    'title': fields.Str(),
    'description': fields.Str(allow_none=True),
    'reporter_id': fields.Int(),
    'status_id': fields.Int(),
})
def update(args, theme_id):
    logger.info('Themes. Updating %s (%s) by %s', theme_id, args, g.people.id)

    theme = db.session.query(Theme).get_or_404(theme_id)

    title = args.get('title', theme.title)
    description = args.get('description', theme.description)
    reporter_id = args.get('reporter_id', theme.reporter_id)
    status_id = args.get('status_id', theme.status_id)

    reporter = validators.people_id(reporter_id, must_exists=True)
    status = validators.theme_status_id(status_id, must_exists=True)

    theme.title = title
    theme.description = description
    theme.reporter = reporter
    theme.status = status
    db.session.commit()

    logger.info('Themes. Updated %s', theme.id)

    return jsonify(results=theme.marshall())
