from flask import Flask

from .routes import blueprint


def init_app():
    app = Flask(__name__)
    app.register_blueprint(blueprint)

    return app


# TODO setup logging
