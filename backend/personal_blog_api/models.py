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
from .fulltext_search import add_to_index, remove_from_index, query_index

"""
    Integrate fulltext search to db
"""
class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db = SQLAlchemy()
db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

"""
    DATABASE
"""
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
                    last_login_at=int(self.last_login_at.replace(tzinfo=pytz.utc).timestamp()))

class Post(SearchableMixin, db.Model):
    __tablename__ = 'posts'
    __searchable__ = ['body']

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
        return '%d\t%d\t%s' % (self.id, self.author_id, self.header)

    def to_dict(self):
        comments = []
        for c in self.comments:
            comments.append(c.to_dict())

        tags = []
        for t in self.tags:
            tags.append(t.to_dict())

        return dict(post_id=self.id,
                    header=self.header,
                    body=self.body,
                    created_at=int(self.created_at.replace(tzinfo=pytz.utc).timestamp()),
                    last_edit_at=int(self.last_edit_at.replace(tzinfo=pytz.utc).timestamp()),
                    author_name=User.query.filter(User.id == self.author_id).first().username,
                    comments=comments,
                    tags=tags,
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
                    preview=preview,
                    created_at=int(self.created_at.replace(tzinfo=pytz.utc).timestamp()),
                    last_edit_at=int(self.last_edit_at.replace(tzinfo=pytz.utc).timestamp()),
                    author_name=User.query.filter(User.id == self.author_id).first().username,
                    comments=len(comments),
                    private_post=self.private_post)

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    def to_dict(self):
        return dict(tag_id=self.id,
                    tag_name=self.name)

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
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
