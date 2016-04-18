# coding=utf-8
import os

import tornado.web
import tornado.log
from tornado.ioloop import IOLoop

from application.utils.libs import ConfigParser
from application.extensions.tornado_redis import redis
from application.extensions.tornado_sqlalchemy import db
from application.extensions.tornado_cache import cache
from application.handlers import Route
from application.handlers.frontend import *


class Application(tornado.web.Application):
    def __init__(self, cfg):
        settings = ConfigParser(cfg)
        super(Application, self).__init__(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            autoreload=settings.get('DEBUG'),
            **settings
        )

        Route.register_routes(self)

        self._register_extensions()
        self._print_starting_info()

    def _register_extensions(self):
        """
            初始化所有扩展
        """
        redis.init_app(self)
        db.init_app(self)
        cache.init_app(self)

    def run(self):
        tornado.log.enable_pretty_logging()
        self.listen(self.settings.get('PORT', 8888))
        IOLoop.current().start()

    def _print_starting_info(self):
        print ' * Running on http://{HOST}:{PORT}/ (Press CTRL+C to quit)'.format(
            HOST=self.settings.get('HOST', '127.0.0.1'),
            PORT=self.settings.get('PORT', 8888),
        )
