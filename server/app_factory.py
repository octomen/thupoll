import os

from flask import Flask

from .views.statistic import blueprint as statistic_blueprint
from .models import db
from .config import DATABASE as DB


def entrypoint_db():
    init_app(mode='db')


def init_app(mode='app'):
    app = Flask(__name__)
    app.register_blueprint(statistic_blueprint, url_prefix='/distribution')

    db_url = os.environ.get('DB_URL')
    if not db_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            'postgresql://{user}:{password}@{host}:{port}/{dbname}'.format(user=DB["user"], password=DB["password"], host=DB["host"], port=DB["port"], dbname=DB["dbname"])
        )
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url

    app.app_context().push()
    db.init_app(app)

    if mode == 'db':
        db.create_all()  # TODO to flask-migrate

    if mode == 'app':
        return app


# TODO setup logging
