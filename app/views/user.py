#!/user/bin/python
# _*_ coding:utf-8 _*_
# author: yk.guan
import random
import string
from flask import Blueprint, jsonify, request, g
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app.models.user import User
from utils.handle import ClientError, CreateSuccess, Success, ParameterError

mod = Blueprint('user', __name__)


# 生成用户名
def generate_username():
    u_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    username_str = 'lr-' + u_str
    # 如果用户表中存在该username 重新生成username
    if User.query.filter_by(username=username_str).first():
        return generate_username()

    return username_str


# 注册
@mod.route('/register/', methods=['get', 'post'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            user = User.query.filter_by(email=email).first()
            # 邮箱已注册
            if user:
                return ClientError(msg='this email has been registered, to login！')
            else:
                username = generate_username()
                user = User()
                user.username = username
                user.password = password
                user.email = email
                user.save()
                return CreateSuccess()
        else:
            return ClientError(msg='email or password can not empty！')


# 登录
@mod.route('/login/', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if user.check_password(password):
                # 使用唯一且不可变的 username 作为identity的值
                access_token = create_access_token(identity=user.username)
                # 返回用户email 和 token值
                return jsonify(email=email, token=access_token)
            else:
                return ClientError(msg='password error!')
        else:
            return ParameterError(msg='user account not exist!')


# 获取用户信息（仅返回本人信息）、修改用户信息
@mod.route('/client/info', methods=['GET', 'POST'])
@jwt_required
def user_info():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first_or_404()
    if request.method == 'GET':
        return jsonify(user)
    if request.method == 'POST':
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        gender = request.form.get('gender')
        if email and mobile and gender:
            user.email = email
            user.mobile = mobile
            # 传入参为Boolean值 传（0、1）
            user.gender = int(gender)
            user.merge()
            return jsonify(user)
        else:
            return ParameterError(msg='missing parameter!')


# 获取所有用户信息，仅测试使用，正常访问接口仅返回本人信息，切记
@mod.route('/all', methods=['GET'])
@jwt_required
def all_user():
    users = User.query.all()
    return jsonify(users)
