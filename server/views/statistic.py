# coding: utf-8

from flask import Blueprint
from flask import request, abort

from ..views.base import BaseView
from ..models import User, Lecture, db
from ..config import THEMES_LIMIT

blueprint = Blueprint('thursday', __name__)


class StatisticView(BaseView):

    object_class = None
    template_name = ''

    def _create_context(self, data=None):
        session = db.session
        created = session.query(Lecture).filter(Lecture.status == 'created').\
            order_by(Lecture.change_date).\
            limit(THEMES_LIMIT).all()
        planning = session.query(Lecture).filter(Lecture.status == 'planning'). \
            order_by(Lecture.change_date). \
            limit(THEMES_LIMIT).all()
        preparing = session.query(Lecture).filter(Lecture.status == 'preparing'). \
            order_by(Lecture.change_date). \
            limit(THEMES_LIMIT).all()
        discarded = session.query(Lecture).filter(Lecture.status == 'discarded'). \
            order_by(Lecture.change_date). \
            limit(THEMES_LIMIT).all()
        session.close()
        return {

        }

    def get(self):
        try:
            context = self._create_context()
            return self._render_template(context)
        except Exception as e:  # TODO
            abort(404)

    def post(self, *args, **kwargs):
        pass

    def dispatch_request(self, *args, **kwargs):
        if request.method == 'POST':
            return self.post(*args, **kwargs)
        return self.get(*args, **kwargs)


blueprint.add_url_rule('/statistic', view_func=StatisticView.as_view('statistic'))
