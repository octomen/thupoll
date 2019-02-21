# coding: utf-8


from views.base import BaseView
from models import User, Lecture, get_session
from flask import request, abort
from config import THEMES_LIMIT


class StatisticView(BaseView):

    template_name = ''

    def _create_data(self):
        session = get_session()
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
        done = session.query(Lecture).filter(Lecture.status == 'done'). \
            order_by(Lecture.change_date). \
            limit(THEMES_LIMIT).all()
        session.close()
        return dict(
            created=[obj.asdict() for obj in created],
            planning=[obj.asdict() for obj in planning],
            preparing=[obj.asdict() for obj in preparing],
            discarded=[obj.asdict() for obj in discarded],
            done=[obj.asdict() for obj in done]
        )

    def get(self, *args, **kwargs):
        try:
            return self._create_data()
        except Exception:
            abort(404)

    def post(self, *args, **kwargs):
        pass

    def dispatch_request(self, *args, **kwargs):
        if request.method == 'POST':
            return self.post(*args, **kwargs)
        return self.get(*args, **kwargs)
