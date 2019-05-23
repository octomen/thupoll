"""Blueprint with entrypoint to telegram webhook."""

from http import HTTPStatus

from flask import Blueprint, request, Response

from thupoll.components import Components

telegram_blueprint = Blueprint('telegram_bot', __name__)


@telegram_blueprint.route("/", strict_slashes=False, methods=["POST"])
def handle():
    """Entrypoint for telegram api."""
    webhook = Components.telegram_hook()
    webhook.handle(request.json)
    return Response(status=HTTPStatus.OK)
