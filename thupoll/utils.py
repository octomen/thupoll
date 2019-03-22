import datetime
import sqlalchemy as sa

from flask import abort, g
from flask.json import JSONEncoder
from functools import wraps
from webargs import fields
from webargs.flaskparser import use_args

from thupoll.models import db, Role, Session


def check_auth(*roles):
    def wrapper(func):
        @wraps(func)
        @use_args(
            {'Authentication': fields.Str(required=True)},
            locations=("headers", "cookies"),
            error_status_code=401,
        )
        def wrap(args, *arg, **kw):
            # find session
            session = db.session.query(Session).filter(
                Session.value == args.get('Authentication')
            ).filter(
                sa.or_(
                    Session.expire > datetime.datetime.now(),
                    Session.expire.is_(None)
                )
            ).one_or_none()
            if not session:
                abort(401)
            # save user to flask-session
            g.people = session.people
            # check role
            if session.people.role_id not in roles:
                abort(403)
            return func(*arg, **kw)
        return wrap
    return wrapper


for_admins = check_auth(Role.OCTOPUS)
for_auth = check_auth(Role.OCTOPUS, Role.INHABITANT)


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()

        return super().default(o)
