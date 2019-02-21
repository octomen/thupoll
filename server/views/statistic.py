# coding: utf-8

from flask import Blueprint

from views.base import BaseView
from models import User, Lecture, get_session

blueprint = Blueprint('thursday', __name__)


class StatisticView(BaseView):

    object_class = None
    template_name = ''

    def _create_context(self, data=None):
        session = get_session()
        select = session.query(Lecture).filter(Product.url.is_(None), getattr(Product, field).is_(None)).limit(limit).all()
        session.close()
        return {

        }

    def get(self):
        try:
            context = self._create_context()
            return self._render_template(context)
        except (TemplateNotFound, DataValidateException, ):
            abort(404)

    def post(self, *args, **kwargs):
        pass

    def dispatch_request(self, *args, **kwargs):
        if request.method == 'POST':
            return self.post(*args, **kwargs)
        return self.get(*args, **kwargs)


blueprint.add_url_rule('/statistic', view_func=StatisticView.as_view('statistic'))
