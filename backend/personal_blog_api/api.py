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
from .config import BaseConfig
from .models import db, User, Post

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
            # TODO: Use logger
            print(e)
            return jsonify(invalid_msg), 401
        except (Exception) as e:
            # TODO: Use logger
            print(e)
            return jsonify(dict(message="Backend error",
                                authenticated=False)), 401

    return _verify

@api.route('/register', methods=['POST'])
@token_required
@login_required
def register(jwt_user):
    if jwt_user.id != current_user.id:
        # User ID stored in JWT token does not match the one stored in session
        # It's better to re-authenticate
        return jsonify(dict(message='Re-authentication required', registered=False)), 401

    data = request.get_json()
    username = data['username']
    if username == '':
        return jsonify(dict(message='Empty username isn\'t allowed', registered=False)), 400

    registered_user = User.query.filter_by(username=username).first()
    if registered_user is None:
        # Generate random string containing 8 characters
        password = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))

        user = User(username, password)
        try:
            db.session.add(user)
            db.session.commit()

            return jsonify(dict(message='Register successfully',
                                registered=True,
                                user_data=dict(id=user.id,
                                               username=username,
                                               password=password,
                                               role=user.role))), 201
        except (SQLAlchemyError) as e:
            # TODO: Use logger
            print(e)
            return jsonify(dict(message='Register failed', registered=False)), 500
    else:
        return jsonify(dict(message='User existed', registered=False)), 400

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
            # TODO: Use logger
            print(e)
            return jsonify(dict(message='Reset failed', registered=False)), 500
    else:
        return jsonify(dict(message='User doesn\'t exist', registered=False)), 400

@api.route('/delete_user', methods=['POST'])
@token_required
@login_required
def delete_user(jwt_user):
    if jwt_user.id != current_user.id:
        # User ID stored in JWT token does not match the one stored in session
        # It's better to re-authenticate
        return jsonify(dict(message='Re-authentication required', delete=False)), 401

    # Only admin has permission to reset password
    if current_user.role != 'admin':
        return jsonify(dict(message='Permission denied', delete=False)), 403

    data = request.get_json()
    username = data['username']
    registered_user = User.query.filter_by(username=username).first()
    if registered_user is not None:
        if registered_user.role == 'admin':
            return jsonify(dict(message='Permission denied', delete=False)), 403

        try:
            # Delete all predictions of the user
            predictions = Prediction.query.filter_by(user_id=registered_user.id).all()
            for p in predictions:
                db.session.delete(p)
                db.session.commit()

            db.session.delete(registered_user)
            db.session.commit()

            return jsonify(dict(message='Delete successfully', delete=True)), 201
        except (SQLAlchemyError) as e:
            # TODO: Use logger
            print(e)
            return jsonify(dict(message='Delete failed', registered=False)), 500
    else:
        return jsonify(dict(message='User doesn\'t exist', registered=False)), 400

@api.route('/login', methods=['POST'])
def login():
    session.permanent = True
    data = request.get_json()
    username = data['username']
    password = data['password']

    registered_user = User.query.filter_by(username=username).first()
    if registered_user is None or bcrypt.check_password_hash(registered_user.password, password) == False:
        return jsonify(dict(message='Username or password is invalid', authenticated=False)), 401

    last_login_at = registered_user.last_login_at
    registered_user.last_login_at = datetime.utcnow()
    try:
        db.session.add(registered_user)
        db.session.commit()
    except:
        pass

    if login_user(registered_user):
        token = jwt.encode({
            'sub': registered_user.id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=24)}, BaseConfig().SECRET_KEY)

        return jsonify(dict(message='Logged in successfully',
                            authenticated=True,
                            token=token.decode('utf-8'),
                            user_data=dict(user_id=registered_user.id,
                                           username=registered_user.username,
                                           role=registered_user.role,
                                           last_login_at=int(last_login_at.timestamp())))), 200
    else:
        return jsonify(dict(message='Logged in failed', authenticated=False)), 500

@api.route('/logout', methods=['POST'])
def logout():
    logout_user()
    session.clear()

    return jsonify(dict(message='Logged out successfully')), 200

@api.route('/change_password', methods=['POST'])
@token_required
@login_required
def change_password(jwt_user):
    if jwt_user.id != current_user.id:
        return jsonify(dict(message='Re-authentication required')), 401

    data = request.get_json()
    old_password = data['old_password']
    new_password = data['new_password']

    registered_user = User.query.filter_by(id=jwt_user.id).first()
    if registered_user is None or bcrypt.check_password_hash(registered_user.password, old_password) == False:
        return jsonify(dict(message='Old password is incorrect', changed=False)), 400

    if new_password == '':
        return jsonify(dict(message='New password can\'t be empty', changed=False)), 400

    password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
    registered_user.password = password_hash
    try:
        db.session.commit()

        return jsonify(dict(message='Password is changed successfully',
                            changed=True)), 201
    except (SQLAlchemyError) as e:
        # TODO: Use logger
        print(e)
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

    all_posts = Post.query.all()
    json_public_posts = []
    for p in all_posts:
        json_public_posts.append(p.to_dict())

    json_response = json.dumps(json_public_posts)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    response.headers.add('content-length', len(json_response))
    response.status_code = 200

    return response

@api.route('/get_public_posts', methods=['GET'])
def get_public_posts():
    public_posts = Post.query.filter(Post.private_post == False).all()
    json_public_posts = []
    for p in public_posts:
        json_public_posts.append(p.to_dict())

    json_response = json.dumps(json_public_posts)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    response.headers.add('content-length', len(json_response))
    response.status_code = 200

    return response

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

    post = Post()
    post.header = header
    post.body = body
    post.author_id = jwt_user.id
    try:
        db.session.add(post)
        db.session.commit()

        return jsonify(dict(message='New post was created successfully',
                            created=True)), 201
    except (SQLAlchemyError) as e:
        # TODO: Use logger
        print(e)
        return jsonify(dict(message='Create new post failed', created=False)), 500
