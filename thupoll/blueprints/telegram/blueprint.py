"""Blueprint with entrypoint to telegram webhook."""

from http import HTTPStatus

from flask import Blueprint, request, Response

from thupoll.settings import env
from thupoll.blueprints.telegram import logger
from thupoll.blueprints.telegram.hook import TelegramHook
from thupoll.blueprints.telegram.mount import mount

telegram_blueprint = Blueprint('telegram_bot', __name__)

webhook = TelegramHook(
    token=env.bot_telegram_token,
    proxy=env.bot_proxy_url,
)
mount(webhook)


@telegram_blueprint.route("/", methods=["POST"])
def handle():
    """Entrypoint for telegram api."""
    try:
        webhook.handle(request.json)
    except Exception:
        logger.exception("Dispatch message from telegram failed")
        return Response(status=HTTPStatus.NOT_FOUND)
    return Response(status=HTTPStatus.OK)
