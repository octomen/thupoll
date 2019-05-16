import logging
from flask import Blueprint, jsonify, abort, g

from thupoll import controllers as ctl
from thupoll.utils import for_auth


blueprint = Blueprint('Namespaces', __name__)
logger = logging.getLogger(__name__)


@blueprint.route('/', strict_slashes=False)
@for_auth
def get_all():
    logger.info('Namespaces. Get info all')
    return jsonify(dict(results=[
        obj.marshall() for obj in ctl.peoplenamespace.all(g.people)]))


@blueprint.route('/<namespace_code>')
@for_auth
def get_one(namespace_code: str):
    logger.info('Namespaces. Get info %s', namespace_code)
    obj = ctl.peoplenamespace.get(people=g.people, code=namespace_code)
    if not obj:
        abort(404)
    return jsonify(dict(results=obj.marshall()))
