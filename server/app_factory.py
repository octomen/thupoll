from flask import Flask

from .views.statistic import blueprint as statistic_blueprint


def init_app():
    app = Flask(__name__)
    app.register_blueprint(statistic_blueprint, url_prefix='/distribution')

    return app


# TODO setup logging
