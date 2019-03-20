from flask import jsonify
from marshmallow.exceptions import ValidationError


def handlerize(app):
    @app.errorhandler(ValidationError)
    def handle_invalid_usage(error):
        response = jsonify(error.normalized_messages())
        response.status_code = 422
        return response
