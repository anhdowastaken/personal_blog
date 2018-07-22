"""
config.py
- Settings for the flask application object
"""

class BaseConfig(object):
    DEBUG = True
    APP_LOG_PATH = '/tmp/personal_blog.log'

    CORS_ORIGINS = ['*']

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///personalblog.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ELASTICSEARCH_URL = 'http://localhost:9200/'

    # String is used for encryption and session management
    SECRET_KEY = 'puSCIAp7PvykT7w0d48U'
    RECAPTCHA_SECRECT_KEY = '6LeNYWQUAAAAAJBkKykVTndhvGRBdUNKKewCFHFD'

    # Blog owner's default information
    BLOG_OWNER_EMAIL = 'doducanh2710@gmail.com'
    BLOG_OWNER_USERNAME = 'anhdo'
    BLOG_OWNER_PASSWORD = '123456'

    POSTS_PER_PAGE = 10
