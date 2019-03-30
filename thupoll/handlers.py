from flask import jsonify
from marshmallow.exceptions import ValidationError


def handlerize(app):
    @app.errorhandler(ValidationError)
    def handle_invalid_usage(error):
        response = jsonify(error.normalized_messages())
        response.status_code = 422
        return response

    @app.errorhandler(422)
    def handle_error(err):
        headers = err.data.get("headers", None)
        messages = err.data.get("messages", ["Invalid request."])
        if headers:
            return jsonify({"errors": messages}), err.code, headers
        else:
            return jsonify({"errors": messages}), err.code
