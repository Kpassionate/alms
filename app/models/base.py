#!/user/bin/python
# _*_ coding:utf-8 _*_
# author: yk.guan
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from utils.handle import NotFound


# 重写第三方库方法，及SQLAlchemy中的query_class对应的BaseQuery
class Query(BaseQuery):
    """
    重写get_or_404和 first_or_404方法
    """

    def get_or_404(self, ident, description=None):
        """Like :meth:`get` but aborts with 404 if not found instead of returning ``None``."""
        rv = self.get(ident)
        if rv is None:
            raise NotFound()
        return rv

    def first_or_404(self, description=None):
        """Like :meth:`first` but aborts with 404 if not found instead of returning ``None``."""
        rv = self.first()
        if rv is None:
            raise NotFound()
        return rv


db = SQLAlchemy(query_class=Query)  # 实例化数据库


class BaseModel(db.Model):
    __abstract__ = True  # 声明当前类为抽象类，可以被继承调用，不会被创建
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    create_at = db.Column(db.DATETIME, default=datetime.now())

    def __getitem__(self, item):
        return getattr(self, item)

    def keys(self):
        return self.fields if hasattr(self, 'fields') else []

    # 此函数作用？
    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    # 增加
    def save(self):
        db.session.add(self)
        db.session.commit()

    # 修改
    def merge(self):
        db.session.merge(self)
        db.session.commit()

    # 删除
    def delete(self):
        db.session.delete(self)
        db.session.commit()
