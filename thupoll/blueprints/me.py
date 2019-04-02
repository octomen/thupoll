import logging
from flask import Blueprint, jsonify, g

from thupoll.utils import for_auth


blueprint = Blueprint('me', __name__)
logger = logging.getLogger(__name__)


@blueprint.route('/', strict_slashes=False)
@for_auth
def get_me():
    logger.info('User %s requested yourself')
    return jsonify(dict(results=g.people.marshall()))
