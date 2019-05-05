import logging

from flask import Flask
from flask_migrate import Migrate

from thupoll.handlers import handlerize
from thupoll.models import db
from thupoll.routes import routify
from thupoll.settings import env
from thupoll.utils import CustomJSONEncoder


def init_app(db_url=env.db_url):
    __setup_logging()

    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder

    handlerize(app=app)
    routify(app=app)

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config["SERVER_NAME"] = env.thupoll_url

    app.app_context().push()
    Migrate(app, db)
    db.init_app(app)

    return app


def __setup_logging():
    # TODO add request_id to logs
    # https://github.com/Workable/flask-log-request-id ?
    logging.basicConfig(
        level=env.log_level,
        format='[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s',
    )
