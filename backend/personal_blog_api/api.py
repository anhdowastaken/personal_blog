"""
api.py
- Provide the API endpoints for consuming and producing
  REST requests and responses
"""

import json
import requests
import random
import string
import copy
from datetime import datetime, timedelta
import time
from dateutil import parser
from dateutil.tz import UTC
import pytz
from functools import wraps
from flask import Blueprint, jsonify, request, Response, redirect, session
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import SQLAlchemyError
import jwt
from .application import bcrypt
from .application import app_logger
from .config import BaseConfig
from .models import db, User, Post, Comment, Tag

api = Blueprint('api', __name__)

def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Re-authentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, BaseConfig().SECRET_KEY)
            user = User.query.filter_by(id=data['sub']).first()
            if not user:
                return jsonify(dict(message="Can't recognize user stored in token",
                                    authenticated=False)), 401
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError) as e:
            app_logger.debug(e)
            return jsonify(invalid_msg), 401
        except (Exception) as e:
            app_logger.debug(e)
            return jsonify(dict(message="Backend error",
                                authenticated=False)), 500

    return _verify

@api.route('/reset_password', methods=['POST'])
@token_required
@login_required
def reset_password(jwt_user):
    if jwt_user.id != current_user.id:
        # User ID stored in JWT token does not match the one stored in session
        # It's better to re-authenticate
        return jsonify(dict(message='Re-authentication required', registered=False)), 401

    # Only admin has permission to reset password
    if current_user.role != 'admin':
        return jsonify(dict(message='Permission denied', registered=False)), 403

    data = request.get_json()
    username = data['username']
    registered_user = User.query.filter_by(username=username).first()
    if registered_user is not None:
        # Generate random string containing 8 characters
        password = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        registered_user.password = password_hash
        try:
            db.session.commit()
            return jsonify(dict(message='Reset successfully',
                                registered=True,
                                user_data=dict(id=registered_user.id,
                                               username=username,
                                               password=password,
                                               role=registered_user.role))), 201
        except (SQLAlchemyError) as e:
            app_logger.debug(e)
            db.session.rollback()
            return jsonify(dict(message='Reset failed', registered=False)), 500
    else:
        return jsonify(dict(message='User doesn\'t exist', registered=False)), 400

@api.route('/login', methods=['POST'])
def login():
    session.permanent = True
    data = request.get_json()
    username = data['username']
    password = data['password']

    app_logger.info('{} is trying to login...'.format(username))

    registered_user = User.query.filter_by(username=username).first()
    if registered_user is None or bcrypt.check_password_hash(registered_user.password, password) == False:
        app_logger.info('-> Failed: Username or password is invalid')
        return jsonify(dict(message='Username or password is invalid', authenticated=False)), 401

    last_login_at = registered_user.last_login_at
    registered_user.last_login_at = datetime.utcnow()

    db.session.add(registered_user)
    try:
        db.session.commit()
    except (SQLAlchemyError) as e:
        app_logger.debug(e)
        db.session.rollback()

    if login_user(registered_user):
        token = jwt.encode({
            'sub': registered_user.id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=24)}, BaseConfig().SECRET_KEY)

        app_logger.info('-> Successfully')
        return jsonify(dict(message='Logged in successfully',
                            authenticated=True,
                            token=token.decode('utf-8'),
                            user_data=registered_user.to_dict())), 200
    else:
        app_logger.info('-> Failed: No session information')
        return jsonify(dict(message='Logged in failed', authenticated=False)), 500

@api.route('/logout', methods=['POST'])
def logout():
    logout_user()
    session.clear()

    return jsonify(dict(message='Logged out successfully')), 200

@api.route('/change_password', methods=['PUT'])
@token_required
@login_required
def change_password(jwt_user):
    if jwt_user.id != current_user.id:
        return jsonify(dict(message='Re-authentication required')), 401

    data = request.get_json()
    old_password = data['old_password']
    new_password = data['new_password']

    if old_password == '':
        return jsonify(dict(message='Old password can\'t be empty', changed=False)), 400

    if new_password == '':
        return jsonify(dict(message='New password can\'t be empty', changed=False)), 400

    registered_user = User.query.filter_by(id=jwt_user.id).first()
    if registered_user is None or bcrypt.check_password_hash(registered_user.password, old_password) == False:
        return jsonify(dict(message='Old password is incorrect', changed=False)), 400

    password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
    registered_user.password = password_hash
    try:
        db.session.commit()
        return jsonify(dict(message='Password is changed successfully',
                            changed=True)), 200
    except (SQLAlchemyError) as e:
        app_logger.debug(e)
        db.session.rollback()
        return jsonify(dict(message='Changed failed', registered=False)), 500

@api.route('/get_all_posts', methods=['GET'])
@token_required
@login_required
def get_all_posts(jwt_user):
    if jwt_user.id != current_user.id:
        return jsonify(dict(message='Re-authentication required')), 401

    registered_user = User.query.filter_by(id=jwt_user.id).first()
    if registered_user is None:
        return jsonify(dict(message='Permission denied')), 401

    page = request.args.get('page', 1, type=int)
    posts_per_page = BaseConfig().POSTS_PER_PAGE
    all_posts = get_posts(registered_user.id, True, page, posts_per_page)

    json_all_posts = []
    for p in all_posts.items:
        json_all_posts.append(p.to_dict_simple())

    return jsonify(dict(posts=json_all_posts,
                        has_next=all_posts.has_next,
                        has_prev=all_posts.has_prev,
                        next_num=all_posts.next_num,
                        prev_num=all_posts.prev_num)), 200

@api.route('/get_public_posts', methods=['GET'])
def get_public_posts():
    page = request.args.get('page', 1, type=int)
    posts_per_page = BaseConfig().POSTS_PER_PAGE
    all_posts = get_posts(None, False, page, posts_per_page)

    json_all_posts = []
    for p in all_posts.items:
        json_all_posts.append(p.to_dict_simple())

    return jsonify(dict(posts=json_all_posts,
                        has_next=all_posts.has_next,
                        has_prev=all_posts.has_prev,
                        next_num=all_posts.next_num,
                        prev_num=all_posts.prev_num)), 200

def get_posts(author_id, including_private, page, posts_per_page):
    if author_id is None:
        return Post.query.filter(Post.private_post == False).order_by(Post.created_at.desc()).paginate(page, posts_per_page, False)

    if including_private == True:
        return Post.query.filter(Post.author_id == author_id).order_by(Post.created_at.desc()).paginate(page, posts_per_page, False)
    else:
        return Post.query.filter(Post.author_id == author_id).filter(Post.private_post == False).order_by(Post.created_at.desc()).paginate(page, posts_per_page, False)

@api.route('/create_new_post', methods=['POST'])
@token_required
@login_required
def create_new_post(jwt_user):
    if jwt_user.id != current_user.id:
        return jsonify(dict(message='Re-authentication required', created=False)), 401

    registered_user = User.query.filter_by(id=jwt_user.id).first()
    if registered_user is None:
        return jsonify(dict(message='Permission denied', created=False)), 401

    data = request.get_json()
    header = data['header']
    body = data['body']
    tags = data['tags']
    private_post = data['private_post']

    post_tags = []
    for t in tags:
        tag = Tag.query.filter(Tag.name == t).first()
        if tag is None:
            tag = Tag()
            tag.name = t
            db.session.add(tag)
        post_tags.append(tag)

    post = Post()
    post.header = header
    post.body = body
    post.author_id = jwt_user.id
    post.tags = post_tags
    post.private_post = private_post
    db.session.add(post)

    try:
        db.session.commit()
        return jsonify(dict(message='New post was created successfully',
                            created=True)), 201
    except (SQLAlchemyError) as e:
        app_logger.debug(e)
        db.session.rollback()
        return jsonify(dict(message='Create new post failed', created=False)), 500

@api.route('/get_post', methods=['GET'])
def get_post():
    auth_headers = request.headers.get('Authorization', '').split()
    post_id = request.args.get('post_id')
    registered_user = None

    if auth_headers:
        if len(auth_headers) != 2:
            return jsonify(dict(message="Invalid token. Authentication required",
                                get=False)), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, BaseConfig().SECRET_KEY)
            registered_user = User.query.filter_by(id=data['sub']).first()
            if not registered_user:
                return jsonify(dict(message="Can't recognize user stored in token",
                                    get=False)), 401
        except jwt.ExpiredSignatureError:
            return jsonify(dict(message="Expired token. Re-authentication required.",
                                get=False)), 401
        except (jwt.InvalidTokenError) as e:
            app_logger.debug(e)
            return jsonify(dict(message="Invalid token. Authentication required",
                                get=False)), 401
        except (Exception) as e:
            app_logger.debug(e)
            return jsonify(dict(message="Backend error",
                                get=False)), 401

    post = None
    if registered_user:
        post = Post.query.filter(Post.id == post_id).filter(Post.author_id == registered_user.id).first()
    else:
        post = Post.query.filter(Post.id == post_id).filter(Post.private_post == False).first()

    if post:
        return jsonify(post.to_dict()), 200
    else:
        return jsonify(dict(message="Post doesn't exist",
                            get=False)), 404

@api.route('/post_comment', methods=['POST'])
def post_comment():
    auth_headers = request.headers.get('Authorization', '').split()
    data = request.get_json()
    post_id = data['post_id']
    content = data['content']
    author_name = data['author_name']
    author_email = data['author_email']
    registered_user = None

    post = Post.query.filter(Post.id == post_id).first()
    if post is None:
        return jsonify(dict(message="Post doesn't exist",
                            created=False)), 404

    if author_name == '':
        return jsonify(dict(message="Author name must not be empty",
                            created=False)), 400

    if author_email == '':
        return jsonify(dict(message="Author email must not be empty",
                            created=False)), 400

    if content == '':
        return jsonify(dict(message="Content must not be empty",
                            created=False)), 400

    if auth_headers:
        if len(auth_headers) != 2:
            return jsonify(dict(message="Invalid token. Authentication required",
                                created=False)), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, BaseConfig().SECRET_KEY)
            registered_user = User.query.filter_by(id=data['sub']).first()
            if not registered_user:
                return jsonify(dict(message="Can't recognize user stored in token",
                                    created=False)), 401
        except jwt.ExpiredSignatureError:
            return jsonify(dict(message="Expired token. Re-authentication required.",
                                created=False)), 401
        except (jwt.InvalidTokenError) as e:
            app_logger.debug(e)
            return jsonify(dict(message="Invalid token. Authentication required",
                                created=False)), 401
        except (Exception) as e:
            app_logger.debug(e)
            return jsonify(dict(message="Backend error",
                                created=False)), 401
    else:
        if not 'recaptcha_response' in data:
           return jsonify(dict(message="reCaptcha is invalid",
                               created=False)), 400

        recaptcha_response = data['recaptcha_response']
        if recaptcha_response is None or recaptcha_response == '' or not is_human(recaptcha_response):
           return jsonify(dict(message="reCaptcha is invalid",
                               created=False)), 400

    comment = Comment()
    comment.post_id = post_id
    comment.content = content
    if registered_user:
        comment.author_name = registered_user.username
        comment.author_email = registered_user.email
        comment.belong_to_post_author = True
    else:
        comment.author_name = author_name
        comment.author_email = author_email
        comment.belong_to_post_author = False

    db.session.add(comment)
    try:
        db.session.commit()
        return jsonify(dict(message='New comment was posted successfully',
                            created=True,
                            comment=comment.to_dict())), 201
    except (SQLAlchemyError) as e:
        app_logger.debug(e)
        db.session.rollback()
        return jsonify(dict(message='Post new comment failed', created=False)), 500

@api.route('/delete_post', methods=['DELETE'])
@token_required
@login_required
def delete_post(jwt_user):
    if jwt_user.id != current_user.id:
        return jsonify(dict(message='Re-authentication required', deleted=False)), 401

    registered_user = User.query.filter_by(id=jwt_user.id).first()
    if registered_user is None:
        return jsonify(dict(message='Permission denied', deleted=False)), 401

    data = request.get_json()
    post_id = data['post_id']

    post = Post.query.filter(Post.id == post_id).first()
    if post is None:
        return jsonify(dict(message="Post doesn't exist",
                            deleted=False)), 404

    # Delete all comments of post first
    comments = Comment.query.filter(Comment.post_id == post_id).all()
    for c in comments:
        db.session.delete(c)

    # Delete post
    db.session.delete(post)
    try:
        db.session.commit()
        return jsonify(dict(message='Post was deleted successfully',
                            deleted=True)), 200
    except (SQLAlchemyError) as e:
        app_logger.debug(e)
        db.session.rollback()
        return jsonify(dict(message='Delete post failed', deleted=False)), 500

@api.route('/update_post', methods=['PUT'])
@token_required
@login_required
def update_post(jwt_user):
    if jwt_user.id != current_user.id:
        return jsonify(dict(message='Re-authentication required', updated=False)), 401

    registered_user = User.query.filter_by(id=jwt_user.id).first()
    if registered_user is None:
        return jsonify(dict(message='Permission denied', updated=False)), 401

    data = request.get_json()
    post_id = data['post_id']
    header = data['header']
    body = data['body']
    tags = data['tags']
    private_post = data['private_post']

    post = Post.query.filter(Post.id == post_id).first()
    if post is None:
        return jsonify(dict(message="Post doesn't exist",
                            updated=False)), 404

    # Add tags to db
    post_tags = []
    for t in tags:
        tag = Tag.query.filter(Tag.name == t).first()
        if tag is None:
            tag = Tag()
            tag.name = t
            db.session.add(tag)
        post_tags.append(tag)

    post.header = header
    post.body = body
    post.tags = post_tags
    post.private_post = private_post
    post.last_edit_at = datetime.utcnow()
    db.session.add(post)

    try:
        db.session.commit()
        return jsonify(dict(message='Post was updated successfully',
                            updated=True)), 200
    except (SQLAlchemyError) as e:
        app_logger.debug(e)
        db.session.rollback()
        return jsonify(dict(message='Update post failed', updated=False)), 500

def is_human(captcha_response):
    """ Validating recaptcha response from google server
        Returns True captcha test passed for submitted form else returns False.
    """
    secret = BaseConfig().RECAPTCHA_SECRECT_KEY
    payload = {'response':captcha_response, 'secret':secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)

    return response_text['success']

@api.route('/delete_comment', methods=['DELETE'])
@token_required
@login_required
def delete_comment(jwt_user):
    if jwt_user.id != current_user.id:
        return jsonify(dict(message='Re-authentication required', deleted=False)), 401

    registered_user = User.query.filter_by(id=jwt_user.id).first()
    if registered_user is None:
        return jsonify(dict(message='Permission denied', deleted=False)), 401

    data = request.get_json()
    comment_id = data['comment_id']

    comment = Comment.query.filter(Comment.id == comment_id).first()
    if comment is None:
        return jsonify(dict(message="Comment doesn't exist",
                            deleted=False)), 404

    db.session.delete(comment)
    try:
        db.session.commit()
        return jsonify(dict(message='Comment was deleted successfully',
                            deleted=True)), 200
    except (SQLAlchemyError) as e:
        app_logger.debug(e)
        db.session.rollback()
        return jsonify(dict(message='Delete comment failed', deleted=False)), 500

@api.route('/get_tags', methods=['GET'])
def get_tags():
    # tags = Tag.query.all()
    tags = Tag.query.join(Post.tags).all()
    json_tags = []
    for tag in tags:
        json_tags.append(tag.to_dict())

    return jsonify(json_tags), 200

@api.route('/get_all_posts_by_tag', methods=['GET'])
@token_required
@login_required
def get_all_posts_by_tad(jwt_user):
    if jwt_user.id != current_user.id:
        return jsonify(dict(message='Re-authentication required')), 401

    registered_user = User.query.filter_by(id=jwt_user.id).first()
    if registered_user is None:
        return jsonify(dict(message='Permission denied')), 401

    page = request.args.get('page', 1, type=int)
    tag_id = request.args.get('tag_id')
    posts_per_page = BaseConfig().POSTS_PER_PAGE
    all_posts = get_posts_by_tag(registered_user.id, True, page, posts_per_page, tag_id)

    json_all_posts = []
    for p in all_posts.items:
        json_all_posts.append(p.to_dict_simple())

    return jsonify(dict(posts=json_all_posts,
                        has_next=all_posts.has_next,
                        has_prev=all_posts.has_prev,
                        next_num=all_posts.next_num,
                        prev_num=all_posts.prev_num)), 200

@api.route('/get_public_posts_by_tag', methods=['GET'])
def get_public_posts_by_tag():
    page = request.args.get('page', 1, type=int)
    tag_id = request.args.get('tag_id')
    posts_per_page = BaseConfig().POSTS_PER_PAGE
    all_posts = get_posts_by_tag(None, False, page, posts_per_page, tag_id)

    json_all_posts = []
    for p in all_posts.items:
        json_all_posts.append(p.to_dict_simple())

    return jsonify(dict(posts=json_all_posts,
                        has_next=all_posts.has_next,
                        has_prev=all_posts.has_prev,
                        next_num=all_posts.next_num,
                        prev_num=all_posts.prev_num)), 200

def get_posts_by_tag(author_id, including_private, page, posts_per_page, tag_id):
    if author_id is None:
        return Post.query.filter(Post.private_post == False) \
               .filter(Post.tags.any(id=tag_id)) \
               .order_by(Post.created_at.desc()) \
               .paginate(page, posts_per_page, False)

    if including_private == True:
        return Post.query.filter(Post.author_id == author_id) \
               .filter(Post.tags.any(id=tag_id)) \
               .order_by(Post.created_at.desc()) \
               .paginate(page, posts_per_page, False)
    else:
        return Post.query.filter(Post.author_id == author_id) \
               .filter(Post.private_post == False) \
               .filter(Post.tags.any(id=tag_id)) \
               .order_by(Post.created_at.desc()) \
               .paginate(page, posts_per_page, False)
