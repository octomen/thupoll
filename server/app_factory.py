from flask import Flask
from flask_migrate import Migrate

from .views.statistic import blueprint as statistic_blueprint
from .models import db
from .setings import env


def init_app(db_url=env.db_url):
    app = Flask(__name__)
    app.register_blueprint(statistic_blueprint, url_prefix='/')

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.app_context().push()
    Migrate(app, db)
    db.init_app(app)

    return app


# TODO setup logging
