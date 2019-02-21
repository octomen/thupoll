from flask import Blueprint, jsonify


blueprint = Blueprint('thursday', __name__)


@blueprint.route('/')
def home():
    return jsonify(ok='ok')
