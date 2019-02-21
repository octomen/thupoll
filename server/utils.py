from functools import wraps

from flask import make_response


def _access_control_allow_origin(func):
    @wraps(func)
    def wrap(*arg, **kw):
        response = func(*arg, **kw)
        response = make_response(response)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    return wrap