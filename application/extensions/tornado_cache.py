# coding=utf-8
import functools


class TornadoRedisCache(object):
    def __init__(self):
        self.cache_key_prefix = 'CACHE_VIEW_'
        self.app = None

    def init_app(self, app):
        self.app = app
        app.cache = self

    def cached(self, timeout=None):
        """
        给视图方法增加数据返回时的缓存装饰器
        用法:
            Class Handler(tornado.web.RequestHandler):
                @cache.cached(10)
                def get(self):
                    return self.write('test')
        :param timeout: 缓存超时秒数, 不填则永不过期
        """
        def decorator(f):
            @functools.wraps(f)
            def decorated_function(handler, *args, **kwargs):
                cache_key = self._generate_cache_key(handler.request)
                cache_value = self.get(cache_key)
                if cache_value:
                    return handler.write(cache_value)
                else:
                    def finish():
                        _buffer = ''.join(handler.cache_buffer)
                        if not callable(timeout):
                            self.set(cache_key, _buffer, timeout)

                        else:
                            self.set(cache_key, _buffer)
                    handler.on_finish()
                    handler.on_finish = finish
                    handler.cache_buffer = handler._write_buffer
                    return f(handler, *args, **kwargs)
            return decorated_function

        if callable(timeout):
            return decorator(timeout)
        else:
            return decorator

    def clear(self):
        keys = self.app.redis.keys(self.cache_key_prefix + '*')
        if not keys:
            return
        self.app.redis.delete(*keys)

    def _generate_cache_key(self, request):
        cache_key = self.cache_key_prefix + request.uri
        return cache_key

    def get(self, key):
        return self.app.redis.get(key)

    def set(self, key, value, timeout=None):
        self.app.redis.set(key, value, timeout)

cache = TornadoRedisCache()
