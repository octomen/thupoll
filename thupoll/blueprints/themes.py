import logging
from flask import Blueprint, jsonify, abort, g
from webargs import fields
from webargs.flaskparser import use_kwargs, use_args

from thupoll import validators
from thupoll.models import db, Theme, ThemeStatus
from thupoll.utils import for_auth


blueprint = Blueprint('themes', __name__)
logger = logging.getLogger(__name__)


@blueprint.route('/', strict_slashes=False)
@for_auth
@use_kwargs({
    'namespace_code': fields.Str(required=True),
})
def get_all(namespace_code):
    logger.info('Themes. Get info all')
    validators.namespace_access(namespace_code)
    q = db.session.query(Theme)
    if not namespace_code and not g.people.is_admin():
        abort(403)  # TODO return all accessed objects
    elif namespace_code:
        q = q.filter_by(namespace_code=namespace_code)
    return jsonify(dict(results=[obj.marshall() for obj in q.all()]))


@blueprint.route('/<int:theme_id>')
@for_auth
def get_one(theme_id: int):
    logger.info('Themes. Get info %s', theme_id)
    obj = db.session.query(Theme).get_or_404(theme_id)  # type: Theme
    validators.namespace_access(obj.namespace_code)
    return jsonify(dict(results=obj.marshall()))


@blueprint.route('/', methods=['POST'], strict_slashes=False)
@for_auth
@use_kwargs({
    'title': fields.Str(required=True),
    'namespace_code': fields.Str(required=True),
    'description': fields.Str(),
    'reporter_id': fields.Int(),
    'status_id': fields.Int(),
})
def create(
        title, namespace_code,
        description=None, reporter_id=None, status_id=None,
):
    author_id = g.people.id
    status_id = status_id or ThemeStatus.NEW
    logger.info(
        'Themes. Creating new (title %s, desc %s, reporter %s, status %s',
        title, description, reporter_id, status_id)

    validators.namespace_access(namespace_code)
    reporter = validators.people_id(reporter_id, must_exists=True)
    author = validators.people_id(author_id, must_exists=True)
    status = validators.theme_status_id(status_id, must_exists=True)

    obj = Theme(
        title=title,
        description=description,
        namespace_code=namespace_code,
        author_id=author_id,
        reporter_id=reporter_id,
        status_id=status_id,
        status=status,
        reporter=reporter,  # fill relation for marshall
        author=author,  # fill relation for marshall
    )
    db.session.add(obj)
    # TODO remove. Now needed for tests (when happens auto-commit?)
    db.session.commit()

    logger.info('Themes. Created %s', obj.id)

    return jsonify(dict(results=obj.marshall())), 201


@blueprint.route('/<int:theme_id>', methods=['DELETE'])
@for_auth
def delete(theme_id):
    logger.info('Themes. Delete %s', theme_id)

    obj = db.session.query(Theme).get_or_404(theme_id)

    validators.namespace_access(obj.namespace_code)

    if not (g.people.is_admin() or g.people.id == obj.author_id):
        abort(403)

    db.session.delete(obj)
    db.session.commit()

    logger.info('Themes. Deleted %s', obj.id)

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

    validators.namespace_access(theme.namespace_code)

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
