# coding: utf-8


from flask import Flask
from views import statistic


app = Flask(__name__)
app.register_blueprint(statistic, url_prefix='/distribution')
