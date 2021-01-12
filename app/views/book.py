#!/user/bin/python
# _*_ coding:utf-8 _*_
# author: yk.guan
import os
import uuid

from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from werkzeug.utils import secure_filename

from app.models.book import Book
from app.validators.forms import BookSearchForm, BookAddForm
from utils.handle import CreateSuccess, ParameterError, DeleteSuccess
from utils.upload_utils import ALLOWED_EXTENSIONS
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

mod = Blueprint('book', __name__)


# 允许文件类型
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 对上传的文件重命名，避免重名覆盖
def rename_for_upload(filename):
    filename = secure_filename(filename).split('.')
    file_name = filename[0] + '_' + str(uuid.uuid1())[:6] + '.' + filename[1]
    return file_name


# 获取全部书籍信息
@mod.route('/all', methods=['GET'])
@jwt_required
def get_all_books():
    # current_user为使用token创建的username
    current_user = get_jwt_identity()
    books = Book.query.all()
    return jsonify(books)


# 获取书籍详情、删除选中书籍信息
@mod.route('/<id>', methods=['GET', 'DELETE'])
@jwt_required
def book_detail(id):
    if request.method == 'GET':
        book = Book.query.filter_by(id=id).first_or_404()
        return jsonify(book)
    elif request.method == 'DELETE':
        book = Book.query.filter_by(id=id).first_or_404()
        book.delete()
        return DeleteSuccess()


# 添加书籍
@mod.route('/add', methods=['POST'])
@jwt_required
def add_new_book():
    name = request.form.get('name')
    author_id = request.form.get('author_id')
    category_id = request.form.get('category_id')
    isbn = request.form.get('isbn')
    content = request.form.get('content')
    file = request.files['image_url']
    if file and allowed_file(file.filename):
        file_name = rename_for_upload(file.filename)
        # 注意：没有的文件夹一定要先创建，不然会提示没有该路径(一定要相对路径)
        upload_path = os.path.join('static/uploads/', file_name)
        file.save(upload_path)
        book = Book()
        book.name = name
        book.author_id = author_id
        book.category_id = category_id
        book.isbn = isbn
        book.content = content
        book.image_url = upload_path
        try:
            book.save()
            return CreateSuccess()
        except:
            return ParameterError()
    else:
        return ParameterError()


@mod.route('/add_new/', methods=['POST'])
def add_new():
    # 使用form重写添加书籍函数，使用form可以直接验证数据字段是否提交
    form = BookAddForm(request.form).validate_for_api()
    name = form.name.data
    author_id = form.author_id.data
    category_id = form.category_id.data
    isbn = form.isbn.data
    content = form.content.data
    # image_url 字段通过request获取
    file = request.files['image_url']
    if file and allowed_file(file.filename):
        file_name = rename_for_upload(file.filename)
        upload_path = os.path.join('static/uploads/', file_name)
        file.save(upload_path)
        book = Book()
        book.name = name
        book.author_id = author_id
        book.category_id = category_id
        book.isbn = isbn
        book.content = content
        book.image_url = upload_path
        book.save()
        return CreateSuccess()
    else:
        return ParameterError()


@mod.route('/search', methods=['GET'])
def search():
    form = BookSearchForm(request.form).validate_for_api()
    q = '%' + form.q.data + '%'
    books = Book.query.filter(
        or_(Book.name.like(q), Book.category_id.like(q))).all()
    return jsonify(books)


"""
我最爱去的唱片店，昨天是她的最后一天。
曾经让我陶醉的碎片，全都散落在街边。
我最爱去的书店，她也没撑过这个夏天。
回忆文字流淌着怀念，可是已没什么好怀念。
"""
