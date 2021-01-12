#!/user/bin/python
# _*_ coding:utf-8 _*_
# author: yk.guan
from flask import request
from wtforms import Form

from utils.handle import ParameterError


class BaseForm(Form):
    """
    由于From表单在validate的时候并不会抛出异常而是将异常信息放在errors参数中，
    所以在此继承Form写一个自动校验并抛出异常的方法
    """
    def __init__(self, formdata=None, obj=None, prefix='', data=None, meta=None, **kwargs):
        # 请查看源码，重写init方法，以避免获取不到数据而报错
        # get方法时从参数中获取数据，如url: http://127.0.0.1:5000/api/book/search?q=1
        # post 等其他方法从body中获取，传参时以form-data方式传输数据
        if request.method == 'GET':
            data = request.get_json(silent=True)
            kwargs = request.args.to_dict()
            super(BaseForm, self).__init__(data=data, **kwargs)
        else:
            super(BaseForm, self).__init__(formdata, **kwargs)

    # 自定义验证失败抛出异常方法
    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            raise ParameterError(msg=self.errors)

        return self
