from thupoll.blueprints.home import blueprint as home_blueprint
from thupoll.blueprints.themes import blueprint as themes_blueprint
from thupoll.blueprints.telegram.blueprint import telegram_blueprint


def routify(app):
    app.register_blueprint(home_blueprint)
    app.register_blueprint(themes_blueprint, url_prefix='/themes')
    app.register_blueprint(telegram_blueprint, url_prefix="/telegram")
