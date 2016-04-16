# coding=utf-8
from application.handlers import Route, BaseHandler


@Route('/')
class FrontendHandler(BaseHandler):
    def get(self):
        return self.render('index.html')
