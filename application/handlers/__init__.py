# coding=utf-8
import functools
from tornado.escape import json_encode
from tornado.web import RequestHandler, HTTPError, URLSpec


class BaseHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.set_status(405)
        return self.write(u'不支持 GET 方法')

    def post(self, *args, **kwargs):
        self.set_status(405)
        return self.write(u'不支持 POST 方法')

    def put(self):
        self.set_status(405)
        return self.write(u'不支持 PUT 方法')

    def delete(self):
        self.set_status(405)
        return self.write(u'不支持 DELETE 方法')

    def jsonify(self, obj):
        return self.write(json_encode(obj))

    @property
    def redis(self):
        return self.application.redis

    @property
    def db(self):
        return self.application.mysql_db


def login_required(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper


class Route(object):
    """
    视图类装饰器, 直接给视图类绑定路由
    用法:
        @Route('/')
        Class Handler(tornado.web.RequestHandler):
            pass
    """
    _routes = []

    def __init__(self, route, host=".*$", name=None, initialize={}):
        self.route = route
        self.host = host
        self.name = name
        self.initialize = initialize

    def __call__(self, handler):
        name = self.name or handler.__name__
        spec = URLSpec(self.route, handler, self.initialize, name=name)
        self._routes.append({'host': self.host, 'spec': spec})
        return handler

    @classmethod
    def register_routes(cls, application=None):
        """
        将路由注册到application实例
        :param application: application实例
        """
        if application:
            for _route in cls._routes:
                application.add_handlers(_route['host'], [_route['spec']])
        else:
            return [_route['spec'] for _route in cls._routes]
