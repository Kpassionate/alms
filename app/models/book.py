#!/user/bin/python
# _*_ coding:utf-8 _*_
# author: yk.guan

from .base import db, BaseModel


class Author(BaseModel):
    __tablename__ = 'author'
    name = db.Column(db.String(100), nullable=False)
    brief = db.Column(db.Text(), nullable=False)

    def keys(self):
        return ['id', 'name', 'brief']


class Category(BaseModel):
    __tablename__ = 'category'
    name = db.Column(db.String(100), nullable=False)

    def keys(self):
        return ['id', 'name']


class Book(BaseModel):
    __tablename__ = 'book'
    name = db.Column(db.String(50), nullable=False)
    author_id = db.Column(db.Integer(), db.ForeignKey('author.id'))
    category_id = db.Column(db.Integer(), db.ForeignKey('category.id'))
    isbn = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text(), nullable=False)

    image_url = db.Column(db.String(200), nullable=False)

    def keys(self):
        return ['id', 'name', 'author_id', 'category_id', 'isbn', 'content', 'image_url']
