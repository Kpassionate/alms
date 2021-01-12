#!/user/bin/python
# _*_ coding:utf-8 _*_
# author: yk.guan

from flask.json import JSONEncoder as _JSONEncoder
from flask import Flask as _Flask
from datetime import date


class JSONEncoder(_JSONEncoder):
    """
    重写json序列化， 让实例对象可序列化
    """

    def default(self, o):
        # 将数据模型中的keys中包含的字段序列化，
        # 定义数据模型时需要同时定义keys函数及getitem函数
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        super().default(o)  # 在python3中直接用super()代替super（JSONEncoder, self）.default(o)


class Flask(_Flask):
    json_encoder = JSONEncoder
