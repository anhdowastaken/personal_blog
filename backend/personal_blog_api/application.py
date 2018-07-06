"""
application.py
- Create a Flask app instance and register the database object
"""

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.filter_by(id = user_id).first()

bcrypt = Bcrypt()

def create_app(app_name='PERSONALBLOG_API'):
    app = Flask(app_name)
    app.config.from_object('personal_blog_api.config.BaseConfig')
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Allows users to make authenticated requests.
    # This allows cookies and credentials to be submitted across domains.
    # https://flask-cors.corydolphin.com/en/latest/api.html
    CORS(app, resource={r"/api/*": {"origin": "*"}}, supports_credentials=True)

    from personal_blog_api.api import api
    app.register_blueprint(api, url_prefix='/api')

    from personal_blog_api.models import db
    db.init_app(app)

    return app
