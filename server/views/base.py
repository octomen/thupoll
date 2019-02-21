# coding: utf-8


from flask.views import View
from flask import request, render_template, abort
from flask.templating import TemplateNotFound


class BaseView(object):

    object_class = None
    template_name = ''

    def _get_template_name(self):
        if self.template_name:
            return self.template_name
        raise NotImplementedError()

    def _create_context(self, data=None):
        return {}

    def _render_template(self, context):
        return render_template(self._get_template_name(), **context)

    def dispatch_request(self):
        context = {}
        return self._render_template(context)



