"""
models.py
- Data classes for the gameapi application
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from .application import bcrypt

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    role = db.Column(db.String, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def __repr__(self):
        return '%d\t%s\t%s\t%s' % (self.id, self.username, self.role, self.last_login_at.strftime('%Y-%m-%d %H:%M:%S'))

    def to_dict(self):
        return dict(user_id=self.id,
                    username=self.username,
                    last_login_at=self.last_login_at)

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    header = db.Column(db.Text)
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_edit_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='comment', lazy='dynamic')
    tags = db.relationship('Tag',
                           secondary=tags,
                           lazy='subquery',
                           backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '%d\t%d\t%s' % (self.id, self.user_id, self.header)

    def to_dict(self):
        return dict(post_id=self.id,
                    user_id=self.user_id,
                    header=self.header)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_edit_at = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    author_name = db.Column(db.String)
    author_email = db.Column(db.String)
    belong_to_post_author = db.Column(db.Boolean, default=False)

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)
