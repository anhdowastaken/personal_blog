"""
models.py
- Data classes for the gameapi application
"""

from datetime import datetime
from hashlib import md5
import pytz
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from .application import bcrypt

db = SQLAlchemy()

post_tag = db.Table('posts_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(16), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def __repr__(self):
        return '%d\t%s\t%s\t%s' % (self.id, self.username, self.email, self.last_login_at.strftime('%Y-%m-%d %H:%M:%S'))

    def to_dict(self):
        return dict(user_id=self.id,
                    email=self.email,
                    username=self.username,
                    last_login_at=self.last_login_at)

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    header = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_edit_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comments = db.relationship('Comment', backref='comment', lazy='dynamic')
    tags = db.relationship('Tag',
                           secondary=post_tag,
                           lazy='subquery',
                           backref=db.backref('posts', lazy=True))
    private_post = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '%d\t%d\t%s' % (self.id, self.user_id, self.header)

    def to_dict(self):
        comments = []
        for c in self.comments:
            comments.append(c.to_dict())

        return dict(post_id=self.id,
                    header=self.header,
                    body=self.body,
                    last_edit_at=int(self.last_edit_at.replace(tzinfo=pytz.utc).timestamp()),
                    author_name=User.query.filter(User.id == self.author_id).first().username,
                    comments=comments,
                    private_post=self.private_post)

    def to_dict_simple(self):
        comments = []
        for c in self.comments:
            comments.append(c.to_dict())

        import re
        html_tags = re.compile('<.*?>')
        clean_body = re.sub(html_tags, '', self.body)
        preview = ' '.join(clean_body.split()[:20])
        if preview != clean_body:
            preview = preview + '&hellip;'
        import html
        preview = html.unescape(preview)

        return dict(post_id=self.id,
                    header=self.header,
                    body=self.body,
                    last_edit_at=int(self.last_edit_at.replace(tzinfo=pytz.utc).timestamp()),
                    author_name=User.query.filter(User.id == self.author_id).first().username,
                    comments=len(comments),
                    private_post=self.private_post)

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_edit_at = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    author_name = db.Column(db.String(64), nullable=False)
    author_email = db.Column(db.String(128), nullable=False)
    belong_to_post_author = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '%d\t%d\t%s' % (self.id, self.post_id, self.author_email)

    def to_dict(self):
        digest = md5(self.author_email.lower().encode('utf-8')).hexdigest()
        avatar = 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, 50)

        return dict(comment_id=self.id,
                    content=self.content,
                    author_name=self.author_name,
                    author_avatar=avatar,
                    created_at=int(self.created_at.replace(tzinfo=pytz.utc).timestamp()))
