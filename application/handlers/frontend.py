# coding=utf-8
from application.handlers import Route, BaseHandler
from application.forms.frontend import TestForm


@Route('/')
class FrontendHandler(BaseHandler):
    def get(self):
        return self.render('index.html')

    def post(self):
        form = TestForm(self)
        print form.test.data
        return self.write('success')
