"""
application.py
- Create a Flask app instance and register the database object
"""

import logging
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .config import BaseConfig

# Configure logger
formater = logging.Formatter('[%(asctime)s][%(filename)10s:%(lineno)5s] %(levelname)8s --- %(message)s')
app_logger = logging.getLogger(__name__)
handler = logging.FileHandler(BaseConfig().APP_LOG_PATH, mode='a')
handler.setFormatter(formater)
app_logger.addHandler(handler)
app_logger.setLevel(logging.DEBUG)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.filter_by(id = user_id).first()

bcrypt = Bcrypt()

def create_app(app_name='PERSONALBLOG_API'):
    app_logger.info('Create app {}'.format(app_name))
    app = Flask(app_name)
    app.config.from_object('personal_blog_api.config.BaseConfig')
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Allows users to make authenticated requests.
    # This allows cookies and credentials to be submitted across domains.
    # https://flask-cors.corydolphin.com/en/latest/api.html
    app_logger.debug('CORS origins {}'.format(BaseConfig().CORS_ORIGINS))
    CORS(app, resource={r"/api/*": {"origin": BaseConfig().CORS_ORIGINS}}, supports_credentials=True)

    from personal_blog_api.api import api
    app.register_blueprint(api, url_prefix='/api')

    from personal_blog_api.models import db
    db.init_app(app)

    return app
