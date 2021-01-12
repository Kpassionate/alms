#!/user/bin/python
# _*_ coding:utf-8 _*_
# author: yk.guan
from wtforms import StringField, IntegerField, SelectField, FileField
from wtforms.validators import DataRequired

from app.validators.base import BaseForm


class BookSearchForm(BaseForm):
    q = StringField(validators=[DataRequired()])


class BookAddForm(BaseForm):
    name = StringField(validators=[DataRequired(message='不能为空')])
    author_id = IntegerField(validators=[DataRequired()])
    category_id = IntegerField(validators=[DataRequired()])
    isbn = StringField(validators=[DataRequired(message='不能为空')])
    content = StringField()
