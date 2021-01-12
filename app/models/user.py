#!/user/bin/python
# _*_ coding:utf-8 _*_
# author: yk.guan
from werkzeug.security import generate_password_hash, check_password_hash

from .base import db, BaseModel


class User(BaseModel):
    username = db.Column(db.String(20), unique=True, nullable=False)
    _password = db.Column(db.String(100), nullable=False)  # 内部使用
    email = db.Column(db.String(24), unique=True, nullable=False)
    mobile = db.Column(db.String(11))
    gender = db.Column(db.Boolean(), default=True, nullable=False)

    def __str__(self):
        return self.username

    def keys(self):
        return ['id', 'username', 'email', 'gender', 'mobile']

    @property
    def password(self):  # 外部使用：取值
        return self._password

    @password.setter
    def password(self, raw):  # 外部使用：赋值
        self._password = generate_password_hash(raw)

    def check_password(self, raw):  # 密码验证
        if not self._password:
            return False
        return check_password_hash(self._password, raw)
