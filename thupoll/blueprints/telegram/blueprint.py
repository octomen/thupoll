"""Blueprint with entrypoint to telegram webhook."""

from http import HTTPStatus

from flask import Blueprint, request, Response

from thupoll.settings import env
from thupoll.blueprints.telegram.hook import TelegramHook
from thupoll.blueprints.telegram.mount import mount

telegram_blueprint = Blueprint('telegram_bot', __name__)

webhook = TelegramHook(
    token=env.bot_telegram_token,
    proxy=env.bot_proxy_url,
)
mount(webhook)


@telegram_blueprint.route("/", strict_slashes=False, methods=["POST"])
def handle():
    """Entrypoint for telegram api."""
    webhook.handle(request.json)
    return Response(status=HTTPStatus.OK)
