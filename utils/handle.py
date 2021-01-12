#!/user/bin/python
# _*_ coding:utf-8 _*_
# author: yk.guan
from flask import json, request
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    msg = 'sorry, we made a mistake (·。·)'

    def __init__(self, msg=None, code=None, headers=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        super(APIException, self).__init__(self.msg, None)

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            code=self.code,
            request=request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        """get a json header"""
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]


class Success(APIException):
    code = 200
    msg = 'success'


class CreateSuccess(APIException):
    code = 201  # 创建成功
    msg = 'created success'


class DeleteSuccess(APIException):
    code = 202  # 删除成功  (204为删除成功状态码，但是其不返回任何值，为保持一致返回202)
    msg = 'delete success'


class ServerError(APIException):
    code = 500  # 服务器错误
    msg = 'sorry, we made a mistake .'


class ClientError(APIException):
    code = 400  # 客户端错误
    msg = 'clients is invalid'


class ParameterError(APIException):
    code = 400  # 参数无效
    msg = 'invalid parameter'


class NotFound(APIException):
    code = 404  # not found
    msg = 'the resource are not found o_o'


class MethodNotAllowed(APIException):
    code = 405  # 请求方法不被允许
    msg = 'the request method is not allowed o_o'


class AuthFailed(APIException):
    code = 401  # 授权失败 Unauthorized
    msg = 'not auth'


class Forbidden(APIException):
    code = 403  # 无权限访问
    msg = 'not auth'
