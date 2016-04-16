# coding=utf-8
from redis import Redis


class TornadoRedis:
    def __init__(self, app=None):
        self.app = app

    def init_app(self, app):
        if not self.app:
            self.app = app
        connection = Redis(
            host=app.settings.get('REDIS_HOST', 'localhost'),
            port=app.settings.get('REDIS_PORT', 6379),
            db=app.settings.get('REDIS_DB', 0),
            password=app.settings.get('REDIS_PASSWORD'),
        )
        app.redis = connection
        return connection

redis = TornadoRedis()
