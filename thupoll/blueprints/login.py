import datetime
import logging
import sqlalchemy as sa

from flask import Blueprint, make_response, abort, jsonify
from webargs import fields
from webargs.flaskparser import use_args
from thupoll.models import db, Token, Session


blueprint = Blueprint('login', __name__)
logger = logging.getLogger(__name__)


@blueprint.route('/', strict_slashes=False)
@use_args({
    'token': fields.Str(required=True),
}, error_status_code=401)
def login(args):
    # find token
    token = db.session.query(Token).filter(
        Token.value == args.get('token')
    ).filter(
        sa.or_(
            Token.expire > datetime.datetime.now(),
            Token.expire.is_(None)
        )
    ).one_or_none()
    if not token:
        abort(401)
    # make session
    session = Session(people_id=token.people_id)
    db.session.add(session)
    # remove temporary token
    db.session.delete(token)
    db.session.flush()
    db.session.commit()
    # make response
    response = make_response(jsonify({'Authentication': session.value}))
    response.set_cookie('Authentication', session.value)
    return response
