import datetime

from functools import wraps

from flask import make_response
from flask.json import JSONEncoder


def _access_control_allow_origin(func):
    @wraps(func)
    def wrap(*arg, **kw):
        response = func(*arg, **kw)
        response = make_response(response)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    return wrap


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()

        return super().default(o)
