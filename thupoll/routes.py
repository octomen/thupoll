from thupoll.blueprints.home import blueprint as home_blueprint
from thupoll.blueprints.login import blueprint as login_blueprint
from thupoll.blueprints.themes import blueprint as themes_blueprint
from thupoll.blueprints.polls import blueprint as polls_blueprint
from thupoll.blueprints.me import blueprint as me_blueprint
from thupoll.blueprints.telegram.blueprint import telegram_blueprint


def routify(app):
    app.register_blueprint(home_blueprint)
    app.register_blueprint(themes_blueprint, url_prefix='/themes')
    app.register_blueprint(polls_blueprint, url_prefix='/polls')
    app.register_blueprint(login_blueprint, url_prefix='/login')
    app.register_blueprint(telegram_blueprint, url_prefix='/telegram')
    app.register_blueprint(me_blueprint, url_prefix='/me')
