# coding=utf-8
from wtforms import form

from tornado import escape
from tornado.web import HTTPError


class TornadoInputWrapper(object):

    def __init__(self, multi_dict):
        self._wrapped = multi_dict

    def __iter__(self):
        return iter(self._wrapped)

    def __len__(self):
        return len(self._wrapped)

    def __contains__(self, name):
        return (name in self._wrapped)

    def __getitem__(self, name):
        return self._wrapped[name]

    def __getattr__(self, name):
        return self.__getitem__(name)

    def getlist(self, name):
        try:
            return [escape.to_unicode(v) for v in self._wrapped[name]]
        except KeyError:
            return []


class Form(form.Form):
    """
    为 RESTful 接口提供表单验证
    """

    def __init__(self, handler=None, obj=None, prefix='', locale_code='en_US', **kwargs):
        self._locale_code = locale_code
        self._handler = handler
        super(Form, self).__init__(handler.request.arguments, obj, prefix, **kwargs)

    def process(self, formdata=None, obj=None, **kwargs):
        if formdata is not None and not hasattr(formdata, 'getlist'):
            formdata = TornadoInputWrapper(formdata)
        super(Form, self).process(formdata, obj, **kwargs)
        if not self.validate():
            self._handler.set_status(400)
            self._handler.finish(self.errors)
            raise HTTPError(400)


__all__ = ['Form']
