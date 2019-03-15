import logging

from flask import Flask
from flask_migrate import Migrate

from thupoll.views.statistic import blueprint as statistic_blueprint
from thupoll.models import db
from thupoll.settings import env


def init_app(db_url=env.db_url):
    __setup_logging()

    app = Flask(__name__)
    app.register_blueprint(statistic_blueprint, url_prefix='/')

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.app_context().push()
    Migrate(app, db)
    db.init_app(app)

    return app


def __setup_logging():
    logging.basicConfig(
        level=env.log_level,
        format='[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s',
    )
