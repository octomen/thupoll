"""Blueprint with entrypoint to telegram webhook."""

from http import HTTPStatus

from flask import Blueprint, request, Response

from thupoll.components import Components
from thupoll.telegram import logger

telegram_blueprint = Blueprint('telegram_bot', __name__)


@telegram_blueprint.route("/", strict_slashes=False, methods=["POST"])
def handle():
    """Entrypoint for telegram api."""
    webhook = Components.telegram_hook()
    try:
        webhook.handle(request.json)
    except Exception:
        logger.exception("Dispatch message from telegram failed")
        return Response(status=HTTPStatus.NOT_FOUND)
    return Response(status=HTTPStatus.OK)
