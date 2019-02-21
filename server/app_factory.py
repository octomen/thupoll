import os

from flask import Flask

from .views.statistic import blueprint as statistic_blueprint
from .models import db
from .config import DATABASE as DB


def init_app():
    app = Flask(__name__)
    app.register_blueprint(statistic_blueprint, url_prefix='/distribution')

    db_url = os.environ.get('DB_URL')
    if not db_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            f'postgresql://{DB["user"]}:{DB["password"]}@'
            f'{DB["host"]}:{DB["port"]}/{DB["dbname"]}'
        )
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url

    app.app_context().push()
    db.init_app(app)
    db.create_all()  # TODO to flask-migrate

    return app


# TODO setup logging
