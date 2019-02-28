import os

from flask import Flask
from flask_migrate import Migrate

from .views.statistic import blueprint as statistic_blueprint
from .models import db
from .config import DATABASE as DB


def init_app():
    app = Flask(__name__)
    app.register_blueprint(statistic_blueprint, url_prefix='/')

    db_url = os.environ.get('DB_URL')
    if not db_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            'postgresql://{user}:{password}@'
            '{host}:{port}/{dbname}'.format(**DB)
        )
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url

    app.app_context().push()
    Migrate(app, db)
    db.init_app(app)

    return app


# TODO setup logging
