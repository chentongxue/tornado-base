# coding=utf-8
from wtforms.fields import StringField
from wtforms.validators import DataRequired, Length

from application.extensions.tornado_wtforms import Form


class TestForm(Form):
    test = StringField(u'', [DataRequired(u'test 不能为空'), Length(min=11, max=11, message=u'长度必须是11位')])

