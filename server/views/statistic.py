# coding: utf-8

from flask import Blueprint
from flask import request, abort
from flask import jsonify

from ..views.base import BaseView
from ..models import People, Theme, db
from ..config import THEMES_LIMIT
from ..utils import _access_control_allow_origin

blueprint = Blueprint('thursday', __name__)


class StatisticView(BaseView):

    template_name = ''

    def _create_data(self):
        session = db.session
        created = session.query(Theme).filter(Theme.status == 'create').\
            order_by(Theme.change_date).\
            limit(THEMES_LIMIT).all()
        planning = session.query(Theme).filter(Theme.status == 'planning'). \
            order_by(Theme.change_date). \
            limit(THEMES_LIMIT).all()
        preparing = session.query(Theme).filter(Theme.status == 'preparing'). \
            order_by(Theme.change_date). \
            limit(THEMES_LIMIT).all()
        discarded = session.query(Theme).filter(Theme.status == 'discarded'). \
            order_by(Theme.change_date). \
            limit(THEMES_LIMIT).all()
        done = session.query(Theme).filter(Theme.status == 'done'). \
            order_by(Theme.change_date). \
            limit(THEMES_LIMIT).all()
        session.close()
        return jsonify(dict(
            created=[obj.asdict() for obj in created],
            planning=[obj.asdict() for obj in planning],
            preparing=[obj.asdict() for obj in preparing],
            discarded=[obj.asdict() for obj in discarded],
            done=[obj.asdict() for obj in done]
        ))

    def get(self, *args, **kwargs):
        try:
            return self._create_data()
        except Exception as e:
            abort(404)

    def post(self, *args, **kwargs):
        pass

    def dispatch_request(self, *args, **kwargs):
        if request.method == 'POST':
            return self.post(*args, **kwargs)
        return self.get(*args, **kwargs)


@blueprint.route('/')
@_access_control_allow_origin
def home():
    return jsonify(ok='ok')


@blueprint.route("/poll/lst", methods=["GET", "POST"])
@_access_control_allow_origin
def poll_lst():
    return jsonify({
        "themes": [
            "blah1",
            "blah2",
            "blah3",
            "blah4",
            "blah4",
            "blahsdfhth4",
            "blah4",
            "blah4",
            "asd",
        ]
    })


blueprint.add_url_rule('/statistic', view_func=StatisticView.as_view('statistic'))
