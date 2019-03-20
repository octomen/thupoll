import logging

from flask import Blueprint


blueprint = Blueprint('home', __name__)
logger = logging.getLogger(__name__)


@blueprint.route('/ping')
def ping():
    return 'pong'
